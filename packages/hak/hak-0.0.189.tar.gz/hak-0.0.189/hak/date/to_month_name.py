from datetime import date
from hak.pf import f as pf
from hak.pxyf import f as pxyf
from hak.data.months import months as m_names_raw

f = lambda x: m_names_raw[x.month-1]

t_jan = lambda: pxyf(date(2023,  1, 15), 'January', f)
t_dec = lambda: pxyf(date(2023, 12, 15), 'December', f)

def t():
  if not t_jan(): return pf('!t_jan')
  if not t_dec(): return pf('!t_dec')
  return 1
