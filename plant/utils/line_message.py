import requests
from django.conf import settings
from requests.exceptions import HTTPError, ConnectionError, Timeout, RequestException

def send_line_message(message:str):
    """ LINE Messaging API を使ってメッセージを送信 """
    url = "https://api.line.me/v2/bot/message/push"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {settings.LINE_CHANNEL_ACCESS_TOKEN}"
    }
    data = {
        "to": settings.LINE_USER_ID,
        "messages": [
            {"type": "text", "text": message}
        ]
    }

    try:
        response = requests.post(url, headers=headers, json=data, timeout=10)
    
        # 4xxまたは5xxエラーの場合、HTTPError例外を発生させる
        response.raise_for_status()

        # ここに成功時の処理（例: response.json()の処理）を記述
        print("リクエスト成功！")
        print(response.json())

    except HTTPError as http_err:
        print(f'HTTPエラーが発生しました: {http_err}') # 4xx, 5xxなどのステータスコードを表示
        print(f'レスポンス本文: {response.text}')
    except ConnectionError as conn_err:
        print(f'接続エラーが発生しました: {conn_err}') # DNSエラー、接続拒否など
    except Timeout as timeout_err:
        print(f'タイムアウトエラーが発生しました: {timeout_err}') # サーバー応答なし
    except RequestException as req_err:
        print(f'その他の予期せぬエラーが発生しました: {req_err}') # 上記以外のrequests関連エラー
    except ValueError:
        print('レスポンスのJSONデコードに失敗しました。') # response.json()でエラーになった場合
