from django.db import models
from django.contrib.auth.models import User
from enum import Enum
from exchange_app.api_scheduler.api_methods import fetch_team_data, fetch_player_data,fecth_season_games, fetch_live_scores_data
from datetime import datetime
import time
import random, string

# ------------------- ENUMS NEEDED FOR THE MODELS --------------
class MatchStatus(Enum):
    SCHEDULED = "Scheduled"
    PLAYING = "Playing"
    FINISHED = "Finished"
    CANCELLED = "Cancelled"


class OrderType(Enum):
    LIMIT = "limit"
    MARKET = "market"


class OrderSide(Enum):
    BUY = "buy"
    SELL = "sell"


class OrderStatus(Enum):
    OPEN = "Open"
    PARTIAL = "Partially Filled"
    FILLED = "Filled"
    CANCELLED = "Cancelled"


class TickerStatus(Enum):
    OPEN = "Open"
    CLOSED = "Closed"

# ------------------- METHODS TO UPDATE MODELS ----------------------
def create_or_update_team(**kwargs):
    try:
        existing_team = Team.objects.get(player_id=kwargs["team_id"])
        existing_team.name = kwargs["name"]
        existing_team.sport = kwargs["sport"]
        existing_team.short_name = kwargs["short_name"]
        existing_team.stadium = kwargs["stadium"]
        existing_team.badge = kwargs["badge"]
        existing_team.jersey = kwargs["jersey"]
        existing_team.logo = kwargs["logo"]
        existing_team.save()
    except Team.DoesNotExist:
        # Object does not exist, create a new object
        new_object = Team(player_id=kwargs["player_id"], name=kwargs["name"], sport=kwargs["sport"], short_name=kwargs["short_name"],
                          stadium = kwargs["stadium"], badge=kwargs["badge"], jersey=kwargs["jersey"], logo=kwargs["logo"])
        new_object.save()
        return new_object
    
def create_or_update_player(**kwargs):
    try:
        existing_player = Player.objects.get(player_id=kwargs["player_id"])
        existing_player.name = kwargs["name"]
        existing_player.number = kwargs["number"]
        existing_player.save()
    except Player.DoesNotExist:
        # Object does not exist, create a new object
        new_object = Team(player_id=kwargs["player_id"], name=kwargs["name"], number=kwargs["number"])
        new_object.save()
        return new_object
    
def create_or_update_game(**kwargs):
    try:
        existing_game = Game.objects.get(game_id=kwargs["game_id"])
        # Check what needs to be updated
        existing_game.sport = kwargs["sport"]
        existing_game.league = kwargs["league"]
        existing_game.league_id = kwargs["league"]
        existing_game.home_team = Team.objects.get(team_id=kwargs["home_team_id"])
        existing_game.away_team = Team.objects.get(team_id=kwargs["away_team_id"])
        existing_game.home_team_score = kwargs["home_team_score"]
        existing_game.away_team_score = kwargs["away_team_score"]
        existing_game.start_time = kwargs["start_time"]
        existing_game.status = kwargs["status"]
        existing_game.save()
    except Game.DoesNotExist:
        # Object does not exist, create a new object
        new_object = Team(game_id=kwargs["game_id"], sport=kwargs["sport"], league_id=kwargs["league"], 
                          home_team=Team.objects.get(id=kwargs["home_team_id"]), 
                          away_team=Team.objects.get(id=kwargs["away_team_id"]),
                          home_team_score=kwargs["home_team_score"], away_team_score=kwargs["away_team_score"],
                          start_time=kwargs["start_time"], status=kwargs["status"]
                          )
        new_object.save()
        return new_object


def update_teams(league_name):
    team_list = fetch_team_data(league_name)
    for team in team_list:
            create_or_update_team(**team)
            team_players_list = fetch_player_data(team["team_id"])
            for player in team_players_list:
                create_or_update_player(**team)


def update_season_games(league_id, season_str):
    season_games_list = fecth_season_games(league_id, season_str)
    for game in season_games_list:
        create_or_update_game(**game)
    

def update_live_games(league_id):
    live_games_list = fetch_live_scores_data(league_id)
    for live_game in live_games_list:
        create_or_update_game(**live_game)


# ----------------------- MODELS NEEDED -----------------------
class UserProfileInfo(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name}"


