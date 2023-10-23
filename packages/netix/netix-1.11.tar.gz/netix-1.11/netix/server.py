from .lib.contexts import ServerContext as WorkerContext 
import asyncio  # noqa: E402
import logging  # noqa: E402
import multiprocessing as mp  # noqa: E402
import os  # noqa: E402
import socket  # noqa: E402
import ssl  # noqa: E402
import sys  # noqa: E402
import time  # noqa: E402
import json
import schedule
import time
from .daemon import Daemonized

from importlib import import_module  # noqa: E402
from shutil import get_terminal_size  # noqa: E402

from . import __version__, handlers  # noqa: E402
from .utils import log_date, server_date  # noqa: E402
from .lib.connections import KeepAliveConnections  # noqa: E402
from .lib.contexts import ServerContext as WorkerContext  # noqa: E402
from .lib.locks import ServerLock  # noqa: E402
from .lib.pools import QueuePool  # noqa: E402


_REUSEPORT_OR_REUSEADDR = {
    True: getattr(socket, 'SO_REUSEPORT', socket.SO_REUSEADDR),
    False: socket.SO_REUSEADDR
}

# Define color codes
BG_YELLOW = "\033[35m"
BLUE = "\033[34m"  # Blue color
GREEN = "\033[32m"  # Green color
RED = "\033[31m"  # Red color
YELLOW = "\033[33m"  # Yellow color
MAGENTA = "\033[35m"  # Magenta color
CYAN = "\033[36m"  # Cyan color
WHITE = "\033[37m"
BOLD = "\033[1m"
RESET = "\033[0m" 

