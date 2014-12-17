

from abc import ABCMeta, abstractmethod


LEVEL_SEPARATOR = '/'
DEEP_SEARCH = '//'
SELF_REF = '.'
BACK_REF = '..'
PREDICATE_OPEN, PREDICATE_CLOSE = '[', ']'



#add **kw?
def get_handler(data, current_level):
  """ Handler for any object that responds to ``.get``
  """
  return data.get(current_level, [])

def iteritems_handler(data, current_level):
  """ Handler for any object that implements to ``__iteritems__``
  """
  #raise NotImplementedError
  return data.get(current_level, [])

def iter_handler(data, current_level):  
  for entry in data:
    raise NotImplementedError

def typeFindAndProc(data, current_level):
  """ Find appropriate handler for unknown type, add to type_cache, and process.
  """
  #Cannot loop over set(type_cache.values) because get_handler takes precendence over iteritems

  #First try .get, highest precedence
  try:
    matched = get_handler(data, current_level)
    #If this was successful, store handler into type_cache
    type_cache[type(data)] = get_handler
    return matched
  except:
    print "Debug: get_handler failed on data type %s. Moving on to next test" % type(data)



  raise NotImplementedError

type_cache = { 
  dict : get_handler,
  list : iter_handler,
  tuple : iter_handler,
  set : iter_handler,
}



class NonStringIterable:
    __metaclass__ = ABCMeta

    @classmethod
    def __subclasshook__(cls, C):
        if cls is NonStringIterable:
            if any("__iter__" in B.__dict__ for B in C.__mro__):
                return True
        return NotImplemented



class IterItems:
  __metaclass__ = ABCMeta

  @abstractmethod
  def __iter__(self):
    pass

  @classmethod
  def __subclasshook__(cls, C):
    if any("iteritems" in B.__dict__ for B in C.__mro__):
      return True
    return False

#Warning, we do not want to iterate on dictionaries nor strings
ITERABLE_NODE_TYPES = {list, tuple, set}
def should_iterate(obj):
  """
  Consider implementing as GroupIterable 
  """
  if type(obj) in ITERABLE_NODE_TYPES:
    return True
  else: 
    return False



assert not isinstance("mystring", NonStringIterable)
assert not isinstance(1, NonStringIterable)
assert isinstance(["mystring",], NonStringIterable)
assert  isinstance({"mystring":"has a dict"}, NonStringIterable)



assert not isinstance("mystring", IterItems)
assert not isinstance(1, IterItems)
assert not isinstance(["mystring",], IterItems)
assert isinstance({"mystring":"has a dict"}, IterItems)





def path_get(data, path, sub_vars=[]):
  """

  """
  
  if not data: 
    return []
  matched = []

  current_level, _, path_remainder = path.partition('LEVEL_SEPARATOR')
  current_level, _, predicate = current_level.partition('[') #Use regex instead, must come AFTER path. Currently still has ']'
  #Replace $(\w+) with vars[_1], and so on

  """
  #If .get exists, use it
  if isinstance(data, IterItems):
    matched = data.get(current_level, [])

  #If no .get but iterable, go through each entry and check if (deeper?) value == current_level
  elif isinstance(data, NonStringIterable):
    for entry in data:
      raise NotImplementedError
  """

  proc = type_cache.get(type(data), typeFindAndProc)
  matched = proc(data, current_level)

  #Filter marched data based on predicate
  if predicate:
    raise NotImplementedError


  #Recursively search path
  if path_remainder:
    return path_get(matched, path_remainder, sub_vars)
  else:
    return matched


