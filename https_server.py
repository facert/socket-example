import socket
import select
from http.server import BaseHTTPRequestHandler, HTTPServer


class ProxyHandler(BaseHTTPRequestHandler):

    def send_data(self, sock, data):
        print(data)
        bytes_sent = 0
        while True:
            r = sock.send(data[bytes_sent:])
            if r < 0:
                return r
            bytes_sent += r
            if bytes_sent == len(data):
                return bytes_sent

    def handle_tcp(self, sock, remote):
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
                    result = self.send_data(remote, data)
                    if result < len(data):
                        raise Exception('failed to send all data')

                if remote in r:
                    data = remote.recv(4096)
                    if len(data) <= 0:
                        break
                    result = self.send_data(sock, data)
                    if result < len(data):
                        raise Exception('failed to send all data')
        except Exception as e:
            raise(e)
        finally:
            sock.close()
            remote.close()

    def do_CONNECT(self):

        # 解析出 host 和 port
        uri = self.path.split(":")
        host, port = uri[0], int(uri[1])
        host_ip = socket.gethostbyname(host)

        remote_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        remote_sock.connect((host_ip, port))
        # 告诉客户端 CONNECT 成功
        self.wfile.write("{protocol_version} 200 Connection Established\r\n\r\n".format(protocol_version=self.protocol_version).encode())

        # 转发请求
        self.handle_tcp(self.connection, remote_sock)


def main():
    try:
        server = HTTPServer(('', 8888), ProxyHandler)
        server.serve_forever()
    except KeyboardInterrupt:
        server.socket.close()


if __name__ == '__main__':
    main()
