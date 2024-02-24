/*
* Filename: Program.cs
* Project: Assignment 3
* By: Jongeon Lee, Honggyu Park
* Date: Feb 24, 2024
* Description: This program is that communication between Client and Server as TCP/IP.
*              This is Client side code that has test cases for server side. test description will be introduce in the code comments.
*/

<<<<<<< HEAD

using System;
using System.Collections.Generic;
using System.Linq;
=======
using System;
using System.Collections.Generic;
using System.Linq;
using System.Net.Sockets;
using System.Net;
>>>>>>> 6e3aa415a13b3d18f5f945ff045824ad20bd00b4
using System.Text;
using System.Threading.Tasks;

namespace NAD_A03_Logging_Client
{
    internal class Program
    {
        static void Main(string[] args)
        {
<<<<<<< HEAD
=======
            // Test setting
            bool Login = true; // false = request test
            // Set the all required information
#if true // true = automatic test, false = manual test
            string serverIP = "192.168.1.86";
            int serverPort = 8000;
            string login_ID = "Chris";
            string login_PW = "Jongeon";
            string request_Filename = "test.txt";
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
            } while (!TCPCommunication.IsValidIP(serverIP) || string.IsNullOrWhiteSpace(serverIP));

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
            Console.WriteLine("Enter the filename to request :");
            request_Filename = Console.ReadLine();
             
#endif

            // Create an instance of TCPIP class
            ClientInformation clientInfo = new ClientInformation(login_ID, login_PW, request_Filename);
            TCPCommunication tcpip = new TCPCommunication(serverIP, serverPort, clientInfo);

            try
            {
                Console.WriteLine("Try to Connect to server...");
                Console.WriteLine("");

                // Connect to the server
                tcpip.ConnectToServer();
                Console.WriteLine("## Connect to server completed! ##");

                // Send message to the server
                if (Login)
                {
                    tcpip.SendMessage(clientInfo.LoginMessage());
                }
                else
                {
                    tcpip.SendMessage(clientInfo.RequestMessage());
                }
                Console.WriteLine("Send message completed!");
                Console.WriteLine("");
                Console.WriteLine("Listening for messages from the server...");

                bool isConnect = true;
                while (isConnect)
                {
                    try
                    {
                        // Receive a message from the server
                        isConnect = tcpip.ReceiveMessage();
                    }
                    catch (Exception ex)
                    {
                        Console.WriteLine($"Error: {ex.ToString()}");
                        break;
                    }
                    Console.WriteLine();
                }

                // Close the socket
                tcpip.CloseSocket();
            }
            catch (Exception ex)
            {
                Console.WriteLine($"Error: {ex.ToString()}");
                tcpip.CloseSocket();
            }
>>>>>>> 6e3aa415a13b3d18f5f945ff045824ad20bd00b4
        }
    }
}
