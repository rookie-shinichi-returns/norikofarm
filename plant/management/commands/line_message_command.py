from django.core.management.base import BaseCommand
from datetime import timedelta
from django.utils import timezone
from plant.models import Work
from plant.utils.line_message import send_line_message

class Command(BaseCommand):
    help = "LINEアプリにメッセージを送る"

    def handle(self, *args, **options):
        today = timezone.now().date()
        target_date = today + timedelta(days=7)
        upcoming_works = []
        for work in Work.objects.all():
            next_date = work.next_scheduled_date
            if next_date and today <= next_date <= target_date:
                upcoming_works.append(work)

        if upcoming_works:
            message ="🌿【植物作業リマインダー】\n"
            for w in upcoming_works:
                message += f"\n ♦ {w.plant.name} の {w.get_work_type_display()}\n 予定日: {w.next_scheduled_date.strftime('%Y-%m-%d')}"
            send_line_message(message) 
