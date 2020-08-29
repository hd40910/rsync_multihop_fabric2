import os
import traceback
from concurrent.futures.thread import ThreadPoolExecutor
from concurrent.futures._base import TimeoutError
from invoke import UnexpectedExit
import patchwork.transfers
default_timeout = 15


# DEFINE A DUMMY EXCEPTION
class FabricException(Exception):
    print (str(Exception))
    pass


def exceptionHandler(f):
    '''
        General description:This method handles the exception.
        Args:
        param1:f
        Returns:none

    '''
    def newFunction(*args, **kw):
        try:
            result = f(*args, **kw)  # VALUES SHOULD BE NEVER RETURND AS STRING
            if result:
                return result
        except (Exception, ValueError) as e:  # catch *all* exceptions
            print ('CustomExceptionHandler handled exception %s' % e)
            traceback.print_exc()
            status_message = str(e)
            status_message = status_message.replace("'", "")
            status_message = status_message.replace('"', "")
            raise Exception(status_message)
        except FabricException as e:
            raise Exception(
                "Fabric exception was received while perform given task")
        except SystemExit as e:
            raise Exception("SystemExit was received while perform given task")
    return newFunction

def handleResult(result):
    result.stdout = result.stdout.encode('ascii', 'ignore').decode('ascii')
    result.stderr = result.stderr.encode('ascii', 'ignore').decode('ascii')
    return result


def handlemessage(message):
    return message.encode('ascii', 'ignore').decode('ascii')


@exceptionHandler
def runCommand(command, warn=False, timeout=default_timeout, **kwargs):
    connect = kwargs['connect']
    command = command.strip()
    shell = kwargs.get("shell_type", "/bin/bash")
    connect.connect_timeout = timeout
    try:
        print ("fabric2:runCommand: '" + str(shell) + " " + str(command) + "' is being executed on: "\
                                 + str(connect.user) + "@" + str(connect.host) + ":" + str(connect.port))
        
        with ThreadPoolExecutor(1,__name__+".runCommand") as p:
            f = p.submit(connect.run,str(command), warn=warn, shell=shell)
            return handleResult(f.result(timeout=timeout))
    except TimeoutError as e:
        print ('Error :' + "Command timed out maximum wait time :"+str(timeout)+" sec")
        raise ValueError("Command timed out maximum wait time :"+str(timeout)+" sec")
    except UnexpectedExit as e:
        if hasattr(e.result, 'stderr') and e.result.stderr:
            print ('Error :' + str(handlemessage(e.result.stderr)))
            raise ValueError(str(handlemessage(e.result.stderr)))
        if hasattr(e.result, 'stdout') and e.result.stdout:
            print ('Error :' + str(handlemessage(e.result.stdout)))
            raise ValueError(str(handlemessage(e.result.stdout)))
        print ('Error :' + str(e.result))
        raise ValueError(str(e.result))
    except Exception as e:
        if hasattr(e, 'message') and e.message:
            e.message = handlemessage(e.message)
            raise ValueError(str(e.message))
        elif hasattr(e, 'strerror') and e.strerror:
            e.strerror = handlemessage(e.strerror)
            raise ValueError(str(e.strerror))
        else:
            raise ValueError(str(e))
    finally:
        try:
            connect.close()
        except Exception:
            pass

@exceptionHandler
def rsync_to_remote(copy_from,copy_to, **kwargs):
    connect = kwargs.pop('connect')
    kwargs.pop("shell_type")
    kwargs.pop("reload_command")
    try:
        patchwork.transfers.rsync(connect, copy_from, copy_to,**kwargs)
    except UnexpectedExit as e:
        if hasattr(e.result, 'stderr') and e.result.stderr:
            print ('Error :' + str(handlemessage(e.result.stderr)))
            raise ValueError(str(handlemessage(e.result.stderr)))
        if hasattr(e.result, 'stdout') and e.result.stdout:
            print ('Error :' + str(handlemessage(e.result.stdout)))
            raise ValueError(str(handlemessage(e.result.stdout)))
        print ('Error :' + str(e.result))
        raise ValueError(str(e.result))
    except Exception as e:
        if hasattr(e, 'message') and e.message:
            e.message = handlemessage(e.message)
            raise ValueError(str(e.message))
        elif hasattr(e, 'strerror') and e.strerror:
            e.strerror = handlemessage(e.strerror)
            raise ValueError(str(e.strerror))
        else:
            raise ValueError(str(e))
    finally:
        try:
            connect.close()
        except Exception:
            pass