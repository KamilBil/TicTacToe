import numpy as np
from sklearn.tree import DecisionTreeClassifier
from sklearn.tree import export_graphviz #ewentualne wygenerowanie podglądu
import pickle
from sklearn.model_selection import train_test_split
from sklearn.model_selection import cross_val_score


board=[0,0,0, 0,0,0, 0,0,0]
#Konwencja zawartości listy
#0-puste pole
#1-komputer
#-1-gracz

def win_check(board):
  """Zwraca 1 gdy wygrała SI, -1 gdy gracz, 0 gdy nikt"""
  if sum(board[0:3])==3 or sum(board[3:6])==3 or sum(board[6:9])==3 or sum(board[0::3])==3 or sum(board[1::3])==3 or sum(board[2::3])==3 or sum(board[0::4])==3 or sum(board[2:8:2])==3:
    return 1
  elif sum(board[0:3])==-3 or sum(board[3:6])==-3 or sum(board[6:9])==-3 or sum(board[0::3])==-3 or sum(board[1::3])==-3 or sum(board[2::3])==-3 or sum(board[0::4])==-3 or sum(board[2:8:2])==-3:
    return -1
  return 0


def probability2(board):
  """Obliczenie wielkości prawdopodobieństwa wygranej/przegranej po danym ruchu dla SI"""
  rate = 0
  for i in range(0,9):
    board_copy = board.copy()
    if board_copy[i]==0:
      board_copy[i]=1
      rate+=win_check(board_copy)
      if board_copy.count(0)>0:
        rate+=probability(board_copy)/10
  return rate



def probability(board):
  """Obliczenie wielkości prawdopodobieństwa wygranej/przegranej po danym ruchu dla gracza"""
  rate = 0
  for i in range(0,9):
    board_copy = board.copy()
    if board_copy[i]==0:
      board_copy[i]=-1
      rate+=win_check(board_copy)
      if board_copy.count(0)>0:
        rate+=probability2(board_copy)/10
  return rate


def best_move(board):
  """Wyznaczenie ruchu dającego największą szansę na szybkie zwycięstwo"""
  board_rate = [0,0,0, 0,0,0, 0,0,0]
  for i in range(0,9):
    board_copy = board.copy()
    if board_copy[i]==0:
      board_copy[i]=1
      board_rate[i]=probability(board_copy)
    else: board_rate[i] = -9999
  return board_rate.index(max(board_rate)) #zwraca pozycję na jakiej znajduje najkorzystniejsza opcja


def make_examples():
  """generowanie zbioru uczącego"""
  X_list=[]
  y_list=[]
  for a in range(0,9):
    for b in range(0,9):
      for c in range(0,9):
        for d in range(0,9):
          for e in range(0,9):
            board=[0,0,0, 0,0,0, 0,0,0]
            if a==b or b==c or a==c:
              pass
            else:
              board[a]=1
              board[b]=-1
              board[c]=1
              board[d]=-1
              board[e]=1
              X_list.append(board)
              y_list.append(best_move(board))


  X=np.array(X_list)
  y=np.array(y_list)

  # podział na zbiór uczący i testowy
  X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.2, random_state = 0)

  # Uczenie drzewa decyzyjnego
  clf = DecisionTreeClassifier(random_state=0)
  clf.fit(X_train, y_train)

  # Ewentualne pokazanie drzewa
  #export_graphviz(clf,out_file="tictactoe_drzewo.dot",rounded=True,filled=True)

  # Zapis gotowego modelu do pliku
  filename = 'ml_model/tictactoe_model.pkl'
  pickle.dump(clf, open(filename, 'wb'))
  print("Wyniki dla kroswalidacji: ",cross_val_score(clf, X_test, y_test, cv=5))
  print("Skuteczność dla całości: ", clf.score(X_test, y_test))

make_examples()