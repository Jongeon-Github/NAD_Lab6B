import socket
import time
import os
import netifaces
import win32evtlogutil
import win32evtlog
import win32security
import win32con

# 서버 설정
PORT = 8000
MAX_CONNECTIONS = 3
BUFFER_SIZE = 1024
LOG_SOURCE = "MyEventLog"  # Windows 이벤트 로그에 사용될 소스 이름

def get_ip_address():
    interfaces = netifaces.interfaces() # Grab host network information and store to the variable
                                        # The network information will be stored like the below line
                                        
    for interface in interfaces:
        addr_info = netifaces.ifaddresses(interface).get(netifaces.AF_INET)
        if addr_info:
            return addr_info[0]['addr']
    return '127.0.0.1'


def log_event_to_windows(source, event_id, message):
    """
    Windows 이벤트 로그에 이벤트를 기록합니다.
    """
    event_type = win32evtlog.EVENTLOG_INFORMATION_TYPE
    category = 0
    data = b''

    try:
        win32evtlogutil.ReportEvent(appName=source, eventID=event_id, eventCategory=category, eventType=event_type, strings=[message], data=data)
        print(f"Windows Event logged: {message}")
    except Exception as e:
        print(f"Error logging event to Windows: {e}")

def log_event(client_address, data):
    """
    이벤트 로깅 함수. 여기서 Windows 이벤트 로그를 호출합니다.
    """
    timestamp = time.strftime('%b %d %H:%M:%S', time.localtime())
    hostname = socket.gethostname()
    syslog_message = f"{timestamp} {hostname} myservice[1234]: {data}"
    print(syslog_message)  # 콘솔에 로그 출력
    log_event_to_windows(LOG_SOURCE, 1, syslog_message)  # Windows 이벤트 로그에 기록


def main():
    HOST = get_ip_address()
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server_socket.bind((HOST, PORT))
        server_socket.listen(MAX_CONNECTIONS)
        print(f"Listening for clients on {HOST}:{PORT}...")

        while True:
            client_socket, client_address = server_socket.accept()
            with client_socket:
                print(f"Connection from {client_address}")
                data = client_socket.recv(BUFFER_SIZE).decode('utf-8')
                if data:
                    log_event(client_address, data)

if __name__ == "__main__":
    main()