import json

class platformType():
    def __init__(self):
        self.op = "register:platform-type"
        self.type = None
        # Optional
        self.desc = None
        self.attr = None
        self.correl = None

    def generateJSON(self):
        # Type must be set for valid output - return if not set
        if self.type == None:
            return(False)

        json = {}
    
        json['op'] = self.op
        json['type'] = self.type

        # Optional fields
        if self.desc != None: json['desc'] = self.desc
        if self.attr != None: json['attr'] = self.attr
        if self.correl != None: json['correl'] = self.correl

        return(json)



class platform():
    def __init__(self):
        self.op = "register:platform"
        self.id = None
        self.type = None
        # Optional
        self.loc = {'lat': None, 'long': None, 'alt': None}
        self.desc = None
        self.attr = None
        self.correl = None

    def generateJSON(self):
        # Type & ID must be set for valid output - return if not set
        if self.type == None or self.id == None:
            return(False)
        
        json = {}

        json['op'] = self.op
        json['id'] = self.id
        json['type'] = self.type
 
        # Optional fields
        if self.loc['lat'] != None and self.loc['long'] != None and self.loc['alt'] != None: json['loc'] = self.loc
        if self.desc != None: json['desc'] = self.desc
        if self.attr != None: json['attr'] = self.attr
        if self.correl != None: json['correl'] = self.correl

        return(json)


class systemType():
    def __init__(self):
        self.op = "register:system-type"
        self.type = None
        self.services = []
        # Optional
        self.desc = None
        self.attr = None
        self.correl = None


    def generateJSON(self):
        # Type must be set for valid output - return if not set
        if self.type == None or len(self.services) < 1:
            return(False)

        # Check service is well defined
        for service in self.services:
            if 'type' not in service or 'desc' not in service or 'attr' not in service:
                return(False)

        json = {}

        json['op'] = self.op
        json['type'] = self.type
        json['services'] = self.services
            
        # Optional fields
        if self.desc != None: json['desc'] = self.desc
        if self.attr != None: json['attr'] = self.attr
        if self.correl != None: json['correl'] = self.correl
           
        return(json)
