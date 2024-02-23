using System;
using System.Linq;
using System.Net;
using System.Net.Sockets;
using System.Runtime.CompilerServices;
using System.Text;

namespace NAD_A03_Logging_Client
{
    public class TCPCommunication
    {
        private string serverIP;
        private int serverPort;
        private Socket clientSocket;
        public string recevedMessage;
        private ClientInformation clientInfo;

        // Constructor
        public TCPCommunication(string serverIP, int serverPort, ClientInformation clientInfo)
        {
            this.serverIP = serverIP;
            this.serverPort = serverPort;
            this.clientInfo = clientInfo;
            clientSocket = new Socket(AddressFamily.InterNetwork, SocketType.Stream, ProtocolType.Tcp);
            this.recevedMessage = "";
        }

        // Method to connect to the server
        public void ConnectToServer()
        {
            try
            {
                // Create an IPEndPoint using the server's IP address and port number
                IPEndPoint serverEndPoint = new IPEndPoint(IPAddress.Parse(serverIP), serverPort);

                // Connect to the server
                clientSocket.Connect(serverEndPoint);
            }
            catch (Exception ex)
            {
                Console.WriteLine($"Error: {ex.ToString()}");
            }
        }

        // Method to send a message to the server
        public void SendMessage(string message)
        {
            try
            {
                // Send the message to the server
                byte[] messageBytes = Encoding.UTF8.GetBytes(message);
                clientSocket.Send(messageBytes);
                Console.WriteLine("Message sent successfully.");
            }
            catch (Exception ex)
            {
                Console.WriteLine($"Error: {ex.ToString()}");
            }
        }

        // Method to receive a message from the server
        public bool ReceiveMessage()
        {
            try
            {
                // Receive data from the server
                byte[] buffer = new byte[1024];
                int bytesRead = clientSocket.Receive(buffer);

                // Convert the received data to a string and display it
                this.recevedMessage = Encoding.UTF8.GetString(buffer, 0, bytesRead);

                byte[] bytes = Encoding.UTF8.GetBytes(this.recevedMessage);
                int size = bytes.Length;

                Console.WriteLine("Received message size : " + size);            
                Console.WriteLine("Received message from server: " + this.recevedMessage);
            }
            catch (Exception ex)
            {
                Console.WriteLine($"Error: {ex.ToString()}");
                return false;
            }
            return true;
        }

        // Method to close the socket
        public void CloseSocket()
        {
            try
            {
                // Close the socket
                clientSocket.Shutdown(SocketShutdown.Both);
                clientSocket.Close();
            }
            catch (Exception ex)
            {
                Console.WriteLine($"Error: {ex.ToString()}");
            }
        }

        // Static method to validate an IP address
        public static bool IsValidIP(string ipString)
        {
            string[] splitValues = ipString.Split('.');
            if (splitValues.Length != 4)
                return false;

            byte tempForParsing;
            return splitValues.All(r => byte.TryParse(r, out tempForParsing));
        }
    }

    public class ClientInformation
    {
        private string login_protocol;
        private string request_protocol;
        private string login_ID;
        private string login_PW;
        private string request_Filename;

        public ClientInformation(string login_ID, string login_PW, string request_Filename)
        {
            this.login_protocol = "LOGIN;";
            this.request_protocol = "REQUEST;";
            this.login_ID = login_ID;
            this.login_PW = login_PW;
            this.request_Filename = request_Filename;
        }

        public string LoginProtocol
        {
            get { return login_protocol; }
            set { login_protocol = value; }
        }
        public string RequestProtocol
        {
            get { return request_protocol; }
            set { request_protocol = value; }
        }

        public string LoginMessage()
        {
            return $"{login_protocol}ID={login_ID}&PW={login_PW}";
        }

        public string RequestMessage()
        {
            return $"{request_protocol}{request_Filename}";
        }

    }

}
