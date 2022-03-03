from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.http import *
from .models import Match, Test_Ville, Team, B_Player, Score_NBL, Bet
from django.template import loader
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User


def index(request):
    if not request.user.is_authenticated:
        response = redirect('/store/login')
        return response

    seven_date = []
    for d in Match.objects.raw("SELECT * FROM store_match ORDER BY date DESC"):
        if(d.date not in seven_date and len(seven_date) < 7):
            seven_date = seven_date + [d.date]
    
    selected_date = seven_date[1]
    
    if request.method == "POST":
        if 'day' in request.POST:
            selected_date = request.POST.get("day")  
        if 'player_v' in request.POST:           
            selected_date = request.POST.get("player_v").split("_")[0]
    match = Match.objects.filter(date = selected_date)

    all_match = []
    
    for ma in match : 
        all_match = all_match + [Team.objects.filter(id = ma.home)[:1].get().surname]
        all_match = all_match + [Team.objects.filter(id = ma.visitor)[:1].get().surname]
    
    all_player = {}
    for ma in all_match: 
        player = [] 
        for play in B_Player.objects.filter(id_team = Team.objects.filter(surname = ma)[:1].get().id):
            player = player + [play.name]
        all_player[ma] = player

    
    if request.method == "POST" and 'player_v' in request.POST:
        if request.user.is_authenticated:
            print("You bet " + request.POST.get("player_v").split("_")[1])
            for p in B_Player.objects.filter(name = request.POST.get("player_v").split("_")[1]):
                p_id = p
            m_id = Match.objects.all()[:1].get()
            if(Match.objects.filter(date = request.POST.get("player_v").split("_")[0], home = p_id.id_team).count() == 1):
                for m in Match.objects.filter(date = request.POST.get("player_v").split("_")[0], home = p_id.id_team):
                    m_id = m
            if(Match.objects.filter(date = request.POST.get("player_v").split("_")[0], visitor = p_id.id_team).count() == 1):
                for m in Match.objects.filter(date = request.POST.get("player_v").split("_")[0],visitor = p_id.id_team):
                    m_id = m
            
            #Je regarde si il y a deja un bet ce jour la
            if(Bet.objects.filter(user_id = request.user.id, date = request.POST.get("player_v").split("_")[0]).count() == 1):
                bet = Bet.objects.filter(user_id = request.user.id, date = request.POST.get("player_v").split("_")[0])
                for b in bet:
                    new_bet = Bet.objects.get(id=int(b.id))
                    new_bet.player_id = int(p_id.id)
                    new_bet.match_id = m_id.id_match
                    new_bet.save()
            else:
                Bet.objects.create(user_id=int(request.user.id), player_id=int(p_id.id), date=request.POST.get("player_v").split("_")[0], match_id = m.id_match)


        else:
            print('You have to be log')

    if request.method == "POST" and 'logout' in request.POST:
        logout(request)

    # Display bet you have already done 
    all_bet = []
    for day in seven_date:
        if(Bet.objects.filter(date = day, user_id = request.user.id).count() == 1):
            bet = Bet.objects.filter(user_id = request.user.id, date = day)               
            for b in bet:
                p = B_Player.objects.get(id = b.player_id)
                all_bet = all_bet + [p.name]
        else:
            all_bet = all_bet + ["None"]

    date_format = []
    for a in seven_date:
        date_format += [a[-4:-2] + "/" + a[-2:]]
    all_bets = zip(date_format, all_bet)

    context = {'match' : all_match,
               'all_date' : seven_date,
               'all_player' : all_player,
               'date' : selected_date,
               'all_bet' : all_bets}
    return render(request, "index.html", context)

def log_in(request):
    if request.method == "POST":
        for a in request.POST:
            print(a)
        if 'btn_log' in request.POST:
            username = request.POST.get('username', False)
            password = request.POST.get('password', False)
            user = authenticate(username=username, password=password)
            if user is not None and user.is_active:
                login(request, user)
                print("You Log")
                response = redirect('/')
                return response
            else:
                print("Wrong log")
        if 'btn_sign' in request.POST:
            response = redirect('/store/createlog')
            return response
    return render(request, "login.html")

def create_log(request):
    if request.user.is_authenticated:
        response = redirect('/')
        return response
    if request.method == "POST":
        username = request.POST.get('username', False)
        password = request.POST.get('password', False)
        mail = request.POST.get('email', False)
        user = authenticate(username=username, password=password)
        if user is not None and user.is_active:
            print("You already have a log")
        else:
            user = User.objects.create_user(username, mail, password)
            user.save()
            response = redirect('/')
            print('Congrats you created your log')
            return response
    return render(request, "create_log.html")

def myScore(request):
    if not request.user.is_authenticated:
        response = redirect('/store/login')
        return response

    else:
        all_bet = Bet.objects.filter(user_id = request.user.id).order_by('date')
        date = []
        name_player = []
        score = []
        for bet in all_bet:
            date = date + [bet.date]
            players = B_Player.objects.filter(id = bet.player_id)
            for play in players:
                name_player = name_player + [play.name]
                print(play.name)
            if(Score_NBL.objects.filter(id_bplayer = bet.player_id, id_match = bet.match_id).count() == 1):
                all_score = Score_NBL.objects.filter(id_bplayer = bet.player_id, id_match = bet.match_id)
                for scores in all_score:
                    score = score + [scores.score]
                    print(str(scores.score))
            else :
                score = score + ["0"]
        bets = zip(date, name_player, score)
        context = {
            "bets" : bets
        }
        return render(request, "my_score.html", context)