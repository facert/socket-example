import socket

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

for data in [b'dog']:
    s.sendto(data, ('127.0.0.1', 8888))
    print(s.recv(1024))
s.close()
