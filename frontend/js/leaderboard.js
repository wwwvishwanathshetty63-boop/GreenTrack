/* leaderboard.js – Leaderboard Logic */
document.addEventListener('DOMContentLoaded', () => {
    'use strict';
    // Set nav auth state
    const user = JSON.parse(localStorage.getItem('greentrack_user') || 'null');
    const navAuth = document.getElementById('navAuth');
    if (navAuth) {
      if (user) {
          navAuth.innerHTML = '<a href="dashboard.html" class="btn btn-primary btn-sm">Dashboard</a>';
      } else {
          navAuth.innerHTML = '<a href="login.html" class="btn btn-primary btn-sm">Get Started</a>';
      }
    }

    // Load leaderboard
    async function loadLeaderboard() {
        const listEl = document.getElementById('leaderboardList');
        if (!listEl) return;
        try {
            const res = await GreenTrack.api('/api/leaderboard');
            if (!res.ok) throw new Error('Failed to load');
            const data = await res.json();

            if (!data.leaderboard || data.leaderboard.length === 0) {
                listEl.innerHTML = `
                <div style="text-align:center;padding:3rem 1rem;color:var(--text-muted);">
                    <div style="font-size:3rem;margin-bottom:1rem;">🌿</div>
                    <p style="font-size:1rem;font-weight:600;">No rankings yet this week</p>
                    <p style="font-size:0.9rem;margin-top:0.5rem;">Start logging your carbon entries to appear on the leaderboard!</p>
                </div>`;
                return;
            }

            const medals = ['🥇', '🥈', '🥉'];
            let html = '';
            data.leaderboard.forEach((item, idx) => {
                const medal = idx < 3 ? medals[idx] : '';
                const rankClass = idx < 3 ? `style="background:${['linear-gradient(135deg,#fbbf24,#f59e0b)','linear-gradient(135deg,#94a3b8,#64748b)','linear-gradient(135deg,#f97316,#ea580c)'][idx]};color:white;"` : `style="background:var(--bg-primary);color:var(--text-muted);"`;
                html += `
                <div class="leaderboard-item animate-in" style="animation-delay:${idx * 0.08}s;">
                    <div class="rank" ${rankClass}>${item.rank}</div>
                    <div class="user-info">
                        <div class="username">${medal} ${GreenTrack.escapeHtml(item.username)}</div>
                        <div class="user-score">Weekly emissions</div>
                    </div>
                    <div class="emission-value">${item.weekly_total.toFixed(1)} kg</div>
                </div>`;
            });
            listEl.innerHTML = html;

        } catch (err) {
            console.error('Leaderboard error:', err);
            listEl.innerHTML = `
            <div style="text-align:center;padding:2rem;color:var(--text-muted);">
                <p>Failed to load leaderboard. <a href="#" onclick="location.reload()">Try again</a></p>
            </div>`;
        }
    }

    loadLeaderboard();
});
