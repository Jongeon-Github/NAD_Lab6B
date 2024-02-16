/*
* Filename: Server.cpp
* Project: Lab_W6B
* By: Jongeon Lee, Honggyu Park
* Date: Feb 16, 2024
* Description:
*/
#include <iostream>
#include <WinSock2.h>
#include <WS2tcpip.h>
#include <windows.h> // for logging
#include <stdlib.h>


#pragma comment(lib, "Ws2_32.lib")
#define DEFALUT_PORT_NUMBER 8000
#define MAXMUM_CONNECTION   3
#define MAX_BUFFER_SIZE     1024

int main() {
    
    WSADATA wsaData;            // WSADATS: Window Socket API DATA
    int server_fd;              // Server_File_Discriptor: Server side socket identifier
    int new_socket;             // Identify the new socket connection (Use for client connection)
    int valread;                // Number of read bytes will be stored
    struct sockaddr_in address; // The information for the internet connection(IP Address, Port Number) will be stored
    int addrlen = sizeof(address); 
    int opt = 1;                // Represents Socket Option
    char buffer[MAX_BUFFER_SIZE] = { 0 };  // Buffer to receive data from client
        
    // instantiate event log object & Register event source and obtain handle
    LPCWSTR eventSourceName = L"MyEventLog";
    HANDLE hEventLog = RegisterEventSource(NULL, eventSourceName);

    // Inititaliz Winodow Socket
    // Request Window Socket Version 2.2
    if (WSAStartup(MAKEWORD(2, 2), &wsaData) != 0) {
        perror("WSAStartup failed");
        return 1;
    }


    // Create Socket
    // Address Family: AF_INET(IPv4)
    // Socket Type   : SOCK_STREAM(= Connection-oriented socket = TCP)
    // Protocol Type : 0 (=TCP)
    if ((server_fd = socket(AF_INET, SOCK_STREAM, 0)) == INVALID_SOCKET) {
        perror("socket failed");
        WSACleanup();
        return 1;
    }


    // Sets the connection informaiton to the socket
    address.sin_family = AF_INET;                   // Using the IPv4 Internet protocol
    address.sin_addr.s_addr = INADDR_ANY;           // Allows any Internet connection
    address.sin_port = htons(DEFALUT_PORT_NUMBER);  // Allocate the port number

    // bind the host address information to the socket 
    if (bind(server_fd, (struct sockaddr*)&address, sizeof(address)) == SOCKET_ERROR) {
        perror("bind failed");
        closesocket(server_fd);
        WSACleanup();
        return 1;
    }


    /*-------------------------------------------------------------------------------------------------------------*/
    /*- Client Connection -----------------------------------------------------------------------------------------*/
    /*-------------------------------------------------------------------------------------------------------------*/
    // Listening for connection
    std::cout << "Listening a new client..." << std::endl;
    if (listen(server_fd, MAXMUM_CONNECTION) == SOCKET_ERROR) {
        perror("listen");
        closesocket(server_fd);
        WSACleanup();
        return 1;
    }

    // Infinite loop to keep the server running
    while (true) {
        // Accept connection
        if ((new_socket = accept(server_fd, (struct sockaddr*)&address, (socklen_t*)&addrlen)) == INVALID_SOCKET) {
            perror("accept");
            continue; // If an error occurs, wait for the next connection.
        }

        // Send and receive data
        valread = recv(new_socket, buffer, (MAX_BUFFER_SIZE - 1), 0); // consider about null 
        if (valread > 0) {
            buffer[valread] = '\0'; // Adds a NULL character to the end of the received data to create a string.
            std::cout << "Received data: " << buffer << std::endl;
            // send(new_socket, data, (int)strlen(data), 0);

            // Log messages in event log
            if (hEventLog != NULL) {
                // Convert received message to a wide string
                wchar_t wBuffer[MAX_BUFFER_SIZE];
                MultiByteToWideChar(CP_ACP, 0, buffer, -1, wBuffer, MAX_BUFFER_SIZE);

                LPCWSTR lpStrings[2] = { wBuffer, NULL };
                ReportEvent(hEventLog, EVENTLOG_INFORMATION_TYPE, 0, 0, NULL, 1, 0, lpStrings, NULL);
            }
        }

        // Close the each server socket
        closesocket(new_socket);
    }

    // Close the main server socket 
    closesocket(server_fd);
    // Clean up Winsock resources
    WSACleanup();

    return 0;
}
