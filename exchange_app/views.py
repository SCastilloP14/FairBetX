
from django.shortcuts import render, redirect
from django.db.models import Sum
from django.db.models.query import QuerySet
from django.views.generic import View, TemplateView, ListView, DetailView, CreateView, UpdateView, DeleteView
from django.http import HttpResponse, HttpResponseRedirect
from exchange_app.models import *
from django.urls import reverse, reverse_lazy
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from exchange_app.forms import UserForm, UserProfileInfoForm, OrderForm, BalanceForm
import random, string
from django.http import JsonResponse
from rest_framework import viewsets
from exchange_app.serializer import TradeSerializer, CustomTradeSerializer
import json
import pandas as pd
from datetime import timedelta
from django.db.models import Min
from rest_framework.response import Response
from django.db.models import Q


# Create your views here.

# --------=======-------- INDEX/WELCOME --------------------

def index(request):
    return render(request, "exchange_app/welcome.html")

class WelcomeView(TemplateView):
    template_name = "exchange_app/welcome.html"


# ----------------- LOGIN/LOGOUT/SIGN UP -----------------

def registration(request):
    registered = False
    if request.method == "POST":
        user_form = UserForm(data=request.POST)
        profile_form = UserProfileInfoForm(data=request.POST)
        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            # This hashes de PW
            user.set_password(user.password)
            user.save()

            profile = profile_form.save(commit=False)
            profile.user = user
            profile.save()
            registered = True
        else:
            print(user_form.errors, profile_form.errors)
            print("Errors")
    else:
        user_form = UserForm()
        profile_form = UserProfileInfoForm()

    context_dict = {"user_form": user_form,
                    "profile_form": profile_form,
                    "registered": registered}
    return render(request, "exchange_app/welcome.html", context_dict)

def user_login(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(username=username, password=password)
        if user:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect(reverse("index"))
            else:
                return HttpResponse("Account not active!")
        else:
            print("Failed login")
            return HttpResponse("Invalid Login Details")
    else:
        return render(request, "exchange_app/login.html", {})


@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))



# ---------------------- USER PAGES -------------------------

class UserDetailView(DeleteView):
    context_object_name = "user_detail"
    model = User
    template_name = "exchange_app/user_detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["balance_form"] = BalanceForm()
        if self.request.user.is_authenticated:
            context["user_orders"] = Order.objects.filter(order_user=self.request.user)
            context["user_positions"] = Position.objects.filter(position_user=self.request.user)
            context["user_fills"] = Fill.objects.filter(fill_user=self.request.user)
        else:
            context["user_orders"] = Order.objects.none()
            context["user_positions"] = Position.objects.none()
            context["user_fills"] = Fill.objects.none()
        return context
    
    def post(self, request, *args, **kwargs):
        if request.method == "POST":
            form = BalanceForm(request.POST)
            if form.is_valid():
                username = request.POST.get("username")
                user = User.objects.get(username=username)
                user_info = UserProfileInfo.objects.get(user=user)
                if user_info.user_available_balance < 100:
                    transaction = Transaction(transaction_user = user,
                                            transaction_type = TransactionType.DEPOSIT.name if request.POST.get("transaction_type") == "deposit" else TransactionType.WITHDRAWAL.name,
                                            transaction_id = f"TRANSACTION-{''.join(random.choices(string.ascii_letters + string.digits, k=28))}",
                                            transaction_amount = 100 - user_info.user_available_balance
                                            )
                    user_info.user_total_balance += int(request.POST.get("new_balance"))
                    user_info.save()
                    transaction.save()
                return redirect("user_detail", pk=self.kwargs["pk"])


# -------------------- OBJECT VIEWS ------------------------

class GamesListView(ListView):
    context_object_name = "games"
    model = Game
    template_name = "exchange_app/game_list.html"

    def get_queryset(self):
        league_filter = self.request.GET.get('league')
        queryset = Game.objects.filter(
                game_league__league_neame=league_filter,
                game_status__in=[GameStatus.PLAYING.name, GameStatus.SCHEDULED.name]) if league_filter else Game.objects.filter(
                game_status__in=[GameStatus.PLAYING.name, GameStatus.SCHEDULED.name])        
        return queryset


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        games = self.get_queryset()
        # ADD TEAMS TO PASS TO HTML
        grouped_games = {}
        for game in games:
            if game.game_league.league_name not in grouped_games.keys():
                grouped_games[game.game_league.league_name] = [game]
            else:
                grouped_games[game.game_league.league_name].append(game)
        context["grouped_games"] = grouped_games
        return context


class GameDetailView(DetailView):
    # If this line does note exist default would be ticker
    context_object_name = "game_detail"
    model = Game
    template_name = 'exchange_app/game_detail.html'

    def get_absolute_url(self):
        return reverse('exchange_app:tickers')


