def subscriberList(filterInclude=None):
  if filterInclude is None:
    return 'show subscriber session'
  return 'show subscriber session | include {0}'.format(filterInclude)

def subscriberDetail(uid=None):
  if uid is not None:
    return 'show subscriber session uid {0}'.format(uid)
  print('ERROR: require uid to query subscriber session detail')
  return None

def subscriberClear(uid=None):
  if uid is not None:
    return 'clear subscriber session uid {0}'.format(uid)
  print('require uid to clear subscriber session')
  return None

# def networkPing(host=None):
#   if host is not None:
#     return 'ping {0}'.format(host)
#   print('require uid to clear subscriber session')
#   return None