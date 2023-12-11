from django.db import models
from django.contrib.auth.models import User
from enum import Enum
import random, string

# ------------------- ENUMS NEEDED FOR THE MODELS --------------

class TransactionType(Enum):
    DEPOSIT = "Deposit"
    WITHDRAWAL = "Withdrawal"


class GameStatus(Enum):
    SCHEDULED = "Scheduled"
    PLAYING = "Playing"
    FINISHED = "Finished"
    CANCELED = "Canceled"
    POSTPONED = "Postponed"
    ABDANDONED = "Abandoned"
    NO_STATUS = "No_Status"

    def __str__(self):
        return self.name

game_status_mapping = {
                        'NS': GameStatus.SCHEDULED.name,
                        'pre': GameStatus.SCHEDULED.name,
                        'PLAYING': GameStatus.PLAYING.name,
                        'FT': GameStatus.FINISHED.name,
                        'Final': GameStatus.FINISHED.name,
                        'Final/OT': GameStatus.FINISHED.name,
                        'HT': GameStatus.PLAYING.name,
                        'BT': GameStatus.PLAYING.name,
                        'CANC': GameStatus.CANCELED.name,
                        'POST': GameStatus.POSTPONED.name,
                        'ABD': GameStatus.ABDANDONED.name,
                        'AOT': GameStatus.FINISHED.name,
                        'AP': GameStatus.FINISHED.name,
                        'Q1': GameStatus.PLAYING.name,
                        'Q2': GameStatus.PLAYING.name,
                        'Q3': GameStatus.PLAYING.name,
                        'Q4': GameStatus.PLAYING.name,
                        'P1': GameStatus.PLAYING.name,
                        'P2': GameStatus.PLAYING.name,
                        'P3': GameStatus.PLAYING.name,
                        'IN1': GameStatus.PLAYING.name,
                        'IN2': GameStatus.PLAYING.name,
                        'IN3': GameStatus.PLAYING.name,
                        'IN4': GameStatus.PLAYING.name,
                        'IN5': GameStatus.PLAYING.name,
                        'IN6': GameStatus.PLAYING.name,
                        'IN7': GameStatus.PLAYING.name,
                        'IN8': GameStatus.PLAYING.name,
                        'IN9': GameStatus.PLAYING.name,
                        'OT': GameStatus.PLAYING.name,
                        'P': GameStatus.PLAYING.name,

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
                         GameStatus.NO_STATUS.name: TickerStatus.OPEN.name,
                         }

class TickerOutcome(Enum):
    LONGS_WIN = "Longs Win"
    SHORTS_WIN = "Shorts Win"
    CANCELED = "Canceled"


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
    CANCELED = "Canceled"
    SETTLED = "Settled"

    def __str__(self):
        return self.name


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
        return self.user_available_balance + self.user_locked_balance
    
    def lock_balance(self, balance_to_lock):
        self.user_locked_balance += balance_to_lock
        self.user_available_balance -= balance_to_lock
        self.save()

    def unlock_balance(self, balance_to_unlock):
        self.user_locked_balance -= balance_to_unlock
        self.user_available_balance += balance_to_unlock
        self.save()

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name}"
        
