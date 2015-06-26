import json
import class_edgware as edgware

def registerEdgwareTypes(mqtt_client=None):
    services = {}
    services['temp-sensor'] = {"type":"temp-sensor", 
                               "mode":"request-response"}

    services['pressure-sensor'] = {"type":"pressure-sensor", 
                                   "mode":"request-response"}

    services['vehicle-control'] = {"type":"vehicle-control", 
                                   "mode":"request-response"}


    systems = {}
    systems['vehicle'] = {"type":"vehicle", 
                          "services":[{"type":services['temp-sensor']['type']}, 
                                      {"type":services['pressure-sensor']['type']}]}

    systems['control'] = {"type":"control",
                          "services":[{"type":services['vehicle-control']['type']}]}


    platforms = {}
    platforms['pi-rover'] = {"type":"pi-rover"}

    i = 100
    for service in services:
        i += 1
        service_type = edgware.serviceType()
        service_type.type = services[service]['type']
        service_type.mode = services[service]['mode']
        service_type.correl = i
#        writeMQTTOutput(mqtt_client, MQTT_TOPIC_IN, json.dumps(service_type.generateJSON()))

    i = 1000
    for system in systems:
        i += 1
        system_type = edgware.systemType()
        system_type.type = systems[system]['type']
        system_type.services = systems[system]['services']
        system_type.correl = i
#        writeMQTTOutput(mqtt_client, MQTT_TOPIC_IN, json.dumps(system_type.generateJSON()))

    i = 2000
    for platform in platforms:
        i += 1
        platform_type = edgware.platformType()
        platform_type.type = platforms[platform]['type']
        platform_type.correl = i
#        writeMQTTOutput(mqtt_client, MQTT_TOPIC_IN, json.dumps(platform_type.generateJSON()))





registerEdgwareTypes()
