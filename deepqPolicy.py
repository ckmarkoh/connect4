from policy import Policy, RandomPolicy, InputPolicy
from copy import deepcopy
import tensorflow as tf
from random import random
import numpy as np
import json


def print_board(board ):
  symbol = {1:"x",-1:"o"}
  s = ""
  for i in range(board.shape[0]):
    s += "%s "%(i)
  s += '\n'
  for row in range(board.shape[1]):
    for col in range(board.shape[0]):
      s0 = "_ "
      if board[col, row] != 0:
        s0 = "%s "%( symbol[board[col, row]] )
      s += s0
    s += '\n'
  print s


class DQN(object):
  def __init__(self,params,model_file=""):
    self._sipt = params["height"]*params["width"]
    self._sl1 = params["sl1"]
    self._sl2 = params["sl2"]
    self._sopt = params["width"]
    if model_file == "":
      self._Wl1_in = tf.Variable(tf.truncated_normal([self._sipt,self._sl1], stddev=0.1/self._sipt))
      self._bl1 = tf.Variable(tf.zeros([1,self._sl1]))
      self._Wl2_l1 = tf.Variable(tf.truncated_normal([self._sl1,self._sl2], stddev=0.1/self._sl1))
      self._bl2 = tf.Variable(tf.zeros([1,self._sl2]))
      self._Wout_l2 = tf.Variable(tf.truncated_normal([self._sl2,self._sopt], stddev=0.1/self._sl2))
      self._bout = tf.Variable(tf.zeros([1,self._sopt]))
    else:
      f = open(model_file,"r")
      model_json = json.loads("".join(f.readline()))
      f.close()
      self._Wl1_in = tf.Variable(model_json["Wl1_in"])
      self._bl1 = tf.Variable(model_json["bl1"])
      self._Wl2_l1 = tf.Variable(model_json["Wl2_l1"])
      self._bl2 = tf.Variable(model_json["bl2"])
      self._Wout_l2 = tf.Variable(model_json["Wout_l2"])
      self._bout = tf.Variable(model_json["bout"])

    self._gin = tf.placeholder("float",[1,self._sipt])
    self._gl1 = tf.sigmoid(tf.matmul(self._gin,self._Wl1_in) + self._bl1 )
    self._gl2 = tf.sigmoid(tf.matmul(self._gl1,self._Wl2_l1) + self._bl2 )
    self._gQout = tf.matmul(self._gl2,self._Wout_l2) + self._bout

    self._gA = tf.placeholder("int64",[1])
    self._gQout_A = tf.nn.embedding_lookup(tf.reshape(self._gQout, [self._sopt,1]), self._gA)

    self._gQ = tf.placeholder("float",[1])
    self._cost = tf.square(self._gQ - self._gQout_A)
    self._trainer = tf.train.AdagradOptimizer(0.1).minimize(self._cost)
    self._sess = tf.Session()
    self._sess.run(tf.initialize_all_variables())

  def save_model(self,model_file):
    f = open(model_file,"w")
    f.write(json.dumps({
      "Wl1_in":self._sess.run(self._Wl1_in).tolist(),
      "bl1":self._sess.run(self._bl1).tolist(),
      "Wl2_l1":self._sess.run(self._Wl2_l1).tolist(),
      "bl2":self._sess.run(self._bl2).tolist(),
      "Wout_l2":self._sess.run(self._Wout_l2).tolist(),
      "bout":self._sess.run(self._bout).tolist(),
      }))
    f.close()
  def get_q(self,s):
    return self._sess.run(self._gQout,feed_dict = {self._gin:s})

  def get_q_a(self,s,a):
    return self.get_q(s)[0,a]

  def get_q_a_rank(self,s):
    return sorted([i for i in enumerate(self.get_q(s).tolist()[0])], 
      key=lambda x:x[1], reverse=True)

  def get_q_max_a(self,s): 
    return np.argmax(self.get_q(s),axis=1)[0]

  def get_q_max_aq(self,s): 
    q = self.get_q(s)
    ids = np.argmax(q,axis=1)[0]
    return q[0,ids]

  def run_train(self,q,s,a):
    self._sess.run(self._trainer,
      feed_dict = {
        self._gin:s,
        self._gA:[a],
        self._gQ:[q]
      })



