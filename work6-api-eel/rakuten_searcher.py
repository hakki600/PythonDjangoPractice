import pandas as pd
import requests
import urllib
import time
import datetime

# 楽天商品検索APIを使用して取得したデータをCSV出力するクラス
class RakutenSearcher:
    def __init__(self):
        self.itemName = []
        self.itemPrice = []
        self.pointRate = []
        self.shopCode = ""
        self.hits = 0
        self.page = 0
        
    def search(self, shopCode, amount, order_select):
        print(amount)
        # 任意のキーワードでAPIを検索した時の 商品名と価格の一覧を取得
        self.shopCode = shopCode
        hits = 30 # 1ページごとの取得数(最大30)
        pages, mod = divmod(int(amount), hits)
        if(mod!=0):
            pages+=1
        
        for i in range(pages):
            print(i)
            page = i+1
            # 最終ページなら必要数までのみ取得
            if (page == pages):
                hits = mod
            
            sort = order_select
            url = f"https://app.rakuten.co.jp/services/api/IchibaItem/Search/20170706?format=json&shopCode={shopCode}&elements=Items,pointRate,count&formatVersion=2&hits={hits}&page={page}&sort={sort}&applicationId=1019079537947262807"
            rakuten = requests.get(url).json()
            # print(rakuten.keys())
            # >> dict_keys(['Items', 'pageCount', 'TagInformation', 'hits', 'last'
            # , 'count', 'page', 'carrier', 'GenreInformation', 'first'])
            
            if 'error' in rakuten.keys():
                error_str = rakuten['error']
                error_description_str = rakuten['error_description']
                error = f'error: {error_str}\n'
                error += f'error_desctiption: {error_description_str}'
                return error
            
            items = rakuten["Items"]
            # print(items[0].keys())
            # >> dict_keys(['mediumImageUrls', 'pointRate', 'shopOfTheYearFlag', 
            # 'affiliateRate', 'shipOverseasFlag', 'asurakuFlag', 'endTime', 'taxFlag', 
            # 'startTime', 'itemCaption', 'catchcopy', 'tagIds', 'smallImageUrls', 
            # 'asurakuClosingTime', 'imageFlag', 'availability', 'shopAffiliateUrl', 
            # 'itemCode', 'postageFlag', 'itemName', 'itemPrice', 'pointRateEndTime', 
            # 'shopCode', 'affiliateUrl', 'giftFlag', 'shopName', 'reviewCount', 
            # 'asurakuArea', 'shopUrl', 'creditCardFlag', 'reviewAverage', 'shipOverseasArea', 
            # 'genreId', 'pointRateStartTime', 'itemUrl']
            
            print(len(items))
            for item in items:
                self.itemName.append(item["itemName"])
                self.itemPrice.append(item["itemPrice"])
                self.pointRate.append(item["pointRate"])
            if not (i == pages):
                time.sleep(1)
                
        df = pd.DataFrame(
            {
            '商品名': self.itemName,
            '価格': self.itemPrice,
            'ポイント倍率': self.pointRate,
            }
        )
        filename = f"./out_{datetime.date.today()}_{self.shopCode}_{len(self.itemName)}.csv"
        df.to_csv(filename, encoding="utf_8-sig")
        return 0    