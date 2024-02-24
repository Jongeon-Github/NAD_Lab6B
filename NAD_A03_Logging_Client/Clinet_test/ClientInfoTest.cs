using Microsoft.VisualStudio.TestTools.UnitTesting;
using System;
using NAD_A03_Logging_Client; 

namespace Clinet_test
{
    [TestClass]
    public class ClientInfoTest
    {
        string serverIP = "192.168.2.18";
        int serverPort = 8000;

        [TestMethod]
        public void LoginMessage_True()
        {
            // Arrange
            bool expectedPacket = false;
            string login_ID = "Chris"; // true
            string login_PW = "Jongeon"; // true
            string request_Filename = "test.txt"; // Don`t care
            ClientInformation clientInfo = new ClientInformation(login_ID, login_PW, request_Filename);
            TCPCommunication tcpip = new TCPCommunication(serverIP, serverPort, clientInfo);
            tcpip.ConnectToServer();
            tcpip.SendMessage(clientInfo.LoginMessage());
            tcpip.ReceiveMessage();

            // Act
            string actualPacket = tcpip.recevedMessage;
            if (actualPacket.StartsWith("INFO;"))
            {
                expectedPacket = true;
            }
            tcpip.CloseSocket();

            // Assert
            Assert.IsTrue(expectedPacket);
        }

        [TestMethod]
        public void RequestMessage_True()
        {
            // Arrange
            bool expectedPacket = false;
            string login_ID = "";
            string login_PW = "";
            string request_Filename = "test.txt"; // true
            ClientInformation clientInfo = new ClientInformation(login_ID, login_PW, request_Filename);
            TCPCommunication tcpip = new TCPCommunication(serverIP, serverPort, clientInfo);
            tcpip.ConnectToServer();
            tcpip.SendMessage(clientInfo.RequestMessage());
            tcpip.ReceiveMessage();

            // Act
            string actualPacket = tcpip.recevedMessage;
            if (actualPacket.StartsWith("INFO;"))
            {
                expectedPacket = true;
            }
            tcpip.CloseSocket();

            // Assert
            Assert.IsTrue(expectedPacket);
        }

        [TestMethod]
        public void LoginMessage_WrongPW()
        {
            // Arrange
            bool expectedPacket = false;
            string login_ID = "Chris"; // true
            string login_PW = "wrong"; // false
            string request_Filename = "test.txt"; // Don`t care
            ClientInformation clientInfo = new ClientInformation(login_ID, login_PW, request_Filename);
            TCPCommunication tcpip = new TCPCommunication(serverIP, serverPort, clientInfo);
            tcpip.ConnectToServer();
            tcpip.SendMessage(clientInfo.LoginMessage());
            tcpip.ReceiveMessage();

            // Act
            string actualPacket = tcpip.recevedMessage;
            if (actualPacket.StartsWith("NOTICE;"))
            {
                expectedPacket = true;
            }
            tcpip.CloseSocket();

            // Assert
            Assert.IsTrue(expectedPacket);
        }

        [TestMethod]
        public void LoginMessage_WrongProtocol()
        {
            // Arrange
            bool expectedPacket = false;
            string login_ID = "Chris"; // true
            string login_PW = "wrong"; // true
            string request_Filename = "test.txt"; // Don`t care
            ClientInformation clientInfo = new ClientInformation(login_ID, login_PW, request_Filename);
            TCPCommunication tcpip = new TCPCommunication(serverIP, serverPort, clientInfo);
            clientInfo.LoginProtocol = "WRONG"; // wrong login protocol
            tcpip.ConnectToServer();
            tcpip.SendMessage(clientInfo.LoginMessage());
            tcpip.ReceiveMessage();

            // Act
            string actualPacket = tcpip.recevedMessage;
            if (actualPacket.StartsWith("NOTICE;"))
            {
                expectedPacket = true;
            }
            tcpip.CloseSocket();

            // Assert
            Assert.IsTrue(expectedPacket);
        }

        [TestMethod]
        public void RequestMessage_WrongProtocol()
        {
            // Arrange
            bool expectedPacket = false;
            string login_ID = "";
            string login_PW = "";
            string request_Filename = "test.txt"; // true
            ClientInformation clientInfo = new ClientInformation(login_ID, login_PW, request_Filename);
            TCPCommunication tcpip = new TCPCommunication(serverIP, serverPort, clientInfo);
            clientInfo.RequestProtocol = "WRONG"; // wrong request protocol
            tcpip.ConnectToServer();
            tcpip.SendMessage(clientInfo.RequestMessage());
            tcpip.ReceiveMessage();

            // Act
            string actualPacket = tcpip.recevedMessage;
            if (actualPacket.StartsWith("NOTICE;"))
            {
                expectedPacket = true;
            }
            tcpip.CloseSocket();

            // Assert
            Assert.IsTrue(expectedPacket);
        }

