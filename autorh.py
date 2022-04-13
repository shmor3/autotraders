import os
import time
import pyotp
import robin_stocks.robinhood as r
from dotenv import load_dotenv

load_dotenv()
localtime = time.asctime( time.localtime(time.time()) )

def auth():
    totp = pyotp.TOTP(os.environ['robin_mfa']).now()
    r.login(os.environ['robin_username'],os.environ['robin_password'], store_session=False, mfa_code=totp)
    accountInfo0 = r.load_crypto_profile(info='user_id')
    accountInfo1 = r.load_account_profile(info='buying_power')
    print('User Id:', accountInfo0)
    print(localtime)
    print('Current OTP:', totp)
    print('Buying Power:', accountInfo1)

auth()

symb = os.environ['robin_symbol']
tokenQuan = os.environ['trade_quantity']
sLimitPrice = 1.16
bLimitPrice = 1.16

def tradeInfo():
    priceSymb = r.get_crypto_quote(symb, info='symbol')
    priceAsk = float(r.get_crypto_quote(symb, info='ask_price'))
    priceMark = float(r.get_crypto_quote(symb, info='mark_price'))
    priceBid = float(r.get_crypto_quote(symb, info='bid_price'))
    print('Quote:', priceSymb, '|', 'Bid', priceBid, '|', 'Mark', priceMark, '|', 'Ask', priceAsk)
tradeInfo()

def limitBuy():
    r.order_buy_crypto_limit(symb, tokenQuan, bLimitPrice, timeInForce='gtc', jsonify=True)
    tradeInfo()
    print('~ buy order sent', '|', localtime, '|', 'limit:', bLimitPrice, '~')
def limitSell():
    r.order_sell_crypto_limit(symb, tokenQuan, sLimitPrice, timeInForce='gtc', jsonify=True)
    tradeInfo()
    print('~ sell order sent', '|', localtime, '|', 'limit:', sLimitPrice, '~')

def autoTrade():
    if 1 > 0.001:
        if 1 < 0.001:
            limitBuy()
            time.sleep(0.05)
            autoTrade()
        elif 1 > -0.001:
            limitSell()
            time.sleep(0.05)
            autoTrade()
        else:
            time.sleep(0.2)
            print("...")
            autoTrade()
    else:
        pass

autoTrade()