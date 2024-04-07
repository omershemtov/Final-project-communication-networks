import socket
import threading
import time
import struct
from questions import trivia_questions, bcolors
import random


def get_server_ip():
    """
    Get the server's IP address.
    """
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
            s.connect(("8.8.8.8", 80))
            ip_address = s.getsockname()[0]
        return ip_address
    except Exception:
        return "127.0.0.1"

# Server configuration
server_IP = get_server_ip()  # Listen on all available network interfaces
UDP_PORT = 13117  # UDP port for broadcasting
server_name = "trivia_server"
magic_cookie = 0xabcddcba
message_type = 0x2
send_offers = True
time_to_play = None
# time_counter = False
FORMAT = "utf-8"
connected_players = [] # List to store connected player addresses
color_class = bcolors()



def check_port_in_use(port):
    # Reuse the same socket instance
    return socket_instance.connect_ex(('localhost', port)) == 0


def find_free_tcp_port(start=49152, end=65535):
    for port in range(start, end + 1):
        if not check_port_in_use(port):
            socket_instance.close()  # Close the socket after finding a free port
            return port
    raise IOError("No free port found.")


# Create a socket object outside the function to reuse it
socket_instance = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
TCP_PORT = find_free_tcp_port()


broadcast_semaphore = threading.Semaphore(1)

# Function to continuously broadcast server details over UDP
def broadcast_server_details():
    global broadcast_semaphore
    broadcast_semaphore.acquire()
    server_name_pad = server_name.ljust(32)  # Pad the server name to ensure it's 32 characters
    # Create a UDP socket
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    server_socket.bind((server_IP, UDP_PORT))
    # Pack the message according to the given format
    server_details = struct.pack('!Ib32sH', magic_cookie, message_type, server_name_pad.encode('utf-8'), TCP_PORT)

    while send_offers:
        # server_details = f"{magic_cookie}:{message_type}:{server_name_pad}:{TCP_PORT}".encode()
        server_socket.sendto(server_details, ('<broadcast>', UDP_PORT))
        time.sleep(1)
    broadcast_semaphore.release()

def generate_random_name():
    name_length = random.randint(2, 3)
    name = ''.join(random.choices(syllables, k=name_length)).capitalize()
    return name

syllables = ['jo', 'ka', 'la', 'ma', 'ri', 'ta', 'na', 'le', 'co', 'be', 'sa', 'mi', 'do', 'lu', 'ka', 'da', 're', 'me',
             'pe', 'zi']
used_names = set()


# Function to handle TCP client connections
def handle_tcp_client(client_socket):
    # global time_counter
    is_bot = client_socket.recv(1024).decode(FORMAT)

    client_name = generate_random_name()
    if is_bot == 'not bot':
        if client_name not in used_names:
            used_names.add(client_name)
    elif is_bot == 'bot':
        client_name = 'BOT ' + client_name
        if client_name not in used_names:
            used_names.add(client_name)
    else:
        raise ValueError("Invalid client type")
    send_msg(client_name, client_socket)
    client_color = bcolors.random_color()
    time.sleep(0.1)
    send_msg(client_color, client_socket)
    # Print the name of the client
    time.sleep(0.1)
    print(f"Player {client_name} joined")

    # Add the player's address to the connected players list
    connected_players.append((client_socket, client_name))
    # Check if there are multiple players connected
    if len(connected_players) > 1:
        print(color_class.GREEN + "Starting trivia game..." + color_class.END)



def send_msg(msg, client_socket):
    message = msg.encode(FORMAT)
    client_socket.send(message)


selected_questions = []


def build_game():
    # Create a TCP socket
    global connected_players
    connected_players = []
    tcp_server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    tcp_server_socket.bind((server_IP, TCP_PORT))
    tcp_server_socket.listen(5)
    tcp_server_socket.settimeout(10)  # Set a timeout of 10 seconds
    print(f"Server started, listening on IP address: {server_IP}, port: {TCP_PORT}")

    # Main server loop to accept TCP connections
    # while time_counter == False:
    while True:
        try:
            # Accept incoming TCP connections with timeout
            client_socket, address = tcp_server_socket.accept()
            print(color_class.GREEN + f"Accepted connection from {address}" + color_class.END)

            # Handle the client connection in a new thread
            client_thread = threading.Thread(target=handle_tcp_client, args=(client_socket,))
            client_thread.start()
            # print(f'active threads: {threading.active_count() - 1}')
        except socket.timeout:
            break  # Break out of the loop if no connection is received within the timeout

    # Randomly select 10 questions
    selected_questions = random.sample(trivia_questions, 10)
    return connected_players, selected_questions


