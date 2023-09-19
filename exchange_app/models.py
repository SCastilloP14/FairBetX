from django.db import models
from django.contrib.auth.models import User
from enum import Enum
from exchange_app.api_scheduler.api_methods import fetch_team_data, fetch_player_data,fetch_season_games, fetch_live_scores_data, fetch_upcoming_games_data
from datetime import datetime
import time
import random, string

# ------------------- ENUMS NEEDED FOR THE MODELS --------------

class MatchStatus(Enum):
    SCHEDULED = "Scheduled"
    PLAYING = "Playing"
    FINISHED = "Finished"
    CANCELLED = "Cancelled"
    POSTPONED = "Postponed"
    ABD = "Abd"

    def __str__(self):
        return self.name

match_status_mapping = {
                        'NS': MatchStatus.SCHEDULED,
                        'PLAYING': MatchStatus.PLAYING,
                        'FT': MatchStatus.FINISHED,
                        'POST': MatchStatus.CANCELLED,
                        'CANC': MatchStatus.CANCELLED,
                        'ABD': MatchStatus.CANCELLED
                        }


class OrderType(Enum):
    LIMIT = "limit"
    MARKET = "market"

    def __str__(self):
        return self.name


class OrderSide(Enum):
    BUY = "buy"
    SELL = "sell"

    def __str__(self):
        return self.name


class OrderStatus(Enum):
    OPEN = "Open"
    PARTIAL = "Partially Filled"
    FILLED = "Filled"
    CANCELLED = "Cancelled"

    def __str__(self):
        return self.name


class TickerStatus(Enum):
    OPEN = "Open"
    CLOSED = "Closed"
    CANCELED = "Canceled"

    def __str__(self):
        return self.name

class TickerOutcome(Enum):
    LONGS_WIN = "Longs Win"
    SHORTS_WIN = "Shorts Win"
    CANCELED = "Cancelled"

    def __str__(self):
        return self.value

ticker_stauts_mapping = {
                        'NS': TickerStatus.OPEN,
                        'PLAYING': TickerStatus.OPEN,
                        'FT': TickerStatus.CLOSED,
                        'POST': TickerStatus.CANCELED,
                        'CANC': TickerStatus.CANCELED,
                        'ABD': TickerStatus.CANCELED
                        }

# ------------------- METHODS TO UPDATE MODELS ----------------------
def create_or_update_team(**kwargs):
    try:
        existing_team = Team.objects.get(team_id=kwargs["team_id"])
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
        new_object = Team(team_id=kwargs["team_id"], name=kwargs["name"], sport=kwargs["sport"], short_name=kwargs["short_name"],
                          stadium = kwargs["stadium"], badge=kwargs["badge"], jersey=kwargs["jersey"], logo=kwargs["logo"])
        new_object.save()
    
def create_or_update_player(team, **kwargs):
    player_team = Team.objects.get(team_id=team["team_id"])
    try:
        existing_player = Player.objects.get(player_id=kwargs["player_id"])
    except Player.DoesNotExist:
        # Object does not exist, create a new object
        if kwargs["number"] == '':
            kwargs["number"] = 0
        new_object = Player(player_id=kwargs["player_id"], name=kwargs["name"], number=kwargs["number"], team=player_team)
        new_object.save()
    
def create_or_update_game(**kwargs):
    try:
        existing_game = Game.objects.get(game_id=kwargs["game_id"])
        existing_game.home_team_score = kwargs["home_team_score"]
        existing_game.away_team_score = kwargs["away_team_score"]
        existing_game.start_time = kwargs["start_time"]
        existing_game.progress = kwargs["progress"]
        existing_game.status = match_status_mapping.get(kwargs["status"])
        existing_game.save()
    except Game.DoesNotExist:
        try:
            # Object does not exist, create a new object
            home_team = Team.objects.get(team_id=kwargs["home_team_id"])
            away_team=Team.objects.get(team_id=kwargs["away_team_id"])
            new_game = Game(game_id=kwargs["game_id"], sport=kwargs["sport"], league=kwargs["league"], league_id=kwargs["league_id"], 
                            home_team=home_team, away_team=away_team, progress = kwargs["progress"],
                            home_team_score=kwargs["home_team_score"], away_team_score=kwargs["away_team_score"],
                            start_time=kwargs["start_time"], status=match_status_mapping.get(kwargs["status"])
                            )
            new_game.save()
        except Team.DoesNotExist:
            print("Missing a team:", kwargs["home_team_id"], kwargs["away_team_id"])
    existing_game = Game.objects.get(game_id=kwargs["game_id"])
    create_or_update_ticker(existing_game, **kwargs)


