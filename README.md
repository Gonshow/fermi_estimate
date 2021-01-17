# fermi_estimate
フェルミ推定のモデル化、計算実行フェーズを可視化するアプリです。
他にも、課題の深堀りの可視化や、工数の算出にも使えると思います。

こちらのページを参考に作りました。
https://blog.narito.ninja/detail/133
また、フェルミ推定の方法論やデモで行なっている解放は、
「現役東大生が書いた地頭を鍛えるフェルミ推定ノート」を参考にしました。
https://www.kinokuniya.co.jp/f/dsg-08-998494011X

ディレクトリ名やクラスが汚いので今後整理する予定です。

--実行方法--
gitでcloneし、
>> cd fermi_estimate/
python manage.py makemigrations blog
python manage.py migrate
python manage.py runserver
すると、
Starting development server at http://...../
とでるのでそこを開く。

moduleエラーはpipなどでinstallしてください

以下デモのキャプチャです。
<img width="1656" alt="スクリーンショット 2021-01-17 14 24 56" src="https://user-images.githubusercontent.com/38319910/104831860-d4681e80-58cf-11eb-91e1-720da967c7f7.png">
