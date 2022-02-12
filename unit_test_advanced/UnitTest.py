'''
	Author  : RoodRepo
	Git     : https://github.com/roodrepo/unit_test_advanced
	Contact : roodrepo@gmail.com
	
	Title       : Unit Test Advanced
	Version     : 0.1.x
	Description : Execute unit tests using the production code - Program multiple scenarios and inject custom data if needed
'''

from importlib import import_module as sys_import_module
import random

class UnitTest:
	
	_memory          : dict = {}
	_execution_plans : list = []
	_loaded_plans    : list = []
	
	_verbose                 : bool
	_is_enabled              : bool
	_parent_execution_plan   : str
	_children_execution_plan : str
	_script_counter          : dict  = {}
	_pooltest                        = None
	
	_count_limit_identify_infinite_loop : int
	
	def __init__(self, is_enabled = False, parent_execution_plan = 'all', children_execution_plan = 'all', count_limit_identify_infinite_loop = 2, verbose = False):
		'''
			is_enabled: If true, UnitTesting is activated, otherwise will execute the default function in all cases
			
			parent_execution_plan / children_execution_plan
				"all"       executes all paths possible
				"random"    executes ONE random path based on all the potential possibilities
				"main"      executes the first path of all tests
			
			count_limit_identify_infinite_loop: Count to prevent looping multiple time on the same class. If set to 2, one class in an execution plan cannot be executed more than twice
			
			verbose: display progress of the execution
		'''
		
		self.updateSettings(**{
			'_verbose'                               : verbose,
			'_is_enabled'                            : is_enabled,
			'_parent_execution_plan'                 : parent_execution_plan,
			'_children_execution_plan'               : children_execution_plan,
			'_count_limit_identify_infinite_loop'    : count_limit_identify_infinite_loop,
		})
		
		
		
	
	def updateSettings(self, **kwargs):
		'''
			Securing the settings to update to a define list. Multiple settings can be updated at once
		'''
		
		updatable_settings = ['verbose', 'is_enabled', 'parent_execution_plan', 'children_execution_plan', 'count_limit_identify_infinite_loop']
		for kwarg, value in kwargs.items():
			if kwarg in updatable_settings:
				setattr(self, f'_{kwarg}', value)
	
	
	
	def print(self, *args, level = 0):
		'''
			Print out texts when verbose mode is enabled
		'''
		
		if self._verbose == True:
			args = list(args)
			
			if level == 1:
				args.insert(0, f'{"":4}')
			elif level == 2:
				args.insert(0, f'{"":8}')
			elif level == 3:
				args.insert(0, f'{"":12}')
			elif level == 4:
				args.insert(0, f'{"":16}')
				
			print(*args)
	
	
	
	def importModule(self, module):
		'''
			Dynamically import modules if a string is passed
		'''
		if isinstance(module, str):
			_tmp = module.split('.')
			module_path = '.'.join(_tmp[:-1])
			class_name  = _tmp[-1]
			
			# Importing the object dynamically
			module = sys_import_module(module_path)
			return getattr(module, class_name)
		else:
			return module
	
	
	
	def resetCounter(self):
		'''
			For each execution plan, resetting both the counter and memory
		'''
		self._script_counter = {}
		
	def resetMemory(self):
		self._memory         = {}
	
	
	
	def inject(self, id, function, *args, **kwargs):
		'''
			id: The function to execute within the class if that function exists
			function: The actual function to execute in case the function-id does not exists
			*args and **kwargs are the argument to pass to both the fake function and real function
		'''
		if self._is_enabled == True and hasattr(self._pooltest, id):
			return getattr(self._pooltest, id)(*args, **kwargs)
		else:
			return function(*args, **kwargs)
	
	
	
	def returnValue(self, value):
		'''
			Simply return the passed value. Useful when just a value needs to be faked out during unit test
		'''
		return value
	
	
	def checkInfiniteLoop(self, module_name):
		'''
			Checks how many time a class is called and raise an error when the limit "count_limit_identify_infinite_loop" is reached
		'''
		if module_name  not in self._script_counter:
			self._script_counter[module_name] = 0
			
		self._script_counter[module_name] += 1
		
		if self._script_counter[module_name] >= self._count_limit_identify_infinite_loop:
			raise Exception(f'Possible infinite loop identified on {module_name}')
	
	
	
	def run(self, module):
		'''
			Executing all the main functions of a class
			pooltest        : Storing the current class executed for the unit test. Passing memory to access previous stored data
			trigger_params  : Parameters (dict) to pass from the class to the triggered function
			trigger         : Action (function) to trigger for the unit test
			final_check     : Final check after the action is complete
		'''
		
		if self._is_enabled == True:
			module = self.importModule(module)
			
			init_params = {}
			if hasattr(self._pooltest, 'init_params'):
				init_params = module.init_params
				
			self._pooltest = module(**init_params)
			module_has_memory = False
			
			if hasattr(self._pooltest, 'setMemory'):
				self._pooltest.setMemory(memory = self._memory)
				module_has_memory = True
				
			params = {}
			if hasattr(self._pooltest, 'trigger_params'):
				params = self._pooltest.trigger_params
				
			if hasattr(module, 'trigger'):
				module.trigger(UT= self, **params)
				
			if hasattr(self._pooltest, 'final_check'):
				self._pooltest.final_check()
				
			# Updating the memory attribute
			if module_has_memory == True:
				self._memory = self._pooltest.memory
	
	
	
	def runExecutionPlan(self, execution_plan):
		'''
			Running an execution plan
		'''
		
		if self._is_enabled == True:
			self.resetMemory()
			self.print('Running execution plan: ', execution_plan)
			for module in execution_plan:
				self.run(module)
	
	
	
	
	def preparePlans(self, list_unit_tests):
		'''
			Preparing the plans according to the settings and list passed.
			This function also prepare the execution tree for parents and children possibilities
		'''
		if self._is_enabled == True:
			for unit_test in list_unit_tests:
				self.resetCounter()
				if isinstance(unit_test, list):
					self._execution_plans.append(unit_test)
				else:
					self.createExecutionPlans(unit_test)
					
			self.preventExecutionPlansDuplicates()
	
	
	
	def getExecutionPlans(self):
		'''
			Return all the current execution plans
		'''
		return self._execution_plans
	
	
	
	def resetExecutionPlans(self):
		'''
			Resetting the execution plan list
		'''
		self._execution_plans    = []
		self._loaded_plans       = []
	
	
	
	def execute(self, list_unit_tests = None):
		'''
			Entry point to start the unit tests
			Either prepare a list and execute or pass the list as argument to perform both actions at once
		'''
		if self._is_enabled == True:
			
			if list_unit_tests != None:
				self.preparePlans(list_unit_tests)
				
			for ep in self._execution_plans:
				self.runExecutionPlan(ep)
				
			self.resetExecutionPlans()
			
			
			
	def preventExecutionPlansDuplicates(self):
		'''
			Removing duplicated plans
		'''
		final_plans = []
		for plan in self._execution_plans:
			_modules_in_plan = []
			for _module in plan:
				_modules_in_plan.append(_module.__name__)
				
			if _modules_in_plan not in self._loaded_plans:
				self._loaded_plans.append(_modules_in_plan)
				final_plans.append(plan)
				
		self._execution_plans = final_plans
		
	
	def checkRelationship(self, obj, attr, check_obj):
		'''
			If verbose mode is enable, print out if the reversed relation is not found
		'''
		if self._verbose == True:
			if (hasattr(obj, attr) == False):
				self.print(f'{obj} do not have {check_obj} in {attr}', level= 1)
			else:
				_imported_modules = []
				for _module in getattr(obj, attr):
					_imported_modules.append(self.importModule(_module))
					
				if check_obj not in _imported_modules:
					self.print(f'{obj} do not have {check_obj} in {attr}', level= 1)

	def getParentPlans(self, plans):
		'''
			From a plan, create the parent tree
		'''
		new_plans = []
		dependencies_found = False
		for plan in plans:
			if hasattr(plan[0], 'dependencies'):
				dependencies_found = True
				if self._parent_execution_plan == 'all':
					for dependency in plan[0].dependencies:
						dependency = self.importModule(dependency)
						new_plans.append([dependency] + plan.copy())
						
						# Relationship verification
						self.checkRelationship(dependency, 'children', plan[-1])
						
				else:
					idx = 0
					if self._parent_execution_plan == 'random':
						idx = random.randint(0, len(plan[0].dependencies) -1)
						
					dependency = self.importModule(plan[0].dependencies[idx])
					new_plans.append([dependency] + plan.copy())
					
					# Relationship verification
					self.checkRelationship(dependency, 'children', plan[-1])
					
			else:
				new_plans.append(plan.copy())
				
		if dependencies_found == True:
			plans = self.getParentPlans(new_plans)
			
		return plans
	
	
	
	def getChildrenPlans(self, plans):
		'''
			From a plan, create the children tree
		'''
		new_plans = []
		dependencies_found = False
		# print(plans)
		for plan in plans:
			
			if hasattr(plan[-1], 'children'):
				dependencies_found = True
				if self._children_execution_plan == 'all':
					for child in plan[-1].children:
						child = self.importModule(child)
						new_plans.append(plan.copy() + [child])
						
						# Relationship verification
						self.checkRelationship(child, 'dependencies', plan[-1])
						
						
				else:
					idx = 0
					if self._children_execution_plan == 'random':
						idx = random.randint(0, len(plan[-1].children) -1)
						
					child = self.importModule(plan[-1].children[idx])
					new_plans.append(plan.copy() + [child])
					
					# Relationship verification
					self.checkRelationship(child, 'dependencies', plan[-1])
			else:
				new_plans.append(plan.copy())
				
		if dependencies_found == True:
			plans = self.getChildrenPlans(new_plans)
			
		return plans
	
	
	
	def createExecutionPlans(self, module):
		'''
			Manage and put together the parent tree and children tree
		'''
		current_plans = [[module]]
		
		self.print('Checking relationships...')
		current_plans = self.getParentPlans(current_plans)
		current_plans = self.getChildrenPlans(current_plans)
		
		self._execution_plans += current_plans
	