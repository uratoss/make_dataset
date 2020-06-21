import urllib.request
import zipfile
import re
import argparse
import os

parser = argparse.ArgumentParser()

parser.add_argument('url',help ='download url from https://www.aozora.gr.jp/*')
parser.add_argument('-o','--out_path',default='./',help='output path of download file')
args = parser.parse_args()

# zipファイルダウンロード
zip_name = args.url.split("/")[-1]

urllib.request.urlretrieve(args.url, zip_name)

# ダウンロードしたzipの解凍
with zipfile.ZipFile(zip_name, 'r') as myzip:
    myzip.extractall()
    # 解凍後のファイルからデータ読み込み
    for myfile in myzip.infolist():
        file_name = myfile.filename
        with open(file_name, encoding='sjis') as file:
            text = file.read()
os.remove(zip_name)
os.remove(file_name)

# ファイル整形
# ヘッダ部分の除去
text = re.split('\-{5,}',text)[2]
# フッタ部分の除去
text = re.split('底本：',text)[0]
# | の除去
text = text.replace('|', '')
# ルビの削除
text = re.sub('《.+?》', '', text)
# 入力注の削除
text = re.sub('［＃.+?］', '',text)
# 空行の削除
#text = re.sub('\n\n', '\n', text) 
#text = re.sub('\r', '', text)

# 整形結果確認
# 頭の100文字の表示 
print(text[:100], end = '\n\n')
# 後ろの100文字の表示 
print(text[-100:])
with open(args.out_path + file_name, 'w') as f:
    print(text,file=f)
