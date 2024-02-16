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

int main() {
    
    WSADATA wsaData;            // WSADATS: Window Socket API DATA
    int server_fd;              // Server_File_Discriptor: Server side socket identifier
    int new_socket;             // Identify the new socket connection (Use for client connection)
    int valread;                // Number of read bytes will be stored
    struct sockaddr_in address; // The information for the internet connection(IP Address, Port Number) will be stored
    int addrlen = sizeof(address); 
    int opt = 1;                // Represents Socket Option
    char buffer[1024] = { 0 };
}
