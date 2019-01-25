#  coding: utf-8 
import socketserver, mimetypes, os

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
        self.data = self.data.decode(encoding="utf-8")
        self.data = self.data.split("\r\n")
        # The HTTP request
        request = self.data[0]
        # Processing headers 
        headers = {}
        for line in self.data[1:]:
            key,value = line.split(": ",maxsplit=1)
            headers[key] = value
        method = request.split(" ")[0]

        if(method == "GET"):
            _,location,HTTP = request.split(" ")
            path = os.path.relpath("www"+location)
            
            if(path[0:3] != 'www'):
                # Trying to go OOB
                self.err404()
                return
            # If a valid file
            if os.path.isfile(path):
                self.sendcontent(path)
            # If 301
            elif location[-1] != "/" and os.path.isdir(path):
                path += "/"
                redirHeader = "HTTP/1.1 301 Moved Permanently\r\nLocation: "+path+"\r\n\r\n"
                self.request.sendall(bytearray(redirHeader,'utf-8'))
                return

           # If an OK dir 
            elif os.path.isdir(path):
                path += "/index.html"
                self.sendcontent(path)
                 
            # Else 404       
            else:
                self.err404() 
                return
        else:
            # Else 405
            errorheader = "HTTP/1.1 405 Method Not Allowed\r\n\r\n"
            self.request.sendall(bytearray(errorheader,'utf-8'))
                
    def err404(self):
        errorheader = "HTTP/1.1 404 Not Found \r\n\r\n"
        self.request.sendall(bytearray(errorheader,'utf-8'))

    def sendcontent(self,path):
        with open(path,"r") as currfile:
                    content = currfile.read() 
                    contentType,_ = mimetypes.guess_type(path)
                    if contentType:
                        foundHeader = "HTTP/1.1 200 OK \r\nContent-type: "+contentType+"\r\n\r\n"
                    else:
                        foundHeader = "HTTP/1.1 200 OK \r\nContent-type:text/plain\r\n\r\n"
                    package = foundHeader+content
                    self.request.sendall(bytearray(package,'utf-8'))


if __name__ == "__main__":
    HOST, PORT = "localhost", 8080

    socketserver.TCPServer.allow_reuse_address = True
    # Create the server, binding to localhost on port 8080
    server = socketserver.TCPServer((HOST, PORT), MyWebServer)

    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    server.serve_forever()
