import requests
import json
from datetime import datetime, timezone, timedelta
from pprint import pprint

# setting.pyからインポート
import settings

# firebaseのrealtime databaseを使うために必要な記述  SDK
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db

cred = credentials.Certificate(
    settings.CRED_JSON)

firebase_admin.initialize_app(cred, {
    'databaseURL': settings.DATABASE_URL,
    'databaseAuthVariableOverride': {
        'uid': 'my-service-worker'
    }
})

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

# Instagram Graph APIの認証用関数
def basic_info():
    # 初期
    config = dict()  # 辞書型に変換
    # 【要修正】アクセストークン
    config["access_token"] = settings.access_token
    # 【要修正】アプリID
    config["app_id"] = settings.app_id
    # 【要修正】アプリシークレット
    config["app_secret"] = settings.app_secret
    # 【要修正】インスタグラムビジネスアカウントID
    config['instagram_account_id'] = settings.instagram_account_id
    # 【要修正】グラフバージョン
    config["version"] = 'v14.0'
    # 【修正不要】graphドメイン
    config["graph_domain"] = 'https://graph.facebook.com/'
    # 【修正不要】エンドポイント
    config["endpoint_base"] = config["graph_domain"]+config["version"] + '/'
    # 出力
    return config

# APIリクエスト用の関数
def InstaApiCall(url, params, request_type):

    # リクエスト
    if request_type == 'POST':
        # POST
        req = requests.post(url, params)
    else:
        # GET
        req = requests.get(url, params)

    # レスポンス
    res = dict()
    res["url"] = url
    res["endpoint_params"] = params
    res["endpoint_params_pretty"] = json.dumps(params, indent=4)
    res["json_data"] = json.loads(req.content)
    res["json_data_pretty"] = json.dumps(res["json_data"], indent=4)
    # json_dataにリクエストした情報が格納される（IGハッシュタグサーチなのか、IGハッシュタグなのか、IGメディアなのかはその時による）
    # ただ、流れとしては IGハッシュタグサーチ -> IGハッシュタグ or IGメディア

    # 出力
    return res


# ハッシュタグ検索結果を取得するID関数(IGハッシュタグサーチ)
# 参考url：https://developers.facebook.com/docs/instagram-api/reference/ig-hashtag-search
# この関数によりハッシュタグIDを得ることができる。ハッシュタグIDを取得できればIGメディアやIGハッシュタグの関数を動かすことができる
def get_hashtag_id(hashtag_word):
    """
    【APIのエンドポイント】
    https://graph.facebook.com/{graph-api-version}/ig_hashtag_search?user_id={user-id}&q={hashtag-name}&fields={fields}  <-なぜfieldsがあるの？
    """
    
    # リクエスト
    Params = basic_info()                   # リクエストパラメータ
    Params['hashtag_name'] = hashtag_word   # ハッシュタグ情報

    # エンドポイントに送付するパラメータ
    Params['user_id'] = Params['instagram_account_id']  # インスタユーザID
    Params['q'] = Params['hashtag_name']                # ハッシュタグ名
    Params['fields'] = 'id,name'                        # フィールド情報
    url = Params['endpoint_base'] + 'ig_hashtag_search'  # エンドポイントURL
    # 作られるエンドポイント -> 'https://graph.facebook.com/v14.0/ (endpoint_base) + ig_hashtag_search (文字列)'
    # 作られるPrrams -> Paramsにはbasic_info()の情報と[hashtag_name],[user_id], [q], [fields]の情報が入っている

    # レスポンス
    response = InstaApiCall(url, Params, 'GET')

    # 戻り値（ハッシュタグID）
    # 結果的に、IGハッシュタグやIGメディアに必要なハッシュタグIDを返す
    return response['json_data']['data'][0]['id']


