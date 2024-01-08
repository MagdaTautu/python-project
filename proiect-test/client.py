import socket
over = False
def start_client():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(('localhost', 9999))  # Change the IP and port if needed
    global over
    print("Connected to the server")

    while  over == False:
        message = client.recv(1024).decode()
        print(message)

        if "Your turn" in message:
            guess = input("Enter your guess: ")
            client.sendall(guess.encode())
        if "Please generate a number to be guessed:" in message:
            generate = input("Generate a number to be guessed: ")
            client.sendall(generate.encode())
        elif "Wait for the other player to generate" in message:
            response = client.recv(1024).decode()
            print(response)
        elif "Wait for the other player to guess" in message:
            response = client.recv(1024).decode()
            print(response)
        elif "Not yet" in message:
            response = client.recv(1024).decode()
            print(response)
        elif "GAME OVER" in message:
            over = True
            client.close()
            break


            # if "Correct" in response or "GAME OVER" in response:
            #     break

start_client()
