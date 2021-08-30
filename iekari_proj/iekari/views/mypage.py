from django.contrib.auth.models import User
from django.shortcuts import render, redirect, get_object_or_404

from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, Http404, JsonResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required

import json
from iekari.models import RentRoom, Cart

@login_required
def mypage_top(request):
    user = request.user
    profile = user.profile
    myrooms = RentRoom.objects.filter(owner_id=profile.id)
    products = Cart.objects.filter(user_id=user.id)
    return render(request, 'iekari/mypage.html', {'profile':profile, 'rooms':myrooms, 'products':products}) 