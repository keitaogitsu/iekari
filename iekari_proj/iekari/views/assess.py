# [ REWRITE ]  ファイル追加

from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, Http404, JsonResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from iekari.scripts.predict_price import PricePredict

from iekari.models import RentRoom

def form_view(request): # フォームを表示
    return render(request, 'iekari/assessment_form.html') 

def result_view(request): # フォームの入力をAPIに伝達、リターン値を用いてテンプレートに表示
    var = request.GET
    predict_price = PricePredict()
    station = float(var.get("station"))
    area = float(var.get("area"))
    year = float(var.get("year"))
    predict_price.load_model("./iekari/scripts/price_model.sav")
    result = predict_price.predict(dist_to_nearest_station =station, area =area, year_pp =year)

    return render(request, 'iekari/assessment_result.html', {"station":station, "area":area, "year":year, 'result':int(result*area)})