using System;
using System.Net.Sockets;
using System.Threading;
using UnityEngine;


public class TCPTestClient : MonoBehaviour
{
    private TcpClient client;
    private NetworkStream stream;
    private Thread receiveThread;

    public string serverAddress;
    public int serverPort;
    bool running = true;


    [SerializeField] GameObject connect_button;
    private void Start()
    {
        connect_button.SetActive(true);
    }

    public void SendMessage(string msg)
    {
        if (!client.Connected) return;
        string message = msg;
        byte[] data = System.Text.Encoding.UTF8.GetBytes(message);
        try
        {
            stream.Write(data, 0, data.Length);
        }
        catch (Exception e)
        {
            Debug.Log("Error acord when tring to send msg : " + e);
        }
    }

    public void SendMessage()
    {
        if (!client.Connected) return;
        string message = "Hello from client!";
        byte[] data = System.Text.Encoding.UTF8.GetBytes(message);
        try
        {
            stream.Write(data, 0, data.Length);
        }
        catch(Exception e)
        {
            Debug.Log("Error acord when tring to send msg : " + e);
        }
    }

    public void ConnectToServer()
    {
        try
        {
            client = new TcpClient(serverAddress, serverPort);
            stream = client.GetStream();
            Debug.Log("Connected to server: " + serverAddress + ":" + serverPort);
            receiveThread = new Thread(new ThreadStart(ReceiveData));
            receiveThread.Start();
            running = true;
        }
        catch (Exception e)
        {
            Debug.Log("Error connecting to server: " + e.Message);
        }
    }
    void ReceiveData()
    {
        while (running)
        {
            try
            {
                // Read data from server
                byte[] buffer = new byte[1024];
                int bytesRead = stream.Read(buffer, 0, buffer.Length);
                if (bytesRead > 0)
                {
                    string response = System.Text.Encoding.UTF8.GetString(buffer, 0, bytesRead);
                    Debug.Log("Received response: " + response);
                    HandleData(response);
                }
            }
            catch (Exception e)
            {
                Debug.Log(e);
            }
        }
    }

    private void HandleData(string response)
    {
        //Do as the server commands

    }

    public void Disconnect()
    {
        // Stop the receive thread
        running = false;
        if (receiveThread != null && receiveThread.IsAlive)
        {
            this.SendMessage("Disconnecting");
            receiveThread.Abort();
        }

        if (client != null)
        {
            client.Close();
            client = null;
        }
    }

    void OnApplicationQuit()
    {
        Disconnect();
    }
}