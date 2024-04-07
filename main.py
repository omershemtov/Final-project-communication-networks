import socket
import threading
import time
import struct
from questions import trivia_questions
import random
from server import build_game, send_question_to_players, send_msg, play_game, broadcast_server_details

# Listen on all available network interfaces
UDP_PORT = 13117  # UDP port for broadcasting
TCP_PORT = 12346  # TCP port for client connections
server_name = "trivia_server"
magic_cookie = 0xabcddcba
message_type = 0x2
send_offers = True
time_to_play = None
time_counter = False
FORMAT = "utf-8"
# List to store connected player addresses
while True:
    broadcast_thread = threading.Thread(target=broadcast_server_details)
    broadcast_thread.start()
    players_list, questions_list = build_game()
    if len(players_list) > 0:
        play_game(players_list, questions_list)
        players_list = []
