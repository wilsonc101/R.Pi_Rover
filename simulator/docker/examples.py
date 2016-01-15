#!/usr/bin/python -B


def _GenerateContainerConfig():
    container = {}
    container['Hostname'] = "test"
    container['Image'] = "scisys/rbase"
    container['AttachStdin'] = "false"
    container['AttachStdout'] = "true"
    container['AttachStderr'] = "true"
    container['Tty'] = "false"
    container['Volumes'] = {"/input":{}, "/output":{}}

#Test 1
#    container['Cmd'] = ["Rscript", "/input/model2.r"]

#Test 2
    container['Cmd'] = ["Rscript", "/input/R_plot_Density_DataSet_items.r"]

    container['HostConfig'] = {"Binds":["/mnt/input:/input", "/mnt/output:/output"]}
   
    return(container)


def main():

## Pretty print JSON data
#    print json.dumps(object, sort_keys=True, indent=4, separators=(',', ': '))


## Build Image from Dockerfile 
#    build_image_handler = HTTPResponseCollector()
#    _BuildImage(DOCKER_HOST, DOCKER_PORT, '/root/dockerfile.tar', 'scisys/rbase', build_image_handler)
    
#    if "Successfully built" in build_image_handler.lastline:
#        print json.loads(build_image_handler.lastline)['stream'].rstrip('\n\r ')
#    else:
#        raise SystemExit("Could not build/pull image")


## Build container
#    container_config = _GenerateContainerConfig()
#    new_container_id = _CreateContainer(DOCKER_HOST, DOCKER_PORT, json.dumps(container_config))

#    if new_container_id != False:
#        print "Created container - " + str(new_container_id)
#    else:
#        raise SystemExit("Could not create container")


## Start container
#    start_container = _StartContainer(DOCKER_HOST, DOCKER_PORT, new_container_id)
#
#    if start_container == True:
#        print "Started container - " + str(new_container_id)
#    else:
#        raise SystemExit("Could not start container")
      
    

## Search for image 
#    image = _SearchImages(DOCKER_HOST, DOCKER_PORT, IMAGE_NAME)

#    if image != False:
#        print image['name']
#    else: 
#        raise SystemExit("Image for not found")


## Download image from repository
#    get_image_handler = HTTPResponseCollector()
#    image = _GetImage(DOCKER_HOST, DOCKER_PORT, IMAGE_NAME, get_image_handler)

    # Check response body for errors
#    for response_item in get_image_handler.responsebodylist:
#        response_item = json.loads(response_item)
#        if 'error' in response_item:
#            raise SystemExit("Could not find or retrieve image")

#    print get_image_handler.lastline


## Start container based on element ##
#    containers =_GetAllContainers(DOCKER_HOST, DOCKER_PORT)
#
#    for i in containers:
#        if "yahoo" in i['Command']:
#            _StartContainer(DOCKER_HOST, DOCKER_PORT, str(i['Id']))



## Print containers ##
    containers =_GetAllContainers(DOCKER_HOST, DOCKER_PORT)

    for i in containers:
        print i['Id']
        print i['Image']
        print "--------------------"




if __name__ == "__main__":
    main()
