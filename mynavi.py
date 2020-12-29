# coding: utf-8_sig
import os
from selenium.webdriver import Chrome, ChromeOptions
import time
import pandas as pd
import sys

# Chromeを起動する関数
def set_driver(driver_path, headless_flg):
    # Chromeドライバーの読み込み
    options = ChromeOptions()

    # ヘッドレスモード（画面非表示モード）をの設定
    if headless_flg == True:
        options.add_argument('--headless')

    # 起動オプションの設定
    options.add_argument(
        '--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36')
    # options.add_argument('log-level=3')
    options.add_argument('--ignore-certificate-errors')
    options.add_argument('--ignore-ssl-errors')
    options.add_argument('--incognito')          # シークレットモードの設定を付与

    # ChromeのWebDriverオブジェクトを作成する。
    return Chrome(executable_path=os.getcwd() + "/" + driver_path, options=options)


def export(search_keyword, df_source):
    # filepath = "./mynavi.csv"
    filepath = "./mynavi_" + search_keyword + ".csv"
    # Byte Order Mark(BOM)付きで出力すると文字化けしない→utf_8_sig 指定
    df_source.to_csv(filepath, encoding='utf_8_sig')
    
def add_log_error(i, page, e, search_keyword):
    log = "Element: " + str(i) + "  Page: " + str(page) + " "+ str(e) + "\n"
    filepath = "./mynavi_" + search_keyword + ".txt"
    fileobj = open(filepath, "a", encoding = "utf_8_sig")
    fileobj.write(log)
    fileobj.close()
 
def add_log(page, data_num, error_num, search_keyword):
    log = f'Page {page} done. Data: {data_num}   Error: {error_num}\n'
    filepath = "./mynavi_" + search_keyword + ".txt"
    fileobj = open(filepath, "a", encoding = "utf_8_sig")
    fileobj.write(log)
    fileobj.close()
    
# main処理
def main():
    print("Please input keyword >>> ")
    search_keyword = input()
    print("Please input number of acquisitions >>> ")
    try:
        search_num = int(input())    
    except:
        sys.exit()
    
    # driverを起動
    if os.name == 'nt': #Windows
        driver = set_driver("chromedriver.exe", False)
    elif os.name == 'posix': #Mac
        driver = set_driver("chromedriver", False)
    # Webサイトを開く
    driver.get("https://tenshoku.mynavi.jp/")
    time.sleep(3)
 
    try:
        # ポップアップを閉じる
        driver.execute_script('document.querySelector(".karte-close").click()')
        time.sleep(5)
        # ポップアップを閉じる
        driver.execute_script('document.querySelector(".karte-close").click()')
    except:
        pass
    
   
    # 検索窓に入力
    driver.find_element_by_class_name(
        "topSearch__text").send_keys(search_keyword)
    time.sleep(2)
    
    # 検索ボタンクリック
    driver.find_element_by_class_name("topSearch__button").click()

    # ページ終了まで繰り返し取得した情報を入れるリスト
    exp_name_list = []
    exp_detail_list = []
    exp_area_list = []
    exp_fee_list = []
    
    i = 1
    page = 1
    error_num = 0
    
    while i <= search_num:
        # オススメ表示が出現した場合
        try:
            recruit_recommend_list = driver.find_elements_by_css_selector(
                ".cassetteRecruitRecommend")
            # 1ページの全求人分繰り返す 
            for recruit in recruit_recommend_list:
                if i <= search_num:
                    try:
                        # 会社名を取得 element:単数
                        name = recruit.find_element_by_css_selector(
                            ".cassetteRecruitRecommend__name")
                        # 詳細情報を取得
                        detail = recruit.find_element_by_css_selector(
                            ".cassetteRecruitRecommend__copy")
                        # 勤務地情報を取得
                        area = recruit.find_element_by_css_selector(
                            ".tableCondition tbody tr:nth-child(3) td")
                        # 給与情報を取得
                        fee = recruit.find_element_by_css_selector(
                            ".tableCondition tbody tr:nth-child(4) td")
                        # リストに追加
                        exp_name_list.append(name.text)
                        exp_detail_list.append(detail.text)
                        exp_area_list.append(area.text)
                        exp_fee_list.append(fee.text)
                        i += 1
                    except Exception as e:
                        add_log_error(i, page, e, search_keyword)
                        error_num += 1
        except Exception as e:
            add_log_error(i, page, e, search_keyword)
            
        try:
            recruit_list = driver.find_elements_by_css_selector(
                ".cassetteRecruit")
            # 1ページの全求人分繰り返す
            for recruit in recruit_list:
                if i <= search_num:
                    try:
                        # 会社名を取得 element:単数
                        name = recruit.find_element_by_css_selector(
                            ".cassetteRecruit__name")
                        # 詳細情報を取得
                        detail = recruit.find_element_by_css_selector(
                            ".cassetteRecruit__copy")
                        # 勤務地情報を取得
                        area = recruit.find_element_by_css_selector(
                            ".tableCondition tbody tr:nth-child(3) td")
                        # 給与情報を取得
                        fee = recruit.find_element_by_css_selector(
                            ".tableCondition tbody tr:nth-child(4) td")
                        # リストに追加
                        exp_name_list.append(name.text)
                        exp_detail_list.append(detail.text)
                        exp_area_list.append(area.text)
                        exp_fee_list.append(fee.text)
                        i += 1
                    except Exception as e:
                        error_num += 1
                        add_log_error(i, page, e, search_keyword)
        except Exception as e:
            add_log_error(i, page, e, search_keyword)
                
        # 進行状況表
        add_log(page, i-1, error_num, search_keyword)
        
        # 次ページへ遷移
        nextpage_href = driver.find_element_by_css_selector(
            "nav ul .pager__item--active + .pager__item a").get_attribute("href")
        driver.get(nextpage_href)
        
        page += 1
        time.sleep(1)
            
    # dataframe作成
    df = pd.DataFrame({
                       'name':exp_name_list,
                       'detail':exp_detail_list,
                       'area':exp_area_list,
                       'fee':exp_fee_list
                       })
    
    # csv出力時に列順が変わってしまうのを防ぐため
    list_col_sorted = ['name', 'detail', 'area', 'fee']
    df = df.loc[:, list_col_sorted]
    
    # csv出力
    try:
        export(search_keyword, df)
        print("csv file exported.")
    except Exception as e:
        print(e)


# 直接起動された場合はmain()を起動(モジュールとして呼び出された場合は起動しないようにするため)
if __name__ == "__main__":
    main()