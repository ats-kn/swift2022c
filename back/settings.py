import os
from os.path import join, dirname
from dotenv import load_dotenv

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

#Twitter Instagramの両方に必要
#Firebase adminを使うのに必要なやつ
CRED_JSON = os.environ.get("CRED_JSON")
DATABASE_URL = os.environ.get("DATABASE_URL")


#Twitter専用のキー

#API_KEY
API_KEY0 = os.environ.get("API_KEY0")
API_KEY1 = os.environ.get("API_KEY1")
API_KEY2 = os.environ.get("API_KEY2")
API_KEY3 = os.environ.get("API_KEY3")
API_KEY4 = os.environ.get("API_KEY4")
API_KEY5 = os.environ.get("API_KEY5")

#API_KEY_SECRET
API_KEY_SECRET0 = os.environ.get("API_KEY_SECRET0")
API_KEY_SECRET1 = os.environ.get("API_KEY_SECRET1")
API_KEY_SECRET2 = os.environ.get("API_KEY_SECRET2")
API_KEY_SECRET3 = os.environ.get("API_KEY_SECRET3")
API_KEY_SECRET4 = os.environ.get("API_KEY_SECRET4")
API_KEY_SECRET5 = os.environ.get("API_KEY_SECRET5")

#ACCESS_TOKEN
ACCESS_TOKEN0 = os.environ.get("ACCESS_TOKEN0")
ACCESS_TOKEN1 = os.environ.get("ACCESS_TOKEN1")
ACCESS_TOKEN2 = os.environ.get("ACCESS_TOKEN2")
ACCESS_TOKEN3 = os.environ.get("ACCESS_TOKEN3")
ACCESS_TOKEN4 = os.environ.get("ACCESS_TOKEN4")
ACCESS_TOKEN5 = os.environ.get("ACCESS_TOKEN5")

#ACCESS_TOKEN_SECRET
ACCESS_TOKEN_SECRET0 = os.environ.get("ACCESS_TOKEN_SECRET0")
ACCESS_TOKEN_SECRET1 = os.environ.get("ACCESS_TOKEN_SECRET1")
ACCESS_TOKEN_SECRET2 = os.environ.get("ACCESS_TOKEN_SECRET2")
ACCESS_TOKEN_SECRET3 = os.environ.get("ACCESS_TOKEN_SECRET3")
ACCESS_TOKEN_SECRET4 = os.environ.get("ACCESS_TOKEN_SECRET4")
ACCESS_TOKEN_SECRET5 = os.environ.get("ACCESS_TOKEN_SECRET5")

#BEARER_TOKEN
BEARER_TOKEN0 = os.environ.get("BEARER_TOKEN0")
BEARER_TOKEN1 = os.environ.get("BEARER_TOKEN1")
BEARER_TOKEN2 = os.environ.get("BEARER_TOKEN2")
BEARER_TOKEN3 = os.environ.get("BEARER_TOKEN3")
BEARER_TOKEN4 = os.environ.get("BEARER_TOKEN4")
BEARER_TOKEN5 = os.environ.get("BEARER_TOKEN5")

#投稿除外用のキーワード
exclude_keyword_place = os.environ.get("exclude_keywords_place")
exclude_keyword_r18 = os.environ.get("exclude_keywords_r18")
exclude_keyword_other = os.environ.get("exclude_keywords_other")


#アクセストークン
access_token = os.environ.get("access_token")

#アプリID
app_id = os.environ.get("app_id")

#アプリシークレット
app_secret = os.environ.get("app_secret")

#インスタグラムビジネスアカウントID
instagram_account_id = os.environ.get("instagram_account_id")

