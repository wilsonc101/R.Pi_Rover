import socket
import threading

import picamera


class camera(threading.Thread):
    def __init__(self, bind_address, port, res_x, res_y, name, log=None):
        self.log = log
        threading.Thread.__init__(self)
        
        # Setup camera/create object
        self.camera = picamera.PiCamera(resolution=(int(res_x), int(res_y)))

        try:
            # Setup socket
            self.server_socket = socket.socket()
            self.server_socket.bind((bind_address, int(port)))
            self.server_socket.listen(0)

            # Accept a single connection and make a file-like object out of it

            if self.log != None: self.log.info("Camera - Socket open.")
            self.running = False


        except:
            # Socket in use or cannot be bound
            self.running = False

            if self.log != None: 
                self.log.error("Camera - port in use.")
            else:
                print "Camera - port in use."




    def run(self):
        # Make camera live and wite to socket connection
        self.running = True

        while self.running:
            try:

                self.connection = self.server_socket.accept()[0].makefile('wb')

                try:
                    self.camera.start_recording(self.connection, format='h264', bitrate=4000000)
                    self.camera.vflip=True
                    self.camera.hflip=True
                    self.camera.wait_recording(6000000)
                    self.recording = True    
                    if self.log != None: self.log.info("Camera - recording started.")


                finally:
                    if self.log != None: self.log.info("Camera - recording stopped.")
    
                    self.camera.stop_recording()
                    self.connection.close()
                    self.server_socket.close()


            except:

                if self.log != None: 
                    self.log.error("Camera - connection dropped")
                else:
                    print "Camera - connection dropped"



