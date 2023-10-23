# HTML Exception Content for web rendring...
from __future__ import annotations

def exception_content(error_message: str, formatted_traceback: str, underlined_line: str, error_type: str, file_and_line: str):
    content = f"""
<html>
<head>
    <title>{error_type}: {error_message}</title>
    <meta name="viewport" content="width=device-width, initial-scale=1, maximum-scale=1, user-scalable=0">
    <style>
        body {{
            font-family: Arial, sans-serif;
            background-color: white;
            margin: 0;
            padding: 0;
            display: flex;
            justify-content: center;
            align-items: center;
            overflow-x: hidden; /* Prevent horizontal scrolling */
        }}
        .container {{
            background-color: white;
            padding: 20px;
            text-align: center;
            width: 100%;
            max-width: none;
            height: 100%;
            max-height: auto;
        }}
        h1 {{
            color: black;
            margin-bottom: 20px;
            font-family: 'Courier New', monospace;
            font-size: 32px;
        }}
        .error-message {{
            margin-bottom: 20px;
            font-size: 18px;
            font-family: 'Courier New', monospace;
            white-space: pre-wrap;
        }}
        pre {{
            white-space: pre-wrap;
            background-color: #f9f9f9;
            padding: 15px;
            border-radius: 3px;
            border: 1px solid #ddd;
            text-align: left;
            font-size: 16px;
            overflow-y: auto;
        }}

        /* Media Queries for Responsive Design */
        @media (max-width: 768px) {{
        body {{
            padding: 20px;
            height: 120vh;
            }}
            h1 {{
                font-size: 24px;
            }}
            .error-message {{
                font-size: 16px;
            }}
            pre {{
                font-size: 14px;
            }}
            .message-tool {{
               font-size: 14px;
            }}
        }}

        @media (max-width: 480px) {{
        body {{
           padding: 20px;
        }}
            h1 {{
                font-size: 20px;
            }}
            .error-message {{
                font-size: 14px;
            }}
            pre {{
                font-size: 12px;
            }}
            .message-tool {{
               font-size: 14px;
            }}
        }}

        @media (max-width: 320px) {{
        body {{
           padding: 20px;
           height: auto;
        }}
            h1 {{
                font-size: 18px;
            }}
            .error-message {{
                font-size: 12px;
            }}
            pre {{
                font-size: 10px;
            }}
            .message-tool {{
               font-size: 14px;
            }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <h1>{error_type}</h1>
        <p class='error-message'><b style="color: red;">{error_type}</b>: {error_message}</p>
        <h2 style="font-family: 'Courier New', monospace;">Traceback</h2>
<p style="color: red; font-size: smaller; font-family: 'Courier New', monospace; text-align: left; margin: 10px 0; word-wrap: break-word;"><u style="color: red;">{file_and_line}</u></p>

        <pre>{underlined_line}</pre>
        <pre>{formatted_traceback}</pre>
        <p class="message-tool" style="text-align: left; color: #2F4F4F;" > The Evelax caught an exception in your ASGI application. You can now look at the traceback which led to the error. </p>
        <ul class="message-tool" style="text-align: left; color: #2F4F4F;">
        <li><b>dump()</b> shows all variables in the frame</li>
        <li><b>dump(obj)</b> dumps all that's known about the object</li>
        </ul>
        <p class="message-tool" style="text-align: left; color: #2F4F4F;">A traceback interpreter is a tool that helps developers understand and diagnose errors in their code. It provides a detailed history of function calls leading to an error. Building a custom traceback interpreter offers several advantages:</p>
        <ul class="message-tool" style="text-align: left; color: #2F4F4F;">
        <li><b>Traceback Generation:</b> Analyze the call stack to collect function call information.</li>
        <li><b>Formatting:</b> A human-readable traceback message with error details.</li>
        </ul>
        <p class="message-tool" style="text-align: right; color: #708090;">Powered  by <b>Evelax</b>, your friendly <b>Netix</b> powered traceback interpreter. </p> <br>
    </div>
</body>
</html>
"""
    return content
    