using NUnit.Framework;
using NAD_A03_Logging_Client;

namespace ClientTest
{
    [TestFixture]
    public class CLNT_INFO_Test
    {
        [SetUp]
        public void Setup()
        {
            // Setup code here (if needed)
        }

        [Test]
        public void LoginMessage_HappyPath()
        {
            // Arrange
            string expectedPacket = "LOGIN;testID;testPW;";
            string loginID = "testID";
            string loginPW = "testPW";
            string requestFilename = "example.txt";
            CLNT_INFO clientInfo = new CLNT_INFO(loginID, loginPW, requestFilename);

            // Act
            string actualPacket = clientInfo.LoginMessage();

            // Assert
            Assert.AreEqual(expectedPacket, actualPacket);
        }
    }
}