import pandas as pd
import os

### 検索ツール
def search():
    word = ""
    while word!="f":
        word =input("鬼滅の登場人物の名前を入力してください. csv読み込み:r csv書き込み:e 現在のリストを確認:l 終了:f >>> ")
        if word == "f":
            print("\n")
            exit()
        
        elif word == "r":
            names = read_csv()
            source.extend(names)
            print("{}人追加しました.".format(len(names)))

        elif word == "e":
            export(source)
            print("csv出力しました.")

        elif word == "l":
            print(source)

        elif word in source:
            print("{}が見つかりました.".format(word))

        else:
            result = input("{}は見つかりません.追加しますか？ y/n >>> ".format(word))
            if  result == "y":
                source.append(word)
                print("{}を追加しました.".format(word))
            else:
                print("キャンセルしました.")
                
        print("---------------------\n")
            
# csvから読み込み
def read_csv():
    filepath = "characters.csv"
    df = pd.read_csv(filepath, header=0)
    names = df["name"]
    # dataframe→listへ変換→[[name],[name],[name]]
    # series→listへ変換→[name,name,name]
    return names.values.tolist()

# csvでリスト内容を出力
def export(source):
    id = list(range(0, len(source), 1))
    df = pd.DataFrame({'id':id,
                       'name':source})
    filepath = "C:\\Users\\hakki\\Documents\\Yonetani\\out.csv"
    df.to_csv(filepath, encoding='utf_8_sig')

if __name__ == "__main__":
    # 検索ソース
    source=["ねずこ","たんじろう","きょうじゅろう","ぎゆう","げんや","かなお","ぜんいつ"]
    search()
    
    