        [TestMethod]
        public void RequestMessage_WithoutFilename()
        {
            // Arrange
            bool expectedPacket = false;
            string login_ID = "";
            string login_PW = "";
            string request_Filename = ""; // without filename
            ClientInformation clientInfo = new ClientInformation(login_ID, login_PW, request_Filename);
            TCPCommunication tcpip = new TCPCommunication(serverIP, serverPort, clientInfo);
            tcpip.ConnectToServer();
            tcpip.SendMessage(clientInfo.RequestMessage());
            tcpip.ReceiveMessage();

            // Act
            string actualPacket = tcpip.recevedMessage;
            if (actualPacket.StartsWith("NOTICE;"))
            {
                expectedPacket = true;
            }
            tcpip.CloseSocket();

            // Assert
            Assert.IsTrue(expectedPacket);
        }

        [TestMethod]
        public void RequestMessage_WithoutExtension()
        {
            // Arrange
            bool expectedPacket = false;
            string login_ID = "";
            string login_PW = "";
            string request_Filename = "test"; // without extension
            ClientInformation clientInfo = new ClientInformation(login_ID, login_PW, request_Filename);
            TCPCommunication tcpip = new TCPCommunication(serverIP, serverPort, clientInfo);
            tcpip.ConnectToServer();
            tcpip.SendMessage(clientInfo.RequestMessage());
            tcpip.ReceiveMessage();

            // Act
            string actualPacket = tcpip.recevedMessage;
            if (actualPacket.StartsWith("NOTICE;"))
            {
                expectedPacket = true;
            }
            tcpip.CloseSocket();

            // Assert
            Assert.IsTrue(expectedPacket);
        }

        [TestMethod]
        public void RequestMessage_WrongExtension()
        {
            // Arrange
            bool expectedPacket = false;
            string login_ID = "";
            string login_PW = "";
            string request_Filename = "test.abc";
            ClientInformation clientInfo = new ClientInformation(login_ID, login_PW, request_Filename);
            TCPCommunication tcpip = new TCPCommunication(serverIP, serverPort, clientInfo);
            tcpip.ConnectToServer();
            tcpip.SendMessage(clientInfo.RequestMessage());
            tcpip.ReceiveMessage();

            // Act
            string actualPacket = tcpip.recevedMessage;
            if (actualPacket.StartsWith("NOTICE;"))
            {
                expectedPacket = true;
            }
            tcpip.CloseSocket();

            // Assert
            Assert.IsTrue(expectedPacket);
        }

        [TestMethod]
        public void RequestMessage_NonExistentFile()
        {
            // Arrange
            bool expectedPacket = false;
            string login_ID = "";
            string login_PW = "";
            string request_Filename = "appleSecurity.txt";
            ClientInformation clientInfo = new ClientInformation(login_ID, login_PW, request_Filename);
            TCPCommunication tcpip = new TCPCommunication(serverIP, serverPort, clientInfo);
            tcpip.ConnectToServer();
            tcpip.SendMessage(clientInfo.RequestMessage());
            tcpip.ReceiveMessage();

            // Act
            string actualPacket = tcpip.recevedMessage;
            if (actualPacket.StartsWith("NOTICE;"))
            {
                expectedPacket = true;
            }
            tcpip.CloseSocket();

            // Assert
            Assert.IsTrue(expectedPacket);
        }


        [TestMethod]
        public void RequestMessage_AccessDenied()
        {
            // Arrange
            bool expectedPacket = false;
            string login_ID = "";
            string login_PW = "";
            string request_Filename = "cannot_open.txt";
            ClientInformation clientInfo = new ClientInformation(login_ID, login_PW, request_Filename);
            TCPCommunication tcpip = new TCPCommunication(serverIP, serverPort, clientInfo);
            tcpip.ConnectToServer();
            tcpip.SendMessage(clientInfo.RequestMessage());
            tcpip.ReceiveMessage();

            // Act
            string actualPacket = tcpip.recevedMessage;
            if (actualPacket.StartsWith("ERROR;"))
            {
                expectedPacket = true;
            }
            tcpip.CloseSocket();

            // Assert
            Assert.IsTrue(expectedPacket);
        }

        
        [TestMethod]
        public void LoginMessage_TooMuchTimeLoginAttempts()
        {
            // Arrange
            int expectedPacket = 3;
            string login_ID = "Chris"; // true
            string login_PW = "wrong"; // wrong
            string request_Filename = "test.txt"; // Don`t care
            ClientInformation clientInfo = new ClientInformation(login_ID, login_PW, request_Filename);
            TCPCommunication tcpip = new TCPCommunication(serverIP, serverPort, clientInfo);
            tcpip.ConnectToServer();
            int count = 1;
            // Act
            while(true)
            {
                tcpip.SendMessage(clientInfo.LoginMessage());
                tcpip.ReceiveMessage();
                string actualPacket = tcpip.recevedMessage;
                if (actualPacket.StartsWith("WARNING;"))
                {
                    break;
                }
                count++;
            }
            tcpip.CloseSocket();

            // Assert
            Assert.AreEqual(expectedPacket, count);
        }
    }
}
