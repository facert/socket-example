import socket
from urllib.parse import urlparse
from http.server import BaseHTTPRequestHandler, HTTPServer


class ProxyHandler(BaseHTTPRequestHandler):

    def _recv_data_from_remote(self, sock):
        data = b''
        while True:
            recv_data = sock.recv(4096)
            if not recv_data:
                break
            data += recv_data
        sock.close()
        return data

    def do_GET(self):
        # 解析 GET 请求信息
        uri = urlparse(self.path)
        scheme, host, path = uri.scheme, uri.hostname, uri.path
        host_ip = socket.gethostbyname(host)
        port = 443 if scheme == "https" else 80

        # 为了简单起见，Connection 都为 close, 也就不需要 Proxy-Connection 判断了
        del self.headers['Proxy-Connection']
        self.headers['Connection'] = 'close'

        # 构造新的 http 请求
        send_data = "GET {path} {protocol_version}\r\n".format(path=path, protocol_version=self.protocol_version)
        headers = ''
        for key, value in self.headers.items():
            headers += "{key}: {value}\r\n".format(key=key, value=value)
        headers += '\r\n'
        send_data += headers

        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((host_ip, port))
        # 发送请求到目标地址
        sock.sendall(send_data.encode())
        data = self._recv_data_from_remote(sock)

        self.wfile.write(data)


def main():
    try:
        server = HTTPServer(('', 8888), ProxyHandler)
        server.serve_forever()
    except KeyboardInterrupt:
        server.socket.close()


if __name__ == '__main__':
    main()
