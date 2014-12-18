import re
import logging


LOG_FILENAME = 'epath.log'
logging.basicConfig(filename=LOG_FILENAME,
                    level=logging.INFO,
                    #level=logging.DEBUG,
                    )
logging.getLogger().addHandler(logging.StreamHandler())


LEVEL_SEPARATOR = '/'
DEEP_SEARCH = '//'
SELF_REF = '.'
BACK_REF = '..'
PREDICATE_OPEN, PREDICATE_CLOSE = '[', ']'


"""
1) Match //  -> full tree-traversal until None
2) Match /  .   []

"""


#add **kw?
def get_handler(data, current_level):
  """ Handler for any object that responds to ``.get``
  """
  return data.get(current_level, [])

#Implement only once a test is written which cannot be handled by get_handler
#def iteritems_handler(data, current_level):
#  """ Handler for any object that implements to ``__iteritems__``
#  """
#  #raise NotImplementedError
#  return data.get(current_level, [])

def iter_handler(data, current_level):  
  for entry in data:
    raise NotImplementedError

def typeFindAndProc(data, current_level):
  """ Find appropriate handler for unknown type, add to TYPE_CACHE, and process.
  """
  #Cannot loop over set(TYPE_CACHE.values) because get_handler takes precendence over iteritems

  #First try .get, highest precedence
  try:
    matched = get_handler(data, current_level)
    #If this was successful, store handler into TYPE_CACHE
    TYPE_CACHE[type(data)] = get_handler
    return matched
  except:
    logging.info("failed to match type '%s' with get_handler. \
Continue handler search for \n  data: %s\n  current_level:%s" % (type(data), data, current_level))


  logging.warning("New unhandled type found: %s" % type(data))

  raise NotImplementedError


def requiresPathHistory(path):
  """
  Implement to improve efficiency. 
  Will not keep track of full path/history if not necessary.

  For example, if '..' is found in path, 
    or '/' is found at beginning of a predicate path, 
    then full path history (every node visited by parent recursions) must be passed to subsequent recursions
  """
  #Not implemented
  return True

#This must appear after handlers are defined unless it becomes part of a class
TYPE_CACHE = { 
  dict : get_handler,
  list : iter_handler,
  tuple : iter_handler,
  set : iter_handler,
}

def matchPredicate(matched, predicate):

  #If predicate is an integer return only that element in matching if it responds to it
  if predicate.isdigit():
    predicate = int(predicate)
    #if isinstance(matched, str):
    try:
      return matched[predicate]
    except:
      logging.warning("Attempting to access item %s of non-indexed structure %s" % (predicate, matched))
      return []
      """
      if predicate == 1:
        pass #Is this right for xpath?
      else:
        matched = []
      """

  else:
    raise NotImplementedError

def pget(data, path, sub_vars=[]):
  """

  """
  
  if not data: 
    return []
  matched = []
  predicate = None
  #Get information about current state
  current_level, _, path_remainder = path.partition(LEVEL_SEPARATOR)
  if PREDICATE_OPEN in current_level:
    current_level, _, predicate = current_level.partition(PREDICATE_OPEN) #Use regex instead? Must come AFTER path. Currently still has ']'
    predicate, _, path_remainder = predicate.partition(PREDICATE_CLOSE)

  logging.debug("current_level:%s _:%s remainder:%s predicate:%s" %(current_level, _, path_remainder, predicate) )


  #Process current state

  #If '.' or nothing before '/' such as leading slash
  if current_level == SELF_REF or not current_level:
    #Move on to next part, nothing to do
    matched = data

  else:
    proc = TYPE_CACHE.get(type(data), typeFindAndProc)
    matched = proc(data, current_level)

  #Filter matched data based on predicate
  if predicate:
    matched = matchPredicate(matched, predicate)


  #Recursively search path
  if path_remainder:
    return pget(matched, path_remainder, sub_vars)
  else:
    return matched