def create_or_update_ticker(match, **kwargs):
    try:
        existing_ticker = Ticker.objects.get(ticker_id=f"{kwargs['game_id']}-T")
        if existing_ticker.status == TickerStatus.OPEN.value:
            existing_ticker.status = ticker_stauts_mapping[kwargs["status"]]
            existing_ticker.save()
            if existing_ticker.status == TickerStatus.CLOSED.value:
                if Ticker.match.home_team_score > Ticker.match.away_team_score:
                    outcome = TickerOutcome.LONGS_WIN.value
                elif Ticker.match.home_team_score < Ticker.match.away_team_score:
                    outcome = TickerOutcome.SHORTS_WIN.value
                existing_ticker.close_ticker(existing_ticker, outcome)
            elif existing_ticker.status == TickerStatus.CANCELED.value:
                existing_ticker.cancel_ticker(existing_ticker)
            existing_ticker.save()
    except Ticker.DoesNotExist:
        new_ticker = Ticker(ticker_id=f"{kwargs['game_id']}-T", 
                            match = match, 
                            status=ticker_stauts_mapping.get(kwargs["status"]))
        new_ticker.save()
        print(f"Created ticker {kwargs['game_id']}-T")


def update_teams(league_name):
    team_list = fetch_team_data(league_name)
    for team in team_list:
            create_or_update_team(**team)
            # team_players_list = fetch_player_data(team["team_id"])
            # for player in team_players_list:
            #     create_or_update_player(team, **player)


def update_season_games(league_id, season_str):
    season_games_list = fetch_season_games(league_id, season_str)
    for game in season_games_list:
        create_or_update_game(**game)


def update_live_games(league_id):
    live_games_list = fetch_live_scores_data(league_id)
    for live_game in live_games_list:
        create_or_update_game(**live_game)


def update_upcoming_games(league_id):
    upcomng_games_list = fetch_upcoming_games_data(league_id)
    for upcoming_game in upcomng_games_list:
        create_or_update_game(**upcoming_game)

# ----------------------- MODELS NEEDED -----------------------
class UserProfileInfo(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)     
    available_balance = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    locked_balance = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    @property
    def fees_paid(self):
        user_orders = Order.objects.get(user=self.user)
        fees_paid = 0
        for order in user_orders:
            order_fees_paid = order.fees_paid
            fees_paid += order_fees_paid
        return fees_paid
        
    @property
    def total_balance(self):
        return self.available_balance + self.locked_balance
    
    def lock_balance(self, balance_to_lock):
        self.locked_balance += balance_to_lock
        self.available_balance -= balance_to_lock
        self.save()

    def unlock_balance(self, balance_to_unlock):
        self.locked_balance -= balance_to_unlock
        self.available_balance += balance_to_unlock
        self.save()

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
    player_id = models.IntegerField()
    name = models.CharField(max_length=100)
    number = models.IntegerField(null=True, blank=True)
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
    home_team_score = models.IntegerField(null=True)
    away_team_score = models.IntegerField(null=True) 
    start_time = models.DateTimeField()
    progress = models.CharField(max_length=100, default="")
    status = models.CharField(max_length=20, choices=[(s.name, s) for s in MatchStatus])

    def __str__(self):
        return f"{self.home_team} vs {self.away_team}"
    

