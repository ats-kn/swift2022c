
import tweepy
from pprint import pprint
from datetime import datetime, timezone, timedelta
import pytz

# setting.pyからインポート
import settings

# firebaseをPythonで使うためにインポートするライブラリ(ここらへんはサイト見た)
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db

cred = credentials.Certificate(
    settings.CRED_JSON)  # 自分専用のやつ

firebase_admin.initialize_app(cred, {
    'databaseURL': settings.DATABASE_URL,  # 自分のデータベースのURL
    'databaseAuthVariableOverride': {
        'uid': 'my-service-worker'
    }
})

#APIキーの配列  格納の順番=> [キーワード検索用API,         (あつしのAPIキー)
                                            # 知る用API,                      (じょざのAPIキー)
                                            # 食べるカテゴリ用API,       (じょざのAPIキー)
                                            # ニュースカテゴリ用API,    (じょざのAPIキー)（使ってない）
                                            # 温泉カテゴリ用API,          (じょざのAPIキー)（使ってない）
                                            # 見るカテゴリ用API]          (じょざのAPIキー)


API_KEY = [settings.API_KEY0,
                settings.API_KEY1,
                settings.API_KEY2,
                settings.API_KEY3,
                settings.API_KEY4,
                settings.API_KEY5,
                ]
API_KEY_SECRET = [settings.API_KEY_SECRET0,
                                settings.API_KEY_SECRET1,
                                settings.API_KEY_SECRET2,
                                settings.API_KEY_SECRET3,
                                settings.API_KEY_SECRET4,
                                settings.API_KEY_SECRET5,
                            ]
ACCESS_TOKEN = [settings.ACCESS_TOKEN0,
                            settings.ACCESS_TOKEN1,
                            settings.ACCESS_TOKEN2,
                            settings.ACCESS_TOKEN3,
                            settings.ACCESS_TOKEN4,
                            settings.ACCESS_TOKEN5,
                            ]
ACCESS_TOKEN_SECRET = [settings.ACCESS_TOKEN_SECRET0,
                                        settings.ACCESS_TOKEN_SECRET1,
                                        settings.ACCESS_TOKEN_SECRET2,
                                        settings.ACCESS_TOKEN_SECRET3,
                                        settings.ACCESS_TOKEN_SECRET4,
                                        settings.ACCESS_TOKEN_SECRET5,
                                        ]
BEARER_TOKEN = [settings.BEARER_TOKEN0,
                            settings.BEARER_TOKEN1,
                            settings.BEARER_TOKEN2,
                            settings.BEARER_TOKEN3,
                            settings.BEARER_TOKEN4,
                            settings.BEARER_TOKEN5,
                            ]

#秒数を年月日で返す関数
def getTime(seconds):
    JST = timezone(timedelta(hours=+9), 'JST')
    time = datetime.fromtimestamp(seconds, JST)
    year_month_day_hour_minutes = str(time).split(' ')
    year_month_day = str(year_month_day_hour_minutes[0]).split('-')
    hour_minutes = str(year_month_day_hour_minutes[1]).split(':')
    # print(year_month_day[0])
    # print(year_month_day[1])
    # print(year_month_day[2])
    # print(hour_minutes[0])
    result = year_month_day[0] + '年' + str(int(year_month_day[1])) + '月' + str(int(year_month_day[2])) + '日' + ' ' + str(int(hour_minutes[0]))  + '時' +str(int(hour_minutes[1])) + '分'
    return result

#関数:　UTCをJSTに変換する
def change_time_JST(u_time):
    #イギリスのtimezoneを設定するために再定義する
    utc_time = datetime(u_time.year, u_time.month,u_time.day, \
    u_time.hour,u_time.minute,u_time.second, tzinfo=timezone.utc)
    #タイムゾーンを日本時刻に変換
    jst_time = utc_time.astimezone(pytz.timezone("Asia/Tokyo"))
    # 文字列で返す
    str_time = jst_time.strftime("%Y-%m-%d_%H:%M:%S")
    return str_time


#クライアント情報をclientに格納する関数
def ClientInfo():
    client = ['', '', '', '', '', '']
    for i in range(len(client)):
        client[i] = tweepy.Client(
                                consumer_key=API_KEY[i],
                                consumer_secret=API_KEY_SECRET[i],
                                access_token=ACCESS_TOKEN[i],
                                access_token_secret=ACCESS_TOKEN_SECRET[i],
                                bearer_token=BEARER_TOKEN[i],
                                )
    return client

