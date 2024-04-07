import random
import socket
import time
from time import sleep
import struct
from client import close_player_connection ,listen_on_udp ,send_msg
from questions import bcolors
# Client configuration
UDP_IP = "0.0.0.0"  # Listen on all available network interfaces
UDP_PORT = 13117  # UDP port for receiving server details
FORMAT = "utf-8"
server_socket = None
server_ip = None
tcp_port = None
end_color = bcolors.END

def main():
    global server_socket, server_ip, tcp_port
    while server_socket is None:  # if someone else trys to connect to the client without correct cookie or message
        server_socket, server_ip, tcp_port = listen_on_udp()


    try:
        server_socket.connect((server_ip, tcp_port))
        send_msg('bot', server_socket)
        player_name = server_socket.recv(1024).decode().strip()
        player_color = server_socket.recv(1024).decode().strip()
        print(player_color + f'My name is {player_name}' + end_color)

        in_game = True
        while in_game:
            in_game_msg = server_socket.recv(1024).decode().strip()
            if in_game_msg[0] == '$':  # only player in the game is you
                print(player_color +in_game_msg[1:] + end_color)
                return
            if in_game_msg == 'not in game':
                in_game = False
                print(player_color+'the game is over for you'+end_color)
            else:
                question_msg = server_socket.recv(1024).decode().strip()
                print(player_color+question_msg+end_color)
                sleep(random.uniform(1, 6))
                answer = random.choice(['1', '0'])
                    # if answer in optional_ans:
                send_msg(answer, server_socket)

                game_status_msg = server_socket.recv(1024).decode().strip()
                print(player_color+game_status_msg+end_color)

        game_over_msg = server_socket.recv(1024).decode().strip()
        print(player_color+game_over_msg+end_color)

        game_over_msg = server_socket.recv(1024).decode().strip()
        print(player_color+game_over_msg+end_color)
        close_player_connection(server_socket)
        server_socket = None

    except:
        server_socket = None
        pass



if __name__ == "__main__":
    main()
