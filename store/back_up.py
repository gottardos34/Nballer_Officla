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
        if 'team' in request.POST:
            selected_date = request.POST.get("team").split("_")[1]
        if 'player_v' in request.POST:
            selected_date = request.POST.get("player_v").split("_")[1]
            

    match = Match.objects.filter(date = selected_date)

    all_match = []
    for ma in match : 
        all_match = all_match + [Team.objects.filter(id = ma.home)[:1].get().surname]
        all_match = all_match + [Team.objects.filter(id = ma.visitor)[:1].get().surname]

    selected_team = all_match[1]
    if request.method == "POST":
        if 'team' in request.POST: 
            selected_team = request.POST.get("team").split("_")[0]
        if 'player' in request.POST:
            selected_team = request.POST.get("player_v").split("_")[0]
            

    
    player = []
    for play in B_Player.objects.filter(id_team = Team.objects.filter(surname = selected_team)[:1].get().id):
        player = player + [play.name]
    
    if request.method == "POST" and 'player_v' in request.POST:
        if request.user.is_authenticated:
            print("You bet " + request.POST.get("player_v").split("_")[2])
            for p in B_Player.objects.filter(name = request.POST.get("player_v").split("_")[2]):
                p_id = p

            if(Match.objects.filter(date = request.POST.get("player_v").split("_")[1], home = p_id.id_team).count() == 1):
                for m in Match.objects.filter(date = request.POST.get("player_v").split("_")[1], home = p_id.id_team):
                    m_id = m
            if(Match.objects.filter(date = request.POST.get("player_v").split("_")[1], visitor = p_id.id_team).count() == 1):
                for m in Match.objects.filter(date = request.POST.get("player_v").split("_")[1],visitor = p_id.id_team):
                    m_id = m
            
            #Je regarde si il y a deja un bet ce jour la
            if(Bet.objects.filter(user_id = request.user.id, date = request.POST.get("player_v").split("_")[1]).count() == 1):
                bet = Bet.objects.filter(user_id = request.user.id, date = request.POST.get("player_v").split("_")[1])
                for b in bet:
                    new_bet = Bet.objects.get(id=int(b.id))
                    new_bet.player_id = int(p_id.id)
                    new_bet.match_id = m.id_match
                    new_bet.save()
            else:
                Bet.objects.create(user_id=int(request.user.id), player_id=int(p_id.id), date=request.POST.get("player_v").split("_")[1], match_id = m.id_match)


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


    context = {'match' : all_match,
               'all_date' : seven_date,
               'all_player' : player,
               'date' : selected_date,
               'team_id' : selected_team,
               'all_bet' : all_bet}
    return render(request, "index.html", context)


{% extends 'base.html' %}

{% block content %}
    <div class = "left_body">
            <div class = "sheldule">
                <h2>All Day</h2>
                <ul class = "all_days">
                    {% for d in all_date %}
                        <form method="post">
                            {% csrf_token %}
                            <li class = "day"><button class = "day_b", type="submit" name = "day" value={{d}}>{{d}}</button>
                        </form>
                    {% endfor %}
                </ul>
            </div>
            <div class = "team">
                <div class = "choose_team">
                    <ul>
                        {% for ma in match %}
                            <form method="post">
                                {% csrf_token %}
                                <li class="City"><button class="City_b", type="submit", name = "team", value = {{ma}}_{{date}} , data-value = "OUI">{{ma}}</button></li>
                            </form>
                        {% endfor %}    
                    </ul>
                </div>
                <div class = "choose_player">
                    <ul>
                        {% for play in all_player %}
                            <form method="post">
                                {% csrf_token %}
                                <li class="player"><button class="player_B", type="submit", name = "player_v", value = "{{team_id}}_{{date}}_{{play}}" , data_value = "OUI" >{{play}}</button></li>
                            </form>                     
                        {% endfor %}
                    </ul>
                </div>
            </div>
        </div>
        <div class = "right_body">
            {% for bet in all_bet %}
                <p>{{bet}}</p>
            {% endfor %}
        </div>
    </div>
    
{% endblock %}