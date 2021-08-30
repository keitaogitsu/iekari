
# Create your models here.
from django.contrib.auth.models import User 
from django.db import models 
 
GENDER_LIST = ( (0, '男性'), (1, '女性') )
dict_gender_list = {0:'男性',1:'女性'}

#デフォルトであるdjango.dbのmodelsを継承して作成する
class Profile(models.Model):
    
    #django仕様のメタクラス(クラス自体の設定を記述)(管理画面での表示内容を設定)
    class Meta:
        verbose_name = 'ユーザー情報データ'
        verbose_name_plural = 'ユーザー情報データ'
    #ユーザーの設定。下記のフィールドとの紐づけはビューで行う
    user = models.OneToOneField(User, verbose_name='ユーザー',null=True, blank=True, on_delete=models.CASCADE)

    #フィールドの設定。コード１行がフィールド１列に対応する。
    id = models.CharField(max_length=6,primary_key=True)
    age = models.IntegerField('年齢')
    gender = models.IntegerField('性別',choices=GENDER_LIST)
    household_num = models.IntegerField('世帯人数')
    
    #管理画面で表示される文字列を定義する
    def __str__(self):

        user_str = ''
        if self.user is not None:
            user_str = '(' + self.user.username + ')'

        return self.id+' '+str(self.age)+'歳 ' \
            +dict_gender_list.get(self.gender)+' ' \
            +str(self.household_num)+'人世帯 ' 


class RentRoom(models.Model):

    class Meta:
        verbose_name = '物件情報データ'
        verbose_name_plural = '物件情報データ'

    id = models.CharField('物件ID',max_length=6,primary_key=True) # 'A00001'
    pref_name = models.CharField('都道府県',max_length=20)      # '東京都'
    city_name = models.CharField('市区町村',max_length=50)      # '世田谷区'
    district_name = models.CharField('町丁目',max_length=50)    # '喜多見７丁目'
    built_year = models.IntegerField('築年')
    structure = models.CharField('構造',max_length=20)
    top_floor_num = models.IntegerField('最上階数')
    room_type = models.CharField('間取り',max_length=20)        # '1R', '1K' など
    price = models.FloatField('平米単価')
    area = models.FloatField('専有面積')
    latitude = models.FloatField('物件緯度')
    longitude = models.FloatField('物件経度')
    nearest_station = models.CharField('最寄り駅', max_length=50)
    dist_to_nearest_station = models.FloatField('最寄駅までの距離')

    owner = models.ForeignKey(Profile,
        verbose_name='所有者',
        null=True, blank=True,
        on_delete=models.CASCADE
    )

    def __str__(self):
        return self.id


class ScoreLog(models.Model):# [ REWRITE ] 追加
    class Meta:
        verbose_name = '賃貸物件評価データ'
        verbose_name_plural = '賃貸物件評価データ'

    profile = models.ForeignKey(Profile, verbose_name='ユーザー情報', on_delete=models.CASCADE)
    rent_room = models.ForeignKey(RentRoom, verbose_name='物件', on_delete=models.CASCADE)

    score = models.IntegerField('評価')                         # 1~5
    timestamp = models.DateTimeField('日時', auto_now_add=True) # 評価時点で更新


class Cart(models.Model):
    class Meta:
        verbose_name = 'カートデータ'
        verbose_name_plural = 'カートデータ'
    
   #ユーザーID
    user_id = models.CharField(max_length=6)
    #商品ID
    product_id = models.CharField(max_length=6)
    #追加時刻
    timestamp = models.DateTimeField('追加日時', auto_now_add=True)
    #管理画面で表示される文字列を定義する
    def __str__(self):
        return self.user_id + ' ' + self.product_id
    