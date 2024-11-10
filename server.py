import socket
import threading

# Definiera serverns IP-adress och portnummer för anslutningar
SERVER_IP = '127.0.0.1' # Använd localhost för lokal anslutning
PORT = 5000 # porten som servern lyssnar på för inkommande anslutningar

# Lista för att hålla reda på alla aktiva klientanslutningar
clients = []

# Funktion som hanterar varje enskild klientanslutning 
def handle_clients(client_socket, client_address):
    try:
        # Mottag klientens namn som det första meddelandet och lägg till i klientlistan
        name = client_socket.recv(1024).decode('utf-8')
        clients.append({'socket': client_socket, 'address': client_address, 'name': name})

        # Skicka ett välkomstmeddelande till alla andra anslutna klienter
        welcome_message = f"{name} har anslutit till chatten!"
        print(welcome_message)
        broadcast(welcome_message, client_socket)

        # Lyssna kontinuerligt på inkommande meddelanden från klienten
        while True:
            message = client_socket.recv(1024).decode('utf-8')
            if message:
                # Om ett meddelande mottas, skicka det till alla andra klienter
                broadcast(f"{name}: {message}", client_socket)
            else:
                # Om meddelandet är tomt, ta bort klienten (brtyder att anslutningen bröts)
                remove_client(client_socket)
                break
    except:
        # Om något undantag sker, ta bort klienten från anslutningarna
        remove_client(client_socket)

# Funktion för att skicka ett meddelande till alla klienter utom avsändaren
def broadcast(message, current_client):
    for client in clients:
        if client['socket'] != current_client:  # Skicka inte meddelandet tillbaka till avsändaren 
            try:
                client['socket'].send(message.encode('utf-8'))  # Skicka meddelandet
            except:
                # Om det uppstår fel, ta bort klienten från anslutningarna
                remove_client(client['socket'])

# Funktion för att hantera bortkoppling av klient och meddela andra om bortkopplingen
def remove_client(client_socket):
    for client in clients:
        if client['socket'] == client_socket:
            clients.remove(client)
            disconnect_message = f"{client['name']} har lämnat chatten!"
            print(disconnect_message)
            broadcast(disconnect_message, client_socket)
            client_socket.close()   # Stäng anslutningen för klienten
            break

# Funktion för att starta servern och hantera inkommande klientanslutningar
def start_server():
    # Skapa en socket för servern och sätt upp inställningar
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind((SERVER_IP, PORT))   # Binda socket till angiven IP-adress och port
    server_socket.listen()

    # Bekräfta att servern startats korrekt
    host, port = server_socket.getsockname()
    print(f"Servern startad på {SERVER_IP}:{PORT}")

    # Evig loop för att acceptera nya klientanslutningar
    while True: 
        client_socket, client_address = server_socket.accept()  # acceptera en ny anslutning
        print(f"Ansluten till {client_address}")

        # Starta en ny tråd för att hantera den anslutna klientens meddelanden
        thread = threading.Thread(target=handle_clients, args=(client_socket, client_address))
        thread.start()

# Om skriptet körs direkt, starta servern
if __name__ == "__main__":
    start_server()