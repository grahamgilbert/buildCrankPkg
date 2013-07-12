#!/usr/bin/env python
#
#    CreateCrankPkg.py
#        Creates a pkg to deploy CrankD from a fresh git clone
#
#    Last Revised - 11/07/2013

import optparse
import argparse
import os
import sys
import shutil
import subprocess

__author__ = 'Graham Gilbert (graham@grahamgilbert.com)'
__version__ = '0.1'

def rchmod(path, permissions):
    '''Recursively sets permissions on a file path. Similar to chmod -R in bash.'''
    for dirpath, dirnames, filenames in os.walk(path):
        for filename in filenames:
            thepath = os.path.join(dirpath, filename)
            os.chmod(thepath, permissions)

def rchown(path, uid, gid):
    '''Recursively sets ownership on a file path. Similar to chown -R in bash.'''
    for root, dirs, files in os.walk(path):  
      for thedir in dirs:  
        os.chown(os.path.join(root, thedir), uid, gid)
      for thefile in files:
        os.chown(os.path.join(root, thefile), uid, gid)

def buildPkg(tempFolder, version, identifier):
    pkgbuild = '/usr/bin/pkgbuild'
    save_path = os.path.join(os.path.dirname(__file__),'CrankD.pkg')
    command = [pkgbuild, '--install-location', '/', '--root', tempFolder, '--identifier', identifier, '--version', version, save_path]
    task = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    task.communicate()
    
def copyFiles(repo):
    tempdir = '/tmp/CrankPkg'
    # remove the folder if it exists
    if os.path.exists(tempdir):
        shutil.rmtree(tempdir)

    #create temp folder
    os.makedirs(tempdir)
    # make the folders we're copying into
    os.makedirs(os.path.join(tempdir,'usr/local/sbin'), 0755)

    #copy files from Preferences to tmpdir/Library/Preferences
    sourcefile = 'Preferences/'
    dest = os.path.join(tempdir,'Library/Preferences/')
    shutil.copytree(sourcefile, dest)
    # set the permissions to 644
    rchmod(dest, 0644)
    # chown to root:wheel
    os.chown(dest, 0, 0)
    
    #copy files from LaunchDaemons to tmpdir/Library/LaunchDaemons
    sourcefile = 'LaunchDaemons/'
    dest = os.path.join(tempdir,'Library/LaunchDaemons/')
    shutil.copytree(sourcefile, dest)
    
    #copy files from crankd to tmpdir/Library/Application Support/crankd
    sourcefile = 'crankd/'
    dest = os.path.join(tempdir,'Library/Application Support/crankd')
    shutil.copytree(sourcefile, dest)
    
    # copy files from the repo to mpdir/Library/Application Support/crankd/PyMacAdmin
    sourcefile = os.path.join(repo,'lib/PyMacAdmin')
    dest = os.path.join(tempdir,'Library/Application Support/crankd/PyMacAdmin')
    shutil.copytree(sourcefile, dest)
    
    #copy files from the repo into the temp folder
    sourcefile = os.path.join(repo,'bin/crankd.py')
    dest = os.path.join(tempdir,'usr/local/sbin/crankd.py')
    shutil.copy(sourcefile, dest)
    
    return tempdir
    
    
def main():
    '''Creates a pkg to deploy CrankD from a fresh git clone.'''
    parser = argparse.ArgumentParser(description='Builds a CrankD package for deployent on OS X')
    parser.add_argument('--repo', help='The path to the clone pymacadmin git repository')
    parser.add_argument('--version', help='The version number of the package you\'re building Defaults to 1.0')
    parser.add_argument('--identifier', help='The identifier of the package. Defaults to com.grahamgilbert.crankd')
    args = vars(parser.parse_args())

    if os.geteuid() != 0:
        print >> sys.stderr, 'You must run this as root, or via sudo!'
        exit(-1)
        
    # crap out of any of the needed arguments havent been passed
    if not args['repo']:
        print 'No repository specified, exiting.'
        sys.exit(1)
        
    # make sure the repo path exists
    if not os.path.isdir(args['repo']):
        print args['repo']+ ' does not exist. Please specify a valid path.'
        sys.exit(1)
    
    if args['version']:
        version = args['version']
    else:
        version = '1.0'
        
    if args['identifier']:
        identifier = args['identifier']
    else:
        identifier = 'com.grahamgilbert.crankd'
        

    tempFolder = copyFiles(args['repo'])
    
    buildPkg(tempFolder, version, identifier)

if __name__ == '__main__':  
    main() 
