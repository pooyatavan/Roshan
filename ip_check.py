import socket

def ip_format_check(radio_ip):
    try:
        socket.inet_aton(radio_ip)
        return True
    except socket.error:
        return False