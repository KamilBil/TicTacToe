from django.shortcuts import render
from .forms import ModelForm
import numpy as np
import random
import pickle


def win_check(board):
    """Zwraca 1 gdy wygrała SI, -1 gdy gracz, 0 gdy nikt, 2 gdy wszystkie pola zostały zajęte"""
    if sum(board[0:3])==3 or sum(board[3:6])==3 or sum(board[6:9])==3 or sum(board[0::3])==3 or sum(board[1::3])==3 or sum(board[2::3])==3 or sum(board[0::4])==3 or sum(board[2:8:2])==3:
        return 1
    elif sum(board[0:3])==-3 or sum(board[3:6])==-3 or sum(board[6:9])==-3 or sum(board[0::3])==-3 or sum(board[1::3])==-3 or sum(board[2::3])==-3 or sum(board[0::4])==-3 or sum(board[2:8:2])==-3:
        return -1
    elif board.count(0)==0:
        return 2
    return 0

def predict_model(request):
    """obsługa zdarzeń"""
    if request.method == 'POST':
        form = ModelForm(request.POST)

        if form.is_valid(): #sprawdzenie poprawności formsa
            print(request.POST)
            if "choice" in request.POST:
                if request.POST['choice'] == 'cross':
                    request.session['choice'] = 'x'
                    request.session['negative'] = 'o'
                elif request.POST['choice'] == 'circle':
                    request.session['choice'] = 'o'
                    request.session['negative'] = 'x'


            for i in range(0,9):
                if str(i) in request.POST:
                    buff = request.session['board']
                    buff[0][i]=-1
                    request.session['board']=buff

                    print("dodano")
            if '-1' in request.POST:
                #button reset
                request.session['board'] = [[0,0,0, 0,0,0, 0,0,0]]
                request.session['status'] = "menu"

            if '-2' in request.POST:
                #button start
                request.session['board'] = [[0, 0, 0, 0, 0, 0, 0, 0, 0]]
                request.session['status'] = "game"

            if win_check(request.session['board'][0])!=0:
                return render(request, 'home.html',
                              {'form': form, 'board': request.session['board'][0], 'status': request.session['status'],
                                'choice': request.session['choice'],
                               'negative': request.session['negative'], 'win': win_check(request.session['board'][0])})

            if "player_first" in request.POST:
                if request.POST['player_first'] == 'on':
                    pass
                return render(request, 'home.html',{'form': form, 'board': request.session['board'][0], 'status': request.session['status'], 'choice': request.session['choice'], 'negative': request.session['negative'], 'win': win_check(request.session['board'][0])})
            else:
                loaded_model = pickle.load(open("ml_model/tictactoe_model.pkl", 'rb'))
                X=np.array(request.session['board'])
                prediction = loaded_model.predict(X)[0]
                if request.session['board'][0][prediction] == 0:
                    request.session['board'][0][prediction] = 1
                else:
                    #model wybrał zajęte pole
                    prediction=random.randint(0, 8)
                    while request.session['board'][0][prediction] != 0:
                        prediction = random.randint(0, 8)
                    request.session['board'][0][prediction] = 1
                return render(request, 'home.html', {'form': form, 'board': request.session['board'][0], 'status': request.session['status'] ,'prediction': prediction, 'choice': request.session['choice'], 'negative': request.session['negative'], 'win': win_check(request.session['board'][0])})

    else:
        form = ModelForm()
        request.session['board'] = [[0, 0, 0, 0, 0, 0, 0, 0, 0]]
        numbers=[0,1,2,3,4,5,6,7,8]
        request.session['status'] = "menu"
        return render(request, 'home.html', {'form': form, 'board': request.session['board'][0], 'status': request.session['status'], 'numbers' : numbers})