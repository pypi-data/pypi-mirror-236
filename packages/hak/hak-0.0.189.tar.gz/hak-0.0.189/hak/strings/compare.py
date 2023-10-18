from hak.puvyz import f as puvyz
from hak.pf import f as pf

def _calc_reason(u, v):
  first_difference =  _get_first_difference(u, v)
  return 'u == v' if u == v else (
    f'len(u): {len(u)} < len(v): {len(v)}'
    if len(u) < len(v) else
    (
      f'len(u): {len(u)} > len(v): {len(v)}'
      if len(u) > len(v) else
      ' != '.join([
        f"x[{first_difference}]: '{u[first_difference]}'",
        f"y[{first_difference}]: '{v[first_difference]}'"
      ])
    )
  )

def _get_first_difference(u, v):
  _first_difference = min([len(u), len(v)])
  for i in range(min([len(u), len(v)])):
    if u[i] != v[i]:
      return i
  return _first_difference

f = lambda u, v: {
  'match': u == v,
  'reason': _calc_reason(u, v),
  'first_difference': _get_first_difference(u, v)
}
  
def t_match():
  u = 'abc'
  v = 'abc'
  y = {'match': True, 'reason': 'u == v', 'first_difference': 3}
  z = f(u, v)
  return puvyz(u, v, y, z)

def t_less():
  u = 'abc'
  v = 'abcd'
  y = {
    'match': False,
    'reason': 'len(u): 3 < len(v): 4',
    'first_difference': 3
  }
  return puvyz(u, v, y, f(u, v))

def t_greater():
  u = 'abcd'
  v = 'abc'
  y = {
    'match': False,
    'reason': 'len(u): 4 > len(v): 3',
    'first_difference': 3
  }
  return puvyz(u, v, y, f(u, v))

def t_not_equal():
  u = 'axc'
  v = 'ayc'
  y = {
    'match': False,
    'reason': "x[1]: 'x' != y[1]: 'y'",
    'first_difference': 1
  }
  return puvyz(u, v, y, f(u, v))

def t():
  if not t_match(): return pf('!t_match')
  if not t_less(): return pf('!t_less')
  if not t_greater(): return pf('!t_greater')
  if not t_not_equal(): return pf('!t_not_equal')
  return 1
