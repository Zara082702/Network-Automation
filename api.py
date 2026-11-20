
from flask import Flask, render_template, request
from netmiko import ConnectHandler
import os

app = Flask(__name__)

# Router configuration
router_device = {
    "device_type": "cisco_ios_telnet",
    "ip": "192.168.10.109",
    "port": 32770,
    "username": os.getenv("ROUTER_USERNAME", "admin"),
    "password": os.getenv("ROUTER_PASSWORD", ""),
    "secret": os.getenv("ROUTER_SECRET", ""),
}

# Allowed router commands
commands = {
    "version": "show version",
    "interfaces": "show ip interface brief",
    "running": "show running-config"
}


@app.route("/", methods=["GET", "POST"])
def index():
    results = None
    error = None
    selected_command = None

    if request.method == "POST":
        selected_command = request.form.get("command")

        if selected_command not in commands:
            error = "Invalid command selected."
        elif not router_device["password"]:
            error = "Please configure your router password."
        else:
            net_connect = None

            try:
                # Connect to Cisco router
                net_connect = ConnectHandler(**router_device)

                # Enter privileged EXEC mode
                net_connect.enable()

                # Execute selected command
                command = commands[selected_command]
                results = net_connect.send_command(
                    command,
                    read_timeout=60
                )

            except Exception as e:
                error = f"Connection failed: {str(e)}"

            finally:
                if net_connect:
                    net_connect.disconnect()

    return render_template(
        "index.html",
        results=results,
        error=error,
        selected_command=selected_command,
        router_ip=router_device["ip"]
    )


if __name__ == "__main__":
    app.run(
        debug=False,
        host="127.0.0.1",
        port=5000
    )
