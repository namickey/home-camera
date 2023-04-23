

uuid=$(< /proc/sys/kernel/random/uuid)
curl -v -X POST https://api.line.me/v2/bot/message/push \
-H 'Content-Type: application/json' \
-H "Authorization: Bearer $line_home_Bearer" \
-H "X-Line-Retry-Key: $uuid" \
-d '{
    "to": "'$line_home_userid'",
    "messages":[
        {
            "type":"text",
            "text":"home image"
        },
        {
            "type": "image",
            "originalContentUrl": "xxxx",
            "previewImageUrl": "xxxx"
        }
    ]
}'

