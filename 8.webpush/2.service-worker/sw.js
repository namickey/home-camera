self.addEventListener('push', (event) => {
    // ここでプッシュ通知をハンドリング
    const data = event.data?.json() || {};
    event.waitUntil(
        // 通知を表示
        self.registration.showNotification(data.title, {
            body: data.body
        })
    );
  });
