/*
* Filename: Program.cs
* Project: Assignment 3
* By: Jongeon Lee, Honggyu Park
* Date: Feb 24, 2024
* Description: This program is that communication between Client and Server as TCP/IP.
*              This is Client side code that has test cases for server side. test description will be introduce in the code comments.
*/

using System;
using System.Collections.Generic;
using System.Linq;
using System.Net.Sockets;
using System.Net;
using System.Text;
using System.Threading.Tasks;

namespace NAD_A03_Logging_Client
{
    internal class Program
    {
        static void Main(string[] args)
        {
            // Set the all required information
#if true
            string serverIP = "127.0.0.1";
            int serverPort = 8000;
            string login_ID = "testID";
            string login_PW = "testPW";
            string request_Filename = "example.txt";
#else
            string serverIP;
            string login_ID;
            string login_PW;
            string request_Filename;
            // Get the IP address from user input
            do
            {
                Console.WriteLine("Enter the server IP address:");
                serverIP = Console.ReadLine();
            } while (!TCPIP_CMNC.IsValidIP(serverIP) || string.IsNullOrWhiteSpace(serverIP));

            // Get the port number from user input
            int serverPort;
            do
            {
                Console.WriteLine("Enter the server port number :");
            } while (!int.TryParse(Console.ReadLine(), out serverPort));

            // Get login credentials from user input
            do
            {
                Console.WriteLine("Enter your login ID :");
                login_ID = Console.ReadLine();
            } while (string.IsNullOrWhiteSpace(login_ID) || login_ID.Length > 20); 

            do
            {
                Console.WriteLine("Enter your login password :");
                login_PW = Console.ReadLine();
            } while (string.IsNullOrWhiteSpace(login_PW) || login_PW.Length > 20); 

            // Get the filename to request from user input
            do
            {
                Console.WriteLine("Enter the filename to request :");
                request_Filename = Console.ReadLine();
            } while (string.IsNullOrWhiteSpace(request_Filename) || !request_Filename.Contains(".")); 
#endif

            // Create an instance of TCPIP class
            ClientInformation clientInfo = new ClientInformation(login_ID, login_PW, request_Filename);
            TCPCommunication tcpip = new TCPCommunication(serverIP, serverPort, clientInfo);

            try
            {
                // Connect to the server
                tcpip.ConnectToServer();

                // Send message to the server
                tcpip.SendMessage(clientInfo.LoginMessage());
                Console.WriteLine("Listening for messages from the server...");
                while (true)
                {
                    try
                    {
                        // Receive a message from the server
                        tcpip.ReceiveMessage();
                        tcpip.ServerMessageParse(tcpip.recevedMessage);
                    }
                    catch (Exception ex)
                    {
                        Console.WriteLine($"Error: {ex.ToString()}");
                        break;
                    }
                    // Check if the user wants to exit
                    Console.WriteLine("Press 'x' to exit, or any other key to continue...");
                    if (Console.ReadKey().Key == ConsoleKey.X)
                        break;

                    Console.WriteLine();
                }

                // Close the socket
                tcpip.CloseSocket();
            }
            catch (Exception ex)
            {
                Console.WriteLine($"Error: {ex.ToString()}");
            }
        }
    }
}
