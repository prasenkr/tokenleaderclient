#! venv/bin/python

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

from tokenleaderclient.client.cli_parser import main

if __name__ == '__main__':
<<<<<<< HEAD
	main()
=======
	main()

	
>>>>>>> 8439fa698f293f7518abc3514db3bcaee7b9f8cd
