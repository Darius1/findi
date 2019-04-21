from __future__ import print_function
from Findi import findi_scan as scan
import sys
import zerorpc  

class FindiAPI(object):
    def scanAddress(self, address):
        '''
            Scan the passed in IP Address to see if it's open on port 80
        '''

        try:
            scan.test_main(address)
        except Exception:
            print("An error occurred while scanning the IP address")
    
    def echo(self, text):
        '''
            echo any text
        '''
        return text

def parse_port():
    return '4242'

def main():
    server_address = 'tcp://127.0.0.1:' + parse_port()
    server = zerorpc.Server(FindiAPI())
    server.bind(server_address)

    print('Begin running on {}'.format(server_address))
    server.run()

if __name__ == '__main__':
    main()
