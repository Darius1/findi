from findi_scan import gui_scan as scan
import sys
'''
    This script serves as a wrapper for the findi_scan script so that the output can be displayed on the electron front end using python-shell
'''

address = sys.argv[1]
scan(address)
print(address)

sys.stdout.flush()
