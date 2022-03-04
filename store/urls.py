from django.urls import include, re_path
from . import views

urlpatterns = [
	re_path(r'^login$', views.log_in),
	re_path(r'^createlog$', views.create_log),
	re_path(r'^my_score$', views.myScore),
	re_path(r'^rank$', views.rank_all),
]