# LGO solver support

import util

# Possible values for the LGO opmode option.
LOCAL_SEARCH_MODE = 0
MULTISTART_MODE   = 3

def make_maxfct_setter(k):
  """
  Return a function that sets g_maxfct, l_maxfct and maxnosuc LGO solver options
  to k * 50 * (num_vars + num_cons + 2)**2.
  """
  def set(nl_file, args):
    header = util.read_nl_header(nl_file.name)
    maxfct = k * 50 * (header.num_vars + header.num_cons + 2)**2
    solver_options = args['solver_options']
    solver_options['g_maxfct'] = maxfct
    solver_options['l_maxfct'] = maxfct
    solver_options['maxnosuc'] = maxfct
  return set
