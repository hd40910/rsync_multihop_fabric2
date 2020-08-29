'''
Created on Jun 20, 2018

@author: PDINDA
'''

from Services import RemoteAuthenticationService
from Services.fabfile import runCommand,rsync_to_remote

class ConnectionHandler():
    def __init__(self,machine_details):
        self.machine_details = machine_details
        self.remote_authentication_service = RemoteAuthenticationService.RemoteAuthenticationService()

    def runCommand(self,command, **keyargs):
        return self.remote_authentication_service.authenticate(self.machine_details, self.run_on_remote,command, **keyargs)

    def run_on_remote(self,command, **keyargs):
        result = runCommand(command, False, **keyargs)
        return str(result.stdout).strip()
    
    def rsync(self,copy_from,copy_to, **keyargs):
        return self.remote_authentication_service.authenticate(self.machine_details, self.rsync_to_remote,copy_from,copy_to, **keyargs)

    def rsync_to_remote(self,copy_from,copy_to, **keyargs):
        result = rsync_to_remote(copy_from,copy_to, **keyargs)
        return str(result.stdout).strip()                
    
