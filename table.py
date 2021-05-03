"""Module to help output and print tables."""

from tabulate import tabulate

class Table():
  def __init__(self, numcols, headers=(), coltypes=None):
    assert numcols >= 0
    self._numcols = numcols

    if headers:
      assert len(headers) == numcols
    self._headers = headers

    if coltypes:
      assert len(coltypes) == numcols
      self._coltypes = coltypes
    else:
      self._coltypes = [None] * self._numcols

    self._rows = []

  def AddRow(self, row):
    assert len(row) <= self._numcols
    self._rows.append(row)
    return self

  def SetRows(self, rows):
    assert max(map(len, rows)) <= self._numcols
    self._rows = rows

  def Headers(self):
    return self._headers

  def ColAlign(self):
    return list(map(
      lambda x: 'right' if x == 'dollars' or x == 'delta_dollars' else 'left',
      self._coltypes))

  def List(self):
    return self._rows

  def StrList(self):
    coltype2func = {
      None: lambda x: x,
      'dollars': lambda x: '${:,.2f}'.format(x) if x != '' else '',
      'delta_dollars': lambda x: '{}${:,.2f}'.format(
        '-' if x < 0 else '+', abs(x)) if x != '' else '',
      'percentage': lambda x: '{}%'.format(round(100*x)) if x != '' else x,
    }

    ret_list = []
    for row in self.List():
      ret_row = []
      for col_num in range(len(row)):
        ret_row.append(coltype2func[self._coltypes[col_num]](row[col_num]))
      ret_list.append(ret_row)
    return ret_list

  def String(self, tablefmt='simple'):
    str_list = self.StrList()
    if not str_list:
      return ''

    return tabulate(str_list,
                    headers = self.Headers(),
                    tablefmt = tablefmt,
                    colalign = self.ColAlign())
