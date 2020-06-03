BRAVO_POKER_EMAIL = "BRAVO POKER EMAIL"            # Enter your Bravo Poker email
BRAVO_POKER_PASSWORD = "BRAVO POKER PASSWORD"      # Enter your Bravo Poker passw
SENDER_EMAIL = "YOUR EMAIL ADDRESS"                # Enter your email address
EMAIL_PASSWORD = "YOUR EMAIL PASSWORD"             # Enter your email pass
RECEIVER_EMAIL = "DESIRED RECEIVER EMAIL ADDRESS"  # Enter receiver email address


import time
import requests
import smtplib
import ssl
import pandas as pd


def send_email(subject, body):
    port = 465  # For SSL
    smtp_server = "smtp.gmail.com"
    message = 'Subject: {}\n\n{}'.format(subject, body)
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
        server.login(SENDER_EMAIL, EMAIL_PASSWORD)
        server.sendmail(SENDER_EMAIL, RECEIVER_EMAIL, message)


# log into Bravo Live Poker website and get html
login_page_url = r"https://www.bravopokerlive.com/login/?ReturnUrl=%2fvenues%2fseminole-hard-rock-tampa%2f"
tampa_page_url = r"https://www.bravopokerlive.com/venues/seminole-hard-rock-tampa/"
session = requests.Session()
payload = {'Email': BRAVO_POKER_EMAIL, 'Password': BRAVO_POKER_PASSWORD}
session.post(login_page_url, data=payload)
html = session.get(tampa_page_url).text

# convert tables in html into dataframes
tables = pd.read_html(html)
active_games = tables[0]
waiting_list = tables[1]

# Send an email if a 1-2 PLO game is running
if '1-2 PLO' in active_games:
    # number of PLO games running
    n_games = active_games.loc[active_games['Current Live Games'] == '1-2 PLO']['# of Tables'].values
    send_email(
        subject=f"{n_games} 1-2 PLO Currently Running",
        body=f"There are {n_games} 1-2 PLO game currently running."
        )