class Ticker(models.Model):
    ticker_id = models.CharField(max_length=100)
    match = models.ForeignKey(Game, on_delete=models.CASCADE, related_name="tickers")
    status = models.CharField(max_length=20, choices=[(s.name, s) for s in TickerStatus])
    last_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    volume = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    maker_fee_pct = models.DecimalField(max_digits=10, decimal_places=4, default=0.5)
    taker_fee_pct = models.DecimalField(max_digits=10, decimal_places=4, default=1.0)
    payout = models.IntegerField(default=10)
    
    def update_ticker(self, trades):
        for trade in trades:
            self.volume += trade.quantity
            self.last_price = trade.price
            self.save()

    def close_ticker(self, outcome):
        ticker_positions = Position.objects.get(ticker=self)
        for position in ticker_positions:
            if position > 0 and outcome == TickerOutcome.LONGS_WIN.value:
                user_info = position.user.userprofileinfo
                user_info.available_balance += self.payout * position.quantity
            elif position > 0 and outcome == TickerOutcome.SHORTS_WIN.value:
                user_info = position.user.userprofileinfo
                user_info.available_balance += self.payout * -position.quantity

    def __str__(self):
        return f"{self.ticker_id} {self.match}"


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
            if self.side == OrderSide.BUY.name:
                balance_to_unlock = self.price * self.quantity
            else:
                balance_to_unlock = (self.ticker.payout - self.price) * self.quantity 
            self.unlock_balance(balance_to_unlock)
            self.save()

    def lock_balance(self, balance_to_lock):
        self.user.userprofileinfo.lock_balance(balance_to_lock)

    def unlock_balance(self, balance_to_unlock):
        self.user.userprofileinfo.unlock_balance(balance_to_unlock)

    def update_order(self, fill):
        if self.avg_fill_price:
            self.avg_fill_price = ((self.filled_quantity * self.avg_fill_price) + (fill.quantity * fill.price)) / (self.filled_quantity + fill.quantity)
        else:
            self.avg_fill_price = fill.price
        self.working_quantity -= fill.quantity
        self.filled_quantity += fill.quantity
        self.paid_fees += fill.price * fill.quantity * (self.ticker.maker_fee_pct / 100)
        
        if self.order_type == OrderType.MARKET.name:
            if self.side == OrderSide.BUY.name:
                balance_to_lock = fill.price * self.quantity
            else:
                balance_to_lock = (self.ticker.payout - fill.price) * self.quantity 
            self.lock_balance(balance_to_lock)
        
        if self.working_quantity == 0:
            self.status = OrderStatus.FILLED.name
        else:
            self.status = OrderStatus.PARTIAL.name
        self.save()

    def execute_order(self):
        if self.side == OrderSide.BUY.name:
            if self.order_type == OrderType.LIMIT.name:
                balance_to_lock = self.price * self.quantity
                self.lock_balance(balance_to_lock)
                counterparties = Order.objects.filter(ticker=self.ticker, price__lte=self.price, side=OrderSide.SELL.name, working_quantity__gt=0,
                                                      status__ne=OrderStatus.CANCELLED.name).order_by("price", "modification_timestamp")
            else:
                counterparties = Order.objects.filter(ticker=self.ticker, side=OrderSide.SELL.name, working_quantity__gt=0, 
                                                    #   status__ne=OrderStatus.CANCELED.name
                                                      ).order_by("price", "modification_timestamp")
        else:
            if self.order_type == OrderType.LIMIT.name:
                balance_to_lock = (self.ticker.payout - self.price) * self.quantity 
                self.lock_balance(balance_to_lock)
                counterparties = Order.objects.filter(ticker=self.ticker, price__gte=self.price, side=OrderSide.BUY.name, working_quantity__gt=0,
                                                    #   status__ne=OrderStatus.CANCELLED.name
                                                      ).order_by("-price", "modification_timestamp")
            else:
                counterparties = Order.objects.filter(ticker=self.ticker, side=OrderSide.BUY.name, working_quantity__gt=0, status__ne=OrderStatus.CANCELED.name
                                                      ).order_by("-price", "modification_timestamp")
        remaining_quantity = self.quantity
        trades = []
        for counterparty in counterparties:
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
            user_fill.save()
            self.update_order(user_fill)
            counterparty_fill = Fill.objects.create(user=counterparty.user, ticker=self.ticker, quantity=trade_quantity, side=counterparty.side, 
                                                    price=trade_price, timestamp=models.DateTimeField(auto_now_add=True),
                                                    fill_id = ''.join(random.choices(string.ascii_letters + string.digits, k=16)))
            counterparty_fill.save()
            counterparty.update_order(counterparty_fill)
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
        return f"{self.ticker.ticker_id}-{self.trade_id}"
    

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