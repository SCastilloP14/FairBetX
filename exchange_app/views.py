
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
from exchange_app.serializer import TradeSerializer
import json
import pandas as pd


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
    else:
        user_form = UserForm()
        profile_form = UserProfileInfoForm()

    context_dict = {"user_form": user_form,
                    "profile_form": profile_form,
                    "registered": registered}
    return render(request, "exchange_app/registration.html", context_dict)

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
            context["user_orders"] = Order.objects.filter(user=self.request.user)
            context["user_positions"] = Position.objects.filter(user=self.request.user)
            context["user_fills"] = Fill.objects.filter(user=self.request.user)
        else:
            context["user_orders"] = Order.objects.none()
            context["user_positions"] = Position.objects.none()
            context["user_fills"] = Fill.objects.none()
        return context
    
    def post(self, request, *args, **kwargs):
        if request.method == "POST":
            form = BalanceForm(request.POST)
            if form.is_valid():
                print(request.POST)
                username = request.POST.get("username")
                user = User.objects.get(username=username)
                user_info = UserProfileInfo.objects.get(user=user)
                user_info.balance = request.POST.get("new_balance")
                user_info.save()
                return redirect("user_detail", pk=self.kwargs["pk"])


# -------------------- OBJECT VIEWS ------------------------

class GamesListView(ListView):
    context_object_name = "games"
    model = Game
    template_name = "exchange_app/game_list.html"

    def get_queryset(self):
        league_filter = self.request.GET.get('league')
        queryset = Game.objects.filter(league=league_filter) if league_filter else Game.objects.all()
        return queryset


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        games = self.get_queryset()
        grouped_games = {}
        print(grouped_games.keys())
        for game in games:
            if game.league not in grouped_games.keys():
                grouped_games[game.league] = [game]
            else:
                grouped_games[game.league].append(game)
        context["grouped_games"] = grouped_games
        for league, games in context["grouped_games"].items():
            for game in games:
                print(league, game, type(game))
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


class TickerDetailView(DetailView):
    # If this line does note exist default would be ticker

    context_object_name = "ticker_detail"
    model = Ticker
    template_name = "exchange_app/ticker_detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        ticker = self.get_object()
        context["buy_orders"] = Order.objects.filter(ticker=ticker, side="BUY", working_quantity__gt=0).values("price").annotate(total_quantity=Sum("working_quantity")).order_by("-price")
        context["sell_orders"] = Order.objects.filter(ticker=ticker, side="SELL", working_quantity__gt=0).values("price").annotate(total_quantity=Sum("working_quantity")).order_by("-price")
        context["order_form"] = OrderForm()
        context["receive_order_url"] = reverse("exchange_app:ticker_detail", kwargs={"pk": self.kwargs["pk"]})
        if self.request.user.is_authenticated:
            context["user_orders"] = Order.objects.filter(ticker=ticker, user=self.request.user)
            context["user_positions"] = Position.objects.filter(ticker=ticker, user=self.request.user)
            context["user_fills"] = Fill.objects.filter(ticker=ticker, user=self.request.user)
        else:
            context["user_orders"] = Order.objects.none()
            context["user_positions"] = Position.objects.none()
            context["user_fills"] = Fill.objects.none()
        return context
    
    def post(self, request, *args, **kwargs):
        if request.method == "POST":
            form = OrderForm(request.POST)
            if form.is_valid():
                ticker_id = request.POST.get("ticker_id")
                ticker = Ticker.objects.get(id=ticker_id)
                order = Order(order_id = ''.join(random.choices(string.ascii_letters + string.digits, k=16)),
                            user=request.user,
                            ticker=ticker, 
                            order_type = form.cleaned_data["order_type"],
                            side = form.cleaned_data["side"],
                            price = form.cleaned_data["price"] if form.cleaned_data["order_type"] =='LIMIT' else None,
                            quantity=form.cleaned_data["quantity"],
                            working_quantity=form.cleaned_data["quantity"]
                            )
                order.save()
                order.execute_order()
                order.save()
                return redirect("exchange_app:ticker_detail", pk=self.kwargs["pk"])
            

# ======== Ticker Data ========    
#    
class TradeViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = TradeSerializer
    queryset = Trade.objects.all()
    basename = "trade"  # Set a suitable basename for your viewset

    def custom_data_view(self):
        queryset = Trade.objects.all()
        ticker_id_filter = self.POST.get("ticker",None)

        OHLC = pd.DataFrame(columns=["Time, Price"])   

        # if ticker_id_filter is not None:
        # #     Use .filter() to retrieve trades related to the selected ticker
        #     queryset = queryset.filter(ticker=ticker_id_filter)
        
        for trade in queryset:  
            df = pd.DataFrame.from_dict({"Time":[trade.timestamp], "Price" : [float(trade.price)]})
            OHLC = pd.concat([OHLC, df])

        OHLC = OHLC.assign(Timestamp = pd.to_datetime(OHLC['Time'],utc=True)).set_index('Time')
        OHLC = OHLC.resample('10min')['Price'].ohlc().ffill()
        chart_data = OHLC.reset_index().to_dict(orient='records')

        formatted_data = [{
                            "time": record["Time"].timestamp(),  # F
                            "open": record["open"],
                            "high": record["high"],
                            "low": record["low"],
                            "close": record["close"],
                        } for record in chart_data]


        return JsonResponse(formatted_data, safe=False)


