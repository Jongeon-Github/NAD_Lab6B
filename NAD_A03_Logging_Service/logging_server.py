# File Name  : logging_server.py
# Author     : Honggyu Park
# Date       : 2024-02-23
# Description: This Python script implements a multi-threaded logging server that listens for client connections on a specified port. 
#              It is designed to handle multiple clients simultaneously, each client being handled by a separate thread.
#              The server has functionalities to process login attempts and file request validations based on predefined criteria.

import socket
import time
import netifaces
import threading  # for multi threading

# -- Server Configuration ----------------------------------------------------------------------------------------- #
PORT = 8000                       # Port number
MAX_CONNECTIONS = 3               # Maximum number of clients 
BUFFER_SIZE = 1024                # Packet size
LOG_FILE = "server_log.txt"       # Log file name
CLIENT_ID_COUNTER = 0             # Client ID counter
TIME_OUT = 60                     # Client's allowed time without responce

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
    global CLIENT_ID_COUNTER        # Declare to use the current script global variable CLIENT_ID_COUNTER
    global current_connections
    HOST = get_ip_address()         # Get an available IP address for conection

    " Create a socket using the current script global variable CLIENT_ID_COUNTER"
    "Declare to use Internet addressing system (AF_INET = IPv4) and stream socket (SOCK_STREAM)"
    # Use 'with' for safe connextion open and close 
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        "About socket.SO_REUSEADDR"
        ": By default, after closing a socket, the system will keep that socket's address (usually a port) in the 'TIME_WAIT' state, which typically lasts for several minutes."
        "By setting the SO_REUSEADDR option, you can bypass this waiting time and reuse the address (port) immediately."
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server_socket.bind((HOST, PORT))                                    # Socket Bindoing (Host IP address & Port Number)
        server_socket.listen(MAX_CONNECTIONS)                               # Start listening the client request...
        print(f"Listening for clients on {HOST}:{PORT}...")


        "Check whether the current number of clients are reached to the maximum or not"
        "If so, log to it as a 'WARNING'"
        while True:
            if current_connections >= MAX_CONNECTIONS:
               # WARNING Leaves a log and does not block further access (just warns)
               with log_file_lock:
                   log_event_to_file("WARNING: Max connections reached. Next connections will be blocked.")
               print("WARNING: Max connections reached. Next connections will be blocked.")

            client_socket, client_address = server_socket.accept()

            "Lock the resource of 'current_connections' to moniter the number of current connection"
            with current_connections_lock:           
                if current_connections >= MAX_CONNECTIONS:
                   "Check whether the current number of clients are exceeded to the maximum or not"
                   "If so, Blocks clients attempting to connect and leaves an ERROR log and close the conneciton"
                   log_message = f"ERROR: Connection from {client_address} blocked due to max connections limit."
                   log_event_to_file(log_message)
                   print(log_message)

                   # send the connection denied message to the client
                   response_message = f"ERROR;Connection_Denied"
                   client_socket.send(response_message.encode('utf-8'))

                   client_socket.close()
                   continue
                else:
                   current_connections += 1

            # Cumulative number of clients connected to the server
            # Use this number as the clientID
            CLIENT_ID_COUNTER += 1
            clientID = CLIENT_ID_COUNTER

            # Displace & log the new client infromation 
            print(f"New client ClientID:{clientID} is connected to {client_address}. \n Current connections: {current_connections}")
            timestamp = time.strftime('%b %d %H:%M:%S', time.localtime())  # Get current date and time
            hostname = socket.gethostname()  # Get the host name
            log_message = f"INFO: {timestamp} {hostname} MyEventLog[1234]: Client_ID {clientID}: from {client_address} is connected - Currentconnections: {current_connections}"
            log_event_to_file(log_message)

            # starting new thread (handle_client)
            # client's socket informaiton, client address information, and client ID will be passed as parameters
            client_thread = threading.Thread(target=handle_client, args=(client_socket, client_address, clientID))
            client_thread.start()
# ----------------------------------------------------------------------------------------------------------------- #
                    

# -- Server & Logging Functions ----------------------------------------------------------------------------------- #        
# Function Name: get_ip_address()
# Description  : This function search host internet connection and return an available IP address
#               If an availble IP address is not found, return the localhost
# Parameters   : void
# Return       : IP address                    
def get_ip_address():
    interfaces = netifaces.interfaces()  # Grab host network information and store to the variable
    
    valid_addresses = []  # List to store valid addresses
    for interface in interfaces:  # Iterator
        addr_info = netifaces.ifaddresses(interface).get(netifaces.AF_INET)  # netifaces.ifaddresses(interface) : return dictionary type of address information
        
        # Search all valid IP Address and store in 'valid_address'
        if addr_info:
            for addr in addr_info:  # If available IPv4 address is found
                if 'addr' in addr and not addr['addr'].startswith('127.'):  # return that address
                    valid_addresses.append(addr['addr'])

    # If a valid address exists, return the last address
    if valid_addresses:
        print(f"Last valid IP found: {valid_addresses[-1]}")
        return valid_addresses[-1]
    else:
        return '127.0.0.1'  # If a usable IP address is not found even after cycling through all the contents, the localhost address is returned.              # If a usable IP address is not found even after cycling through all the contents, the localhost address is returned.


