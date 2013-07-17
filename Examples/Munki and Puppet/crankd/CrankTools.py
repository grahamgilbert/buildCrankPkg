#!/usr/bin/env python
#
#    CrankTools.py
#        The OnNetworkLoad method is called from crankd on a network state change, all other
#            methods assist it. Modified from Gary Larizza's script (https://gist.github.com/glarizza/626169).
#
#    Last Revised - 10/07/2013

__author__ = 'Graham Gilbert (graham@grahamgilbert.com)'
__version__ = '0.5'

import syslog
import subprocess
from time import sleep

syslog.openlog("CrankD")

class CrankTools():
    """The main CrankTools class needed for our crankd config plist"""
    
    def puppetRun(self):
        """Checks for an active network connection and calls puppet if it finds one.
            If the network is NOT active, it logs an error and exits
        ---
        Arguments: None
        Returns:  Nothing
        """
        command = ['/usr/bin/puppet','agent','-t']
        if not self.LinkState('en1'):
            self.callCmd(command)
        elif not self.LinkState('en0'):
            self.callCmd(command)
        else:
            syslog.syslog(syslog.LOG_ALERT, "Internet Connection Not Found, Puppet Run Exiting...")
    
    def munkiRun(self):
        """Checks for an active network connection and calls Munki if it finds one.
            If the network is NOT active, it logs an error and exits
        ---
        Arguments: None
        Returns:  Nothing
        """
        command = ['/usr/local/munki/managedsoftwareupdate','--auto']
        if not self.LinkState('en1'):
            self.callCmd(command)
        elif not self.LinkState('en0'):
            self.callCmd(command)
        else:
            syslog.syslog(syslog.LOG_ALERT, "Internet Connection Not Found, Munki Run Exiting...")
    
    def callCmd(self, command):
        """Simple utility function that calls a command via subprocess
        ---
        Arguments: command - A list of arguments for the command
        Returns: Nothing
        """
        task = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        task.communicate()
    
    def LinkState(self, interface):
        """This utility returns the status of the passed interface.
        ---
        Arguments:
            interface - Either en0 or en1, the BSD interface name of a Network Adapter
        Returns:
            status - The return code of the subprocess call
        """
        return subprocess.call(["ipconfig", "getifaddr", interface])
    
    def OnNetworkLoad(self, *args, **kwargs):
        """Called from crankd directly on a Network State Change. We sleep for 10 seconds to ensure that
            an IP address has been cleared or attained, and then perform a Puppet run and a Munki run.
        ---
        Arguments:
            *args and **kwargs - Catchall arguments coming from crankd
        Returns:  Nothing
        """
        sleep(10)
        self.puppetRun()
        self.munkiRun()

def main():
    crank = CrankTools()
    crank.OnNetworkLoad()

if __name__ == '__main__':  
    main() 