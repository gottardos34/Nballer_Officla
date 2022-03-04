from django.db import models

class User_score(models.Model):
    last_update = models.CharField(max_length=20)
    score_tot = models.IntegerField()
    id_user = models.IntegerField()

class Match(models.Model):
	id_match = models.CharField(max_length=20)
	date = models.CharField(max_length=20)
	home = models.CharField(max_length=30)
	visitor = models.CharField(max_length=30)
	can_bet = models.BooleanField()

class Team(models.Model):
	name = models.CharField(max_length=20)
	surname = models.CharField(max_length=20)
	code = models.CharField(max_length=5)

class B_Player(models.Model):
	name = models.CharField(max_length=30)
	poste = models.CharField(max_length=5)
	id_team = models.IntegerField()

class Test_Ville(models.Model):
	date = models.CharField(max_length=20)
	city = models.CharField(max_length=30)

class Score_NBL(models.Model):
	id_bplayer = models.IntegerField()
	id_match = models.IntegerField()
	score = models.IntegerField()
	time_play = models.CharField(max_length=20)

class Bet(models.Model):
	user_id = models.IntegerField()
	match_id = models.IntegerField()
	player_id = models.IntegerField()
	date = models.CharField(max_length=20)
