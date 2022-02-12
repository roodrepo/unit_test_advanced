import os
from unit_test_advanced.UnitTest import UnitTest

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

'''
	Writing some content in the file created from step1
'''

# For each entry point, the function must accept the UT parameter and initialize it when Null
def run(UT = None):
	UT = UT if UT != None else UnitTest()
	
	f = open(f'{BASE_DIR}/myfile.txt', 'w+')
	f.write('This package sucks')
	f.close()
	
	f = open(f'{BASE_DIR}/myfile.txt', 'r')
	print(f'File content after executing {os.path.basename(__file__)}: "{f.read()}"')
	f.close()

if __name__ == '__main__':
	run()