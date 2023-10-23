def print_data( monitoring_data):
    # Define the table headers based on the provided data
    headers = ["PID", "Process Name", "Username", "Port", "Workers", "Memory Usage", "CPU Usage", "Status", "Process", "Start Time", "Threads", "Open File"]

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
    RESET = "\033[0m"  # Reset color

    # Define column widths
    column_widths = [7, 14, 12, 6, 7, 14, 9, 9, 9, 19, 7, 9]

    # Print table headers
    header_row = [f"{header:{width}}" for header, width in zip(headers, column_widths)]
    header = f"+{'+'.join(['-' * (width + 2) for width in column_widths])}+"
    print(header)
    print(f"| {' | '.join(header_row)} |")
    print(header)

    # Format and print the data rows
    for data in monitoring_data:
        pid = data["PID"]
        process_name = data["Process Name"]
        username = data['Username']
        port = data.get("Port", "N/A")
        workers = data.get("Workers", 1)
        memory_usage = f"{data['Memory Usage'] / (1024 * 1024):.3f} MB"
        cpu_usage = f"{data['CPU Usage']:.2f}%"
        status = data["Status"]
        start_time = data["Start Time"]
        thread_count = data["Thread Count"]
        open_file_count = data["Open File Count"]
        process_status = data['Process Status']

        # Apply color based on status and CPU usage
        status_color = GREEN if status == "online" else RED if status == "offline" else YELLOW
        process_status_colour = GREEN if process_status == 'running' else RED if process_status == 'stopped' or 'zombie' else YELLOW if process_status == 'sleeping' or 'disk-sleep' else MAGENTA 
        cpu_color = RED if data["CPU Usage"] > 50 else GREEN

        process_name = 'Python 3.12' if process_name == 'python' else 'Netix (ASGI)' if process_name == 'netix' else process_name 

        # Use different colors for different rows
        row_color = MAGENTA if pid % 2 == 0 else CYAN

        # Format the data row
        data_row = [
            f"{BG_YELLOW}{pid:7}{RESET}",
            f"{process_name[:14].ljust(14)}",
            f"{RED}{username:12}{RESET}",
            f"{CYAN}{port:6}{RESET}",
            f"{GREEN}{workers:7}{RESET}",
            f"{YELLOW}{memory_usage:14}{RESET}",
            f"{cpu_color}{cpu_usage:9}{RESET}",
            f"{status_color}{status:9}{RESET}",
            f"{process_status_colour}{process_status:9}{RESET}",
            f"{YELLOW}{start_time[:19].ljust(19)}{RESET}",
            f"{thread_count:7}",
            f"{open_file_count:9}",
        ]
        print(f"| {row_color}{' | '.join(data_row)}{RESET} |")

    print(header)


from pprint import pprint

def bytes_to_mb(bytes_value):
    return f"{bytes_value / (1024 * 1024):.2f} MB"

def print_dict(monitor_data):
    if not monitor_data:
        return

    max_key_length = max(len(key) for entry in monitor_data for key in entry.keys())
    max_value_length = max(
        max(
            len(str(value))
            for key, value in entry.items()
            if not isinstance(value, dict) and not isinstance(value, list)
        )
        for entry in monitor_data
    )

    # Increase the width by adding extra spaces
    max_key_length += 6  # Adjust as needed
    max_value_length += 6  # Adjust as needed

    separator = f"+{'-' * (max_key_length + 2)}+{'-' * (max_value_length + 2)}+"

    print(separator)
    for entry in monitor_data:
        color_index = 0  # To cycle through colors
        for key, value in entry.items():
            if isinstance(value, dict):
                # Handle nested dictionary
                nested_keys = value.keys()
                for sub_key in nested_keys:
                    nested_key = f"{key}.{sub_key}"
                    sub_value = value[sub_key]
                    color = f"\033[{31 + (color_index % 6)}m"  # Cycle through colors 31-36
                    color_index += 1
                    if key in ["Memory Usage", "Virtual Memory Usage"]:
                        # Convert Memory Usage and Virtual Memory Usage to MB
                        sub_value = bytes_to_mb(sub_value)
                    print(f"| \033[36m{nested_key:{max_key_length}}\033[0m | {color}{sub_value:>{max_value_length}}\033[0m |")
            elif isinstance(value, list):
                # Handle lists (e.g., "Network Connections" and "Command Line Argument")
                for i, item in enumerate(value):
                    if isinstance(item, dict):
                        # Handle nested dictionary within a list
                        nested_keys = item.keys()
                        for sub_key in nested_keys:
                            nested_key = f"{key}[{i}].{sub_key}"
                            sub_value = item[sub_key]
                            color = f"\033[{31 + (color_index % 6)}m"  # Cycle through colors 31-36
                            color_index += 1
                            print(f"| \033[36m{nested_key:{max_key_length}}\033[0m | {color}{sub_value:>{max_value_length}}\033[0m |")
                    else:
                        if key == "Command Line Argument":
                            # Adjust the key for "Command Line Argument" with indices
                            nested_key = f"{key}[{i}]"
                            color = f"\033[{31 + (color_index % 6)}m"  # Cycle through colors 31-36
                            color_index += 1
                            print(f"| \033[36m{nested_key:{max_key_length}}\033[0m | {color}{item:>{max_value_length}}\033[0m |")
                        else:
                            # Right-align list items
                            color = f"\033[{31 + (color_index % 6)}m"  # Cycle through colors 31-36
                            color_index += 1
                            print(f"| \033[36m{key}[{i}]\033[0m | {color}{item:>{max_value_length}}\033[0m |")
            else:
                color = f"\033[{31 + (color_index % 6)}m"  # Cycle through colors 31-36
                color_index += 1
                if key in ["Memory Usage", "Virtual Memory Usage"]:
                    # Convert Memory Usage and Virtual Memory Usage to MB
                    value = bytes_to_mb(value)
                # Right-align values
                print(f"| \033[36m{key:{max_key_length}}\033[0m | {color}{value:>{max_value_length}}\033[0m |")

        print(separator)