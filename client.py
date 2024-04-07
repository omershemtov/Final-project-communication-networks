import socket
import threading
import time
from time import sleep
import struct
from inputimeout import inputimeout
from questions import bcolors

# Client configuration
UDP_IP = "0.0.0.0"  # Listen on all available network interfaces
UDP_PORT = 13117  # UDP port for receiving server details
FORMAT = "utf-8"
server_socket = None
server_ip = None
tcp_port = None
color_class = bcolors()


def close_player_connection(player_socket):
    try:
        player_socket.shutdown(socket.SHUT_RDWR)  # Shutdown the socket for both reading and writing
        player_socket.close()  # Close the socket
    except socket.error:
        pass


def listen_on_udp():
    global server_socket, server_ip, tcp_port
    # Create a UDP socket for receiving server details
    client_udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    client_udp_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    client_udp_socket.bind((UDP_IP, UDP_PORT))

    print(f"Client started, listening for offer requests...")

    # Receive the server details from the UDP broadcast
    try:
        data, address = client_udp_socket.recvfrom(1024)
        magic_cookie, message_type, server_name, tcp_port = struct.unpack('!Ib32sH', data)
        server_name = server_name.decode(FORMAT).rstrip()

        if magic_cookie == 0xabcddcba and message_type == 0x2:
            server_ip = address[0]
            print(f"received offer from server {server_name} at address {server_ip}, attempting to connect...")
            # Connect to the server over TCP
            server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            return server_socket, server_ip, tcp_port
        else:
            print("Invalid server details received, ignoring and continuing listening...")
    except struct.error as e:
        print(f"Error unpacking data: {e}")


def main():
    global server_socket, server_ip, tcp_port
    while server_socket is None:  # if someone else trys to connect to the client without correct cookie or message
        server_socket, server_ip, tcp_port = listen_on_udp()

    optional_ans = ['1', '0', 't', 'f', 'n', 'y']
    try:
        server_socket.connect((server_ip, tcp_port))
        send_msg('not bot', server_socket)
        player_name = server_socket.recv(1024).decode().strip()
        player_color = server_socket.recv(1024).decode().strip()
        print(player_color+f'My name is {player_name}'+color_class.END)

        in_game = True
        while in_game:
            in_game_msg = server_socket.recv(1024).decode().strip()
            if in_game_msg[0] == '$':  # only player in the game is you
                print(player_color+in_game_msg[1:]+color_class.END)
                return
            # print(1)
            if in_game_msg == 'not in game':
                in_game = False
                # print(in_game_msg)
                print(player_color+'the game is over for you'+color_class.END)
                # print(2)
            else:
                # print(in_game_msg)
                question_msg = server_socket.recv(1024).decode().strip()
                # no_ans = True
                # # message = server_socket.recv(1024).decode().strip()
                #
                # while no_ans:
                #     answer = input(question_msg).strip()
                #     if answer in optional_ans:
                #         send_msg(answer, server_socket)
                #         no_ans = False
                #     else:
                #         print("not valid answer .\n optional answers: 1,0,t,f,n,y ")
                t = time.time()
                time_left = 10
                while time.time() < t + 10:
                    try:
                        answer = inputimeout(prompt=player_color+question_msg+color_class.END, timeout=time_left)
                    except:  # answer = input(question_msg).strip()
                        print(player_color+'too long to answer'+color_class.END)
                        print(player_color+'the game is over for you'+color_class.END)
                        in_game = False
                        break

                    if answer in optional_ans:
                        send_msg(answer, server_socket)
                        break
                    else:
                        print(player_color+"not valid answer .\n optional answers: 1,0,t,f,n,y "+color_class.END)
                        time_left = t + 10 - time.time()
                game_status_msg = server_socket.recv(1024).decode().strip()
                print(player_color+game_status_msg+color_class.END)
                # print(3)
        # time.sleep(1)
        game_over_msg = server_socket.recv(1024).decode().strip()
        print(player_color+game_over_msg+color_class.END)
        # time.sleep(1)
        # game_over_msg = server_socket.recv(1024).decode().strip()
        # print(game_over_msg)
        # print(4)
        # print('asdasddasda')
        # time.sleep(5)
        # Close the TCP connection
        close_player_connection(server_socket)
        server_socket = None

    except:
        server_socket = None
        pass


def send_msg(msg, client_socket):
    message = msg.encode(FORMAT)
    client_socket.send(message)


if __name__ == "__main__":
    main()
