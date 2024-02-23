import socket
import time
import os
import netifaces
import threading  # for multi threading

# -- Server Configuration ----------------------------------------------------------------------------------------- #
PORT = 8000                       # Port number
MAX_CONNECTIONS = 3               # Maximum number of clients 
BUFFER_SIZE = 1024                # Packet size
LOG_FILE = "server_log.txt"       # Log file name
CLIENT_ID_COUNTER = 0             # Client ID counter

# Creating a Lock object for log file operations
log_file_lock = threading.Lock()
# Initialize dictionary and Lock objects to track number of login attempts
login_attempts = {}
login_attempts_lock = threading.Lock()
# Track the number of clients currently connected as a global variable
current_connections = 0
current_connections_lock = threading.Lock()
# ----------------------------------------------------------------------------------------------------------------- #

# -- Test Components ---------------------------------------------------------------------------------------------- #
TEST_ID = "Chris"
TEST_PW = "Jongeon"
TEST_FILE_NAME = "test.txt"
TEST_INVALID_FILE_NAME = "cannot_open.txt"
TEST_FILE_EXTENTIONS = {"txt", "pdf", "jpg", "png"}
TEST_LIMIT_TIME = 60
# ----------------------------------------------------------------------------------------------------------------- #


# -- Main Function ------------------------------------------------------------------------------------------------ #
def main():
    global CLIENT_ID_COUNTER
    HOST = get_ip_address()
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server_socket.bind((HOST, PORT))
        server_socket.listen(MAX_CONNECTIONS)
        print(f"Listening for clients on {HOST}:{PORT}...")

        while True:
            if current_connections >= MAX_CONNECTIONS:
               # WARNING Leaves a log and does not block further access (just warns)
               with log_file_lock:
                   log_event_to_file("WARNING: Max connections reached. Next connections will be blocked.")
               print("WARNING: Max connections reached. Next connections will be blocked.")

            client_socket, client_address = server_socket.accept()

            with current_connections_lock:
                if current_connections >= MAX_CONNECTIONS:
                   # Blocks clients attempting to connect and leaves an ERROR log
                   log_message = f"ERROR: Connection from {client_address} blocked due to max connections limit."
                   log_event_to_file(log_message)
                   print(log_message)
                   client_socket.close()
                   continue
                else:
                   current_connections += 1

            CLIENT_ID_COUNTER += 1
            clientID = CLIENT_ID_COUNTER
            print(f"Assigned Client ID {clientID} to {client_address}")
            client_thread = threading.Thread(target=handle_client, args=(client_socket, client_address, clientID))
            client_thread.start()
# ----------------------------------------------------------------------------------------------------------------- #
                    

 # -- Server & Logging Functions ----------------------------------------------------------------------------------- #        
def handle_client(client_socket, client_address, clientID):
    global current_connections

    with client_socket:
        print(f"Connection from {client_address}, Client ID: {clientID}")
        try:
            data = client_socket.recv(BUFFER_SIZE).decode('utf-8')
            if data:
                log_event(client_address, data, clientID)
        except UnicodeDecodeError as e:
            error_message = f"Error decoding data from Client ID {clientID}: {e}"
            print(error_message)
            log_event(client_address, error_message, clientID)
        except Exception as e:
            error_message = f"General error from Client ID {clientID}: {e}"
            print(error_message)
            log_event(client_address, error_message, clientID)
        finally:
            with current_connections_lock:
                current_connections -= 1
            client_socket.close()

# Function Name: get_ip_address()
# Description  : This function search host internet connection and return an available IP address
#               If an availble IP address is not found, return the localhost
# Parameters   : void
# Return       : IP address                    
def get_ip_address():
    interfaces = netifaces.interfaces() # Grab host network information and store to the variable
                                        # The network information will be stored like the below line
                                        # [
                                        #   {
                                        #     'addr': '192.168.1.4',         >> IP address 
                                        #     'netmask': '255.255.255.0',    >> Subnet Mask
                                        #     'broadcast': '192.168.1.255'   >> Broadcast Address
                                        #   }
                                        # ]
                                        # If an user wants to get IP address information from the ,
                                        #  >> addr_info[0]['addr'] 
                                        
    for interface in interfaces:                                            # Iterator
        addr_info = netifaces.ifaddresses(interface).get(netifaces.AF_INET) # netifaces.ifaddresses(interface) : return dictionary type of address inforamtion
                                                                            # .get(netifaces.AF_INET) : Used to look up the part representing IPv4 address information in the dictionary returned 
                                                                            # from the function. If an IPv4 address is assigned to the interface, it returns information; if not, None.
        if addr_info:                    # If available IPv4 address is found
            return addr_info[0]['addr']  # return that address   
    return '127.0.0.1'                   # If a usable IP address is not found even after cycling through all the contents, the localhost address is returned.


