from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.expected_conditions import url_changes
from kiteconnect import KiteConnect
from time import sleep
from functools import partial
import pyotp
import pandas as pd
from datetime import datetime, timedelta, time
from volstreet.utils import current_time
from volstreet.dealingroom import get_index_constituents


def get_greenlit_kite(
    kite_api_key,
    kite_api_secret,
    kite_user_id,
    kite_password,
    kite_auth_key,
    chrome_path=None,
):
    if chrome_path is None:
        driver = webdriver.Chrome()
    else:
        driver = webdriver.Chrome(chrome_path)

    authkey_obj = pyotp.TOTP(kite_auth_key)
    kite = KiteConnect(api_key=kite_api_key)
    login_url = kite.login_url()

    driver.get(login_url)
    wait = WebDriverWait(driver, 10)  # waits for up to 10 seconds

    userid = wait.until(EC.presence_of_element_located((By.ID, "userid")))
    userid.send_keys(kite_user_id)

    password = wait.until(EC.presence_of_element_located((By.ID, "password")))
    password.send_keys(kite_password)

    submit = wait.until(
        EC.presence_of_element_located((By.CLASS_NAME, "button-orange"))
    )
    submit.click()

    sleep(10)  # wait for the OTP input field to be clickable
    otp_input = wait.until(EC.element_to_be_clickable((By.TAG_NAME, "input")))
    otp_input.send_keys(authkey_obj.now())

    # wait until the URL changes
    wait.until(url_changes(driver.current_url))

    # now you can safely get the current URL
    current_url = driver.current_url

    split_url = current_url.split("=")
    request_token = None
    for i, string in enumerate(split_url):
        if "request_token" in string:
            request_token = split_url[i + 1]
            request_token = (
                request_token.split("&")[0] if "&" in request_token else request_token
            )
            break

    driver.quit()

    if request_token is None:
        raise Exception("Request token not found")

    data = kite.generate_session(request_token, api_secret=kite_api_secret)
    kite.set_access_token(data["access_token"])

    return kite


def get_1m_data(kite, symbol, path="C:\\Users\\Administrator\\"):
    def fetch_minute_data_from_kite(_kite, _token, _from_date, _to_date):
        date_format = "%Y-%m-%d %H:%M:%S"
        _prices = _kite.historical_data(
            _token,
            from_date=_from_date.strftime(date_format),
            to_date=_to_date.strftime(date_format),
            interval="minute",
        )
        return _prices

    instruments = kite.instruments(exchange="NSE")
    token = [
        instrument["instrument_token"]
        for instrument in instruments
        if instrument["tradingsymbol"] == symbol
    ][0]

    try:
        main_df = pd.read_csv(
            f"{path}{symbol}_onemin_prices.csv", index_col=0, parse_dates=True
        )
        from_date = main_df.index[-1] + timedelta(minutes=1)
    except FileNotFoundError:
        print(f"No existing data for {symbol}, starting from scratch.")
        main_df = False
        from_date = datetime(2015, 1, 1, 9, 16)

    end_date = current_time()
    mainlist = []

    fetch_data_partial = partial(fetch_minute_data_from_kite, kite, token)

    default_time_delta_days = 34
    while from_date < end_date:
        to_date = from_date + timedelta(days=default_time_delta_days)
        prices = fetch_data_partial(from_date, to_date)
        if (
            len(prices) < 2 and not mainlist
        ):  # if there is no data for the period and no data at all
            print(
                f'No data for {from_date.strftime("%Y-%m-%d %H:%M:%S")} to {to_date.strftime("%Y-%m-%d %H:%M:%S")}'
            )
            if to_date > current_time():
                return None
            else:
                from_date += timedelta(days=default_time_delta_days)
                continue
        else:  # if there is data for the period
            mainlist.extend(prices)
            from_date += timedelta(days=default_time_delta_days)

    df = pd.DataFrame(mainlist).set_index("date")
    df.index = df.index.tz_localize(None)
    df = df[~df.index.duplicated(keep="first")]
    df = df[(df.index.time >= time(9, 15)) & (df.index.time <= time(15, 30))]
    df.to_csv(
        f"{path}{symbol}_onemin_prices.csv",
        mode="a",
        header=not isinstance(main_df, pd.DataFrame),
    )
    print(
        f"Finished fetching data for {symbol}. Fetched data from {df.index[0]} to {df.index[-1]}"
    )
    full_df = pd.concat([main_df, df]) if isinstance(main_df, pd.DataFrame) else df
    return full_df


def get_constituent_1m_data(kite_object, index_name, path="C:\\Users\\Administrator\\"):
    tickers, _weights = get_index_constituents(index_name)
    for ticker in tickers:
        print(f"Fetching data for {ticker}")
        get_1m_data(kite_object, ticker, path=path)
