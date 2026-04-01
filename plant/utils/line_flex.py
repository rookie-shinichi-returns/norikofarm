import requests
from datetime import timedelta
from django.utils import timezone
from django.conf import settings
from plant.models import Work, UserProfile


def send_schedule_flex(reply_token, line_user_id):
    try:
        profile = UserProfile.objects.get(line_user_id=line_user_id)
        user = profile.user
    except UserProfile.DoesNotExist:
        return

    today = timezone.now().date()
    target_date = today + timedelta(days=7)

    works = Work.objects.filter(
        plant__user=user
    )

    upcoming = []
    for w in works:
        next_date = w.next_scheduled_date
        if next_date and today <= next_date <= target_date:
            upcoming.append((w, next_date))

    # upcoming = sorted(upcoming, key=lambda x: x[1])[:5]
    upcoming = sorted(upcoming, key=lambda x: x[1])[:5]

    if not upcoming:
        send_text(reply_token, "🌿 直近の予定はありません")
        return
        
    bubbles = []

    for work, next_date in upcoming:
        # 画像URL(なければデフォルト画像)
        if work.plant.image:
            image_url = f"{settings.BASE_URL}{work.plant.image.url}"
        else:
            image_url = "https://images.unsplash.come/photo-1501004318641-b39e6451bevc6"

        days_left = (next_date - today).days        

        bubble = {
            "type": "bubble",
            "size": "mega",
            "hero": {
                "type": "image",
                "url": image_url,
                "size": "full",
                "aspectRatio": "10:15", # アスペクト比　{幅}:{高さ}
                "aspectMode": "fit",
            },
            "body": {
                "type": "box",
                "layout": "vertical",
                "spacing": "md",
                "contents": [
                    {
                        "type": "text",
                        "text": work.plant.name,
                        "weight": "bold",
                        "size": "xl"
                    },
                    {
                        "type": "text",
                        "text": work.get_work_type_display(),  # 表示用メソッド（DB値でなく人のわかる値を表示 obj.get_foo_display (fooはフィールド名)）
                        "size": "md",
                        "color": "#888888"
                    },
                    {
                        "type": "separator",
                        "margin": "md"
                    },
                    {
                        "type": "text",
                        "text": f"📅 {next_date.strftime('%Y-%m-%d')}",
                        "size": "lg",
                        "weight": "bold",
                        "color": "#27ACB2",
                        "margin": "md"
                    },
                    {
                        "type": "text",
                        "text": f"あと{days_left}日",
                        "size": "sm",
                        "color": "#FF5551",
                        "margin": "sm"
                    }
                ]
            },
            "footer": {
                "type": "box",
                "layout": "vertical",
                "contents": [
                    {
                        "type": "button",
                        "style": "primary",
                        "action": {
                            "type": "message",
                            "label": "作業完了",
                            "text": f"{work.id}:完了"
                        }
                    }
                ]
            }
        }
        bubbles.append(bubble)

    flex_message = {
        "replyToken": reply_token,
        "messages": [
            {
                "type": "flex",
                "altText": "植物の作業予定",
                "contents": {
                    "type": "carousel",
                    "contents": bubbles
                }
            }
        ]
    }
    
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {settings.LINE_CHANNEL_ACCESS_TOKEN}"
    }

    requests.post(
        "https://api.line.me/v2/bot/message/reply",
        headers=headers,
        json=flex_message
    )


def send_text(reply_token, text):
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {settings.LINE_CHANNEL_ACCESS_TOKEN}"
    }

    data = {
        "replyToken": reply_token,
        "messages": [
            {"type": "text", "text": text}
        ]
    }

    requests.post(
        "https://api.line.me/v2/bot/message/reply",
        headers=headers,
        json=data
    )