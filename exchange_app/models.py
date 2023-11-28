from django.db import models
from django.contrib.auth.models import User
from enum import Enum
import random, string

# ------------------- ENUMS NEEDED FOR THE MODELS --------------

class GameStatus(Enum):
    SCHEDULED = "Scheduled"
    PLAYING = "Playing"
    FINISHED = "Finished"
    CANCELED = "Cancelled"
    POSTPONED = "Postponed"
    ABDANDONED = "Abandoned"
    NO_STATUS = "No_Status"

    def __str__(self):
        return self.name

game_status_mapping = {
                        'NS': GameStatus.SCHEDULED.name,
                        'PLAYING': GameStatus.PLAYING.name,
                        'FT': GameStatus.FINISHED.name,
                        'HT': GameStatus.PLAYING.name,
                        'BT': GameStatus.PLAYING.name,
                        'CANC': GameStatus.CANCELED.name,
                        'POST': GameStatus.POSTPONED.name,
                        'ABD': GameStatus.ABDANDONED.name,
                        '': GameStatus.NO_STATUS.name,
                        'AOT':GameStatus.FINISHED.name,
                        'AP':GameStatus.FINISHED.name
                        }

class TickerStatus(Enum):
    OPEN = "Open"
    CLOSED = "Closed"
    CANCELED = "Canceled"

    def __str__(self):
        return self.name
    
ticker_status_mapping = {GameStatus.SCHEDULED.name: TickerStatus.OPEN.name,
                         GameStatus.PLAYING.name: TickerStatus.OPEN.name,
                         GameStatus.FINISHED.name: TickerStatus.CLOSED.name,
                         GameStatus.CANCELED.name: TickerStatus.CANCELED.name,
                         GameStatus.POSTPONED.name: TickerStatus.CANCELED.name,
                         GameStatus.ABDANDONED.name: TickerStatus.CANCELED.name,
                         GameStatus.NO_STATUS.name: TickerStatus.CLOSED.name,
                         }

class TickerOutcome(Enum):
    LONGS_WIN = "Longs Win"
    SHORTS_WIN = "Shorts Win"
    CANCELED = "Cancelled"


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
    CANCELED = "Cancelled"

    def __str__(self):
        return self.name

    def __str__(self):
        return self.value

ticker_stauts_mapping = {
                        'NS': TickerStatus.OPEN.name,
                        'PLAYING': TickerStatus.OPEN.name,
                        'FT': TickerStatus.CLOSED.name,
                        'POST': TickerStatus.CANCELED.name,
                        'CANC': TickerStatus.CANCELED.name,
                        'ABD': TickerStatus.CANCELED.name
                        }

# ----------------------- MODELS NEEDED -----------------------
class UserProfileInfo(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)     
    user_available_balance = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    user_locked_balance = models.DecimalField(max_digits=10, decimal_places=2, default=0)

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


class League(models.Model):
    league_id = models.IntegerField()
    league_sport = models.CharField(max_length=100)
    league_name = models.CharField(max_length=100)
    league_alternative_name = models.CharField(max_length=100)
    league_current_season = models.CharField(max_length=100)
    league_formed_year = models.IntegerField()
    league_first_event = models.CharField(max_length=100)
    league_gender = models.CharField(max_length=100)
    league_country = models.CharField(max_length=100)
    league_description = models.CharField(max_length=5000)
    league_badge = models.CharField(max_length=100)
    league_logo = models.CharField(max_length=100)
    league_trophy = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.league_sport} {self.league_name}"

 