# Function Name: handle_client()
# Description  : Handle the connection close and keep in track of clients' responsing time
#               If a client has not responce in set time, close the connection
#               For whatever reason, disconnection of client will be displayed and logged    
# Parameters   : client_socket : Socket information
#                client_address: Connected client's address information
#                clientID      : Assigned client ID
# Return       : void     
def handle_client(client_socket, client_address, clientID):
    global current_connections

    with client_socket:       
        # Set timeout on client socket to 60 seconds
        client_socket.settimeout(TIME_OUT)

        try:
            while True:
                try:
                    data = client_socket.recv(BUFFER_SIZE).decode('utf-8')
                    if not data:
                        # Receive connection termination signal (empty data) from client
                        print(f"Client ID {clientID} has closed the connection.")
                        break
                except socket.timeout:
                    # If no data is received for 60 seconds, break
                    print(f"Timeout: Client ID {clientID} did not respond for 60 seconds.")
                    break
                
                # Analyze client packet and proccess it depending on the logic
                # The proccessing result will be sent and logged at the logging file  
                log_event(client_socket, client_address, data, clientID)               

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
                # Decrease the number of currently connected clients
                current_connections -= 1
                
                # print and log disconnected customer info and the number of currently connecting client
                print(f"ClientID:{clientID} is disconnected. \n Current connections: {current_connections}")
                timestamp = time.strftime('%b %d %H:%M:%S', time.localtime())  # Get current date and time
                hostname = socket.gethostname()  # Get the host name
                log_message = f"INFO: {timestamp} {hostname} MyEventLog[1234]: Client_ID {clientID}: from {client_address} is disconnected - Current connections: {current_connections}"
                log_event_to_file(log_message)

            # Close the connection
            client_socket.close()
    

# Function Name: log_event()
# Description  : This function makes a log message format and passes it to the log_envent_to_file() for logging
#               Also, the severity level and proccessing result will be sent to the client
#               The packet protocol is the same as below
#                   >> {severity_level}; {processed_result_message}             
#               The log format is the same as below
#                   >> {severity_level}: {current_date_time} {host_name} applicaiton_name: {clientID}: recieved_data_from_client - {processed_result_message}
# Parameters   :client_socket : Socket information
#               client_address: Connected client's address information
#               data          : Message sent from the client side that requires processing
#               clientID      : Assigned client ID       
# Return       : void
def log_event(client_socket, client_address, data, clientID):
    """
    Writes logs to a text file
    """
    timestamp = time.strftime('%b %d %H:%M:%S', time.localtime())  # Get current date and time
    hostname = socket.gethostname() 

    # Extract the severity_level and process_result from the event_result
    event_result = event_handle(data, clientID)
    severity_level = event_result.get("severity_level", "INFO")      # Default to INFO if not specified
    process_result = event_result.get("process_result", "Undefined") # Default to Undefined if not specified

    # Set the log message format
    log_message = f"{severity_level}: {timestamp} {hostname} MyEventLog[1234]: Client_ID {clientID}: {data} from {client_address} - {process_result}"
    print(log_message)              # print the log message
    log_event_to_file(log_message)  # write the log message to the text file

    # Handling events and responding to clients
    response_message = f"{severity_level};{process_result}"
    client_socket.send(response_message.encode('utf-8'))


# Function Name: log_event_to_file()
# Description  : Log the log_message to the text file        
# Parameters   : log_message             
# Return       : void
def log_event_to_file(log_message):
    """
    write the log message to the text file
    """
    global log_file_lock    # Prevent simultaneous access to resources (text files)
    with log_file_lock:
        with open(LOG_FILE, "a") as log_file:
            log_file.write(log_message + "\n")
            print(f"Logged to file: {log_message}")


