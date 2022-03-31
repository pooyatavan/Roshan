import socket
from requests import get

def get_ip():
    try:
        hostname = socket.gethostname()
        local_ip = socket.gethostbyname(hostname)
        public_ip = get('https://api.ipify.org').text
        # print(local_ip, public_ip)
        return f"Server local ip {local_ip} - Public {public_ip}"
    except:
        return "Oops, Something wrong for find ip address"