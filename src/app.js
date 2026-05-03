// Notification badge polling
async function updateNotifBadge() {
  try {
    const res = await fetch('/notifications/unread-count/');
    const data = await res.json();
    const badge = document.getElementById('notif-badge');
    if (badge) {
      if (data.count > 0) {
        badge.textContent = data.count;
        badge.classList.remove('d-none');
      } else {
        badge.classList.add('d-none');
      }
    }
  } catch (_) {}
}

if (document.getElementById('notif-bell')) {
  updateNotifBadge();
  setInterval(updateNotifBadge, 30000);
}