class TickerListView(ListView):
    # If this line does note exist default would be ticker_list
    context_object_name = "tickers"
    model = Ticker
    template_name = "exchange_app/ticker_list.html"

    def get_queryset(self):
        league_filter = self.request.GET.get('league')
        ticker_queryset = Ticker.objects.filter(
            ticker_game__game_league__league_neame=league_filter,
            ticker_status__in=[TickerStatus.OPEN.name]) if league_filter else Ticker.objects.filter(
                ticker_status__in=[TickerStatus.OPEN.name])
        ticker_queryset = ticker_queryset.order_by('ticker_game__game_start_datetime')
        return ticker_queryset


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        tickers = self.get_queryset()
        grouped_tickers = {}
        for ticker in tickers:
            if ticker.ticker_game.game_league.league_name not in grouped_tickers.keys():
                grouped_tickers[ticker.ticker_game.game_league.league_name] = [ticker]
            else:
                grouped_tickers[ticker.ticker_game.game_league.league_name].append(ticker)
        context["grouped_tickers"] = grouped_tickers

        teams = Team.objects.all()
        grouped_teams = {}
        for team in teams:
            if team.team_league_1 not in grouped_teams.keys():
                grouped_teams[team.team_league_1] = [team]
            else:
                grouped_teams[team.team_league_1].append(team)
        context["grouped_teams"] = grouped_teams


        unique_dates = set()

        for league, league_tickers in grouped_tickers.items():
            for ticker in league_tickers:
                unique_dates.add(ticker.ticker_game.game_start_datetime.date())

        context['unique_dates'] = sorted(unique_dates)
        return context

class TickerDetailView(DetailView):
    # If this line does note exist default would be ticker
    context_object_name = "ticker_detail"
    model = Ticker
    template_name = "exchange_app/ticker_detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        ticker = self.get_object()
        context["buy_orders"] = Order.objects.filter(order_ticker=ticker, order_side="BUY", order_status__in=["OPEN", "PARTIAL"]).values("order_price").annotate(total_quantity=Sum("order_working_quantity")).order_by("-order_price")
        context["sell_orders"] = Order.objects.filter(order_ticker=ticker, order_side="SELL", order_status__in=["OPEN", "PARTIAL"]).values("order_price").annotate(total_quantity=Sum("order_working_quantity")).order_by("-order_price").reverse()
        context["order_form"] = OrderForm()
        context["receive_order_url"] = reverse("exchange_app:ticker_detail", kwargs={"pk": self.kwargs["pk"]})
        if self.request.user.is_authenticated:
            context["user_orders"] = Order.objects.filter(order_user=self.request.user)
            context["user_positions"] = Position.objects.filter(position_user=self.request.user)
            context["user_fills"] = Fill.objects.filter(fill_user=self.request.user)
        else:
            context["user_orders"] = Order.objects.none()
            context["user_positions"] = Position.objects.none()
            context["user_fills"] = Fill.objects.none()
        return context
        
    def post(self, request, *args, **kwargs):
        if request.method == "POST":
            action = request.POST.get("action")
            if action == "submit_order":
                form = OrderForm(request.POST)
                # if form.data['order_type'] == OrderType.MARKET.name:
                #     mutable_data = request.POST.copy()  # Create a mutable copy of the POST data
                #     mutable_data['order_price'] = None
                #     del mutable_data['order_price']
                #     form = OrderForm(data=mutable_data)
                #     print("NEW FORM DATA", form.data)
                print(form.data)
                if form.is_valid():
                    print("FORM IS VALID!!!")
                    ticker_id = request.POST.get("ticker_id")
                    ticker = Ticker.objects.get(id=ticker_id)
                    user = request.user
                    order_type = form.cleaned_data["order_type"]
                    order_side = form.cleaned_data["order_side"]
                    order_price = form.cleaned_data["order_price"] if form.cleaned_data["order_type"] =='LIMIT' else None
                    order_quantity=form.cleaned_data["order_quantity"]
                    order_working_quantity=form.cleaned_data["order_quantity"]

                    if form.cleaned_data["order_type"] == OrderType.MARKET.name:
                        enough_liquidity = ticker.check_enough_liquidity(order_side, order_quantity)
                        if not enough_liquidity:
                            print("Not enough Liq")
                            return redirect("exchange_app:ticker_detail", pk=self.kwargs["pk"])
                    enough_balance = user.userprofileinfo.check_enough_balance(order_type, order_side, order_price, order_quantity, ticker)
                    if not enough_balance:
                        print("Not enough Bal")
                        return redirect("exchange_app:ticker_detail", pk=self.kwargs["pk"])
                    
                    order = Order(order_id = f"ORD-{''.join(random.choices(string.ascii_letters + string.digits, k=30))}",
                                order_user=user,
                                order_ticker=ticker, 
                                order_type = order_type,
                                order_side = order_side,
                                order_price = order_price,
                                order_quantity = order_quantity,
                                order_working_quantity = order_working_quantity
                                )
                    order.save()
                    order.execute_order()
                    order.save()
                else:
                    print("INVALID FORM", form.errors)  # Check for any validation errors
            elif action == "cancel_order":
                order_id = request.POST.get("order_id")
                order = Order.objects.get(order_id=order_id, order_user=request.user)
                order.cancel_order()
            elif action == "close_ticker":
                ticker_id = request.POST.get("ticker_id")
                ticker = Ticker.objects.get(ticker_id=ticker_id)
                ticker.close_ticker()
                
            return redirect("exchange_app:ticker_detail", pk=self.kwargs["pk"])             

