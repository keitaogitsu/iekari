from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, Http404, JsonResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from django.core.paginator import Paginator
from iekari.models import RentRoom, Profile, Cart
from django.contrib.auth.models import User #User追加

import random

def list_view(request):
    rentroom_list = RentRoom.objects.all().order_by('-id')
    paginator = Paginator(rentroom_list, 20) # ページ当たり20個表示

    try:
        page = int(request.GET.get('page'))
    except:
        page = 1

    rentrooms = paginator.get_page(page)
    return render(request, 'iekari/rentroom_list.html', {'rentrooms': rentrooms, 'page': page, 'last_page': paginator.num_pages})


def detail_view(request, rentroom_id):
    rentroom = get_object_or_404(RentRoom, id=rentroom_id)

    try:
        page = int(request.GET.get('from_page'))
    except:
        page = 1
    return render(request, 'iekari/rentroom_detail.html', {'rentroom': rentroom, 'page': page })


def edit_cart(request, rentroom_id):
    #表示しているページの物件を取得
    rentroom = get_object_or_404(RentRoom, id=rentroom_id)
    #遷移前の一覧ページを取得
    try:
        page = int(request.GET.get('from_page'))
    except:
        page = 1
    #ログインしているユーザのIDを取得
    user_id = request.user.id
    #編集前のカートの中身にこの商品はある？
    previous_cart = Cart.objects.filter(user_id=user_id, product_id=rentroom_id)
    if previous_cart.exists():
        #あればその商品を削除
        previous_cart.delete()
    else:
        #無ければユーザID・商品IDの組をカートに追加
        #productはCartクラスのインスタンス
        product = Cart(user_id=user_id, product_id=rentroom_id)
        product.save()
    return render(request, 'iekari/rentroom_detail.html', {'rentroom': rentroom, 'page': page })