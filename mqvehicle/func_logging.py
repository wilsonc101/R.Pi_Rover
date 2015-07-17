import logging


log_format = logging.Formatter('%(asctime)s -- %(message)s')


def CreateLogger(toconsole=0, tofile=0, filepath=0, level='WARNING'):

        # Create logger instance
        logger = logging.getLogger('pi_rover')
        SetLevel(logger, level)

        if toconsole == 1:
                ## Console Output
                log_out_console = logging.StreamHandler()
                SetLevel(log_out_console, level)
                log_out_console.setFormatter(log_format)
                logger.addHandler(log_out_console)


        if tofile == 1:
                ## File output
                log_out_file = logging.FileHandler(filepath)
                SetLevel(log_out_file, level)
                log_out_file.setFormatter(log_format)
                logger.addHandler(log_out_file)

        return(logger)


# Set logging level
def SetLevel(log_output, level):
        if level == 'CRITICAL':
                log_output.setLevel(logging.CRITICAL)
        elif level == 'ERROR':
                log_output.setLevel(logging.ERROR)
        elif level == 'WARNING':
                log_output.setLevel(logging.WARNING)
        elif level == 'INFO':
                log_output.setLevel(logging.INFO)
        elif level == 'DEBUG':
                log_output.setLevel(logging.DEBUG)