class Team(models.Model):
    team_id = models.IntegerField()
    team_name = models.CharField(max_length=100)
    team_short_name = models.CharField(max_length=10, null=True, blank=True)
    team_year_formed = models.IntegerField(null=True, blank=True)
    team_sport = models.CharField(max_length=20, null=True, blank=True)
    team_league_1 = models.ForeignKey(League, on_delete=models.CASCADE, related_name="team_league_1", null=True, blank=True)
    team_league_2 = models.ForeignKey(League, on_delete=models.CASCADE, related_name="team_league_2", null=True, blank=True)
    team_league_3 = models.ForeignKey(League, on_delete=models.CASCADE, related_name="team_league_3", null=True, blank=True)
    team_league_4 = models.ForeignKey(League, on_delete=models.CASCADE, related_name="team_league_4", null=True, blank=True)
    team_league_5 = models.ForeignKey(League, on_delete=models.CASCADE, related_name="team_league_5", null=True, blank=True)
    team_league_6 = models.ForeignKey(League, on_delete=models.CASCADE, related_name="team_league_6", null=True, blank=True)
    team_league_7 = models.ForeignKey(League, on_delete=models.CASCADE, related_name="team_league_7", null=True, blank=True)
    team_stadium = models.CharField(max_length=100, null=True, blank=True)
    team_stadium_description = models.CharField(max_length=100, null=True, blank=True)
    team_stadium_capacity = models.IntegerField(null=True, blank=True)
    team_location = models.CharField(max_length=100, null=True, blank=True)
    team_country = models.CharField(max_length=100, null=True, blank=True)
    team_gender = models.CharField(max_length=100, null=True, blank=True)
    team_description = models.CharField(max_length=5000, null=True, blank=True)
    team_badge = models.CharField(max_length=100, null=True, blank=True)
    team_jersey = models.CharField(max_length=100, null=True, blank=True)
    team_logo = models.CharField(max_length=100, null=True, blank=True)
    

    def __str__(self):
        return f"{self.team_name} {self.team_league_1.league_name}"