# 実際にデータベースにデータを保存する関数
def SaveToDatabase(tweets, tweets_data, data_label):
    if tweets_data != None:  # tweets_dataにうまくデータが入った場合
        for tweet in tweets_data:
            # databaseにデータを追加する
            try:
                if tweet.attachments is not None:  #そのツイートに画像があるか（リンクのみだった時も除外しちゃうので一旦保留）
                    if tweet.source != "twittbot.net" and tweet.source != "TravelRaku" and tweet.source != "rt_10" :  #ここでBOTを除外する
                        for i in range(len(tweets.includes['users'])):
                            if tweet.author_id == tweets.includes['users'][i]['id']:
                                if tweets.includes['users'][i]['username'] != "ri_Zu_n_" and tweets.includes['users'][i]['username'] != "KY1225kataware" and tweets.includes['users'][i]['username'] != "Miyabi207Vzs72" and  tweets.includes['users'][i]['username'] != "bonzu207" and tweets.includes['users'][i]['username'] != "flan_staff":
                                    ref.child(str(tweet.id)).set({  # キーはツイートID
                                        'data_label' : data_label,                                    
                                        'date': -(tweet.created_at.timestamp()),  #float型（確認済み）
                                        'date2': change_time_JST(tweet.created_at),
                                        'date3': getTime(tweet.created_at.timestamp()),
                                        # 投稿日  ISO 8601形式の投稿日時をUNIX時間に変換した。（投稿日時を秒数に変換）
                                        'text': tweet.text.split('https://t.co/')[0],  # 投稿文
                                        'link': 'https://twitter.com/twitter/status/' + str(tweet.id),  #投稿リンク
                                        'good': tweet.public_metrics['like_count'],  #いいね数
                                        'source': tweet.source,
                                        'user': tweets.includes['users'][i]['name'],  #ユーザ名
                                        'username': tweets.includes['users'][i]['username'],   #ユーザ名(@のやつ)
                                        'profile_image_url': tweets.includes['users'][i]['profile_image_url'],   #プロフィール画像
                                        'SNS_type': 'Twitter'
                                    })
                                    break
                        media_ref = db.reference('/' + Key + '/' + str(tweet.id)).child('media')
                        roop_count = 0 #その投稿のメディアの数に合わせたループ回数を保存する変数？
                        for i in range(len(tweets.includes['media'])):  #取得してきたツイート10件に格納されたメディアのurlの数
                            if roop_count == len(tweet.attachments['media_keys']) :  #その投稿に格納する画像や動画がなくなったら次の投稿へ
                                break                            
                            for j in range(len(tweet.attachments['media_keys'])): #ツイートに格納されてあるメディアのurlの数
                                if tweets.includes['media'][i]['media_key'] == tweet.attachments['media_keys'][j]: #メディアのキーが同じだったら...
                                    if tweets.includes['media'][i]['type'] == 'photo' :
                                        media_ref.child('url' + str(j)).set({
                                            'media_type': tweets.includes['media'][i]['type'], #メディアの種類
                                            'media_url': tweets.includes['media'][i]['url']  #urlをDBに格納！全てのurlを格納できる！
                                        })
                                        roop_count += 1   #画像情報を格納出来たら、roopcountに+1して、その投稿の次のメディアを探す
                                    else :
                                        for k in range(4) :                                            
                                            if (tweets.includes['media'][i]['variants'][k]['content_type'] == 'video/mp4') :                                                        
                                                media_ref.child('url' + str(j)).set({
                                                    'media_type': tweets.includes['media'][i]['type'], #メディアの種類
                                                    'media_url': tweets.includes['media'][i]['variants'][k]['url']  #urlをDBに格納！全てのurlを格納できる！
                                                })
                                                roop_count += 1
                                                break  #video/mp4タイプの動画を一つでも格納出来たら、roop_countに+1して、その投稿の次のメディアを探す
                                        
            except:
                pass
        return 'done!'
    
    else:  # tweets_dataにうまくデータが入らなかった場合
        return 'fail!'

# 「函館」のテキストが含まれる投稿を最新順で取得してくる関数
def SearchTweets(search, tweet_max, client):
    # 直近のツイート取得
    tweets = client.search_recent_tweets(
        query=search,
        max_results=tweet_max,
        tweet_fields=['created_at', 'public_metrics', 'source'],
        user_fields=['profile_image_url', 'username', 'entities'],
        expansions=['author_id', 'attachments.media_keys'],
        media_fields=['url', 'variants'],
    )

    # 取得したデータ加工
    tweets_data = tweets.data

    return SaveToDatabase(tweets, tweets_data, 'Search')