class Team(models.Model):
    team_id = models.IntegerField()
    name = models.CharField(max_length=100)
    sport = models.CharField(max_length=100)
    short_name = models.CharField(max_length=100)
    stadium = models.CharField(max_length=100)
    badge = models.CharField(max_length=100)
    jersey = models.CharField(max_length=100)
    logo = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Player(models.Model):
    name = models.CharField(max_length=100)
    number = models.IntegerField(default="")
    team = models.ForeignKey(Team, on_delete=models.CASCADE)

    def __str__(self):
        return self.name
    

class Game(models.Model):
    game_id = models.IntegerField()
    sport = models.CharField(max_length=100, default="")
    league = models.CharField(max_length=100, default="")
    league_id = models.IntegerField(default=0)
    home_team = models.ForeignKey(Team, related_name="home_games", on_delete=models.CASCADE)
    away_team = models.ForeignKey(Team, related_name="away_games", on_delete=models.CASCADE)
    home_team_score = models.IntegerField()
    away_team_score = models.IntegerField() 
    start_time = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=[(s.name, s.value) for s in MatchStatus], default=MatchStatus.SCHEDULED.value)


    # @classmethod
    # def create_ticker(cls):
    #     Ticker.objects.create(match=cls, ticker_id=cls.id)

    def __str__(self):
        return f"{self.home_team} vs {self.away_team}"
    

class Ticker(models.Model):
    ticker_id = models.CharField(max_length=100)
    match = models.ForeignKey(Game, on_delete=models.CASCADE, related_name="tickers")
    status = models.CharField(max_length=20, choices=[(s.name, s.value) for s in TickerStatus], default=TickerStatus.OPEN.value)
    last_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    volume = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    maker_fee_pct = models.DecimalField(max_digits=10, decimal_places=4, default=0.5)
    taker_fee_pct = models.DecimalField(max_digits=10, decimal_places=4, default=1.0)
    
    def update_ticker(self, trades):
        for trade in trades:
            print(trade.quantity, trade.price)
            self.volume += trade.quantity
            self.last_price = trade.price
            self.save()

    def __str__(self):
        return self.ticker_id


class Order(models.Model):
    order_id = models.CharField(max_length=100)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    ticker = models.ForeignKey(Ticker, on_delete=models.CASCADE)
    order_type = models.CharField(max_length=20, choices=[(s.name, s.value) for s in OrderType])
    side = models.CharField(max_length=20, choices=[(s.name, s.value) for s in OrderSide])
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True, default=None)
    quantity = models.IntegerField(default=0)
    filled_quantity = models.IntegerField(default=0)
    working_quantity = models.IntegerField(default=0)
    avg_fill_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, default=None)
    status = models.CharField(max_length=20, choices=[(s.name, s.value) for s in OrderStatus], default=OrderStatus.OPEN.name)
    paid_fees = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    creation_timestamp = models.DateTimeField(auto_now_add=True)
    modification_timestamp = models.DateTimeField(auto_now_add=True)

    def cancel(self):
        if self.status != OrderStatus.FILLED.value:
            self.status = OrderStatus.CANCELLED.value
            self.save()

    def update_order(self, fill):
        print(self.user.first_name, self.quantity, self.filled_quantity, self.working_quantity)
        print(fill.quantity)
        if self.avg_fill_price:
            self.avg_fill_price = ((self.filled_quantity * self.avg_fill_price) + (fill.quantity * fill.price)) / (self.filled_quantity + fill.quantity)
        else:
            self.avg_fill_price = fill.price
        self.working_quantity -= fill.quantity
        self.filled_quantity += fill.quantity
        self.paid_fees += fill.price * fill.quantity * (self.ticker.maker_fee_pct / 100)
        if self.working_quantity == 0:
            self.status = OrderStatus.FILLED.name
        else:
            self.status = OrderStatus.PARTIAL.name
        print(self.user.first_name, self.quantity, self.filled_quantity, self.working_quantity)
        self.save()

    def execute_order(self):
        # Find counterparties
        if self.side == OrderSide.BUY.name:
            if self.order_type == OrderType.LIMIT.name:
                counterparties = Order.objects.filter(ticker=self.ticker, price__lte=self.price, side=OrderSide.SELL.name, working_quantity__gt=0
                                                    ).order_by("price", "modification_timestamp")
            else:
                counterparties = Order.objects.filter(ticker=self.ticker, side=OrderSide.SELL.name, working_quantity__gt=0,
                                                      ).order_by("price", "modification_timestamp")
        else:
            if self.order_type == OrderType.LIMIT.name:
                counterparties = Order.objects.filter(ticker=self.ticker, price__gte=self.price, side=OrderSide.BUY.name, working_quantity__gt=0
                                                    ).order_by("-price", "modification_timestamp")
            else:
                counterparties = Order.objects.filter(ticker=self.ticker, side=OrderSide.BUY.name, working_quantity__gt=0,
                                                      ).order_by("-price", "modification_timestamp")
        remaining_quantity = self.quantity
        trades = []
        for counterparty in counterparties:
            print('Remaining', remaining_quantity)
            if remaining_quantity <= 0:
                break
            trade_quantity = min(remaining_quantity, counterparty.working_quantity)
            trade_price = counterparty.price
            trade = Trade.objects.create(buy=counterparty if self.side == OrderSide.SELL.name else self, 
                                         sell=self if self.side == OrderSide.SELL.name else counterparty, 
                                         quantity=trade_quantity,price=trade_price, ticker=self.ticker)
            trades.append(trade)
            remaining_quantity -= trade_quantity

            user_fill = Fill.objects.create(user=self.user, ticker=self.ticker, quantity=trade_quantity, side=self.side, 
                                            price=trade_price, timestamp=models.DateTimeField(auto_now_add=True),
                                            fill_id = ''.join(random.choices(string.ascii_letters + string.digits, k=16)))
            print("UPDATING", self.user.first_name)
            user_fill.save()
            self.update_order(user_fill)
            counterparty_fill = Fill.objects.create(user=counterparty.user, ticker=self.ticker, quantity=trade_quantity, side=counterparty.side, 
                                                    price=trade_price, timestamp=models.DateTimeField(auto_now_add=True),
                                                    fill_id = ''.join(random.choices(string.ascii_letters + string.digits, k=16)))
            print("UPDATING", counterparty.user.first_name)
            counterparty_fill.save()
            counterparty.update_order(counterparty_fill)
        print(trades)
        self.ticker.update_ticker(trades)
        Position.update_positions(trades)

    def __str__(self):
        return f"{self.user}: {self.side} - {self.quantity} @ {self.price}"


