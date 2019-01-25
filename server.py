#  coding: utf-8 
import socketserver

# Copyright 2013 Abram Hindle, Eddie Antonio Santos
# 
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# 
#     http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
#
# Furthermore it is derived from the Python documentation examples thus
# some of the code is Copyright © 2001-2013 Python Software
# Foundation; All Rights Reserved
#
# http://docs.python.org/2/library/socketserver.html
#
# run: python freetests.py

# try: curl -v -X GET http://127.0.0.1:8080/


class MyWebServer(socketserver.BaseRequestHandler):

    def handle(self):
        self.data = self.request.recv(1024).strip()
        print(self.data)
        self.data = self.data.decode(encoding="utf-8")
        print(self.data)
        self.data = self.data.split("\r\n")
        print(self.data)
        # The HTTP request
        request = self.data[0]
        # Processing headers 
        headers = {}
        for line in self.data[1:]:
            key,value = line.split(": ",maxsplit=1)
            headers[key] = value
        method = request.split(" ")[0]
        error404page = "<html><h1>404 Error: Not Found</h1></html>"  
        error405page = "<html><h1>405 Error: Method not supported</h1></html>"  

        if(method == "GET"):
            print("Recieved a GET request")
            _,location,HTTP = request.split(" ")
            try:
                with open("www"+location,"r") as currfile:
                    content = currfile.read() 
                foundHeader = "HTTP/1.1 200 OK \r\n\r\n"
                package = foundHeader+content
                self.request.sendall(bytearray(package,'utf-8'))
                print("THAT FILE DOES EXIST")
            except FileNotFoundError:
                errorheader = """HTTP/1.1 404 Not Found \r\n\r\n"""
                package = errorheader + self.error404page
                self.request.sendall(bytearray(package,'utf-8'))
                print("THAT FILE DOESN'T EXIST")

        else:
            errorheader = """HTTP/1.1 405 Method Not Allowed\r\n\r\n"""
            package = errorheader + self.error405page
            self.request.sendall(bytearray(package,'utf-8'))
            
        self.request.sendall(bytearray("OK",'utf-8'))

if __name__ == "__main__":
    HOST, PORT = "localhost", 8080

    socketserver.TCPServer.allow_reuse_address = True
    # Create the server, binding to localhost on port 8080
    server = socketserver.TCPServer((HOST, PORT), MyWebServer)

    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    server.serve_forever()
