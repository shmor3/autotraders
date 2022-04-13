import os
import time
import pyotp
import robin_stocks.robinhood as r
from dotenv import load_dotenv

load_dotenv()
symb = os.environ['robin_symbol']
shareQuan = os.environ['trade_quantity']

def auth():
    totp = pyotp.TOTP(os.environ['robin_mfa']).now()
    login = r.login(os.environ['robin_username'],os.environ['robin_password'], store_session=False, mfa_code=totp)
    print('Login Successful')
    print('Current OTP:', totp)
    accountInfo0 = r.load_crypto_profile(info='user_id')
    accountInfo1 = r.load_account_profile(info='buying_power')
    equiHold0 = r.load_portfolio_profile(info='market_value')
    print('User Id:', accountInfo0)
    print('Buying Power:', accountInfo1)
    print('Position:', equiHold0)

def infoAll():
    priceSymb = r.get_crypto_quote(symb, info='symbol')
    priceAsk = r.get_crypto_quote(symb, info='ask_price')
    priceMark = r.get_crypto_quote(symb, info='mark_price')
    priceBid = r.get_crypto_quote(symb, info='bid_price')
    print('Quote:', priceSymb, '|', 'Bid', priceBid, '|', 'Mark', priceMark, '|', 'Ask', priceAsk)

def autoBLSH():
    if float(r.load_portfolio_profile(info='market_value')) == 0.00:
        if float(r.get_crypto_quote(symb, info='mark_price')) > 0.2905:
            r.order_sell_crypto_by_quantity(symb, shareQuan, timeInForce='gtc', jsonify=True)
            print('DODGE SOLD!')
        time.sleep(0.1)
        print('sellcycle')
        infoAll()
        autoBLSH()
    elif float(r.load_account_proficcle(info='buying_power')) > 5.00:
        if float(r.get_crypto_quote(symb, info='mark_price')) < 0.2303:
            r.order_buy_crypto_by_quantity(symb, shareQuan, timeInForce='gtc', jsonify=True)
            print('DODGE BOUGHT!')
            pass
        infoAll()
        time.sleep(0.1)
        print('buycycle')
        autoBLSH()
    else:
        time.sleep(0.2)
        infoAll()
        print('sleep')
        autoBLSH()
auth()
autoBLSH()