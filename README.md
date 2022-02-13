Unit Test Advanced
==========

## _The Python Unit Test Toolkit_


Unit Test Advanced is the Python testing toolkit and programmable execution plans. It makes it easy to write, test and scale complex applications and libraries.

This package gives you the flexibility to use the production code to run the tests, assert data at any time within the code, and inject custom data. Lightweight with no dependencies, you can use it on top of any other framework such as Django or Flask.


## Features

- Program multiple execution plans
- Pass values from one step to another within an execution plan
- No code duplication; use production code to run tests
- Inject custom data
- Auto-create execution plans from the relationship between all tests

## Advantages

- Highly flexible
- Lightweight and no dependency
- Open-source
- Real use cases
- Support & documentation

## Install
The easiest way to install the Unit Test Advanced library is to use a package manager:
`pip install unit-test-advanced`


## Prepare the tests

Examples can be found [here](https://github.com/roodrepo/unit_test_advanced/tree/v0.1.1/examples)

### Create a test class

```python
from unit_test_advanced.UnitTestAction import UnitTestAction
import os, sys

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

sys.path.append(BASE_DIR)
from step1 import run as step1_run
		
class step1_checkFileExist_success(UnitTestAction):
	
    # Function to execute to run the action to test. 
	trigger = step1_run # NOT step1_run()
	
	def __init__(self, **kwargs):
		super().__init__(**kwargs)
		
		self.memory = {
			'print_memory_message'  : False,
			'value_in_memory'       : '######### This value is passed along all the classes of a plan and can be modified at any time'
		}
		
	def final_check(self):
		if os.path.exists(f'{BASE_DIR}/{FILE_NAME}') == False:
			raise BaseException(f'The file {FILE_NAME} is missing')

```

###Main attributes of a test class

| Attribute  | Type | Required | Info |
|:-:|:-:|:-:|:-|
| `init_params`  | dict  | no | * Kwargs to pass to the test-class when instantiate * |
| `trigger_params`  | dict  | no | * Kwargs to pass to trigger when executed * |
| `trigger`  | function  | no | * Action to execute to run the action to test. * |
| `dependencies`  | list  | no | * Previous test-classes required to run the current test (N-1) * |
| `children`  | list  | no | * Next test-classes to run after the current test (N+1) * |
| `memory`  | dict  | no | * Passing values from one test action to the next ones within the current execution plan * |
| `finalCheck`  | method  | no | * Final method called when the action is complete * |

** Make sure not to execute function while passing it to "trigger":  **
`trigger = step1_run`
** NOT **
`trigger = step1_run(*args, **kwargs)`

#### Create relationships
```python

class relationExample_lvl1_1:
	children = ['scenarios.relationExample_lvl2_1', 'scenarios.relationExample_lvl2_2']

class relationExample_lvl1_2:
	children           = ['scenarios.relationExample_lvl1_2']
	
	


class relationExample_lvl2_1:
	dependencies  = [relationExample_lvl1_1, relationExample_lvl1_2]
	children           = ['scenarios.relationExample_lvl3_1']

class relationExample_lvl2_2:
	dependencies = [relationExample_lvl1_1]
	
	
	
	
# Extending the class "UnitTestAction" gives more features such as memory
class relationExample_lvl3_1(UnitTestAction):
	dependencies = [relationExample_lvl2_1]
	
		def __init__(self, **kwargs):
			super().__init__(**kwargs)
```

### Execute your scenarios
```python
from unit_test_advanced.UnitTest import UnitTest

UT = UnitTest(
    is_enabled              = True,  # Default is False. MUST be set to true here when we run the unit tests
    parent_execution_plan   = 'all', # Default is 'all'. Accepted values are 'all', 'main', or 'random'
    children_execution_plan = 'all', # Default is 'all'. Accepted values are 'all', 'main', or 'random'
    count_limit_identify_infinite_loop = 2, # Default is 2
    verbose                 = True, # Default is False
)

UT.execute([
    # When a single test-class is passed, the relationship tree will get build based on the settings "parent_execution_plan" and "children_execution_plan"
    relationExample_lvl1_1,
    # A list of unit test classes
    [
        relationExample_lvl1_1,
        relationExample_lvl1_2,
    ],
])
```

###UnitTest methods

| Attribute | Description |
|:-:|:-|
| `__init__`  | |
| `updateSettings`  | * Update the settings * |
| `inject`  | * Inject data in the function triggered by the test-class * |
| `returnValue`  | * Used when the value to inject is a single value * |
| `preparePlans`  | * Preparing all scenarios according to the settings and list passed * |
| `getExecutionPlans`  | * Get all the execution plans prepared * |
| `resetExecutionPlans`  | * Reset all the prepared execution plans * |
| `execute`  | * Execute all the unit-tests from the list * |

####\_\_init\_\_ and updateSettings
| Argument | Type | Default | Description |
|:-:|:-:|:-:|:-|
| `is_enabled` | bool | False | * Set to "True" ** only ** when used to run the unit-tests * |
| `parent_execution_plan` | str | all | * Algorithm to create the branches from on the dependencies side. Accepted values are "all", "main", and "random" * |
| `children_execution_plan` | str | all | * Algorithm to create the branches from on the children side. Accepted values are "all", "main", and "random" * |
| `count_limit_identify_infinite_loop` | int | 2 | * Max amount to execute a test-class within an execution plan * |
| `verbose` | bool | False | * Display information when running * |

Execution plan algorithms:
- ** all ** : All possible execution plans are prepared
- ** main ** : If multiple dependencies or children, the algorithm select the first one
- ** random ** : If multiple dependencies or children, the algorithm randomly select the path

####inject
| Argument | Type | Default | Description |
|:-:|:-:|:-:|:-|
| `id` | bool |  | * Method to execute within the test-class to override the original function * |
| `function` | str |  | * Function to execute if the override method is not found within the test-class * |
| `*args` | str |  | * Arguments to pass to the function and the override method * |
| `**kwargs` | str |  | * Arguments to pass to the function and the override method * |

####returnValue
| Argument | Type | Default | Description |
|:-:|:-:|:-:|:-|
| `value` |  |  | * Return the value passed * |

####preparePlans
| Argument | Type | Default | Description |
|:-:|:-:|:-:|:-|
| `list_unit_tests` | list | [] | * Prepare all the execution plans * |

####getExecutionPlans
Return all the execution plans ready to be executed

####resetExecutionPlans
Reset all the prepared execution plans

####execute
| Argument | Type | Default | Description |
|:-:|:-:|:-:|:-|
| `list_unit_tests` | list | None | * Execute the prepared unit tests. The method "preparePlans" is not previously required if the list of plans is passed here.  * |

## Prepare the actions
####With decorators
```python
from unit_test_advanced.functools import initUT

# For each entry point, the function must accept the parameter UT
@initUT
def run(UT):
	pass

if __name__ == '__main__':
	run()
```

####Without decorators
```python
from unit_test_advanced.UnitTest import UnitTest

# For each entry point, the function must accept the parameter UT
def run(UT = None):
	UT = UT if type(UT) == type(UnitTest) else UnitTest()

if __name__ == '__main__':
	run()
```