class Transaction(models.Model):
    transaction_user = models.ForeignKey(User, on_delete=models.CASCADE)
    transaction_type = models.CharField(max_length=20, choices=[(s.name, s) for s in TransactionType])
    transaction_id = models.CharField(max_length=100)
    transaction_time = models.DateTimeField(auto_now_add=True)
    transaction_amount = models.DecimalField(max_digits=10, decimal_places=2, null=True, default=None)


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
    team_stadium_description = models.CharField(max_length=5000, null=True, blank=True)
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
    player_sport = models.CharField(max_length=50, null=True, blank=True)
    player_nationality = models.CharField(max_length=50, null=True, blank=True)
    player_date_of_birth = models.DateTimeField(null=True, blank=True)
    player_number = models.IntegerField(null=True, blank=True)
    player_birth_location = models.CharField(max_length=200, null=True, blank=True)
    player_status = models.CharField(max_length=50, null=True, blank=True)
    player_description = models.CharField(max_length=10000, null=True, blank=True)
    player_gender = models.CharField(max_length=50, null=True, blank=True)
    player_position = models.CharField(max_length=50, null=True, blank=True)
    player_height = models.CharField(max_length=50, null=True, blank=True)
    player_weight = models.CharField(max_length=50, null=True, blank=True)
    player_photo = models.CharField(max_length=100, null=True, blank=True)
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
    game_results = models.CharField(max_length=300, null=True, blank=True)
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
            self.ticker_volume += trade.trade_quantity
            self.ticker_last_price = trade.trade_price
        self.save()

    def check_outcome(self):
        print(self.ticker_game.game_filename)
        if self.ticker_game.game_home_team_score > self.ticker_game.game_away_team_score:
            self.ticker_outcome = TickerOutcome.LONGS_WIN.name
        else:
            self.ticker_outcome = TickerOutcome.SHORTS_WIN.name
        
    def close_ticker(self):
        self.ticker_status = TickerStatus.CLOSED.name
        # Close all open orders on the ticker.
        self.check_outcome()
        self.save()
        self.pay_winners()

    def cancel_ticker(self):
        #   Finish sending back the money
        self.ticker_status = TickerStatus.CANCELED.name
        self.save()

    def close_remaining_orders(self):
        ticker_orders_to_cancel = Order.objects.filter(order_ticker=self)
        ticker_orders_to_cancel.update(order_status=OrderStatus.SETTLED.name)

    def pay_winners(self):
        try:
            ticker_positions = Position.objects.filter(position_ticker=self)
            print("Paying winners for", self.ticker_game.game_filename, len(ticker_positions))
            for position in ticker_positions:
                print("Pos info:", position.position_user.username, position.position_quantity)
                position_payout= self.ticker_payout * abs(position.position_quantity)
                position_user = position.position_user

                if position.position_quantity > 0 and self.ticker_outcome == TickerOutcome.LONGS_WIN.name:
                    print("LONG WINNER!")
                    position.position_settled_pnl = (self.ticker_payout - position.position_average_price) * position.position_quantity
                    position_user.userprofileinfo.user_available_balance += position_payout
                    position_user.userprofileinfo.user_locked_balance -= position.position_quantity * position.position_average_price

                elif position.position_quantity > 0 and self.ticker_outcome == TickerOutcome.SHORTS_WIN.name:
                    print("LONG LOSER!")
                    position.position_settled_pnl = -position.position_average_price * position.position_quantity
                    position_user.userprofileinfo.user_locked_balance -= position.position_quantity * position.position_average_price

                elif position.position_quantity < 0 and self.ticker_outcome == TickerOutcome.SHORTS_WIN.name:
                    print("SHORT WINNER!")
                    position.position_settled_pnl += position.position_average_price * position.position_quantity
                    position_user.userprofileinfo.user_available_balance += position_payout
                    position_user.userprofileinfo.user_locked_balance -= position.position_quantity * (self.ticker_payout - position.position_average_price)

                elif position.position_quantity < 0 and self.ticker_outcome == TickerOutcome.LONGS_WIN.name:
                    print("SHORT LOSER!")
                    position.position_settled_pnl = -(self.ticker_payout - position.position_average_price) * position.position_quantity
                    position_user.userprofileinfo.user_locked_balance -= position.position_quantity * (self.ticker_payout - position.position_average_price)
                
                position.position_settled = True
                position.save()
                position_user.userprofileinfo.save()

        except Position.DoesNotExist:
            print(f"{self.ticker_game.game_filename} closed without any positions")

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
        if self.order_status != OrderStatus.FILLED.name:
            self.order_status = OrderStatus.CANCELED.name
            if self.order_side == OrderSide.BUY.name:
                balance_to_unlock = self.order_price * self.order_working_quantity
            else:
                balance_to_unlock = (self.order_ticker.ticker_payout - self.order_price) * self.order_working_quantity 
            self.unlock_balance(balance_to_unlock)
            self.save()

    def lock_balance(self, balance_to_lock):
        self.order_user.userprofileinfo.lock_balance(balance_to_lock)

    def unlock_balance(self, balance_to_unlock):
        self.order_user.userprofileinfo.unlock_balance(balance_to_unlock)

    def update_order(self, fill):
        if self.order_avg_fill_price:
            self.order_avg_fill_price = ((self.order_filled_quantity * self.order_avg_fill_price) + (fill.fill_quantity * fill.fill_price)) / (self.order_filled_quantity + fill.fill_quantity)
        else:
            self.order_avg_fill_price = fill.fill_price
        self.order_working_quantity -= fill.fill_quantity
        self.order_filled_quantity += fill.fill_quantity
        self.order_paid_fees += fill.fill_price * fill.fill_quantity * (self.order_ticker.ticker_maker_fee_pct / 100)

        if self.order_type == OrderType.MARKET.name:
            if self.order_side == OrderSide.BUY.name:
                balance_to_lock = fill.fill_price * self.order_quantity
            else:
                balance_to_lock = (self.order_ticker.ticker_payout - fill.fill_price) * self.order_quantity 
            self.lock_balance(balance_to_lock)

        if self.order_working_quantity == 0:
            self.order_status = OrderStatus.FILLED.name
        else:
            self.order_status = OrderStatus.PARTIAL.name
        self.save()

    def execute_order(self):
        if self.order_side == OrderSide.BUY.name:
            if self.order_type == OrderType.LIMIT.name:
                balance_to_lock = self.order_quantity * self.order_price
                self.lock_balance(balance_to_lock)
                counterparties = Order.objects.filter(order_ticker=self.order_ticker, order_price__lte=self.order_price, order_side=OrderSide.SELL.name, order_working_quantity__gt=0,
                                                      order_status__in=["OPEN", "PARTIAL"]
                                                      ).order_by("order_price", "order_modification_timestamp")
                print("counterparties found: ", len(counterparties))
            else:
                counterparties = Order.objects.filter(order_ticker=self.order_ticker, order_side=OrderSide.SELL.name, order_working_quantity__gt=0, 
                                                      order_status__in=["OPEN", "PARTIAL"]
                                                      ).order_by("order_price", "order_modification_timestamp")
                if len(counterparties) == 0:
                    exit
        else:
            if self.order_type == OrderType.LIMIT.name:
                balance_to_lock = self.order_quantity * (self.order_ticker.ticker_payout - self.order_price)
                self.lock_balance(balance_to_lock)
                counterparties = Order.objects.filter(order_ticker=self.order_ticker, order_price__gte=self.order_price, order_side=OrderSide.BUY.name, order_working_quantity__gt=0,
                                                      order_status__in=["OPEN", "PARTIAL"]
                                                      ).order_by("-order_price", "order_modification_timestamp")
            else:
                counterparties = Order.objects.filter(order_ticker=self.order_ticker, order_side=OrderSide.BUY.name, order_working_quantity__gt=0,
                                                      order_status__in=["OPEN", "PARTIAL"]
                                                      ).order_by("-order_price", "order_modification_timestamp")
                if len(counterparties) == 0:
                    exit

        remaining_quantity = self.order_quantity
        trades = []
        for counterparty in counterparties:
            if remaining_quantity <= 0:
                break
            trade_quantity = min(remaining_quantity, counterparty.order_working_quantity)
            trade_price = counterparty.order_price
            trade = Trade.objects.create(trade_buy=counterparty if self.order_side == OrderSide.SELL.name else self, 
                                         trade_sell=self if self.order_side == OrderSide.SELL.name else counterparty, 
                                         trade_quantity=trade_quantity, trade_price=trade_price, trade_ticker=self.order_ticker,
                                         trade_id=f"TRADE-{''.join(random.choices(string.ascii_letters + string.digits, k=16))}")
            trade.save()
            trades.append(trade)
            remaining_quantity -= trade_quantity

            user_fill = Fill.objects.create(fill_id = f"FILL-{''.join(random.choices(string.ascii_letters + string.digits, k=16))}",
                                            fill_user = self.order_user, fill_ticker=self.order_ticker,
                                            fill_quantity=trade_quantity, fill_side=self.order_side, 
                                            fill_price=trade_price, fill_timestamp=models.DateTimeField(auto_now_add=True), fill_order=self)
            user_fill.save()
            self.update_order(user_fill)
            counterparty_fill = Fill.objects.create(fill_id = f"FILL-{''.join(random.choices(string.ascii_letters + string.digits, k=16))}",
                                                    fill_user=counterparty.order_user, fill_ticker=counterparty.order_ticker,
                                                    fill_quantity=trade_quantity, fill_side=counterparty.order_side, 
                                                    fill_price=trade_price, fill_timestamp=models.DateTimeField(auto_now_add=True), fill_order=counterparty)
            counterparty.update_order(counterparty_fill)
        self.order_ticker.update_ticker_activity(trades)
        Position.update_positions(trades)

    def __str__(self):
        return f"{self.order_user}: {self.order_side} - {self.order_quantity} @ {self.order_price}"


