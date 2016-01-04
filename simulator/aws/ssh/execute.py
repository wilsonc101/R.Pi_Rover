import paramiko

def runRemoteScript(remotehost, scriptpath, username, password=None, keyfilepath=None, port=22):
    try:
        # Setup client, accepting unknown host keys
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

        # Use key as a preference over password, fail if neither are provided
        if keyfilepath is not None:
            client.connect(remotehost,
                           port=int(port),
                           username=str(username),
                           key_filename=str(keyfilepath),
                           allow_agent=False)

        elif password is not None:
            client.connect(remotehost,
                           port=int(port),
                           username=str(username),
                           password=str(password),
                           allow_agent=False)

        else:
            return(False)

        script_file = open(scriptpath, 'r')

        script_output = []
        script_errors = []
        for line in script_file:
            stdin, stdout, stderr = client.exec_command(line)
            stdout_txt = stdout.read()
            stderr_txt = stderr.read()

            if len(stdout_txt) > 0: script_output.append(stdout_txt)
            if len(stderr_txt) > 0: script_errors.append(stderr_txt)

        return((script_errors, script_output))

    except:
        return(False)
