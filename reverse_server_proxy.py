import threading
import socket
import select


# AF_INET: 基于 IPV4 的网络通信 SOCK_STREAM: 基于 TCP 的流式 socket 通信
s1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s1.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

# 将套接字绑定到地址
s1.bind(('', 2333))
# 监听TCP传入连接
s1.listen(5)


# AF_INET: 基于 IPV4 的网络通信 SOCK_STREAM: 基于 TCP 的流式 socket 通信
s2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s2.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
# 将套接字绑定到地址
s2.bind(('', 8000))
# 监听TCP传入连接
s2.listen(5)


# def handle_tcp(con1, con2):
#     os.dup2(con1.fileno(), con2.fileno())


def send_data(sock, data):
    print(data)
    bytes_sent = 0
    while True:
        r = sock.send(data[bytes_sent:])
        if r < 0:
            return r
        bytes_sent += r
        if bytes_sent == len(data):
            return bytes_sent


def handle_tcp(sock, remote):
    # 处理 client socket 和 remote socket 的数据流
    try:
        fdset = [sock, remote]
        while True:
            # 用 IO 多路复用 select 监听套接字是否有数据流
            r, w, e = select.select(fdset, [], [])
            if sock in r:
                data = sock.recv(4096)
                if len(data) <= 0:
                    break
                result = send_data(remote, data)
                if result < len(data):
                    raise Exception('failed to send all data')

            if remote in r:
                data = remote.recv(4096)
                if len(data) <= 0:
                    break
                result = send_data(sock, data)
                if result < len(data):
                    raise Exception('failed to send all data')
    except Exception as e:
        raise(e)
    finally:
        sock.close()
        remote.close()


while True:
    con1, addr1 = s1.accept()
    print("new connection from %s:%s" % addr1)
    con2, addr2 = s2.accept()
    print("new connection from %s:%s" % addr2)
    t = threading.Thread(target=handle_tcp, args=(con1, con2))
    t.start()
