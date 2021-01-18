var shop_code = document.getElementById('shop-code');
var items_num = document.getElementById('items-num');
var get_items_btn = document.getElementById('get-items-btn');
var order_select = document.getElementById('order-select');
var result_area = document.getElementById('result-area');

// 0埋め関数
function zeroPadding(num,length){
    return ('0000000000' + num).slice(-length);
}

// 全角判定関数
function isZenkaku(str) {
    return (String(str).match(/[\x01-\x7E\uFF65-\uFF9F]/)) ? false : true;
}

// 全角→半角関数
function toHalfWidth(value) {
  return value.replace(/./g, s => {
    return String.fromCharCode(s.charCodeAt(0) - 0xfee0)
  })
}

async function get_rakuten_items() {
    let ret = await eel.get_rakuten_items(code, amount, order_select.value)();
    return ret;
}

// 商品取得ボタンクリックイベント
get_items_btn.addEventListener('click', () => {
    // ユーザー入力は全角も対応
    // code = document.registerform.item_code.value;
    code = shop_code.value;
    // amount = document.registerform.item_amount.value;
    amount = items_num.value;
    if (isZenkaku(code)) {
        code = toHalfWidth(code)
    }

    if (isZenkaku(amount)) {
        amount = toHalfWidth(amount)
    }

    if (code && amount && isNaN(amount)==false) {
        result_area.value = "取得開始しました.\n";
        // pythonから楽天APIの関数を呼ぶ
            promise = get_rakuten_items(code, amount, order_select.value);
            promise.then((ret) => {
                if(ret==0){
                    result_area.value += "CSV出力しました.\n"
                }
                else{
                    result_area.value += "失敗しました.入力内容を確認してください.\n"
                    result_area.value += ret
                }

            });
    }
    else {
        window.alert("ショップコードと個数を入力してください.");
    }
})