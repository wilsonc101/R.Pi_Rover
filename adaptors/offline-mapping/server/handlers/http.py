from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import ConfigParser
import time


# from StringIO import StringIO
class http_handler(BaseHTTPRequestHandler):
    import actions.get as actionGet
    import actions.post as actionPost

    def log_message(self, *args):
        self.log = None


    def do_GET(self):
       # Example URL dictionary
       # urls = {'/action/getmap': self.actionGet.getMap,
       #         '/action/platformlist': self.actionGet.getPlatforms}
        
        print "TEST PATH -- " + self.path

        urls = {'/test': self.actionGet.test}

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
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "POST, GET, OPTIONS")
        self.end_headers()
        self.wfile.write(response)


    def do_POST(self):

        post_data_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(post_data_length)

        http_code, response = self.actionPost.post(self.path, 
                                                self.headers, 
                                                post_data)

        self.send_response(int(http_code))
        self.send_header("Content-type", "text/html")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "POST, GET, OPTIONS")
        self.end_headers()
        self.wfile.write(response)
