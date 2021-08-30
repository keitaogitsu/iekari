import numpy as np
import pandas as pd
import pickle

from sklearn.metrics import mean_squared_error
from sklearn import linear_model

class PricePredict:
    def __init__(self):
        self.clf = None     # 学習モデル
        self.x_train = None # RentRoom.csvの中の最寄り駅からの距離、敷地面積、築年数のデータ集合
        self.Y_train = None # RentRoom.csvの中の家賃一覧

    def load_model(self, fpath):
         self.clf = pickle.load(open(fpath, 'rb'))

    def predict(self, dist_to_nearest_station = 0, area = 0, year_pp = 0):
        df = pd.DataFrame([{'dist_to_nearest_station':dist_to_nearest_station, 'area':area, 'year_pp':year_pp }])
        return self.clf.predict(df)


    # -----------------------------------   学習用(Djangoでは使用しない)  ------------------------------------------------
    def load_test_data(self, path):
        self.data_all = pd.read_csv(path)# CSVファイルを読み込む
        # 本来ならばテストデータと学習用データを分けるべきだが、
        # Djangoで使用する場合はすべて学習用に使って良いだろうと思い、
        # このプログラムではテストデータを用意せずRentroom.csvの中身をすべて学習に費やしている
        self.Y_train = self.data_all[['price']] # 予測するものは価格（price)なので、価格データのみを取り出す
        self.X_train = self.data_all.drop(['id', 'pref_name', 'city_name', 'district_name', 'built_year', 'structure', 'price', 'top_floor_num', 'room_type', 'nearest_station_id'], axis=1)
        self.X_train = self.X_train.drop(['latitude','longitude'], axis=1) # 学習に不要な値を削除（drop)
        self.X_train['year_pp'] = 2021 - self.data_all['built_year'] # 新しく’year_pp’のデータ列を追加

    def learn(self):
        #モデルの枠組みを設定
        self.clf = linear_model.LinearRegression()
        # clsにあわせ型を変換
        X_train = self.X_train.values
        Y_train = self.Y_train.values

        # 予測モデルを作成
        self.clf.fit(X_train, Y_train)

        print(self.clf.coef_)# 回帰係数
        print(self.clf.intercept_)# 切片 (誤差)

    def check_res(self):
        pred_train = self.clf.predict(self.X_train)
        print(np.sqrt(mean_squared_error(self.Y_train, pred_train)))

    def save_model(self, fpath):
        pickle.dump(self.clf, open(fpath, 'wb'))


if __name__ == "__main__":
    
    price_predict = PricePredict()
    
    # 事前に学習モデルを作成
    price_predict.load_test_data("../../day4_startupData/RentRoom.csv") # 学習用データ作成
    price_predict.learn() # 学習
    price_predict.check_res() # 学習結果を表示
    price_predict.save_model("price_model.sav")

    # 事前に学習したモデルを読込、予測
    price_predict.clf = None # 一行下のload_modelメソッドで price_predict.clf が置き換わることを確認するために一応書いた一行
    price_predict.load_model("price_model.sav")
    result = price_predict.predict(dist_to_nearest_station = 1000, area = 30, year_pp = 5)
    print("家賃＝", result[0][0])