from django.core.management.base import BaseCommand
from plant.models import Plant
from plant.tasks import notify_upcoming_works 

class Command(BaseCommand):
    help = "植物データを処理するサンプルコマンド"

    def add_arguments(self, parser):
        # 引数を追加したい場合（任意）
        parser.add_argument('--days', type=int, default=7)

    def handle(self, *args, **options):
        days = options['days']
        self.stdout.write(self.style.SUCCESS(f"処理を開始します (days={days})"))
        # ここに実処理を書く
        notify_upcoming_works()
        self.stdout.write(self.style.SUCCESS("処理が完了しました"))

