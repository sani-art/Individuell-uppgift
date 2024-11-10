import socket
import threading

# Definiera IP-adressen och porten som klienten snsluter till
SERVER_IP = '127.0.0.1' # Standard-IP för lokal anslutning
PORT = 5000 # Standardport för serverkommunikation

# Funktion för att lyssna på inkommande meddelanden från servern 
def receive_messages(client_socket, name):
    while True:
        message = input(f"{name}: ")
        # Om meddelandet är 'avslut', avsluta loopen utan att trigga exception
        if message.lower() == 'avslut':
            print("Chatten avslutas! Until next time.")
            client_socket.close()
            break 
        try:
            client_socket.send(message.encode('utf-8'))

        except socket.error: # Hantera socketfel
            # Om socketen stängs av servern eller användaren
            print("Kunde inte skicka meddelande!")
            client_socket.close()
            break
        except Exception as e: 
            # Hantera eventuella fel genom att avsluta anslutningen 
            print(f"Ett fel uppstod: {e}")
            client_socket.close()
            break

# Funktion för att starta klienten och ansluta till servern
def start_client():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Be användaren om servern IP och portnummer för anslutning
    server_ip = input("Ange servenrs IP-adress: ")
    server_port = int(input("Ange serverns portnummer: "))
    
    # Försök att ansluta till servern med de angivna uppgifterna
    try:
        client_socket.connect((SERVER_IP, PORT))
    except:
        print("Kunde inte ansluta till servern. Kontrollera IP-adress och portnummer.")
        return

    # Be om användarnamn och skicka det till servern
    name = input("Ange ditt namn här: ")
    client_socket.send(name.encode('utf-8'))

    # Starta en tråd för att hantera inkommande meddelanden från servern
    thread = threading.Thread(target=receive_messages, args=(client_socket, name))
    thread.start()

    # Ett välkomstmeddelande
    print('Välkommen till chatten ' + name + '!')

    # Förklara för användaren hur de kan lämna chatten
    print("För att lämna chatten, skriv 'Avslut'.")

    # Låt användaren skriva och skicka meddelanden till de avslutar
    while True: 
        message = input(f"{name}: ")
        if message.lower() == 'avslut':  # Avsluta vid "Avslut"
            print('Chatten avslutas! Until next time.')
            client_socket.close()   # Stänger anslutningen
            break   # Avlsuta loopen, ingen mer input eller meddelande skickas
        try:
            client_socket.send(message.encode('utf-8'))
        except:
            # Vid fel, informera användaren och avsluta anslutningen
            print("Kunde inte skicka meddelandet.")
            client_socket.close()
            break

# Om skriptet körs direkt, starta klienten
if __name__ == "__main__":
    start_client()