import cProfile
from path import path_get





class myDict(dict):
  pass

d_root = {'a':1}
d_inherited = myDict({'a':1})

base_struct = {"level1": 1,
              "level2": {"level2-1": "level2-1-1", "level2-2": "level2-2-1"},
              "level3":{
                "level3-4": "level3-4-1 unordered",
                "level3-1": {'level3-1-1': 'level3-1-1-1'}, 
                "level3-2": 'level3-2-1', 
                "level3-3": ['level3-3-1', 'level3-3-2', 'level3-3-3',], 
              }, 
              "2015": [{'monday':'first monday'},{'monday':'second monday'}, {'tuesday': 'first tuesday'}, {'monday': ['third monday', 'paired'], 'tuesday': ['second tuesday', 'paired']},],
              '3x3 matrix': [[1,0,0],[0,1,0],[0,0,1]],
              'object-dict-root': d_root,
              'object-dict-inherited': d_inherited,
              }



tests_and_results = {
  'root_notfound': [],
  '/root_notfound': [],
  'level1': 1,
  '/level1': 1,
  './level1': 1,
  'level2/level2-1/':'level2-1-1',
  'level2/level2-2/':'level2-2-1',
  'level3[1]': [], #Dictionaries are not ordered, cannot return first element?
  'level3/level3-3[2]': 'level3-3-2',
  'level1/../level2/level2-1':'level2-1-1',
  #type 'object-dict-inherited': 'myDict',

}

import pprint
#pp = pprint.PrettyPrinter(indent=2)
#pp.pprint(base_struct)
pprint.pprint(base_struct)
print ''

passed = {}
failed = {}

def runAllTests():
  for test_path, exp_result in tests_and_results.items():
    try:
      returned_result = path_get(base_struct, test_path)
    except:
      returned_result = 'ERROR'

    print "test: %s, exp result: %s, returned: %s" % (test_path, exp_result, returned_result)
    if exp_result == returned_result:
      print "PASS"
      passed[test_path] = {'expected': exp_result, 'returned': returned_result}
    else:
      print "FAILED"
      failed[test_path] = {'expected': exp_result, 'returned': returned_result}

    print ""

cProfile.run('runAllTests()')

print "Passed: "
pprint.pprint(passed)

print "\nFailed: " 
pprint.pprint(failed)