class Player(models.Model):
    player_id = models.IntegerField()
    player_name = models.CharField(max_length=50)
    player_sport = models.CharField(max_length=100, null=True, blank=True)
    player_nationality = models.CharField(max_length=100, null=True, blank=True)
    player_date_of_birth = models.DateTimeField(null=True, blank=True)
    player_number = models.IntegerField(null=True, blank=True)
    player_birth_location = models.CharField(max_length=100, null=True, blank=True)
    player_status = models.CharField(max_length=100, null=True, blank=True)
    player_description = models.CharField(max_length=5000, null=True, blank=True)
    player_gender = models.CharField(max_length=10, null=True, blank=True)
    player_position = models.CharField(max_length=50, null=True, blank=True)
    player_height = models.CharField(max_length=50, null=True, blank=True)
    player_weight = models.CharField(max_length=50, null=True, blank=True)
    player_photo = models.CharField(max_length=10, null=True, blank=True)
    player_team = models.ForeignKey(Team, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return f"{self.player_name} {self.player_team.team_name}"
    

class Game(models.Model):
    game_id = models.IntegerField()
    game_name = models.CharField(max_length=100)
    game_alternative_name = models.CharField(max_length=100, null=True, blank=True)
    game_filename = models.CharField(max_length=100, null=True, blank=True)
    game_season = models.CharField(max_length=100)
    game_home_team = models.ForeignKey(Team, related_name="home_games", on_delete=models.CASCADE)
    game_away_team = models.ForeignKey(Team, related_name="away_games", on_delete=models.CASCADE)
    game_home_team_score = models.IntegerField(null=True, blank=True)
    game_away_team_score = models.IntegerField(null=True, blank=True) 
    game_round = models.IntegerField(null=True, blank=True)
    game_spectators = models.IntegerField(null=True, blank=True)
    game_official = models.CharField(max_length=100, null=True, blank=True)
    game_start_datetime = models.DateTimeField(null=True, blank=True)
    game_results = models.CharField(max_length=100, null=True, blank=True)
    game_venue = models.CharField(max_length=100, null=True, blank=True)
    game_country = models.CharField(max_length=100, null=True, blank=True)
    game_city = models.CharField(max_length=100, null=True, blank=True)
    game_progress = models.CharField(max_length=100, null=True, blank=True)
    game_status = models.CharField(max_length=20, choices=[(s.name, s) for s in GameStatus])
    game_postponed = models.BooleanField(default=False)
    game_league = models.ForeignKey(League, on_delete=models.CASCADE, related_name="league_games")

    def __str__(self):
        return f"{self.game_filename}"
    

class Ticker(models.Model):
    ticker_id = models.CharField(max_length=100)
    ticker_game = models.ForeignKey(Game, on_delete=models.CASCADE, related_name="tickers")
    ticker_status = models.CharField(max_length=20, choices=[(s.name, s) for s in TickerStatus], default=TickerStatus.OPEN.name)
    ticker_last_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    ticker_best_bid = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    ticker_best_ask = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    ticker_volume = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    ticker_maker_fee_pct = models.DecimalField(max_digits=10, decimal_places=4, default=0.5)
    ticker_taker_fee_pct = models.DecimalField(max_digits=10, decimal_places=4, default=1.0)
    ticker_payout = models.IntegerField(default=10)
    ticker_outcome = models.CharField(max_length=20, choices=[(s.name, s) for s in TickerOutcome])

    def update_ticker_activity(self, trades):
        for trade in trades:
            self.volume += trade.quantity
            self.last_price = trade.price
            self.save()

    def check_outcome(self):
        if self.ticker_game.game_home_team_score > self.ticker_game.game_away_team_score:
            self.ticker_outcome = TickerOutcome.LONGS_WIN.name
        else:
            self.ticker_outcome = TickerOutcome.SHORTS_WIN.name
        
    def close_ticker(self):
        self.ticker_status = TickerStatus.CLOSED.name
        self.save()
        self.check_outcome()
        self.pay_winners()

    def cancel_ticker(self):
        #   Finish sending back the money
        self.ticker_status = TickerStatus.CANCELED.name
        self.save()

    def pay_winners(self):
        try:
            ticker_positions = Position.objects.get(position_ticker=self)
            for position in ticker_positions:
                position_payout= self.payout * abs(position.quantity)
                if position.quantity > 0 and self.ticker_outcome == TickerOutcome.LONGS_WIN.name:
                    position_user = position.user
                    position_user.userprofileinfo.available_balance += position_payout
                    position_user.userprofileinfo.locked_balance -= position.quantitity * position.average_price 
                elif position.quantity < 0 and self.ticker_outcome == TickerOutcome.SHORTS_WIN.name:
                    position_user = position.user.userprofileinfo
                    position_user.available_balance += position_payout
                    position_user.userprofileinfo.locked_balance -= position.quantitity * (self.payout - position.average_price)
        except Position.DoesNotExist:
            print(f"{self.ticker_game.game_filename} closed without any positions")

    def update_ticker(game: Game, **kwargs):
        try:
            existing_ticker = Ticker.objects.get(ticker_id=f"{kwargs['game_id']}-T")
            # if "IN" in kwargs["status"]:
            #     print(existing_ticker.status, TickerStatus.OPEN.name, existing_ticker.status == TickerStatus.OPEN.name)
            if existing_ticker.status == TickerStatus.OPEN.name:
                existing_ticker.status = ticker_stauts_mapping[kwargs["status"]]
                existing_ticker.save()
                if existing_ticker.status == TickerStatus.CLOSED.name:
                    if Ticker.game.home_team_score > Ticker.game.away_team_score:
                        print("Closing Ticker", f"{kwargs['game_id']}-T with longs win")
                        outcome = TickerOutcome.LONGS_WIN.name
                    elif Ticker.game.home_team_score < Ticker.game.away_team_score:
                        outcome = TickerOutcome.SHORTS_WIN.name
                        print("Closing Ticker", f"{kwargs['game_id']}-T with shorts win")
                    existing_ticker.close_ticker(existing_ticker, outcome)
                elif existing_ticker.status == TickerStatus.CANCELED.name:
                    print("Canceling Ticker", f"{kwargs['game_id']}-T")
                    existing_ticker.cancel_ticker(existing_ticker)
                existing_ticker.save()
        except Ticker.DoesNotExist:
            if ticker_stauts_mapping[kwargs["status"]] == TickerStatus.OPEN:
                new_ticker = Ticker(ticker_id=f"{kwargs['game_id']}-T", 
                                    ticker_game = game, 
                                    status=TickerStatus.OPEN)
                new_ticker.save()
                print(f"Created ticker {kwargs['game_id']}-T")

    def __str__(self):
        return f"{self.ticker_game.game_filename}-T"


class Order(models.Model):
    order_id = models.CharField(max_length=100)
    order_user = models.ForeignKey(User, on_delete=models.CASCADE)
    order_ticker = models.ForeignKey(Ticker, on_delete=models.CASCADE)
    order_type = models.CharField(max_length=20, choices=[(s.name, s.value) for s in OrderType])
    order_side = models.CharField(max_length=20, choices=[(s.name, s.value) for s in OrderSide])
    order_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, default=None)
    order_quantity = models.IntegerField(default=0)
    order_filled_quantity = models.IntegerField(default=0)
    order_working_quantity = models.IntegerField(default=0)
    order_avg_fill_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, default=None)
    order_status = models.CharField(max_length=20, choices=[(s.name, s.value) for s in OrderStatus], default=OrderStatus.OPEN.name)
    order_paid_fees = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    order_creation_timestamp = models.DateTimeField(auto_now_add=True)
    order_modification_timestamp = models.DateTimeField(auto_now_add=True)

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
        # If statement to check balance and return error message.
        required_balance = self.price * self.quantity if self.side == OrderSide.BUY.name else (self.payout - self.price) * self.quantity
        if required_balance > self.user.userprofileinfo.available_balance:
            return "NOT ENOUGH BALANCE"
        try:
            user_position = Position.objects.get(user=self.user, ticker=self.ticker)
            user_posittion_quantity = user_position.quantity
            user_position_avg_price = user_position.average_price
        except Position.DoesNotExist:
            user_posittion_quantity = 0
            user_position_avg_price = 0
        if self.side == OrderSide.BUY.name:
            if self.order_type == OrderType.LIMIT.name:
                if user_posittion_quantity >= 0:
                    # Case 1 + Case 2
                    balance_to_lock = self.price * self.quantity
                    self.lock_balance(balance_to_lock)
                elif user_posittion_quantity < 0:
                    if abs(user_posittion_quantity) >= self.quantity:
                        # Case 3 & Case 4
                        pass
                    else:
                        balance_needed_after_flip = (user_posittion_quantity + self.quantity) * self.price
                        balance_needed_currently = (self.ticker.payout - user_position_avg_price) * self.price
                        # Case 5
                        
                counterparties = Order.objects.filter(ticker=self.ticker, price__lte=self.price, side=OrderSide.SELL.name, working_quantity__gt=0,
                                                    #   status__ne=OrderStatus.CANCELLED.name
                                                      ).order_by("price", "modification_timestamp")
            else:
                counterparties = Order.objects.filter(ticker=self.ticker, side=OrderSide.SELL.name, working_quantity__gt=0, 
                                                    #   status__ne=OrderStatus.CANCELLED.name
                                                      ).order_by("price", "modification_timestamp")
        else:
            if self.order_type == OrderType.LIMIT.name:
                balance_to_lock = (self.ticker.payout - self.price) * self.quantity 
                self.lock_balance(balance_to_lock)
                counterparties = Order.objects.filter(ticker=self.ticker, price__gte=self.price, side=OrderSide.BUY.name, working_quantity__gt=0,
                                                    #   status__ne=OrderStatus.CANCELLED.name
                                                      ).order_by("-price", "modification_timestamp")
            else:
                counterparties = Order.objects.filter(ticker=self.ticker, side=OrderSide.BUY.name, working_quantity__gt=0, 
                                                    #   status__ne=OrderStatus.CANCELED.name
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
    fill_user = models.ForeignKey(User, on_delete=models.CASCADE)
    fill_ticker = models.ForeignKey(Ticker, on_delete=models.CASCADE)
    fill_side = models.CharField(max_length=20, choices=[(s.name, s.value) for s in OrderSide])
    fill_quantity = models.PositiveIntegerField(default=0)
    fill_price = models.DecimalField(max_digits=10, decimal_places=2)
    fill_timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.fill_id}"


class Trade(models.Model):
    trade_trade_id = models.CharField(max_length=20)
    trade_ticker = models.ForeignKey(Ticker, on_delete=models.CASCADE)
    trade_buy = models.ForeignKey(Order, related_name="buy_trades",on_delete=models.CASCADE)
    trade_sell = models.ForeignKey(Order, related_name="sell_trades", on_delete=models.CASCADE)
    trade_quantity = models.PositiveIntegerField()
    trade_price = models.DecimalField(max_digits=10, decimal_places=2)
    trade_timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.ticker.ticker_id}-{self.trade_id}"
    

class Position(models.Model):
    position_user = models.ForeignKey(User, on_delete=models.CASCADE)
    position_ticker = models.ForeignKey(Ticker, on_delete=models.CASCADE)
    position_quantity = models.IntegerField(default=0)
    position_average_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    position_open_pnl = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    position_closed_pnl = models.DecimalField(max_digits=10, decimal_places=2, default=0)

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