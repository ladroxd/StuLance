// Badge polling — called from base.html inline script
async function updateNotifBadge() {
    try {
        const res = await fetch('/notifications/unread-count/');
        const data = await res.json();
        const badge = document.getElementById('notif-badge');
        if (!badge) return;
        if (data.count > 0) {
            badge.textContent = data.count > 99 ? '99+' : data.count;
            badge.classList.remove('d-none');
        } else {
            badge.classList.add('d-none');
        }
    } catch (e) {}
}
