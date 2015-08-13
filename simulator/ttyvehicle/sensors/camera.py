from StringIO import StringIO
import pycurl
import uuid


class camera():
    def __init__(self, log=None):
        self.log = log
        self.running = True


    def captureStill(self, lat, long, heading=0, tilt=0, capturepath="/tmp", size=(600,600)):
        buffer = StringIO()


        # Form Google API URL
        url = "https://maps.googleapis.com/maps/api/streetview\
?size=" + str(size[0]) + "x" + str(size[1]) + "\
&location=" + str(lat) + "," + str(long) + "\
&fov=90\
&heading=" + str(heading) + "\
&pitch=" + str(tilt)


        c = pycurl.Curl()
        c.setopt(c.URL, url)
        c.setopt(c.WRITEDATA, buffer)
        c.perform()

        capture_filename = str(uuid.uuid1()) + ".jpg"
        capture_filepath = capturepath + "/" + capture_filename

        try:
            file = open(capture_filepath, "wb")
            file.write(buffer.getvalue())
            file.close()
            return(capture_filename)        
           
        except:
            return(False)
