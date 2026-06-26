from django.shortcuts import render,get_object_or_404, redirect
from django.contrib.auth import get_user_model, authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView # CustomLoginView作成
from django.contrib.auth.forms import AuthenticationForm # 上に同じ
from django.views.decorators.http import require_POST
from django.contrib import messages
from .models import Plant, Work
from .forms import CustomUserCreationForm
from .forms import PlantForm, PlantWork
import json
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from django.utils import timezone 
from plant.utils.line_flex import send_schedule_flex

from PIL import Image
from PIL.ExifTags import TAGS

def index(request):
    plants = Plant.objects.all()
    return render(request, 'plant\\index.html', {'plants': plants})

@login_required
def plants_new(request):
    if request.method == "POST":
        form = PlantForm(request.POST, request.FILES)
        if form.is_valid():
            plant = form.save(commit=False)
            plant.user = request.user
            plant.save() 
            messages.success(request, '投稿が完了しました！')
        return redirect('plant:users_detail', pk=request.user.pk)
    else:
        form = PlantForm()
    return render(request, 'plant\\plants_new.html', {'form': form})

def plants_detail(request, pk):
    plant = get_object_or_404(Plant, pk=pk)
    if request.method == "POST":
        form = PlantWork(request.POST)
        if form.is_valid():
            plant_work = form.save(commit=False)
            plant_work.plant = plant
            plant_work.save()
        return redirect('plant:plants_detail', pk=plant.id)
    else:
        form = PlantWork()  
    return render(request, 'plant\\plants_detail.html', {'plant': plant, 'form': form})

def plants_edit(request, pk):
    plant = get_object_or_404(Plant, pk=pk)
    if request.method == "POST":
        form = PlantForm(request.POST, request.FILES, instance=plant)
        if form.is_valid():
            form.save()
            return redirect('plant:plants_edit', pk=plant.id)
    else:
        form = PlantForm(instance=plant)
    return render(request, 'plant\\plants_edit.html', {'form': form, 'plant': plant})

def users_detail(request, pk):
    user = get_object_or_404(get_user_model(), pk=pk)
    plants = user.plant_set.all()
    return render(request, 'plant\\users_detail.html', {'user': user, 'plants': plants})

@require_POST
def plants_delete(request, pk):
    plant = get_object_or_404(Plant, pk=pk, user=request.user)
    plant.delete()
    return redirect('plant:users_detail', pk=request.user.id)             

def signup(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            input_email = form.cleaned_data['email']
            input_password = form.cleaned_data['password1']
            new_user = authenticate(email=input_email, password=input_password)
            if new_user is not None:
                login(request, new_user)
                return redirect('plant:index')
    else:
        form = CustomUserCreationForm()
    return render(request, 'plant\\signup.html', {'form': form})

import hmac
import hashlib
import base64

def verify_signature(request):
    signature = request.headers.get("X-Line-Signature")
    if not signature:
        return False
    
    body = request.body
    hash = hmac.new(
        settings.LINE_CHANNEL_SECRET.encode("utf-8"),
        body,
        hashlib.sha256
    ).digest()

    expected_signature = base64.b64encode(hash).decode()
    return hmac.compare_digest(signature, expected_signature)

from django.http import HttpResponse, HttpResponseForbidden
import re

@csrf_exempt
def callback(request):
    if not verify_signature(request):
        return HttpResponseForbidden("Invalid signature")
    
    body = json.loads(request.body.decode("utf-8"))

    for event in body.get("events", []):
        if event["type"] == "message":
            reply_token = event["replyToken"]
            user_id = event["source"]["userId"]
            text = event["message"]["text"]

            if ':' in text and '完了' in text:
                work_id = text.split(':')[0]
                Work.objects.filter(id=work_id).update(performed_at=timezone.now())
            elif "予定" in text:
                numbers = re.findall(r"\d+", text)
                if numbers:
                    period = int(numbers[0])
                    send_schedule_flex(reply_token, user_id, period)
                else:
                    print("数字が見つかりませんでした")
                
    return HttpResponse("OK")

# CutomAuthenticationForm作成
class CustomAuthenticationForm(LoginView):
    template_name = "plant\\login.html"

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        # ユーザー名とパスワードの入力欄にcssクラスを追加
        form.fields["username"].widget.attrs.update({"class": "form-control", "placeholder": "ユーザー名を入力"})
        form.fields["password"].widget.attrs.update({"class": "form-control", "placeholder": "パスワードを入力"})
        return form