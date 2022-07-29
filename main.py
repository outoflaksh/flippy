from datetime import timedelta
from pprint import pprint
import requests, os, redis, json
from bs4 import BeautifulSoup
from dotenv import load_dotenv

load_dotenv()


def get_product_details(PRODUCT_URL: str):
    try:
        response = requests.get(url=PRODUCT_URL)
    except:
        raise Exception("Could not complete request on the requested url")

    if response.status_code == 200:
        print(f"Request hit successful on url: {PRODUCT_URL[:30]}...\n")

        soup = BeautifulSoup(response.content, "html.parser")
        product_name = soup.find("span", {"class": "B_NuCI"}).text
        product_img = soup.find("img", {"class": "_396cs4"})["src"]
        product_price = soup.find("div", {"class": "_30jeq3 _16Jk6d"}).text
        search_q = soup.find_all("td", {"class": "col-9-12"})[2].text

        return {
            "name": product_name,
            "img": product_img,
            "price": product_price,
            "search_term": search_q,
        }
    else:
        raise Exception("Unsuccessful request hit: " + response.status_code)


def analyze_sentiment(q):
    import requests

    url = "https://text-analysis12.p.rapidapi.com/sentiment-analysis/api/v1.1"

    payload = {
        "language": "english",
        "text": q,
    }
    headers = {
        "content-type": "application/json",
        "X-RapidAPI-Key": os.environ.get("RAPID_API_KEY"),
        "X-RapidAPI-Host": "text-analysis12.p.rapidapi.com",
    }

    response = requests.request("POST", url, json=payload, headers=headers).json()

    if response["ok"] is True:
        return response["sentiment"]
    else:
        print(response["msg"])


def get_tweets(q):
    redis_client = redis.Redis(host="localhost", port=6379, db=0)
    key = q[:2] + "-tweets"
    if redis_client.get(key):
        return json.loads(redis_client.get(key))

    url = "https://twitter-scraper2.p.rapidapi.com/api/v2/search"

    querystring = {
        "allOfTheseWords": q,
        "theseHashTags": "#review",
        "lang": "en",
        "searchMode": "top",
    }

    headers = {
        "X-RapidAPI-Key": os.environ.get("RAPID_API_KEY"),
        "X-RapidAPI-Host": "twitter-scraper2.p.rapidapi.com",
    }

    response = requests.request("GET", url, headers=headers, params=querystring)

    if response.status_code == 200:
        tweet_texts = [r["tweet"]["full_text"] for r in response.json()["data"]]

        redis_client.set(key, json.dumps(tweet_texts))
        redis_client.expire(key, timedelta(minutes=20))

        return tweet_texts
    else:
        raise Exception("error")


PRODUCT_URLS = [
    "https://www.flipkart.com/nothing-phone-1-black-128-gb/p/itmeea53a564de47?pid=MOBGCYGPFEGDMYQR&lid=LSTMOBGCYGPFEGDMYQROW9GCT&marketplace=FLIPKART&sattr[]=color&sattr[]=storage&sattr[]=ram&st=storage",
    "https://www.flipkart.com/quiet/p/itmfc4vdg6rrpqcc?pid=9780141029191&lid=LSTBOK9780141029191ZY8WGA&marketplace=FLIPKART&fm=factBasedRecommendation%2FrecentlyViewed&iid=R%3Arv%3Bpt%3App%3Buid%3A7121f3e8-08b0-11ed-8a17-872e8f2be35a%3B.9780141029191&ppt=pp&ppn=pp&ssid=uo912786cvr5hq801658378872174&otracker=pp_reco_Recently%2BViewed_5_37.productCard.RECENTLY_VIEWED_Quiet_9780141029191_factBasedRecommendation%2FrecentlyViewed_4&otracker1=pp_reco_PINNED_factBasedRecommendation%2FrecentlyViewed_Recently%2BViewed_DESKTOP_HORIZONTAL_productCard_cc_5_NA_view-all&cid=9780141029191",
    "https://www.flipkart.com/croma-10000-mah-power-bank/p/itm82c84993253ba?pid=PWBGDM5BRCYZRC8N&lid=LSTPWBGDM5BRCYZRC8N7TNX3U&marketplace=FLIPKART&fm=factBasedRecommendation%2FrecentlyViewed&iid=R%3Arv%3Bpt%3App%3Buid%3A7121f3e8-08b0-11ed-8a17-872e8f2be35a%3B.PWBGDM5BRCYZRC8N&ppt=pp&ppn=pp&ssid=uo912786cvr5hq801658378872174&otracker=pp_reco_Recently%2BViewed_4_37.productCard.RECENTLY_VIEWED_Croma%2B10000%2BmAh%2BPower%2BBank_PWBGDM5BRCYZRC8N_factBasedRecommendation%2FrecentlyViewed_3&otracker1=pp_reco_PINNED_factBasedRecommendation%2FrecentlyViewed_Recently%2BViewed_DESKTOP_HORIZONTAL_productCard_cc_4_NA_view-all&cid=PWBGDM5BRCYZRC8N",
    "https://www.flipkart.com/google-pixel-6a-charcoal-128-gb/p/itme5ae89135d44e?pid=MOBGFKX5YUXD74Z3&lid=LSTMOBGFKX5YUXD74Z3MXA2OB",
]

PRODUCT_URL = "https://www.flipkart.com/apple-iphone-13-pro-max-alpine-green-512-gb/p/itme5529c8267abe?pid=MOBGC9VGHZAHZH6H&lid=LSTMOBGC9VGHZAHZH6HCLMPD7&marketplace=FLIPKART&fm=personalisedRecommendation%2Fp2p-same&iid=R%3As%3Bp%3AMOBGDWFEAHHTW8CF%3Bpt%3Ahp%3Buid%3A40eb2592-0f0c-11ed-a8d9-517e9f364fe2%3B.MOBGC9VGHZAHZH6H&ppt=pp&ppn=pp&ssid=l7xvib0jtoje7eo01659077609209&otracker=hp_reco_You%2BMay%2BLike..._5_7.productCard.PMU_V2_APPLE%2BiPhone%2B13%2BPro%2BMax%2B%2528Alpine%2BGreen%252C%2B512%2BGB%2529_MOBGC9VGHZAHZH6H_personalisedRecommendation%2Fp2p-same_4&otracker1=hp_reco_WHITELISTED_personalisedRecommendation%2Fp2p-same_You%2BMay%2BLike..._DESKTOP_HORIZONTAL_productCard_cc_5_NA_view-all&cid=MOBGC9VGHZAHZH6H"
print(get_product_details(PRODUCT_URL))
# prod_name = get_product_name(PRODUCT_URL)

# print("Scraped product name:", " ".join(prod_name.split(" ")[:3]))

# tweets = get_tweets(prod_name)

# print("Tweets scraped")
# score = 0

# grades = {"negative": 0, "neutral": 0, "positive": 0}

# print("Running analysis...")
# for t in tweets[:15]:
#     sent = analyze_sentiment(t)
#     grades[sent] += 1

# print("Score: ", grades)

# max_score = max(grades.values())
# print("Net result:")
# for i in grades:
#     if grades[i] == max_score:
#         print(i)
