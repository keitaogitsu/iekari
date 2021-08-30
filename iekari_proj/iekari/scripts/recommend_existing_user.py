import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import pairwise_distances

from iekari.scripts.make_cross_table import * # [ REWRITE ] クロス集計表を作成する。algorithm回ではCSVを使っていたがDjangoのデータベース(db.sqlite)から読み込む

def calc_similarities(x):
    # x はn * mの行列である。x[i]とx[j]の類似度f(i, j)を相関係数を使って実装する
    sim_mt = np.corrcoef(x)
    return sim_mt

class Recommend_Existing():
    def __init__(self): # [ REWITE ]fpath引数削除
        # cross.csvの中身：
        # id,     age, gender, household_num, A00001, A00002, A00003......
        # B00001, 62,  1,      1,             0,      0,       3, .......
        # B00002. 35,  0,      1,             3,      0,       1, ....... 
        
        self.df = get_cross_table()  # [ REWRITE ]データ読み取り先をCSVファイルからSqliteに書き換える。詳細はmake_cross_tabke.py参照

        self.scores = np.array(self.df.iloc[:,4:]) # 各アイテムの評価（4列目以降）のみをnumoy行列として保存
        self.scores_T = self.scores.T
        self.num_user = len(self.scores)
        self.num_item = (self.scores.shape)[1]

    # ------------------------------------ ユーザーベースのリコメンデーション ------------------------------------------
    def recommend_user_base(self, userid, num=3):
        sim = self.get_sim_user(userid) #  各userについて (userid, 類似度（-1. ~ 1.0)) を類似度が大きい順に並べたリスト 
        sorted_item = self.rank_items_user(sim, userid)
        print(sorted_item[:num])

    def get_sim_user(self, target_userid):
        #コサイン類似度の計算
        sim_mt = 1 - pairwise_distances(self.scores, metric='cosine')

        #評価マトリクスと類似度マトリクスから、指定ユーザーの記録を抽出
        score_target = self.scores[target_userid]
        sim_target = sim_mt[target_userid]
        
        #評価物件の共通件数を計算し、10件以上ある場合に参照する
        def check_valid_user(i):
            indices = np.where(((score_target) * (self.scores[i])) != 0)[0]
            return len(indices) > 10 and i != target_userid
        
        # 3項演算子と内包表記という記法を使っています。調べてみて下さい。
        similarities = [ 
          ((i, sim_target[i]) if check_valid_user(i) else (i, 0)) 
          for i in range(self.num_user)
        ]

        #降順に並び替えて返す
        return sorted(similarities, key=lambda s: s[1], reverse=True)


    def rank_items_user(self, similarities, target_userid):
        rankings = []
        target_score = self.scores[target_userid]
        # 物件全てで評価値を予測
        for i in range(self.num_item):
            # 既に評価済みの場合はスキップ
            if target_score[i] >= 1:
                continue
            #関数参照のためself挿入
            rankings.append(("A" + str(i+1).zfill(5), self.predict_user(similarities, target_userid, i))) # [ REWRITE ]データベース似合わせてデータ型を変更
        return sorted(rankings, key=lambda r: r[1], reverse=True)


    def predict_user(self, similarities, target_userid, target_item_idx, k=8):
        target_score = self.scores[target_userid]
        avg_target = np.mean(target_score[np.where(target_score >= 1)])

        numerator = 0.0
        denominator = 0.0
        k_tmp = 0

        for similarity in similarities:
            s_usr   = similarity[0]
            s_sim = similarity[1]

            if k_tmp > k or s_sim <= 0.0: break # 類似度の高いユーザk件のみを評価する
            score = self.scores[s_usr]
            if score[target_item_idx] >= 1: # そのユーザーがtarget_item_idxの商品を評価している時
                denominator += s_sim
                numerator += s_sim * (score[target_item_idx] - np.mean(score[np.where(score >= 1)]))
                k_tmp += 1
        return avg_target + (numerator / denominator) if denominator > 0 else 0


    # ------------------------------------ アイテムベースのリコメンデーション ------------------------------------------
    def recommend_item_base(self, userid, num=3):
        sim = self.get_sim_item()
        sorted_item = self.rank_items_item(sim, userid)
        print(sorted_item[:num])

    def get_sim_item(self):
        similarities = 1 - pairwise_distances(self.scores_T, metric='cosine')
        # np.fill_diagonal(similarities, 0) # 体格成分を0にする
        return similarities
        
    def rank_items_item(self, similarities, target_userid):
        u = self.scores[target_userid]

        x = np.zeros(self.num_item)
        x[u > 0] = 1

        nominater = similarities.dot(u)
        denominater = similarities.dot(x)

        rankings = [(i, 0) for i in range(self.num_item)]
        
        for i in range(self.num_item):
            if denominater[i] != 0 and u[i] > 0:
                rankings[i] = ("A" + str(i+1).zfill(5), nominater[i] / denominater[i]) # [ REWRITE ]データベース似合わせてデータ型を変更

        return sorted(rankings, key=lambda r: r[1], reverse=True)

    def recommend(self, userid, num, base):
        # [ REWITE ] recommend関数追記
        # DjangoのViewから読み込まれる関数。recommend_user_base関数とrecommend_item_base関数のラッパー
        # recommend_user_base関数とrecommend_item_base関数はリコメンド結果を標準出力（print()）するので、Viewに返すように変更
        # 引数　：userid = ユーザーID, num = 表示件数, base = ユーザーベース("user") or アイテムベース("item")
        # 返り値：リコメンド結果（物件リスト）

        if str(base).lower() == "user":
          sim = self.get_sim_user(userid) #  各userについて (userid, 類似度（-1. ~ 1.0)) を類似度が大きい順に並べたリスト 
          sorted_item = self.rank_items_user(sim, userid)
          return sorted_item[:num]
        else:
          sim = self.get_sim_item()
          sorted_item = self.rank_items_item(sim, userid)
          return sorted_item[:num]

# [ REWRITE ] ↓の三行をコメントアウト。コメントアウトしなかったらimportの時に実行されてしまう。他にも if __name__ is "__main__"を使う方法などもある。
# re = Recommend_Existing(fpath = "./data/cross.csv")
# re.recommend_user_base(userid=20, num=3)
# re.recommend_item_base(userid=20, num=3)