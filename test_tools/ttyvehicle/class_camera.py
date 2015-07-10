import uuid
import pycurl

from StringIO import StringIO


class camera():
    def __init__(self, log=None):
        self.log = log
        self.running = True


    def captureStill(self, lat, long, heading=0, tilt=0, capturepath="/var/www/html/capture", size=(600,600)):
        print "HERE"
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

        capture_filepath = capturepath + "/" + str(uuid.uuid1()) + ".jpg"

        try:
            file = open(capture_filepath, "wb")
            file.write(buffer.getvalue())
            file.close()
            return(capture_filepath)        
           
        except:
            return(False)
