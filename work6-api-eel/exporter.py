import pandas as pd
import requests
import urllib
import time
import datetime

class Exporter():
    def __init__(self):
        # self.df = pd.DataFrame(columns=
        #                        ['商品名',
        #                         '価格',
        #                         'ポイント倍率',
        #                         ])

    def export(self, df, filename):
        df = pd.DataFrame(
        {
        '商品名': self.itemName,
        '価格': self.itemPrice,
        'ポイント倍率': self.pointRate,
        }
    )
    filename = f"./out_{datetime.date.today()}_{self.shopCode}_{len(self.itemName)}.csv"
    df.to_csv(filename, encoding="utf_8-sig")
    