class Fill(models.Model):
    fill_id = models.CharField(max_length=20)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    ticker = models.ForeignKey(Ticker, on_delete=models.CASCADE)
    side = models.CharField(max_length=20, choices=[(s.name, s.value) for s in OrderSide])
    quantity = models.PositiveIntegerField(default=0)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.fill_id}"


class Trade(models.Model):
    trade_id = models.CharField(max_length=20)
    ticker = models.ForeignKey(Ticker, on_delete=models.CASCADE)
    buy = models.ForeignKey(Order, related_name="buy_trades",on_delete=models.CASCADE)
    sell = models.ForeignKey(Order, related_name="sell_trades", on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.trade_id}"
    

class Position(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    ticker = models.ForeignKey(Ticker, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=0)
    average_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    open_pnl = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    closed_pnl = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    @classmethod
    def update_positions(cls, trades):
        for trade in trades:
            buy = trade.buy
            sell = trade.sell

            # Update the positions for the buy user
            buy_position, _ = cls.objects.get_or_create(user=buy.user, ticker=buy.ticker)
            if buy_position.quantity == 0:
                buy_position.average_price = trade.price
            elif buy_position.quantity < 0:
                buy_position.closed_pnl = (buy_position.average_price - trade.price) * trade.quantity
                if buy_position.quantity + trade.quantity == 0:
                    buy_position.average_price = 0
            else:
                buy_position.average_price = ((buy_position.average_price * buy_position.quantity) + (trade.price * trade.quantity)) / (buy_position.quantity + trade.quantity)
            buy_position.quantity += trade.quantity
            buy_position.open_pnl = (buy_position.average_price - trade.ticker.last_price) * buy_position.quantity
            buy_position.save()

            # Update the positions for the sell user
            sell_position, _ = cls.objects.get_or_create(user=sell.user, ticker=sell.ticker)
            if sell_position.quantity == 0:
                sell_position.average_price = trade.price
            elif sell_position.quantity > 0:
                sell_position.closed_pnl = (trade.price - sell_position.average_price) * trade.quantity
                if sell_position.quantity - trade.quantity == 0:
                    sell_position.average_price = 0
            else:
                sell_position.average_price = ((sell_position.average_price * sell_position.quantity) - (trade.price * trade.quantity)) / (sell_position.quantity - trade.quantity)
            sell_position.quantity -= trade.quantity
            sell_position.open_pnl = (trade.ticker.last_price - sell_position.average_price) * sell_position.quantity
            sell_position.save()

        def __str__(self):
            return f"{self.user.username} {self.ticker.ticker_id}"