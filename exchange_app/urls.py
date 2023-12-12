from django.urls import path
from exchange_app import views

# FOR TEMPLATE TAGGING
app_name = "exchange_app"

urlpatterns = [
    path("games/", views.GamesListView.as_view(), name="game_list"),
    path("tickers/", views.TickerListView.as_view(), name="ticker_list"),
    path("games/<int:pk>/", views.GameDetailView.as_view(), name="game_detail"),
    path("tickers/<int:pk>/", views.TickerDetailView.as_view(), name="ticker_detail"),
    path("leagues/<int:pk>/", views.LeagueDetailView.as_view(), name="league_detail"),
    path("teams/<int:pk>/", views.TeamDetailView.as_view(), name="team_detail"),
]

