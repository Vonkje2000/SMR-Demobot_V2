import socket
import time
import select 

def udp_start(HOST, PORT, TRG_HOST_R, TRG_HOST_L):
    # Create a UDP socket
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_socket.bind((HOST, PORT))
    print("UDP server started.")
    server_socket.setblocking(0)

    left = True
    while True:
        # Send responses
        response = '1'
        print("Sending data (L = true / R = false) -> ", left)
        if (left):
            server_socket.sendto(response.encode(), TRG_HOST_L)
            time.sleep(2)
        else:
            server_socket.sendto(response.encode(), TRG_HOST_R)
            time.sleep(2)
        # Wait for confirmation message
        ready = select.select([server_socket], [], [], 5)
        if ready[0]:
            print("Socket ready to recieve data")
            data, addr = server_socket.recvfrom(1024)
            print("Received confirmation : ", data.decode())
        left = not left
        
    # Close the socket (never reached in this example)
    server_socket.close()

if __name__ == '__main__':
    RIGHT_KAWA = '192.168.0.1'
    LEFT_KAWA = '192.168.0.2'
    HOST = '192.168.0.10'  # Your PC's IP address
    PORT = 10010  # Port to listen on (non-privileged ports are > 1023)
    TRG_HOST_L = (LEFT_KAWA, PORT)
    TRG_HOST_R = (RIGHT_KAWA, PORT)
    udp_start(HOST, PORT, TRG_HOST_R, TRG_HOST_L)