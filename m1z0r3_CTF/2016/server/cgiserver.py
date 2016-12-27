import http.server

server_address = ("", 12345)
handler_class = http.server.CGIHTTPRequestHandler #1 ハンドラを設定
server = http.server.HTTPServer(server_address, handler_class)
server.serve_forever()
