#!./venv/bin/python

# -*- coding: utf-8 -*-

import os
import sys
import argparse

possible_topdir = os.path.normpath(os.path.join(os.path.abspath(sys.argv[0]),
                                                os.pardir,
                                                os.pardir))
apppath = (os.path.join(possible_topdir,
                               'tokenleaderclient',
                               'tokenleaderclient'))

sys.path.insert(0, apppath)

from tokenleaderclient.configs.config_handler import Configs
conf =Configs()

parser = argparse.ArgumentParser()
parser.add_argument('-u', '--username', 
                  action = "store", dest = "username",
                  required = True,
                  help = "tokenleader user accoount",
                  default = "")
parser.add_argument('-p', '--password', 
                  action = "store", dest = "password",
                  required = True,
                  help = "tokenleader user password, note down this password , this will be stored as encrypted",
                  default = "")
parser.add_argument( '--url', 
                  action = "store", dest = "url",
                  required = True,
                  help = "url for the tokenleader service including port , client will try to connect here",
                  default = "")

try:                  
    options = parser.parse_args()    
except:
    #print usage help when no argument is provided
    parser.print_help(sys.stderr)
    sys.exit(1)


def main():
    conf.generate_user_auth_file(options.username, options.password, options.url )
