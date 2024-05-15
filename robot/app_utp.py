import socket
import time

def udp_start(HOST, PORT, TRG_HOST):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_socket.bind((HOST, PORT))
    print("UDP server started.")

    while True:
        input("Press Enter to send data...")  # Waits for Enter key press to proceed
        response = '1'
        print("Sending data")
        server_socket.sendto(response.encode(), TRG_HOST)
        time.sleep(2)  # Optional: delay between sends

if __name__ == '__main__':
    HOST = '192.168.0.2'  # Local IP address
    PORT = 10010  # Port to listen on
    TRG_HOST = ('192.168.0.1', PORT)  # Target host and port
    udp_start(HOST, PORT, TRG_HOST)
