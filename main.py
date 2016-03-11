import numpy as np
import policy
import minimaxPolicy
import mctsPolicy
import deepqPolicy
import board

WIDTH = 7
HEIGHT = 6
CONNECT = 4

BOARD = np.zeros((WIDTH, HEIGHT))

# PLAYER = {
#    1:{"symbol":"x", "policy":policy.InputPolicy(1, BOARD, check_put, check_win)},
#    #-1:{"symbol":"o", "policy":policy.RandomPolicy(-1, BOARD, check_put, check_win)},
#    -1:{"symbol":"o", "policy":deepqPolicy.DeepQPolicy(-1, BOARD, check_put, check_win, "model.json")},
#    }


PLAYER = {
    1: {"symbol": "x"},
    # -1:{"symbol":"o", "policy":policy.RandomPolicy(-1, BOARD, check_put, check_win)},
    -1: {"symbol": "o"},
}

BOARD = board.Board(PLAYER)
PLAYER[1]["policy"] = policy.InputPolicy(1, BOARD)
# PLAYER[-1]["policy"] = policy.RandomPolicy(-1,BOARD)
#PLAYER[-1]["policy"] = minimaxPolicy.MinimaxPolicy(-1, BOARD)
PLAYER[-1]["policy"] = mctsPolicy.MctsPolicy(-1, BOARD)



def train():
    PLAYER[-1]["policy"].train("model2.json")


def play():
    BOARD.print_board()
    while True:
        win_result = "NONE"
        for idx in PLAYER.keys():
            print "player :%s" % (PLAYER[idx]["symbol"])
            posx = PLAYER[idx]["policy"].put()
            posy = BOARD.put(idx, posx)
            BOARD.print_board()
            win_result = BOARD.check_win(idx, posx, posy)
            if win_result == "WIN":
                print "winner is :%s" % (PLAYER[idx]["symbol"])
                break
            elif win_result == "EVEN":
                print "even"
                break
        if win_result != "NONE":
            break


if __name__ == "__main__":
    play()
