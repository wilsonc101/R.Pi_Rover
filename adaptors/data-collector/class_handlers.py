from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import ConfigParser
import time


# from StringIO import StringIO
class http_handler(BaseHTTPRequestHandler):
    import func_actions as actions

    def log_message(self, *args):
        self.log = None

    def do_GET(self):
        urls = {'/action/getmap': self.actions.getMap,
                '/action/platformlist': self.actions.getPlatforms}

        if "?" in self.path:
            url = self.path[:self.path.find("?")]
            query = self.path[self.path.find("?"):]

        else:
            url = self.path
            query = None


        if url in urls:
            response_code, response = urls[url](query, self)
        else:
            response_code = 404
            response = "Invalid URL - " + self.path


        self.send_response(int(response_code))
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write(response)


    def do_POST(self):

        post_data_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(post_data_length)

        http_code, response = self.actions.postData(self.path, 
                                                    self.headers, 
                                                    post_data)

        self.send_response(int(http_code))
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write(response)