class Fill(models.Model):
    fill_id = models.CharField(max_length=20)
    fill_user = models.ForeignKey(User, on_delete=models.CASCADE)
    fill_ticker = models.ForeignKey(Ticker, on_delete=models.CASCADE)
    fill_side = models.CharField(max_length=20, choices=[(s.name, s.value) for s in OrderSide])
    fill_quantity = models.PositiveIntegerField(default=0)
    fill_price = models.DecimalField(max_digits=10, decimal_places=2)
    fill_timestamp = models.DateTimeField(auto_now_add=True)
    fill_order = models.ForeignKey(Order, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.fill_id}-{self.fill_ticker.ticker_game}"


class Trade(models.Model):
    trade_id = models.CharField(max_length=20)
    trade_ticker = models.ForeignKey(Ticker, on_delete=models.CASCADE)
    trade_buy = models.ForeignKey(Order, related_name="buy_trades",on_delete=models.CASCADE)
    trade_sell = models.ForeignKey(Order, related_name="sell_trades", on_delete=models.CASCADE)
    trade_quantity = models.PositiveIntegerField()
    trade_price = models.DecimalField(max_digits=10, decimal_places=2)
    trade_timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.trade_ticker.ticker_id}-{self.trade_id}"
    

class Position(models.Model):
    position_user = models.ForeignKey(User, on_delete=models.CASCADE)
    position_ticker = models.ForeignKey(Ticker, on_delete=models.CASCADE)
    position_quantity = models.IntegerField(default=0)
    position_average_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    position_open_pnl = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    position_closed_pnl = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    position_settled_pnl = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    position_settled = models.BooleanField(default=False)


    @classmethod
    def update_positions(cls, trades: [Trade]):
        for trade in trades:
            buy = trade.trade_buy
            sell = trade.trade_sell

            print("buy", type(buy))
            print("sell", type(sell))

            # Update the positions for the buy user
            buy_position, buy_position_created = Position.objects.get_or_create(position_user=buy.order_user, position_ticker=buy.order_ticker)
            if buy_position_created or buy_position.position_quantity == 0:
                buy_position.position_average_price = trade.trade_price
            elif buy_position.position_quantity < 0:
                buy_position.position_closed_pnl += (buy_position.position_average_price - trade.trade_price) * trade.trade_quantity
                if buy_position.position_quantity + trade.trade_quantity == 0:
                    buy_position.position_average_price = 0
            else:
                buy_position.position_average_price = ((buy_position.position_average_price * buy_position.position_quantity) + (trade.trade_price * trade.trade_quantity)) / (buy_position.position_quantity + trade.trade_quantity)
            buy_position.position_quantity += trade.trade_quantity
            buy_position.position_open_pnl = (buy_position.position_average_price - trade.trade_ticker.ticker_last_price) * buy_position.position_quantity
            buy_position.save()

            # Update the positions for the sell user
            sell_position, sell_position_created = Position.objects.get_or_create(position_user=sell.order_user, position_ticker=sell.order_ticker)
            if sell_position_created or sell_position.position_quantity == 0:
                sell_position.position_average_price = trade.trade_price
            elif sell_position.position_quantity > 0:
                sell_position.position_closed_pnl += (trade.trade_price - sell_position.position_average_price) * trade.trade_quantity
                if sell_position.position_quantity - trade.trade_quantity == 0:
                    sell_position.position_average_price = 0
            else:
                sell_position.position_average_price = ((sell_position.position_average_price * sell_position.position_quantity) - (trade.trade_price * trade.trade_quantity)) / (sell_position.position_quantity - trade.trade_quantity)
            sell_position.position_quantity -= trade.trade_quantity
            sell_position.position_open_pnl = (trade.trade_ticker.ticker_last_price - sell_position.position_average_price) * sell_position.position_quantity
            sell_position.save()

        def __str__(self):
            return f"{self.position_user} {self.position_ticker.ticker_id}"