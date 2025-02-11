#!/bin/bash

# 過去送信で使用していない、ユニークなIDを取得
uuid=$(< /proc/sys/kernel/random/uuid)

# 送信（コマンド内で使用する変数については、事前に環境変数に設定しておく）
curl -v -X POST https://api.line.me/v2/bot/message/push \
-H 'Content-Type: application/json' \
-H "Authorization: Bearer $LINE_TOKEN_MAMA" \
-H "X-Line-Retry-Key: $uuid" \
-d '{
    "to": "'$LINE_USER_ID_MAMA'",
    "messages":[
        {
            "type":"text",
            "text":"わかは家を出発しました。"
        }
    ]
}'
