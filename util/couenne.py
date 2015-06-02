# Couenne solver support

def options():
  "Return solver options that reduce output verbosity to manageable level."
  return {'print_level': 0, 'bonmin.bb_log_level': 0,
          'bonmin.lp_log_level': 0, 'bonmin.nlp_log_level': 0}.copy()
