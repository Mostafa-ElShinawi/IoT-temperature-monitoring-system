import socket
import threading

TEMP_THRESHOLD = (15, 30)  
HUMIDITY_THRESHOLD = (30, 60)  

def evaluate_readings(temp, humidity):
    if temp < TEMP_THRESHOLD[0]:
        return "TEMP LOW"
    elif temp > TEMP_THRESHOLD[1]:
        return "TEMP HIGH"
    elif humidity < HUMIDITY_THRESHOLD[0]:
        return "HUMIDITY LOW"
    elif humidity > HUMIDITY_THRESHOLD[1]:
        return "HUMIDITY HIGH"
    else:
        return "NORMAL"


def handle_client(client_socket, client_id):
    print(f"Client {client_id} connected.")
    try:
        while True:
      
            message = client_socket.recv(1024)
            if not message:
                print(f"Client {client_id} disconnected.")
                break

            decoded_message = message.decode('utf-8')
            print(f"Received from Client {client_id}: {decoded_message}")


            try:
                temp, humidity = map(float, decoded_message.split(","))
            except ValueError:
                print(f"Invalid data format from Client {client_id}.")
                continue

        
            status = evaluate_readings(temp, humidity)
            print(f"Evaluation for Client {client_id}: {status}")

            client_socket.send(status.encode('utf-8'))
    except Exception as e:
        print(f"Error with Client {client_id}: {e}")
    finally:
        client_socket.close()
        print(f"Client {client_id} connection closed.")


def main():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    port = 5375  
    try:
        server_socket.bind(('192.168.1.7', port))
        server_socket.listen(5)
        print(f"Server is listening on port {port}...")

        client_id = 1
        while True:
           
            try:
                client_socket, addr = server_socket.accept()
                print(f"Connection from {addr}")
                client_thread = threading.Thread(target=handle_client, args=(client_socket, client_id))
                client_thread.start()
                client_id += 1
            except Exception as e:
                print(f"Error accepting a connection: {e}")
    except Exception as e:
        print(f"Server error: {e}")
    finally:
        server_socket.close()
        print("Server socket closed.")

if __name__ == '__main__':
    main()
