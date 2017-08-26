import socket
import select


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
    s_conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s_conn.connect(("**.**.**.**", 2333))

    client_conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_conn.connect(('127.0.0.1', 8000))

    handle_tcp(s_conn, client_conn)
