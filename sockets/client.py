import socket

def send_data_to_server(host, port, data):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
        client_socket.connect((host, port))
        client_socket.sendall(data.encode())
        response = client_socket.recv(1024).decode()
        print(f"Server response: {response}")

if __name__ == "__main__":
    host = '127.0.0.1'  # localhost
    port = 5000
    data_to_send = "username=user&message=Hello, World!"
    send_data_to_server(host, port, data_to_send)