import requests
import json
import codecs
import sys, os
from tabulate import tabulate
from cryptography.fernet import Fernet


def encrypt(data, key):
    fernet = Fernet(key)
    return fernet.encrypt(data)


def decrypt(data, key):
    fernet = Fernet(key)
    return fernet.decrypt(data)


def gen_credentials(
    user,
    password,
    key=b"DJ4hV8Bzq_UVRqtKvHbVwwlr9zJDFAhVxro0S3tE4QM=",
    path="coki_credentials.txt",
):
    with open(path, "wb") as f:
        user = encrypt(str(user).encode(), key)
        password = encrypt(str(password).encode(), key)
        f.writelines([user, b"\n", password])


def read_credentials(
    key=b"DJ4hV8Bzq_UVRqtKvHbVwwlr9zJDFAhVxro0S3tE4QM=", path="coki_credentials.txt"
) -> (str, str):
    with open(path, "r", encoding="utf8") as f:
        user, password = f.readlines()
        user = user.strip()

    return decrypt(user, key).decode(), decrypt(password, key).decode()


def get_access_token(
    key=b"DJ4hV8Bzq_UVRqtKvHbVwwlr9zJDFAhVxro0S3tE4QM=",
    credentials_path="coki_credentials.txt",
) -> str:
    headers = {
        "authority": "api.cocos.capital",
        "apikey": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyAgCiAgICAicm9sZSI6ICJhbm9uIiwKICAgICJhdWRpZW5jZSI6ICJjb2NvcyIsCiAgICAiaXNzIjogInN1cGFiYXNlIiwKICAgICJpYXQiOiAxNjQxOTU2NDAwLAogICAgImV4cCI6IDM5NDgzNDE1MzEKfQ.Q5ZiL7KCUKP7iSM_LHWd3gffZ0k5Ce6CemOX9CUfEdM",
        "origin": "https://app.cocos.capital",
        "referer": "https://app.cocos.capital/",
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": "Windows",
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-site",
    }
    user, password = read_credentials(key, credentials_path)
    data = json.dumps({"email": user, "password": password})
    r = requests.post(
        "https://api.cocos.capital/auth/v1/token?grant_type=password",
        headers=headers,
        data=data,
    )
    s = r.content.decode("utf-8")
    with open("coki_token.txt", "w") as f:
        f.write(json.loads(s)["access_token"])
    return json.loads(s)["access_token"]


def parse_headers(token):
    headers = {
        "accept": "application/json, text/plain, */*",
        "accept-language": "es-ES,es;q=0.9",
        "authorization": f"Bearer {token}",
        "if-none-match": 'W/"42-WJmuy/h7CrOCewTOtVPh5zV6UTY"',
        "recaptcha-token": "undefined",
        "sec-ch-ua": '"Chromium";v="118", "Google Chrome";v="118", "Not=A?Brand";v="99"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"Windows"',
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-site",
        "x-account-id": "54107",
    }
    return headers


# Pasar autentificacion como archivo
def get_ticker_data(ticker: str, currency: str = "AUTO", plazo=48):
    plazo_conversion = {"48": "0003", "24": "0002", "CI": "0001", "C.I.": "0001"}
    liquidacion_str = plazo_conversion[str(plazo).upper()]

    if (
        currency == "AUTO"
    ):  # Si currency es auto, pasa a usd si termina en D o C (para casos como AMD, no va a andar auto, hay que poner currency ARS)
        if ticker[-1] in ["D", "C"]:
            currency = "USD"
            ticker = ticker[:-1]
        else:
            currency = "ARS"

    currency = "USD" if currency == "D" else currency
    species = "D" if currency == "USD" else ""
    link = f"https://api.cocos.capital/api/v1/markets/ticker/{ticker}{species}-{liquidacion_str}-C-CT-{currency}"

    if os.path.exists("coki_token.txt"):
        token = open("coki_token.txt", "r").read()
        r = requests.get(link, headers=parse_headers(token))
        if r.status_code == 200:
            j = r.json()
            if "bids" in j.keys():
                return j
    else:
        token = get_access_token()
        r = requests.get(link, headers=parse_headers(token))
        if r.status_code == 200:
            j = r.json()
            if "bids" in j.keys():
                return j
        else:
            print(r.content)
            raise Exception("Error en la consulta")


def gen_table(ticker: str, currency: str = "AUTO", plazo=48):
    data = get_ticker_data(ticker, currency, plazo)

    compra_size = []
    compra_price = []
    for row in data["bids"]:
        compra_size.append(row["size"])
        compra_price.append(row["price"])

    venta_size = []
    venta_price = []
    for row in data["asks"]:
        venta_size.append(row["size"])
        venta_price.append(row["price"])

    table = {
        "Cant. compra": compra_size,
        "Precio compra": compra_price,
        "": "",
        "Precio venta": venta_price,
        "Cant. venta": venta_size,
    }

    print(
        "\t", data["short_ticker"], "-", data["instrument_name"], "-", data["currency"]
    )
    print(
        "\t",
        f'Last: {data["last"]:,} - High: {data["high"]:,} - Low: {data["low"]:,} - Volume: {data["volume"]:,}',
    )

    print(
        tabulate(
            table,
            headers="keys",
            tablefmt="rounded_outline",
            floatfmt=".2f",
            stralign="center",
        )
    )
