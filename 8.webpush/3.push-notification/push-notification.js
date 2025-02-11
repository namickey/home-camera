const webPush = require('web-push');
const fs = require('fs');

// VAPIDキーの読み込み
const vapidKeys = JSON.parse(fs.readFileSync('./vapid.json.key', 'utf8'));

// Push Subscriptionの読み込み
const subscription = JSON.parse(fs.readFileSync('./push-subscription.json.key', 'utf8'));

// VAPID設定
webPush.setVapidDetails(
    vapidKeys['mailto'],
    vapidKeys['public-key'],
    vapidKeys['private-key']
);

// 通知内容
const notification = {
    title: 'テスト通知',
    body: 'これはテスト通知です'
};

// 通知送信
webPush.sendNotification(subscription, JSON.stringify(notification))
    .then(() => {
        console.log('通知を送信しました');
        process.exit(0);
    })
    .catch(err => {
        console.error('通知の送信に失敗しました:', err);
        process.exit(1);
    });