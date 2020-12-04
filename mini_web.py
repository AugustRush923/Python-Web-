import socket
import threading


class HTTPServer:
    def __init__(self):
        tcp_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        tcp_server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, True)
        tcp_server.bind(('', 9000))
        tcp_server.listen(128)
        self.tcp_server = tcp_server

    @staticmethod
    def handle_client(new_socket):
        # 接收客户端的请求信息
        recv_data = new_socket.recv(4096).decode('utf-8')
        # 如果recv_data没有信息，后面代码中切片取值会报错，所以要检测一下是否为空值
        if not recv_data:
            new_socket.close()
            return
        file_path = recv_data.split('\r\n', maxsplit=2)[0].split(' ')[1]
        print(file_path)
        # 如果没跟详细地址，则返回首页
        if file_path == '/':
            file_path = '/index.html'
        # 如果没有页面，则返回404页面
        # if os.path.exists('static/' + file_path):
        #     with open('static/' + file_path, 'rb') as file:
        #         file_data = file.read()
        #
        #     # 响应行
        #     response_line = 'HTTP/1.1 200 OK\r\n'
        #     # 响应头
        #     response_header = 'Server: PWS/1.1\r\n'
        #     # 响应体
        #     response_body = file_data
        #     # 把数据封装成HTTP 响应报文格式的数据
        #     # 因为打开方式以rb模式打开，file_data为二进制格式，所以需要把响应行，响应头，和空行直接转换成二进制然后返回套接字
        #     response = (response_line + response_header + '\r\n').encode('utf-8') + response_body
        #     # 发送给浏览器的套接字
        #     new_socket.send(response)
        # else:
        #     # 响应行
        #     response_line = 'HTTP/1.1 404 Not Found\r\n'
        #     # 响应头
        #     response_header = 'Server: PWS/1.1\r\n'
        #     with open('static/error.html', 'rb') as file:
        #         file_data = file.read()
        #     response_body = file_data
        #
        #     response = (response_line + response_header + '\r\n').encode('utf-8') + response_body
        #     new_socket.send(response)
        try:
            # 打开文件
            with open('static/' + file_path, 'rb') as file:
                file_data = file.read()
            # 响应行
            response_line = 'HTTP/1.1 200 OK\r\n'
            # 响应头
            response_header = 'Server: PWS/1.1\r\n'
            # 响应体
            response_body = file_data
            # 把数据封装成HTTP 响应报文格式的数据
            # 因为打开方式以rb模式打开，file_data为二进制格式，所以需要把响应行，响应头，和空行直接转换成二进制然后返回套接字
            response = (response_line + response_header + '\r\n').encode('utf-8') + response_body
            # 发送给浏览器的套接字
        except FileNotFoundError:
            # 响应行
            response_line = 'HTTP/1.1 404 Not Found\r\n'
            # 响应头
            response_header = 'Server: PWS/1.1\r\n'
            with open('static/error.html', 'rb') as file:
                file_data = file.read()
            response_body = file_data

            response = (response_line + response_header + '\r\n').encode('utf-8') + response_body
        finally:
            new_socket.send(response)
            new_socket.close()

    def run(self):
        while True:
            new_socket, ip_port = self.tcp_server.accept()
            threading_task = threading.Thread(target=self.handle_client, args=(new_socket,), daemon=True)
            threading_task.start()


def main():
    server = HTTPServer()
    server.run()


if __name__ == '__main__':
    main()
