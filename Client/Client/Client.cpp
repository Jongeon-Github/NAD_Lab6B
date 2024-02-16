/*
* Filename: Client.cpp
* Project: Lab_W6B
* By: Jongeon Lee, Honggyu Park
* Date: Feb 15, 2024
* Description: Make Server and Client with syslog login feature.
*/

#include <iostream>
#include <WS2tcpip.h>

#pragma comment(lib, "ws2_32.lib")

int main() {
    // Winsock initilation
    WSADATA wsData;
    WORD ver = MAKEWORD(2, 2);

    int wsResult = WSAStartup(ver, &wsData);
    if (wsResult != 0) {
        std::cerr << "Winsock initialization failed. error code: " << wsResult << std::endl;
        return -1;
    }

    // Create socket
    SOCKET sock = socket(AF_INET, SOCK_STREAM, 0);
    if (sock == INVALID_SOCKET) {
        std::cerr << "Socket creation failed. error code: " << WSAGetLastError() << std::endl;
        WSACleanup();
        return -2;
    }







    // Socket Shutdown
    closesocket(sock);

    // Winsock shutdown
    WSACleanup();
    
    return 0;
}
