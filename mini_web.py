import socket


if __name__ == '__main__':
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
        # 接收客户端的请求信息
        recv_data = new_socket.recv(4096).decode('utf-8')
        print(recv_data)

        # 打开文件
        with open('static/login.html', 'r') as file:
            file_data = file.read()

        # 响应行
        response_line = 'HTTP/1.1 200 OK\r\n'
        # 响应头
        response_header = 'Server: PWS/1.1\r\n'
        # 响应体
        response_body = file_data
        # 把数据封装成HTTP 响应报文格式的数据
        response = response_line + response_header + '\r\n' + response_body
        response_data = response.encode('utf-8')
        # 发送给浏览器的套接字
        new_socket.send(response_data)

        new_socket.close()
