/*
* Filename: Client.cpp
* Project: Lab_W6B
* By: Jongeon Lee, Honggyu Park
* Date: Feb 15, 2024
* Description: Make Server and Client with syslog login feature.
*/

#include <iostream>
#include <WS2tcpip.h>
#include <string>
#include <chrono>
#include <thread>


#pragma comment(lib, "ws2_32.lib")

#define IP "192.168.2.13"

int main() {
    // Winsock initialization
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

    // Connection
    sockaddr_in hint;
    hint.sin_family = AF_INET;
    hint.sin_port = htons(8000);
    inet_pton(AF_INET, IP, &hint.sin_addr);

    int connResult = connect(sock, (sockaddr*)&hint, sizeof(hint));
    if (connResult == SOCKET_ERROR) {
        std::cerr << "Unable to connect to server. error code: " << WSAGetLastError() << std::endl;
        closesocket(sock);
        WSACleanup();
        return -3;
    }

    // Setting data to transmit
    const char* msg = "REQUEST;test.hello";

    // Transfer data
    int sendResult = send(sock, msg, strlen(msg), 0);
    if (sendResult == SOCKET_ERROR) {
        std::cerr << "Data cannot be sent. error code: " << WSAGetLastError() << std::endl;
        closesocket(sock);
        WSACleanup();
        return -4;
    }

    // Receive data from server
    char buf[4096];
    ZeroMemory(buf, 4096); // Make sure the buffer is clean before receiving data
    int bytesReceived = recv(sock, buf, 4096, 0);
    if (bytesReceived > 0) {
        // Successfully received data from server
        std::cout << "SERVER> " << std::string(buf, 0, bytesReceived) << std::endl;
    }
    
    std::this_thread::sleep_for(std::chrono::seconds(200));

    // Socket Shutdown
    closesocket(sock);

    // Winsock shutdown
    WSACleanup();

    return 0;
}