# 知るカテゴリ用アカウントのタイムラインの投稿をデータベースに保存する
def GetKnowTimeLine(tweet_max, client):
    # 直近のツイート取得
    tweets = client.get_home_timeline(
        max_results=tweet_max,
        tweet_fields=['created_at', 'public_metrics', 'source'],
        user_fields=['profile_image_url', 'username', 'entities'],
        expansions=['author_id', 'attachments.media_keys'],
        media_fields=['url', 'variants'],
        exclude = ['retweets', 'replies'] #リツイート リプライを省く
    )

    # 取得したデータ加工
    tweets_data = tweets.data

    return SaveToDatabase(tweets, tweets_data, 'KnowTimeLine')



# 食べるカテゴリ用アカウントのタイムラインの投稿をデータベースに保存する
def GetEatTimeLine(tweet_max, client):
    # 直近のツイート取得
    tweets = client.get_home_timeline(
        max_results=tweet_max,
        tweet_fields=['created_at', 'public_metrics', 'source'],
        user_fields=['profile_image_url', 'username', 'entities'],
        expansions=['author_id', 'attachments.media_keys'],
        media_fields=['url', 'variants'],
        exclude = ['retweets', 'replies'] #リツイート リプライを省く
    )

    # 取得したデータ加工
    tweets_data = tweets.data

    return SaveToDatabase(tweets, tweets_data, 'EatTimeLine')


# 使わない
# # ニュースカテゴリ用アカウントのタイムラインの投稿をデータベースに保存する
# def GetNewsTimeLine(tweet_max, client):
#     # 直近のツイート取得
#     tweets = client.get_home_timeline(
#         max_results=tweet_max,
#         tweet_fields=['created_at', 'public_metrics', 'source'],
#         user_fields=['profile_image_url', 'username', 'entities'],
#         expansions=['author_id', 'attachments.media_keys'],
#         media_fields=['url', 'variants'],
#         exclude = ['retweets', 'replies'] #リツイート リプライを省く
#     )

#     # 取得したデータ加工
#     tweets_data = tweets.data

#     return SaveToDatabase(tweets, tweets_data, 'NewsTimeLine')



# 使わない
# # 温泉カテゴリ用アカウントのタイムラインの投稿をデータベースに保存する
# def GetSpaTimeLine(tweet_max, client):
#     # 直近のツイート取得
#     tweets = client.get_home_timeline(
#         max_results=tweet_max,
#         tweet_fields=['created_at', 'public_metrics', 'source'],
#         user_fields=['profile_image_url', 'username', 'entities'],
#         expansions=['author_id', 'attachments.media_keys'],
#         media_fields=['url', 'variants'],
#         exclude = ['retweets', 'replies'] #リツイート リプライを省く
#     )

#     # 取得したデータ加工
#     tweets_data = tweets.data

#     return SaveToDatabase(tweets, tweets_data, 'SpaTimeLine')



# 見るカテゴリ用アカウントのタイムラインの投稿をデータベースに保存する
def GetSeeTimeLine(tweet_max, client):
    # 直近のツイート取得
    tweets = client.get_home_timeline(
        max_results=tweet_max,
        tweet_fields=['created_at', 'public_metrics', 'source'],
        user_fields=['profile_image_url', 'username', 'entities'],
        expansions=['author_id', 'attachments.media_keys'],
        media_fields=['url', 'variants'],
        exclude = ['retweets', 'replies'] #リツイート リプライを省く
    )

    # 取得したデータ加工
    tweets_data = tweets.data

    return SaveToDatabase(tweets, tweets_data, 'SeeTimeLine')





# 以下実行するコード




# databaseに初期データを追加する(1回初期データを追加すれば2回目以降は参照)
Key = 'SNS_data'              #Keyに格納したいキー名を指定する。　ここだけ必要に応じて書き換える必要がある。
ref = db.reference(Key)     #キー名のパスにアクセス
tweet_max = 10               # 取得したいツイート数(10〜100で設定可能)
client = ClientInfo()           #clientという配列にクライアント情報（トークン等）を格納

add_func = " -is:retweet -is:reply -is:quote has:media"
place = settings.exclude_keyword_place
r_18 = settings.exclude_keyword_r18
other = settings.exclude_keyword_other
# 検索対象（リツイート除外, 返信除外, 画像付きの投稿に絞る）

search = "函館" + add_func + place + r_18 + other


#「函館」のテキストが含まれる投稿を最新順で取得してくる関数を実行
pprint(SearchTweets(search, tweet_max, client[0]))

#カテゴリごとに、アカウントのタイムラインの投稿をデータベースに保存する関数を実行
pprint(GetKnowTimeLine(tweet_max, client[1]))
pprint(GetEatTimeLine(tweet_max, client[2]))
# pprint(GetNewsTimeLine(tweet_max, client[3]))    #使わない
# pprint(GetSpaTimeLine(tweet_max, client[4]))       #使わない
pprint(GetSeeTimeLine(tweet_max, client[5]))
