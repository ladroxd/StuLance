// ── Click sound ───────────────────────────────────────────
(function () {
    let ctx = null;

    function playKick() {
        if (!ctx) ctx = new (window.AudioContext || window.webkitAudioContext)();
        if (ctx.state === 'suspended') ctx.resume();

        const now = ctx.currentTime;

        const osc = ctx.createOscillator();
        const gain = ctx.createGain();

        osc.type = 'sine';
        osc.frequency.setValueAtTime(120, now);
        osc.frequency.exponentialRampToValueAtTime(40, now + 0.08);

        gain.gain.setValueAtTime(0.35, now);
        gain.gain.exponentialRampToValueAtTime(0.001, now + 0.12);

        osc.connect(gain);
        gain.connect(ctx.destination);

        osc.start(now);
        osc.stop(now + 0.12);
    }

    document.addEventListener('click', function (e) {
        const el = e.target.closest('a, button, [role="button"], .btn, input[type="submit"], input[type="button"], label[for]');
        if (el) playKick();
    });
})();

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
