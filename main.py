"""This module runs the whole application"""

import os
import sys
os.chdir(os.path.dirname(os.path.abspath(sys.argv[0])))

from source.app.application import Main

def main():
    Main().run()

if __name__ == '__main__':
    main()