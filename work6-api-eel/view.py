import eel
import desktop
import numpy as np
import pandas as pd
from rakuten_searcher import RakutenSearcher

@eel.expose
def get_rakuten_items(code, amount, order_select):
    searcher=RakutenSearcher()
    return searcher.search(code, amount, order_select)

@eel.expose
def export_rakuten_items():
    return searcher.export()

def main():
    start_dir="web"
    end_point="index.html"
    size=(430,500)
    desktop.start(start_dir, end_point, size)

if __name__ == "__main__":
    main()