def log_event_to_file(log_message):
    """
    write the log message to the text file
    """
    global log_file_lock    # Prevent simultaneous access to resources (text files)
    with log_file_lock:
        with open(LOG_FILE, "a") as log_file:
            log_file.write(log_message + "\n")
            print(f"Logged to file: {log_message}")


def log_event(client_address, data, clientID):
    """
    Writes logs to a text file
    """
    timestamp = time.strftime('%b %d %H:%M:%S', time.localtime())  # Get current date and time
    hostname = socket.gethostname() 

    # Extract the severity_level and process_result from the event_result
    event_result = event_handle(data, clientID)
    severity_level = event_result.get("severity_level", "INFO")      # Default to INFO if not specified
    process_result = event_result.get("process_result", "Undefined") # Default to Undefined if not specified

                                   # Get the host name
    log_message = f"{severity_level}: {timestamp} {hostname} MyEventLog[1234]: Client_ID {clientID}: {data} from {client_address} - {process_result}"
    print(log_message)              # print the log message
    log_event_to_file(log_message)  # write the log message to the text file

def event_handle(data, clientID):
    # Check if there is a semicolon in the data string
    if ';' in data:
        command, params = data.split(';', 1)

        # Processing when the command is LOGIN
        if command == "LOGIN":
            # Separate parameters and convert to dictionary
            params_dict = dict(param.split('=') for param in params.split('&'))
            
            # ID and PW extraction
            user_id = params_dict.get("ID")
            password = params_dict.get("PW")
            print(f"Login attempt with ID: {user_id}, Password: {password}")

            # ID and PW validaiton
            "Return INFO with process result message when the ID and PW is correct"
            "Return NOTICE with process result message when the ID or PW is incorrect"
            "Return WARNING with process result message when the ID or PW is incorrect 3 times"
            if user_id == TEST_ID and password == TEST_PW:
                    print("Login successful.")
                    login_attempts[clientID] = 0  # Reset the number of attempts upon successful login
                    return {"severity_level": "INFO", "process_result": "Login_Success"}
            else:
                attempts += 1
                login_attempts[clientID] = attempts
                if attempts >= 3:
                    print("Login failed. Too many failed attempts.")
                    return {"severity_level": "WARNING", "process_result": "Too_Many_Failed_Attempts"}
                else:
                    print("Login failed. Invalid ID or Password.")
                    return {"severity_level": "NOTICE", "process_result": "Invalid_ID_or_PW"}
            
        # File request validation
        " 1. Return INFO when the allowed file is requested and successfully sent to client"
        " 2. Return NOTICE when requesting an incompatible file extension & file not found"
        " 3. Return WARNING when a client requests a file to which it does not have access rights"
        if command == "REQUST":
                file_extension = params.split('.')[-1]
                
                # Extension check
                if file_extension not in TEST_FILE_EXTENTIONS:
                    print(f"The file extension '{file_extension}' is not allowed.")
                    return {"severity_level": "NOTICE", "process_result": f"Not allowed_file_extension: {file_extension}"}
                
                # Check for file requests you don't have permission to access
                if params == TEST_INVALID_FILE_NAME:
                    print(f"File access denied.")
                    return {"severity_level": "WARNING", "process_result": f"Access_Denied"}
                
                # file name check
                if params == TEST_FILE_NAME:
                    print(f"File exists. File is sent.")
                    return {"severity_level": "INFO", "process_result": f"File_Sent"}
                else:
                    print(f"File not exists.")
                    return {"severity_level": "Notice", "process_result": f"File_Not_Found"}

            
    else:
        print("Protocol Error.")
        return {"severity_level": "NOTICE", "process_result": "Protocol_Error"}
# ----------------------------------------------------------------------------------------------------------------- #


if __name__ == "__main__":
    main()