class LeagueDetailView(DetailView):
    # If this line does note exist default would be ticker
    context_object_name = "league_detail"
    model = League
    template_name = "exchange_app/league_detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        league = self.get_object()
        context["tickers"] = Ticker.objects.filter(ticker_game__game_league=league, ticker_status__in=["OPEN", "PARTIAL"]).order_by("-ticker_game__game_start_datetime").reverse()
        context["teams"] = Team.objects.filter(team_league_1=league)
        return context
    
class TeamDetailView(DetailView):
    # If this line does note exist default would be ticker
    context_object_name = "team_detail"
    model = Team
    template_name = "exchange_app/team_detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        team = self.get_object()
        context["tickers"] = Ticker.objects.filter(ticker_game__game_home_team=team, ticker_status__in=["OPEN", "PARTIAL"]).order_by("-ticker_game__game_start_datetime").reverse()
        context["players"] = Player.objects.filter(player_team=team).order_by('-player_number').reverse()
        return context

class TradeViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = TradeSerializer
    queryset = Trade.objects.all()
    basename = "trade"  # Set a suitable basename for your viewset

    def get_queryset(self):
        ticker_id_filter = self.request.query_params.get("ticker_id", None)
        if ticker_id_filter == "":
            ticker_id_filter = None
        timeframe_filter = self.request.query_params.get("timeframe", None)
        if ticker_id_filter is not None:
            selected_ticker = Ticker.objects.get(id=ticker_id_filter)
            trades = Trade.objects.filter(ticker=selected_ticker).order_by('timestamp')
            
            if timeframe_filter:
                # Your OHLC candle calculation logic here
                ohlc_candles = []  # Store OHLC candle data here

                # Your OHLC candle calculation logic goes here
                current_candle = None
                timeframe_minutes = int(timeframe_filter.split(" ")[0])
                next_candle_timestamp = None

                for trade in trades:
                    if current_candle is None:
                        current_candle = {
                            'ticker': trade.ticker,
                            'quantity': trade.quantity,
                            'price': trade.price,
                            'timestamp': trade.timestamp.replace(second=0, microsecond=0),
                            'open': trade.price,
                            'high': trade.price,
                            'low': trade.price,
                            'close': trade.price,
                        }
                        next_candle_timestamp = current_candle['timestamp'] + timedelta(minutes=timeframe_minutes)
                    elif trade.timestamp >= next_candle_timestamp:
                        # Close the current candle and append it to the list
                        ohlc_candles.append(current_candle)

                        # Calculate the next timestamp for the new candle
                        next_candle_timestamp += timedelta(minutes=timeframe_minutes)

                        # Start a new candle
                        current_candle = {
                            'ticker': trade.ticker,
                            'quantity': trade.quantity,
                            'price': trade.price,
                            'timestamp': next_candle_timestamp,
                            'open': trade.price,
                            'high': trade.price,
                            'low': trade.price,
                            'close': trade.price,
                        }
                    else:
                        # Update high and low prices within the current candle
                        current_candle['high'] = max(current_candle['high'], trade.price)
                        current_candle['low'] = min(current_candle['low'], trade.price)
                        # Update the close price with each trade
                        current_candle['close'] = trade.price

                # Append the last candle
                if current_candle is not None:
                    ohlc_candles.append(current_candle)

                return ohlc_candles  # Return the list of OHLC candle dictionaries

            else:
                # If no timeframe is provided, return all trades
                return trades

        else:
            return Trade.objects.none()

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        
        # Check if "timeframe" is in the request query params
        if "timeframe" in request.query_params:
            # Use the custom serializer for candlestick data
            serializer = CustomTradeSerializer(queryset, many=True)
        else:
            # Use the regular TradeSerializer for other cases
            serializer = self.get_serializer(queryset, many=True)
        
        return Response(serializer.data)