from unit_test_advanced.UnitTest import UnitTest

def initUT(func):
	def wrapper(*args, **kwargs):
		if 'UT' in kwargs and kwargs['UT'] != None:
			UT = kwargs['UT']
		else:
			UT = UnitTest()
		return func(UT, *args, **kwargs)
	return wrapper