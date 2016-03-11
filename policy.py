import random

class Policy(object):
  def __init__(self, myid, board):
    self._board = board 
    self._myid = myid

  def get_next_player(self, cur):
    if cur == 1:
      return -1
    else:
      return 1
  #def check_put_bdata(self, pos, bdata):
  #  if pos < 0 or pos >= bdata.shape[0]:
  #    return -1
  #  if bdata[pos, 0] != 0:
  #    return -1 
  #  depth = 1
  #  while True:
  #    if depth >= bdata.shape[1]:
  #      break
  #    if bdata[pos, depth] != 0:
  #      break
  #    depth += 1
  #  return depth-1 

  #def putxy_bdata(self, idx, posx, posy, bdata):
  #  assert posx >= 0 and posx <= bdata.shape[0]
  #  assert posy >= 0 and posy <= bdata.shape[1]
  #  assert bdata[posx, posy] == 0
  #  bdata[posx, posy] = idx

  #def check_win_bdata(self, idx, posx, posy, bdata):
  #  s_function = [
  #   lambda x, y, d:(x+d, y), 
  #   lambda x, y, d:(x, y+d), 
  #   lambda x, y, d:(x+d, y+d),
  #   lambda x, y, d:(x+d, y-d), 
  #  ]
  #  def search_seq(idx, posx, posy, sdir, sfunc):
  #    posx, posy = sfunc(posx, posy, sdir)
  #    if posx < 0  or posx >= bdata.shape[0] or posy < 0 or posy >= bdata.shape[1]:
  #      return 0
  #    if bdata[posx, posy] != idx:
  #      return 0 
  #    else:
  #      count = 1
  #      count += search_seq(idx, posx, posy, sdir, sfunc)
  #      return count
  #  for s_fun in s_function:
  #    if search_seq(idx, posx, posy, -1, s_fun) + search_seq(idx, posx, posy, 1, s_fun) >= self._board._connect - 1:
  #      return "WIN" 
  #  has_zero = False 
  #  for x in range(bdata.shape[0]):
  #    for y in range(bdata.shape[1]):
  #      if bdata[x, y] == 0:
  #        has_zero = True
  #        break
  #  if has_zero == False:
  #    return "EVEN" 
  #  else:
  #    return "NONE" 

class InputPolicy(Policy):
  def __init__(self, myid, board):
    super( InputPolicy, self ).__init__( myid, board)
  def put(self):
    while True: 
      pos = input(">")
      if(self._board.check_put(pos) != -1):
        return pos
      else:
        print "invalid position"

class RandomPolicy(Policy):
  def __init__(self, myid, board):
    super( RandomPolicy, self ).__init__( myid, board)
  def put(self):
    return self._board.get_random_pos()
    #while True:
    #  pos = int(random.random()*self._board._bdata.shape[0])
    #  if(self._board.check_put(pos) != -1):
    #    return pos
        
