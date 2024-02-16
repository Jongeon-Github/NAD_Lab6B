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

#pragma comment(lib, "Ws2_32.lib")

#define DEFALUT_PORT_NUMBER 8000

int main() {
    
    WSADATA wsaData;            // WSADATS: Window Socket API DATA
    int server_fd;              // Server_File_Discriptor: Server side socket identifier
    int new_socket;             // Identify the new socket connection (Use for client connection)
    int valread;                // Number of read bytes will be stored
    struct sockaddr_in address; // The information for the internet connection(IP Address, Port Number) will be stored
    int addrlen = sizeof(address); 
    int opt = 1;                // Represents Socket Option
    char buffer[1024] = { 0 };  // Buffer to receive data from client


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



}
