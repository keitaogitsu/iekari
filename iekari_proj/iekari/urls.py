# path()関数のインボート 
from django.urls import path
from iekari.views import rentroom, mypage, assess, recommend #追加！

app_name = 'iekari'
#変更！
urlpatterns = [
    path('rentroom', rentroom.list_view, name='rentroom_list'),
    path('rentroom/<slug:rentroom_id>', rentroom.detail_view, name='rentroom_detail'),

    path('recommend', recommend.form_view, name='recommend_form'), #[ REWRITE ] 追加
    path('recommend/result', recommend.result_view, name='recommend_result'), # [ REWRITE ]追加

    path('assess', assess.form_view, name='assess_form'), #[ REWRITE 2 ] 追加
    path('assess/result', assess.result_view, name='assess_result'), # [ REWRITE 2 ]追加

    path('mypage', mypage.mypage_top, name='mypage_top'),
    path('edit_cart/<slug:rentroom_id>', rentroom.edit_cart, name='edit_cart'), #追加
    ]