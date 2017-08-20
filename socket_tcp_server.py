import socket
import threading

# AF_INET: 基于 IPV4 的网络通信 SOCK_STREAM: 基于 TCP 的流式 socket 通信
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# 将套接字绑定到地址
s.bind(('127.0.0.1', 8888))
# 监听TCP传入连接
s.listen(5)


def handle_tcp(sock, addr):
    print("new connection from %s:%s" % addr)
    sock.send(b'Welcome!')

    while True:
        data = sock.recv(1024)
        if not data:
            break
        sock.send(b'Hello, %s!' % data)
    sock.close()


while True:
    sock, addr = s.accept()
    t = threading.Thread(target=handle_tcp, args=(sock, addr))
    t.start()
