import socket

# Создаем TCP-сокет
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Подключаемся к серверу
server_address = ('localhost', 12345)
client_socket.connect(server_address)

# Отправляем сообщение серверу
message = "Как дела?"
client_socket.send(message.encode())

# Получаем ответ от сервера
print(client_socket.recv(1024).decode())

# Закрываем соединение
client_socket.close()