class DeepQPolicy(Policy):
  def __init__(self, myid, board, check_put, check_win, model_file=""):
    super( DeepQPolicy, self ).__init__( myid, board, check_put, check_win )
    self._D = []
    self._N = 100 
    self._M = 5000
    self._eps = 0.1
    self._gamma = 0.9
    params = {
      "height":self._board.shape[1],
      "width":self._board.shape[0],
      "sl1":self._board.shape[1]*self._board.shape[0],
      "sl2":int(self._board.shape[1]*self._board.shape[0]/2),
    }
    self._dqn = DQN(params, model_file)
    #self.train()

  def d_append(self,item):
    if len(self._D) > self._N: 
      self._D = self._D[1:]
    self._D.append(item)


  def d_random_sample(self):
    ids = []
    while len(ids) < int((len(self._D)-1)/10) + 1:
      nid = int(random()* len(self._D))
      if nid not in ids:
        ids.append(nid)
    return [self._D[d] for d in ids]
      
      
  def get_put_rank(self, board):
    return self._dqn.get_q_a_rank(np.reshape(board,[1,board.shape[0]*board.shape[1]]))

  def get_put(self, board):
    pos = self.get_put_rank(board)
    print [i[0] for i in pos]
    for ipos in pos:
      if(self._check_put(ipos[0],board) != -1):
        return ipos[0]
    else:
      assert 0

  def put(self):
    return self.get_put(self._board)

  def train(self, model_file):
    for e in range(self._M):
      print "iteration:",e
      board_now = deepcopy(self._board)
      while True: 
        print_board(board_now)
        to_break = False
        board_next = deepcopy(board_now)
        bx = int(random() * board_next.shape[0])
        if random() > self._eps:
          bx = self.get_put(board_next)
          #bx = self._dqn.get_q_max_a(np.reshape(board_now,[1,board_now.shape[0]*board_now.shape[1]]))
        by = self._check_put(bx, board_next)
        while by == -1:
          bx = int(random() * board_next.shape[0])
          by = self._check_put(bx, board_next)
        board_next[bx, by] = self._myid
        reward = 0
        if self._check_win(self._myid, bx, by, board_next) in ["WIN","EVEN"]:
          to_break = True 
          print "PLAYER_WIN"
          reward = 1 
        else:
          oid = self.get_next_player(self._myid)
          bx2 = self.get_put(-1*board_next)
          by2 = self._check_put(bx2, board_next)
          board_next[bx2, by2] = oid 
          if self._check_win(oid, bx2, by2, board_next) in ["WIN","EVEN"]:
            print "OPPONENT_WIN"
            to_break = True 
            reward = -1 
        self.d_append([
            np.reshape(board_now,[1,board_now.shape[0]*board_now.shape[1]]),
            np.reshape(board_next,[1,board_now.shape[0]*board_now.shape[1]]),
            bx,reward])
        board_now = board_next
        for item in self.d_random_sample():
          y = item[3] 
          if not to_break:
            y += self._gamma * self._dqn.get_q_max_aq(item[1])
          self._dqn.run_train(y,item[0],item[2])
        if to_break:
          print_board(board_now)
          print "---FINISH---"
          break
    self._dqn.save_model(model_file)

        #self._board[bx,self._check_put(bx, board)] = myid
          
  
def main():
  #pass
  height = 6
  width = 7
  params = {
    "height":height,
    "width":width,
    "sl1":20,
    "sl2":15,
  }
  s = np.ones((1,height*width))
  dqn = DQN(params)
  print dqn.get_q(s)
  print dqn.get_q_a(s,1)
  print dqn.get_q_a_rank(s)
  print dqn.get_q_max_a(s)
  dqn.run_train(0.5,s,1)
  print dqn.get_q(s)
  print dqn.get_q_a(s,1)
  print dqn.get_q_max_a(s)
  print dqn.get_q_a_rank(s)
  
if __name__ == "__main__":
  main()
