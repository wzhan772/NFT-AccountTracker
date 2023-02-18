#import libraries
from requests import get
from datetime import datetime

#registered API key
#NOTE: yours will be different
API_KEY = "EJFNJARWMRG3RQQ1M62R6Z327VBKARUXPP"
ETHER_VALUE = 10 ** 18
BASE_URL = "https://api.etherscan.io/api"

def make_api_url(module, action, address, **kwargs):
    url = BASE_URL + f"?module={module}&action={action}&address={address}&apikey={API_KEY}"
    for key, value in kwargs.items():
        url += f"&{key}={value}"

    return url

#if you want to get the account balance
def get_account_balance(address):
    get_balance_url = make_api_url("account", "balance", address, tag="latest")
    response = get(get_balance_url)
    data = response.json()
    value = (int(data["result"]) / ETHER_VALUE)
    return value

#if you want to get the transactions of an account
def get_transactions(address):
    #offset shows the number of tx in the output, sorting by asc is by latest date
    get_transactions_url = make_api_url("account", "txlist", address, startblock=0, endblock=99999999, page=1, offset=10, sort="asc")
    response = get(get_transactions_url)
    data = response.json()["result"]
    #goes through each transaction feature and converts them accordingly
    for tx in data:
        to = tx["to"]
        from_addr = tx["from"]
        value = int(tx["value"]) / ETHER_VALUE
        #convert from wei to eth
        gas = int(tx["gasUsed"]) * int(tx["gasPrice"]) / ETHER_VALUE
        time = datetime.fromtimestamp(int(tx["timeStamp"]))
        print("----------------------------------")
        print("To:", to)
        print("From:", from_addr)
        print("Value", value)
        print("Gas Cost", gas)
        print("Time", time)

#here you would enter the address that you want to get the transactions for
address = "0x2a93E999816c9826aDe0B51AAa2d83240d8F4596"
#finally call the function
get_transactions(address)
