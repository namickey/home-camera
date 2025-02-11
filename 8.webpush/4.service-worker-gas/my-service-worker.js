// (Service Workerの最低限の内容)
self.addEventListener('push', (event) => {
    // ここでプッシュ通知をハンドリングできます
    console.log('Push received:', event);
    const data = event.data?.json() || {};
    event.waitUntil(
        self.registration.showNotification(data.title || "ママより", {
            body: data.body || "わかメールが届いています"
        })
    );
  });
