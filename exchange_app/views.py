
from django.shortcuts import render, redirect
# Creating views using Django views
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
        ticker = self.get_object()
        context["modify_balance_url"] = reverse("user_detail", kwargs={"pk": self.kwargs["pk"]})
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
            form = UserForm(request.POST)
            if form.is_valid():
                user_id = request.POST.get("user_id")
                user = User.objects.get(id=user_id)
                user.balance += request.POST.get("balance")
                user.save()
                return redirect("user_detail", pk=self.kwargs["pk"])
    


# -------------------- OBJECT VIEWS ------------------------

class GamesListView(ListView):
    context_object_name = "games"
    model = Game
    template_name = "exchange_app/game_list.html"

    # def get_queryset(self):
    #     return Game.objects.filter().order_by("league")

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