# build_game()
true_ans = ['1', 't', "y"]
false_ans = ['0', 'f', 'n']


# Function to send a question to all connected players and collect their answers
def send_question_to_players(connected_players, question, correct_answer):
    # if correct_answer :
    not_playing = []
    correct_answer = true_ans
    # else:
    #     correct_answer = false_ans

    # Send the question to each player
    for player_socket, _ in connected_players:
        client_thread = threading.Thread(target=send_msg, args=(question, player_socket,))
        client_thread.start()
    # Wait for answers from players
    start_time = time.time()
    correct_players = []
    while time.time() < start_time + 10:
        pass

    for player_socket, _ in connected_players:
        try:
            # if time.time() + epsilon
            player_socket.settimeout(0.1)
            player_answer = player_socket.recv(1024).decode(FORMAT).strip().lower()
            # print('player_answer:', player_answer)

            if player_answer in correct_answer:
                correct_players.append((player_socket, _))
        except socket.error:
            not_playing.append((player_socket, _))
            pass  # Handle possible socket errors gracefully
    round_result_str = ''
    server_round_result_str = ''
    for player in connected_players:
        player_name = player[1]
        if player in correct_players:
            round_result_str = round_result_str + player_name + ' correct!\n'
            server_round_result_str = server_round_result_str + player_name +\
                            color_class.GREEN + ' correct!\n' + color_class.END
        else:
            round_result_str = round_result_str + player_name + ' incorrect!\n'
            server_round_result_str = server_round_result_str + player_name + \
                            color_class.RED + ' incorrect!\n' + color_class.END
    print(server_round_result_str)

    if round_result_str != '':
        for player in connected_players:
            client_thread = threading.Thread(target=send_msg, args=(round_result_str, player[0],))
            client_thread.start()

    return correct_players, not_playing


def play_game(connected_players, questions_list):
    global send_offers
    send_offers = False
    players_in_game = connected_players
    loss_this_round = []

    if len(connected_players) == 1:
        send_msg('$you are the only player who wants to play, try again later', connected_players[0][0])
        print('only one player wants to play, not enough players to start the game')
        send_offers = True
        close_player_connection(connected_players[0][0])
        return

    print("Trivia game started!")
    while len(players_in_game) > 1:
        # print(len(players_list))
        for i in loss_this_round:
            client_thread = threading.Thread(target=send_msg, args=('not in game', i[0],))
            client_thread.start()

        for i in players_in_game:
            client_thread = threading.Thread(target=send_msg, args=('in game', i[0],))
            client_thread.start()
            # send_msg('in game', i[0])

        time.sleep(1)  # Wait for 1 second
        # send_msg('not in game',i[0])
        loss_this_round = players_in_game
        players_in_game2, not_playing = send_question_to_players(players_in_game, questions_list[0][0],
                                                                 questions_list[0][1])
        if len(players_in_game2) > 0:
            players_in_game = players_in_game2
        players_in_game = [x for x in players_in_game if x not in not_playing]
        questions_list = questions_list[1:]
        loss_this_round = [x for x in loss_this_round if (x not in players_in_game and x not in not_playing)]
    # send_msg('not in game', i[0])
    if len(players_in_game) == 0:
        for player in connected_players:
            close_player_connection(player[0])
        send_offers = True
        return
    for i in loss_this_round:
        client_thread = threading.Thread(target=send_msg, args=('not in game', i[0],))
        client_thread.start()
    client_thread = threading.Thread(target=send_msg, args=('not in game', players_in_game[0][0],))
    client_thread.start()
    winner = players_in_game[0][1]

    time.sleep(1)
    winner_msg = f'game over!\ncongraduation to the winner: {winner}'
    for player in connected_players:
        threading.Thread(target=send_msg, args=(winner_msg, player[0],)).start()
        time.sleep(5)
        close_player_connection(player[0])
    print(color_class.CYAN + winner_msg + color_class.END)
    print('game over sending out offer requests')
    send_offers = True


def close_player_connection(player_socket):
    try:
        player_socket.shutdown(socket.SHUT_RDWR)  # Shutdown the socket for both reading and writing
        player_socket.close()  # Close the socket
    except socket.error:
        pass  # Handle possible socket errors gracefully
