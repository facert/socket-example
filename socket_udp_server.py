import socket

# AF_INET: 基于 IPV4 的网络通信 SOCK_DGRAM: 基于 udp 的流式 socket 通信
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
# 将套接字绑定到地址
s.bind(('127.0.0.1', 8888))

while True:
    data, addr = s.recvfrom(1024)
    print('Received from %s:%s.' % addr)
    s.sendto(b'Hello, %s!' % data, addr)
