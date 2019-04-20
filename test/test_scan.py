import pytest
from findi import findi_scan

@pytest.mark.openEmpty
def test_open_ip_scan_empty():
	'''
		Tests finding an open IP address and ensuring that the webpage we found is empty
	'''
	
	ip_address_str = '192.252.144.8'
	
	
	findi_scan.test_main(ip_address_str)

	# Ensure the the webpage is empty
	assert findi_scan.get_page_size(ip_address_str + '.80') < 1,"test failed, non-empty page found"

@pytest.mark.openNotEmpty
def test_open_ip_scan_has_data():
	'''
		Tests finding an open IP address and ensuring that the webpage we found is has data on the webpage
	'''
	
	ip_address_str = '24.13.60.62'
	
	
	findi_scan.test_main(ip_address_str)

	# Ensure the the webpage is empty
	assert findi_scan.get_page_size(ip_address_str+ '.80') > 0,"test failed, empty page found"