# 「最近」のハッシュタグメディアの検索結果(IGハッシュタグ)
# 参考url：https://developers.facebook.com/docs/instagram-api/reference/ig-hashtag/recent-media#reading
def get_hashtag_media_recent(params, hashtag_id):
    """
    【APIのエンドポイント】
    https://graph.facebook.com/{graph-api-version}/{ig-hashtag-id}/recent_media?user_id={user-id}&fields={fields}
    """
    # パラメータ
    Params = dict()
    Params['user_id'] = params['instagram_account_id']
    Params['fields'] = 'id, children{id,media_url,media_type}, caption, comment_count, like_count, media_type, media_url, permalink, timestamp'
    # id, children?, 投稿文, コメント数, いいね数, メディアの種類, メディアのurl, パーマリンク、投稿日  (thumbnail_url,username)?
    Params['access_token'] = params['access_token']

    # エンドポイントURL
    url = params['endpoint_base'] + hashtag_id + '/' + 'recent_media'
    # 作られるエンドポイント -> 'https://graph.facebook.com/v14.0/ (endpoint_base) + hashtag_id/ (個別に違う) + recent_media'
    # 作られるPrrams -> Paramsにはbasic_info()の情報と[user_id], [fields],[access_token]の情報が入っている

    return InstaApiCall(url, Params, 'GET')


######################################################################
# databaseに初期データを追加する(1回初期データを追加すれば2回目以降は参照)
ref = db.reference('/SNS_data')

# 【要修正】検索したいハッシュタグワードを記述
hashtag_word = '函館'

# ハッシュタグIDを取得
hashtag_id = get_hashtag_id(hashtag_word)
print("「"+hashtag_word+"」のハッシュタグID: "+str(hashtag_id))

# パラメータセット
params = basic_info()

# ハッシュタグ情報取得
hashtag_response = get_hashtag_media_recent(params, hashtag_id)

# 出力
for post in hashtag_response['json_data']['data']:
    # databaseにデータを追加する
    try:  # いいね数とメディアurlは存在しないときがあるので、存在しなかったらtryは実行せず、passする。なので25件全て執れない可能性高い15件とかかな...
        if post['media_type'] != 'CAROUSEL_ALBUM' :
            time = datetime.fromisoformat(post['timestamp'].split('+')[0]).timestamp() + 32400  #float型(確認済み)
            ref.child(str(post["id"])).set({  # キーはツイートID、データは投稿文
                'data_label': 'Search',                
                'date': -(time),  
                'date2': post['timestamp'],
                'date3': getTime(time),
                # 投稿日  ISO 8601形式の投稿日時をUNIX時間に変換した。（投稿日時を秒数に変換）
                'text': post['caption'],  # 投稿文
                'link': post['permalink'],  # 投稿リンク
                'good': post['like_count'],  # いいね数
                'media_url': post['media_url'],  # メディアurl(画像)
                'media_type': post['media_type'],  # メディアの種類
                'SNS_type': 'Instagram'
            })
        else :
            time = datetime.fromisoformat(post['timestamp'].split('+')[0]).timestamp() + 32400  #float型(確認済み)
            ref.child(str(post["id"])).set({  # キーはツイートID、データは投稿文
                'data_label': 'Search',                
                'date': -(time),
                'date2': post['timestamp'],
                'date3': getTime(time),
                # 投稿日  ISO 8601形式の投稿日時をUNIX時間に変換した。（投稿日時を秒数に変換）
                'text': post['caption'],  # 投稿文
                'link': post['permalink'],  # 投稿リンク
                'good': post['like_count'],  # いいね数
                'media_type': post['media_type'],  # メディアの種類
                'SNS_type': 'Instagram'
            })
            media_ref = db.reference('/SNS_data/' + str(post["id"])).child('media')
            for i in range(len(post['children']['data'])):
                media_ref.child('url' + str(i)).set({
                    'media_type': post['children']['data'][i]['media_type'],
                    'media_url': post['children']['data'][i]['media_url'],
                })
    except:
        pass

print('done!!')