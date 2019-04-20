import pytest
from findi import findi_scan

def test_blank_ip_scan():
	ip_address_str = '192.252.144.8'
	x=5
	y=6
	
	assert x+1 == y,"test failed"
	findi_scan.test_main(ip_address_str)
	assert x == y,"test failed"
