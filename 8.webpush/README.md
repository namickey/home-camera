##　1.generate-vapid-keys

秘密鍵と公開鍵の生成
```shell
npm install web-push
npx web-push generate-vapid-keys
```

## 2.python web server
WEBサーバを起動し、`http://localhost:8000`を開く
`Push通知を許可する`ボタンを押す


### subscribe時にエラーとなる場合
以下、メッセージが表示された場合、readyの実装を追加する。  
`Subscription failed - no active Service Worker`  
https://stackoverflow.com/questions/42063006/failed-to-subscribe-the-user-domexception-subscription-failed-no-active-serv/42584178#42584178


### ブラウザ設定で、localhostの通知を許可
通知がブロックされているとsubscriveができないため、通知を許可する。


### Push Subscriptionの保管
ブラウザのコンソールログ出力されたjson形式の`Push Subscription`をテキストファイルに保管する。
コンソールログはブラウザでF12キーを押し、コンソールに出力されたログを参照する。

## 3.push通知

```shell
node push-notification.js
```

https://qiita.com/murasuke/items/b1df2f72e75524a816ed


## gas for post

ログ  
https://qiita.com/chihiro/items/09c996d41d80f0d30e17  

POST  
https://qiita.com/khidaka/items/ebf770591100b1eb0eff  