class ASGIServer:
    def __init__(self) -> None:
        self._ports = {}
        self.worker_num = 1
        self.monitoring_data = []
        self.monitoring_data_file = os.path.expanduser('~/.netix/daemon/monitoring.json')

        self.routes = {
            0: [
                (400, handlers.error_400, {}),
                (404, handlers.error_404, dict(status=(404, b'Not Found'),
                                               stream=False))
            ],
            1: [
                (
                    b'^/+(?:\\?.*)?$',
                    handlers.index, dict(status=(503, b'Service Unavailable'))
                )
            ],
            -1: []
        }

        self.middlewares = {
            'connect': [],
            'close': [],
            'request': [],
            'response': []
        }

        self.events = {
            'worker_start': [],
            'worker_stop': []
        }

        self._loop = None
        self._logger = None

    def listen(self, port, host=None, **options):
        if not isinstance(port, int):
            # assume it's a UNIX socket path
            host = port
            port = None

        if (host, port) in self._ports:
            return False

        self._ports[(host, port)] = options
        return (host, port) in self._ports

    async def _serve(self, host, port, **options):
        context = WorkerContext()

        for func in self.events['worker_start']:
            if (await func(context=context,
                           loop=self._loop,
                           logger=self._logger)):
                break

        options['_conn'].send(os.getpid())
        backlog = options.get('backlog', 100)

        if hasattr(socket, 'fromshare'):
            # Windows
            sock = socket.fromshare(options['_conn'].recv())
            sock.listen(backlog)
        else:
            fd = options['_conn'].recv()

            try:
                # Linux 'fork'
                sock = socket.fromfd(fd, options['_sa_family'],
                                     socket.SOCK_STREAM)
                sock.listen(backlog)
                options['_conn'].send(True)
            except OSError:
                # Linux 'spawn'
                options['_conn'].send(False)
                sock = options['_conn'].recv()
                sock.listen(backlog)

        if ('ssl' in options and options['ssl'] and
                isinstance(options['ssl'], dict)):
            ssl_context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
            ssl_context.load_cert_chain(
                certfile=options['ssl'].get('cert', ''),
                keyfile=options['ssl'].get('key'),
                password=options['ssl'].get('password')
            )
        else:
            ssl_context = None

        server_name = b'Netix'

        if isinstance(server_name, str):
            server_name = server_name.encode('latin-1')

        if isinstance(host, str):
            host = host.encode('latin-1')

        lock = ServerLock(options['_locks'], loop=self._loop)
        connections = KeepAliveConnections(
            maxlen=options.get('keepalive_connections', 512)
        )
        pools = {
            'queue': QueuePool(1024, self._logger)
        }
        lifespan = None

        if 'app' in options and isinstance(options['app'], str):
            from .asgi_lifespan import ASGILifespan
            from .asgi_server import ASGIServer as Server

            # 'module:app'               -> 'module:app'   (dir: os.getcwd())
            # '/path/to/module.py'       -> 'module:app'   (dir: '/path/to')
            # '/path/to/module.py:myapp' -> 'module:myapp' (dir: '/path/to')

            if (':\\' in options['app'] and options['app'].count(':') < 2 or
                    ':' not in options['app']):
                options['app'] += ':app'

            path, attr_name = options['app'].rsplit(':', 1)
            dir_name, base_name = os.path.split(path)
            module_name = os.path.splitext(base_name)[0]

            if dir_name == '':
                dir_name = os.getcwd()

            sys.path.insert(0, dir_name)

            options['app'] = getattr(import_module(module_name), attr_name)

            print(log_date(), end=' ')
            sys.stdout.flush()
            sys.stdout.buffer.write(
                b'Starting %s ASGI server for /\ ' % server_name
            )
            print(
                getattr(options['app'], '__name__',
                        f"{BOLD}{options['app'].__class__.__name__}{RESET}")
            )

            if server_name != b'':
                server_name = server_name + b' (ASGI)'

            lifespan = ASGILifespan(options['app'],
                                    loop=self._loop, logger=self._logger)

            lifespan.startup()
            exc = await lifespan.exception()

            if exc:
                raise exc
        else:
            pass

        server_info = {
            'date': server_date(),
            'name': server_name
        }
        server = await self._loop.create_server(
            lambda: Server(loop=self._loop,
                           logger=self._logger,
                           lock=lock,
                           worker=context,
                           debug=options.get('debug', False),
                           ws=options.get('ws', True),
                           download_rate=options.get('download_rate', 1048576),
                           upload_rate=options.get('upload_rate', 1048576),
                           buffer_size=options.get('buffer_size', 16 * 1024),
                           client_max_body_size=options.get(
                               'client_max_body_size', 2 * 1048576
                           ),
                           request_timeout=options.get('request_timeout', 30),
                           keepalive_timeout=options.get(
                               'keepalive_timeout', 30
                           ),
                           server_info=server_info,
                           _connections=connections,
                           _pools=pools,
                           _app=options['app'],
                           _root_path=options.get('root_path', ''),
                           _routes=options['_routes'],
                           _middlewares=options['_middlewares']),
            sock=sock, backlog=backlog, ssl=ssl_context)

        print(log_date(), end=' ')
        sys.stdout.flush()
        sys.stdout.buffer.write(
            b'%s (pid %d) is started at ' % (server_name, os.getpid())
        )

        if sock.family.name == 'AF_UNIX':
            print(sock.getsockname(), end='')
        else:
            print('%s:%d' % sock.getsockname()[:2], end=' (Press CTRL+C to quit)')

        if ssl_context is not None:
            sys.stdout.flush()
            sys.stdout.buffer.write(b' (https)')

        print()

        process_num = 1

        # serve forever
        while process_num:
            try:
                # ping parent process
                options['_conn'].send(None)

                for _ in range(2 * process_num):
                    await asyncio.sleep(1)

                    # update server date
                    server_info['date'] = server_date()

                    if options['_conn'].poll():
                        break

                process_num = options['_conn'].recv()
            except (BrokenPipeError, ConnectionResetError, EOFError):
                break

        server.close()
        await server.wait_closed()

        if lifespan is None:
            i = len(self.events['worker_stop'])

            while i > 0:
                i -= 1

                if (await self.events['worker_stop'][i](
                        context=context,
                        loop=self._loop,
                        logger=self._logger)):
                    break
        else:
            lifespan.shutdown()
            exc = await lifespan.exception()

            if exc:
                self._logger.error(exc)

    async def _stop(self, task):
        await task
        self._loop.stop()

    def _worker(self, host, port, **kwargs):
        self._logger = logging.getLogger(mp.current_process().name)
        self._logger.setLevel(
            getattr(logging, kwargs['log_level'], logging.DEBUG)
        )

        handler = logging.StreamHandler()
        formatter = logging.Formatter(
            '[%(asctime)s] %(levelname)s: %(message)s'
        )

        handler.setFormatter(formatter)
        self._logger.addHandler(handler)

        self._loop = asyncio.new_event_loop()
        asyncio.set_event_loop(self._loop)
        task = self._loop.create_task(self._serve(host, port, **kwargs))

        try:
            self._loop.run_until_complete(task)
        except KeyboardInterrupt:
            self._logger.info('Shutting down')
            self._loop.create_task(self._stop(task))
            self._loop.run_forever()
        finally:
            self._loop.close()

    def create_sock(self, host, port, reuse_port=True):
        try:
            try:
                socket.getaddrinfo(host, None)

                if ':' in host:
                    sock = socket.socket(socket.AF_INET6, socket.SOCK_STREAM)

                    if host == '::' and hasattr(socket, 'IPPROTO_IPV6'):
                        sock.setsockopt(socket.IPPROTO_IPV6,
                                        socket.IPV6_V6ONLY, 0)
                else:
                    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            except socket.gaierror:
                _host = host
                host = 'localhost'
                sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
                host = _host
        except AttributeError:
            print('either AF_INET6 or AF_UNIX is not supported')
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        sock.setblocking(False)
        sock.set_inheritable(True)

        if sock.family.name == 'AF_UNIX':
            if not host.endswith('.sock'):
                host += '.sock'

            for _ in range(2):
                try:
                    sock.bind(host)
                    break
                except OSError:
                    if os.path.exists(host) and os.stat(host).st_size == 0:
                        os.unlink(host)
        else:
            sock.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
            sock.setsockopt(socket.SOL_SOCKET,
                            _REUSEPORT_OR_REUSEADDR[reuse_port], 1)
            sock.bind((host, port))

        return sock

    def _ctxrun(self, host=None, port=0, reuse_port=True, worker_num=1, **kwargs):
        kwargs['log_level'] = kwargs.get('log_level', 'DEBUG').upper()
        terminal_width = min(get_terminal_size()[0], 72)

        print(
            'Starting Netix v%s (%s %d.%d.%d, %s)' %
            (__version__,
             sys.implementation.name,
             *sys.version_info[:3],
             sys.platform)
        )
        print('-' * terminal_width)

        if 'app' in kwargs:
            if not isinstance(kwargs['app'], str):
                import __main__

                if hasattr(__main__, '__file__'):
                    for attr_name in dir(__main__):
                        if attr_name.startswith('__'):
                            continue

                        if getattr(__main__, attr_name) == kwargs['app']:
                            break
                    else:
                        attr_name = 'app'

                    kwargs['app'] = '{:s}:{:s}'.format(__main__.__file__,
                                                       attr_name)

            locks = []
        else:
            locks = [mp.Lock() for _ in range(kwargs.get('locks', 16))]

            if kwargs['log_level'] in ('DEBUG', 'INFO'):
                print('Routes:')

                for routes in self.routes.values():
                    for route in routes:
                        pattern, func, kwds = route

                        print(
                            '  %s -> %s(%s)' % (
                                pattern,
                                func.__name__,
                                ', '.join(
                                    '%s=%s' % item for item in kwds.items()))
                        )

                print()

        if host is None:
            if not self._ports:
                raise ValueError(
                    'with host=None, listen() must be called first'
                )

            host = 'localhost'
        else:
            self.listen(port, host=host, **kwargs)

        try:
            worker_num = min(worker_num, len(os.sched_getaffinity(0)))
        except AttributeError:
            worker_num = min(worker_num, os.cpu_count() or 1)

        processes = []
        socks = {}

        print('Settings: [')

        for (_host, _port), options in self._ports.items():
            if _host is None:
                _host = host

            if _port is None:
                _port = port

            options = {**kwargs, **options}

            print(
                '  host=%s, port=%d, reuse_port=%s, worker_num=%d, %s \n]' % (
                    _host,
                    _port,
                    reuse_port,
                    worker_num,
                    ', '.join('%s=%s' % item for item in options.items()))
            )

            args = (_host, _port)
            socks[args] = self.create_sock(
                _host, _port, options.get('reuse_port', reuse_port)
            )

            for _ in range(options.get('worker_num', worker_num)):
                parent_conn, child_conn = mp.Pipe()

                p = mp.Process(
                    target=self._worker,
                    args=args,
                    kwargs=dict(options,
                                _locks=locks,
                                _conn=child_conn,
                                _sa_family=socks[args].family,
                                _routes=self.routes,
                                _middlewares=self.middlewares)
                )

                p.start()
                child_pid = parent_conn.recv()

                if hasattr(socks[args], 'share'):
                    parent_conn.send(socks[args].share(child_pid))
                else:
                    parent_conn.send(socks[args].fileno())

                    if parent_conn.recv() is False:
                        parent_conn.send(socks[args])

                processes.append((parent_conn, p, args, options))

        print('-' * terminal_width)

        while True:
            try:
                for i, (parent_conn, p, args, options) in enumerate(processes):
                    if not p.is_alive():
                        print('A worker process died. Restarting...')

                        parent_conn.close()
                        parent_conn, child_conn = mp.Pipe()
                        p = mp.Process(
                            target=self._worker,
                            args=args,
                            kwargs=dict(options,
                                        _locks=locks,
                                        _conn=child_conn,
                                        _sa_family=socks[args].family,
                                        _routes=self.routes,
                                        _middlewares=self.middlewares)
                        )

                        p.start()
                        pid = parent_conn.recv()

                        if hasattr(socks[args], 'share'):
                            parent_conn.send(socks[args].share(pid))
                        else:
                            parent_conn.send(socks[args].fileno())

                            if parent_conn.recv() is False:
                                parent_conn.send(socks[args])

                        processes[i] = (parent_conn, p, args, options)

                    # response ping from child
                    while parent_conn.poll():
                        parent_conn.recv()
                        parent_conn.send(len(processes))

                    time.sleep(1)
            except KeyboardInterrupt:
                break

        for parent_conn, p, *_ in processes:
            # stopping serve forever
            parent_conn.send(0)
            parent_conn.close()
            p.join()
            print('Waiting for server shutdown.')
            print('Server shutdown completed.')
            print('pid {:d} terminated.'.format(p.pid))
            print('Finished server process [{:d}].'.format(p.pid))

        for sock in socks.values():
            try:
                sock.shutdown(socket.SHUT_RDWR)
                sock.close()

                if sock.family.name == 'AF_UNIX':
                    os.unlink(sock.getsockname())
            except FileNotFoundError:
                pass
            except OSError:
                sock.close()

    def set_concurrency(self, worker_num):
        self.worker_num = worker_num

    def get_monitoring_data(self):
        # Fetch monitoring data from the JSON file
        if os.path.exists(self.monitoring_data_file):
            with open(self.monitoring_data_file, "r") as json_file:
                monitoring_data = json.load(json_file)
        else:
            monitoring_data = []

        return monitoring_data
    
    def run(self, app, host='127.0.0.1', port=8000, debug=False, **options):

        if 'host' not in options:
            options['host'] = host

        if 'port' not in options:
            options['port'] = port

        if 'debug' not in options:
            options['debug'] = debug

        self._ctxrun(app=app, **options)
    
    def daemon(self, app=None, pidfile=None, **options):

        if app is None:
            app = options['app']

        if 'host' not in options:
            options['host'] = '127.0.0.1'

        if 'port' not in options:
            options['port'] = 8000

        if pidfile is None:
            pidfile = 'pids.txt'  # Default PID file name

        if 'worker_num' not in options:
            options['worker_num'] = 4

        daemon = Daemonized(pidfile, lambda: self._ctxrun(app=app, **options), port=options['port'], workers=options['worker_num'])
        if 'worker_num' in options:
            self.set_concurrency(options['worker_num'])
        daemon.start()  # Schedule the status check
        self.schedule_status_check(daemon)
    
    def schedule_status_check(self, daemon):
        import traceback

        def run_status_check():
            try:
                daemon.check_monitoring_status()
            except Exception as e:
                traceback.print_exc()  # Print the traceback of the exception
                # Log the exception to your log file
                print("An error occurred during the status check. Stopping the scheduler.")
                schedule.clear()
                return

        # Schedule the status check to run every hour
        schedule.every(30).minutes.do(run_status_check)

        # Run the scheduled tasks
        while True:
            schedule.run_pending()
            time.sleep(1)