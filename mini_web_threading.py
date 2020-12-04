import socket
import os
import threading


def handle_client(new_socket, ip_addr):
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


def main():
    # 创建tcp套接字
    tcp_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # 设置端口复用
    tcp_server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, True)
    # 绑定端口号
    tcp_server.bind(('', 9000))
    # 设置监听
    tcp_server.listen(128)

    while True:
        # 等待接收客户端的连接请求
        new_socket, ip_addr = tcp_server.accept()
        threading_task = threading.Thread(target=handle_client, args=(new_socket, ip_addr), daemon=True)
        threading_task.start()


if __name__ == '__main__':
    main()
