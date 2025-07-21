import os
import requests
from dotenv import load_dotenv

load_dotenv()

ETHERSCAN_API_KEY = os.getenv("ETHERSCAN_API_KEY")
TOKEN_ADDRESS = os.getenv("TOKEN_ADDRESS")
ETHERSCAN_URL = "https://api.etherscan.io/api"

def get_token_info():
    params = {
        "module": "token",
        "action": "tokeninfo",
        "contractaddress": TOKEN_ADDRESS,
        "apikey": ETHERSCAN_API_KEY
    }
    r = requests.get(ETHERSCAN_URL, params=params)
    return r.json()

def get_holders():
    params = {
        "module": "token",
        "action": "tokenholderlist",
        "contractaddress": TOKEN_ADDRESS,
        "apikey": ETHERSCAN_API_KEY
    }
    r = requests.get(ETHERSCAN_URL, params=params)
    return r.json()

def analyze_token():
    print(f"🕵️ Analyzing token: {TOKEN_ADDRESS}")
    # Heuristic 1: Top holder control
    holders = get_holders()
    if holders.get("status") != "1":
        print("⚠️ Could not fetch holders info.")
        return

    items = holders.get("result", [])
    total_top_10 = 0
    for i in range(min(10, len(items))):
        total_top_10 += float(items[i]['TokenHolderQuantity'])

    print(f"Top 10 holders control: {total_top_10:,.0f} tokens")
    if total_top_10 > 0.9e9:
        print("🚨 Warning: Top holders control a suspiciously large amount!")

    print("✅ RugPullRadar analysis completed.")

if __name__ == "__main__":
    analyze_token()
