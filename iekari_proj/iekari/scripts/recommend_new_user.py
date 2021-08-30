import pandas as pd
import numpy as np
import argparse

from iekari.models import Profile, RentRoom # [ REWRITE ]追加
pd.set_option('display.max_columns', 100)

from iekari.scripts.make_cross_table import * # [ REWRITE ] クロス集計表を作成する。algorithm回ではCSVを使っていたがDjangoのデータベース(db.sqlite)から読み込む


class RecommendNew():
    def __init__(self):
        # self.df_estate = pd.read_csv("./data/RentRoom.csv") # [ REWITE ]削除

        # RentRoom.csvの中身
        # id,     pref_name, city_name,  district_name, built_year, structure,  top_floor_num, room_type, \
        # A00001, 東京都,     世田谷区,    喜多見７丁目,     1988,      ＲＣ,        2,              1R,  \
        # price,   area,  latitude,    longitude,    nearest_station_id,  dist_to_nearest_station
        # 2812.27,  23,   35.63129425, 139.5940049,  S00001,              1096.93

        # self.df_user = pd.read_csv("./data/cross.csv") # [ REWITE ]削除
        # cross.csvの中身：
        # id,     age, gender, household_num, A00001, A00002, A00003......
        # B00001, 62,  1,      1,             0,      0,       3, .......
        # B00002. 35,  0,      1,             3,      0,       1, ....... 

        # [ REWRITE ]　CSVファイルではなく、DjangoのModelからデータを読み込むように追加、df_stationは使用しないので削除
        self.df_estate = pd.DataFrame.from_records(list(RentRoom.objects.values() ))
        self.df_user = get_cross_table()

        self.df_user["age_10"] = self.df_user["age"].map(lambda x: str(x)[:1]) # 一時的な抽出用として、ユーザーの年齢から10の位を抽出


    def recommend(self, age, station_name, limit=10):
        # 年代が同じ人のみを抽出
        df_user_extracted = self.df_user[abs(self.df_user["age"] - age) <= 10] # 年齢の10のくらいが同じ人のみ集める
        
        # 最寄り駅がstation_nameの物件のみを抽出して、valid_estate_idsに案件idをリストで格納
        # station_id = self.get_station_id(station_name)
        df_extracted = self.df_estate[self.df_estate["nearest_station"] == station_name] # [ REWRITE ] データベースに格納されているカラム名との整合性を取る
        valid_estate_ids = df_extracted["id"].tolist()

        rankings = self.make_rankings(df_user_extracted[valid_estate_ids])
        return rankings[0:limit]

    # [ REWRITE ] get_station_idメソッドを削除

    def make_rankings(self, df_extracted):
        mean_scores = df_extracted.mean().sort_values(ascending=False).reset_index()
        rankings = [list(mean_scores.loc[i]) for i in range(len(mean_scores))]
        return rankings

# [ REWRITE ] ↓の2行をコメントアウト。コメントアウトしなかったらimportの時に実行されてしまう。他にも if __name__ is "__main__"を使う方法などもある。
# rn = RecommendNew()
# rn.recommend(age=20, station_name="明大前", limit=15)