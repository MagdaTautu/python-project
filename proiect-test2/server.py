import socket
import threading
import random
generated = False
over=False
clients_score = [0,0]
def generate_number():
    return random.randint(1, 50)

def handle_client(client_socket, client_number, mode, number_of_clients):
    global client_sockets
    global num_to_guess
    global generated
    global over
    global num_players
    global clients_score
    if num_players == 1:
        num_to_guess = generate_number()
        print(f"The server generated the number {num_to_guess}")
        client_sockets[client_number].sendall("Server generated a number".encode())
        client_sockets[client_number].sendall("Your turn. Please guess a number!".encode())
        while True:
                guess = client_sockets[client_number].recv(1024).decode()
                clients_score[client_number] +=1 
                if guess.isdigit():
                    guess = int(guess)
                    if guess == num_to_guess:
                        client_socket.sendall(f"Correct! You guessed it! GAME OVER! Current score: {clients_score[client_number]}".encode())
                        print("Client guessed the number!")
                        for sock in client_sockets:
                            sock.close()
                        break
                    else:
                        if guess < num_to_guess:
                            client_sockets[client_number].sendall(f"Try a higher number. Current score:{clients_score[client_number]}".encode())
                        else: client_sockets[client_number].sendall(f"Try a smaller number. Current score:{clients_score[client_number]}".encode())
                        print("Client guessed ", guess)

    if num_players == 2:
        clients_score=[1,1]
        if mode == 1:  # Server generates the number
            if client_number == 0:
                num_to_guess = generate_number() 
                print(f"The server generated the number {num_to_guess}")
                client_socket.sendall(f"Your turn. Please guess a number!".encode())
            else:
                client_socket.sendall(f"Wait for the other player to guess.".encode())

            while over == False:
                guess = client_socket.recv(1024).decode()
                if "end" in guess:
                    for sock in client_sockets:
                        sock.close()
                    break
                if guess.isdigit():
                    guess = int(guess)
                    if guess == num_to_guess:
                        clients_score[client_number] +=1 
                        client_socket.sendall(f"Correct! You guessed it! GAME OVER! Current score: {clients_score[client_number]}".encode())
                        other_client = 1 - client_number
                        client_sockets[other_client].sendall(f"You lost! The other player guessed it! GAME OVER! Current score: {clients_score[other_client]}".encode())
                        over = True
                       
                    else:
                        clients_score[client_number] +=1 
                        if guess < num_to_guess:
                            client_sockets[client_number].sendall(f"Try a higher number. Wait for the other player. ".encode())
                        else: client_sockets[client_number].sendall(f"Try a smaller number. Wait for the other player.".encode())
                        other_client = 1 - client_number
                        client_sockets[other_client].sendall(f"Current score: {clients_score[other_client]}".encode())
                        client_sockets[other_client].sendall(f"Your turn. Please guess a number!".encode())

        elif mode == 2:  # First client generates the number
            global generated
            if generated is False:
                if client_number == 0:
                    client_socket.sendall("Please generate a number to be guessed: ".encode())
                    num_to_guess = client_socket.recv(1024).decode()
                    client_sockets[1].sendall("The first client generated the number. ".encode())

                    print(f"The first client generated the number {num_to_guess}")
                    generated = True
                else:
                    client_socket.sendall("Wait for the other player to generate.".encode())

                while not generated:
                    pass 

                if client_number == 1:
                    client_sockets[client_number].sendall("Your turn. Please guess the number! ".encode())
                num_to_guess=int(num_to_guess)
                while True:
                    if client_number == 1:
                        print("waiting for client 2")
                        guess = client_sockets[1].recv(1024).decode()

                        if guess.isdigit():
                            guess = int(guess)
                            if guess == num_to_guess:
                                client_sockets[client_number].sendall("Correct! You guessed it! GAME OVER!".encode())
                                other_client = 1 - client_number
                                client_sockets[other_client].sendall(f"Client {client_number + 1} guessed it! GAME OVER!".encode())
                                for sock in client_sockets:
                                    sock.close()
                                break
                            else:
                                other_client = 1 - client_number
                                client_sockets[other_client].sendall("Not yet ".encode())
                                if guess < num_to_guess:
                                    client_sockets[client_number].sendall("Try a higher number. Your turn.".encode())
                                else: client_sockets[client_number].sendall("Try a smaller number. Your turn.".encode())
                    elif client_number == 0:
                        pass

number_of_clients = 0
def start_server(num_players, mode):
    global client_sockets
    global generated 
    global number_of_clients
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(('localhost', 9999))
    server.listen(num_players)

    print(f"Server started. Waiting for {num_players} connections...")

    client_sockets = []
    generated = False

    while len(client_sockets) < num_players:
        
        client_socket, addr = server.accept()
        client_sockets.append(client_socket)

        client_thread = threading.Thread(target=handle_client, args=(client_socket, len(client_sockets) - 1, mode, number_of_clients))
        client_thread.start()

mode = 1 #default
num_players = int(input("Enter the number of players: "))
if num_players == 1:
    mode = 1
    start_server(num_players, mode)
elif num_players >2:
    print("Maximum number of players = 2")
else:
    mode = int(input("Who will generate the number to be guessed? 1-SERVER 2-CLIENT: "))
    start_server(num_players, mode)
