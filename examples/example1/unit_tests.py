from unit_test_advanced.UnitTest import UnitTest
import os, sys
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

sys.path.append(BASE_DIR)

# from scenarios import SCENARIO_1, SCENARIO_2
# from scenarios import resetWorkspace, step1_checkFileExist_success, step2_WithInjectedSimpleValue
from scenarios import relationExample_lvl3_1
def run():
	UT = UnitTest(
		is_enabled              = True,  # Default is False. MUST be set to true here when we run the unit tests
		parent_execution_plan   = 'random', # Default is 'all', other accepted values are 'all', 'main', or 'random'
		children_execution_plan = 'all', # Default is 'all', other accepted values are 'all', 'main', or 'random'
		count_limit_identify_infinite_loop = 2, # Default is 2
		verbose                 = True, # Default is False
	)
	
	
	UT.preparePlans([
		relationExample_lvl3_1
	])
	for plan in UT.getExecutionPlans():
		print(plan)
	
	# UT.execute([
	# 	resetWorkspace,
	# 	[
	# 		resetWorkspace,
	# 		step1_checkFileExist_success,
	# 		step2_WithInjectedSimpleValue
	# 	],
	# 	SCENARIO_1, # Unit test passed
	# 	SCENARIO_2, # Unit test failed on step 3
	# ])
	#
	# # ------------------------------------
	# # Create plan for all scenarios possible
	#
	# UT.resetExecutionPlans()
	# UT.preparePlans()
	# print(UT.getExecutionPlans())
	#
	#
	# # ------------------------------------
	# # Create plan for all scenarios possible for the parents and only the first scenario for the children
	#
	# UT.resetExecutionPlans()
	# UT.updateSettings(
	# 	children_execution_plan = 'main',
	# )
	# UT.preparePlans()
	# print(UT.getExecutionPlans())
	#
	#
	# # ------------------------------------
	# # Create plan for a random scenario for the parents and only the first scenario for the children
	#
	# UT.resetExecutionPlans()
	# UT.updateSettings(
	# 	parent_execution_plan   = 'random',
	# )
	# UT.preparePlans()
	# print(UT.getExecutionPlans())
	
	
run()