# Function Name: event_handle()
# Description  : This function has the major business logic of this application
#                Two major features of this application are 'login validation' and 'requested file validation'
#                The functionality of those two features are the same as below:
#                 1. Login Validation       
#                   >> Firstly it checks wheter the flag(first block of the packet) is 'LOGIN' or not
#                   >> If so, it split the ID and PW information from the second bock using key-value pair
#                   >> Next it checks whether the ID and PW are matched or not
#                     >> If they are mathced, returns 'INFO' as severity_level and 'Login_Success' as proccess_result 
#                     >> It they are not matched, checks  the number of login attempts made so far by the client.
#                       >> If less than 3 times, returns 'NOTICE' as severity_level and 'Invalid_ID_or_PW' as proccess_result    
#                       >> If more than 3 times, returns 'WARNING' as severity_level and 'Too_Many_Failed_Attempts' as proccess_result
#                 2. File Request Validation                                             
#                   >> Firstly it checks wheter the flag(first block of the packet) is 'REQUEST' or not
#                   >> If so, extract the file extention and check whether it is valid or not
#                     >> If the client request an invalid extention of file, returns 'NOTICE' as severity_level and 'Not_allowed_file_extension:{file_extension}' as proccess_result 
#                   >> If the client requests a file with a valid file extension, check whether the file exists in the directory 
#                     >> If the file exists, returns 'INFO' as severity_level and 'File_Sent' as proccess_result
#                     >> If the file exists but you do not have access rights, 'ERROR' as severity_level and 'Access_Denied' as proccess_result  
#                     >> If the file not exists, returns 'NOTICE' as severity_level and 'File_Not_Found' as proccess_result
#                 3. Non of above - returns 'NOTICE' as severity_level and 'Protocol_Error' as proccess_result                                   
# Parameters   : data, clientID             
# Return       : {severity_level: , process_result: } pair
#               >> Wrong format                  : {"severity_level": "NOTICE", "process_result": "Protocol_Error"}
#               >> Login success                 : {"severity_level": "INFO", "process_result": "Login_Success"} 
#               >> Invaild ID/PW                 : {"severity_level": "NOTICE", "process_result": "Invalid_ID_or_PW"}
#               >> Login failed more than 3 times: {"severity_level": "WARNING", "process_result": "Too_Many_Failed_Attempts"}
#               >> Valid file request            : {"severity_level": "INFO", "process_result": f"File_Sent"}
#               >> Invalid file extention        : {"severity_level": "NOTICE", "process_result": f"Not allowed_file_extension: {file_extension}"}
#               >> Requested file not exits      : {"severity_level": "NOTICE", "process_result": f"File_Not_Found"}
#               >> Request a file that requires access: {"severity_level": "ERROR", "process_result": f"Access_Denied"}            
def event_handle(data, clientID):
    if ';' in data:
        command, params = data.split(';', 1)

        if command == "LOGIN":
            global login_attempts
            client_attempts = login_attempts.get(clientID, 0)  # 기존 시도 횟수 가져오기

            params_dict = dict(param.split('=') for param in params.split('&'))
            user_id = params_dict.get("ID")
            password = params_dict.get("PW")

            if user_id == TEST_ID and password == TEST_PW:
                print("Login successful.")
                login_attempts[clientID] = 0  # Reset number of attempts on success
                return {"severity_level": "INFO", "process_result": "Login_Success"}
            else:
                client_attempts += 1                        # Increase number of attempts in case of failure
                login_attempts[clientID] = client_attempts  # Save updated attempts
                print(f"Login attempt with ID: {user_id}, Password: {password}, Attempts: {client_attempts}")
                
                if client_attempts >= 3:
                    print("Login failed. Too many failed attempts.")
                    return {"severity_level": "WARNING", "process_result": "Too_Many_Failed_Attempts"}
                else:
                    return {"severity_level": "NOTICE", "process_result": "Invalid_ID_or_PW"} 


        # File request validation
        " 1. Return INFO when the allowed file is requested and successfully sent to client"
        " 2. Return NOTICE when requesting an incompatible file extension & file not found"
        " 3. Return WARNING when a client requests a file to which it does not have access rights"
        if command == "REQUEST":
                file_extension = params.split('.')[-1]
                
                # Extension check
                if file_extension not in TEST_FILE_EXTENTIONS:
                    print(f"The file extension '{file_extension}' is not allowed.")
                    return {"severity_level": "NOTICE", "process_result": f"Not_allowed_file_extension:{file_extension}"}
                
                # Check for file requests you don't have permission to access
                if params == TEST_INVALID_FILE_NAME:
                    print(f"File access denied.")
                    return {"severity_level": "ERROR", "process_result": f"Access_Denied"}
                
                # file name check
                if params == TEST_FILE_NAME:
                    print(f"File exists. File is sent.")
                    return {"severity_level": "INFO", "process_result": f"File_Sent"}
                else:
                    print(f"File not exists.")
                    return {"severity_level": "NOTICE", "process_result": f"File_Not_Found"}

            
    else:
        print("Protocol Error.")
        return {"severity_level": "NOTICE", "process_result": "Protocol_Error"}
# ----------------------------------------------------------------------------------------------------------------- #


if __name__ == "__main__":
    main()