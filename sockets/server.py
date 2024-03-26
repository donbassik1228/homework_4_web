import socket
import json
from datetime import datetime

def save_to_json(data):
    dict_data = {key: value for key, value in [el.split("=") for el in data.split("&")]}
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")
    with open("storage/data.json", "r+", encoding="utf-8") as f:
        try:
            existing_data = json.load(f)
        except json.JSONDecodeError:
            existing_data = {}
        existing_data[timestamp] = dict_data
        f.seek(0)
        json.dump(existing_data, f, indent=2, ensure_ascii=False)
        f.truncate()

def socket_server(host, port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.bind((host, port))
        server_socket.listen()
        print(f"Socket server is listening on {host}:{port}")
        while True:
            client_socket, client_address = server_socket.accept()
            with client_socket:
                print(f"Connected by {client_address}")
                data = client_socket.recv(1024).decode()
                if data:
                    save_to_json(data)
                    response = "Data saved successfully!"
                else:
                    response = "No data received."
                client_socket.sendall(response.encode())

if __name__ == "__main__":
    host = '127.0.0.1'  # localhost
    port = 5000
    socket_server(host, port)