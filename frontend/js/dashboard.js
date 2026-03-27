/* dashboard.js – Dashboard Logic */
document.addEventListener('DOMContentLoaded', () => {
  'use strict';
  
  // Auth check
  const user = JSON.parse(localStorage.getItem('greentrack_user') || 'null');
  if (!user) {
    window.location.href = 'login.html';
    return;
  }

  const greetingEl = document.getElementById('greetingText');
  const hour = new Date().getHours();
  let greeting = hour < 12 ? 'Good morning' : hour < 18 ? 'Good afternoon' : 'Good evening';
  greetingEl.textContent = `${greeting}, ${user.username}! 🌿`;

  document.getElementById('todayDate').textContent = new Date().toLocaleDateString('en-US', {
    weekday: 'long', year: 'numeric', month: 'long', day: 'numeric'
  });

  // Chart instances
  let weeklyChart = null;
  let categoryChart = null;

  // Load dashboard data
  async function loadDashboard() {
    try {
      const res = await GreenTrack.api('/api/user-data');
      if (res.status === 401) {
        localStorage.removeItem('greentrack_user');
        window.location.href = 'login.html';
        return;
      }
      if (!res.ok) throw new Error('Failed to load data');

      const data = await res.json();

      // Update stat cards
      document.getElementById('weeklyTotal').textContent = data.weekly_total.toFixed(1);
      document.getElementById('monthlyTotal').textContent = data.monthly_total.toFixed(1);

      // Green score animation
      const score = data.green_score;
      document.getElementById('greenScore').textContent = score;
      const circle = document.getElementById('scoreCircle');
      const dashOffset = 377 - (377 * score / 100);
      setTimeout(() => { 
        if(circle) {
          circle.style.transition = 'stroke-dashoffset 1.5s ease-out'; 
          circle.style.strokeDashoffset = dashOffset; 
        }
      }, 200);

      // Weekly bar chart
      const labels = Object.keys(data.daily_data);
      const values = Object.values(data.daily_data);

      const isDark = document.documentElement.getAttribute('data-theme') === 'dark';
      const textColor = isDark ? '#d1fae5' : '#064e3b';
      const gridColor = isDark ? 'rgba(209,250,229,0.1)' : 'rgba(6,78,59,0.08)';

      if (weeklyChart) weeklyChart.destroy();
      const weeklyCanvas = document.getElementById('weeklyChart');
      if (weeklyCanvas) {
        weeklyChart = new Chart(weeklyCanvas, {
          type: 'bar',
          data: {
            labels: labels,
            datasets: [{
              label: 'CO₂ (kg)',
              data: values,
              backgroundColor: [
                'rgba(16, 185, 129, 0.7)', 'rgba(20, 184, 166, 0.7)',
                'rgba(132, 204, 22, 0.7)', 'rgba(16, 185, 129, 0.7)',
                'rgba(20, 184, 166, 0.7)', 'rgba(132, 204, 22, 0.7)',
                'rgba(16, 185, 129, 0.7)'
              ],
              borderRadius: 8,
              borderSkipped: false,
            }]
          },
          options: {
            responsive: true, maintainAspectRatio: false,
            plugins: { legend: { display: false } },
            scales: {
              y: { beginAtZero: true, grid: { color: gridColor }, ticks: { color: textColor } },
              x: { grid: { display: false }, ticks: { color: textColor } }
            }
          }
        });
      }

      // Category pie chart
      const cat = data.category_breakdown;
      if (categoryChart) categoryChart.destroy();
      const categoryCanvas = document.getElementById('categoryChart');
      if (categoryCanvas) {
        categoryChart = new Chart(categoryCanvas, {
          type: 'doughnut',
          data: {
            labels: ['Travel', 'Electricity', 'Food'],
            datasets: [{
              data: [cat.travel, cat.electricity, cat.food],
              backgroundColor: ['#10b981', '#14b8a6', '#84cc16'],
              borderWidth: 0,
              hoverOffset: 8,
            }]
          },
          options: {
            responsive: true, maintainAspectRatio: false,
            cutout: '60%',
            plugins: {
              legend: { position: 'bottom', labels: { color: textColor, padding: 16, usePointStyle: true } }
            }
          }
        });
      }

      // Suggestions
      const suggList = document.getElementById('suggestionsList');
      if (suggList && data.suggestions && data.suggestions.length) {
        suggList.innerHTML = data.suggestions.map(s => `<div class="suggestion-item">${GreenTrack.escapeHtml(s)}</div>`).join('');
      }

      // Recent entries
      const entriesEl = document.getElementById('recentEntries');
      if (entriesEl && data.recent_entries && data.recent_entries.length) {
        const modeEmojis = { car: '🚗', bus: '🚌', bike: '🚲', walking: '🚶' };
        const foodEmojis = { veg: '🥬', 'non-veg': '🍖', vegan: '🌱' };
        let html = '<table style="width:100%;border-collapse:collapse;font-size:0.88rem;">';
        html += '<thead><tr style="border-bottom:2px solid var(--border-color);text-align:left;">';
        html += '<th style="padding:0.5rem;">Date</th><th style="padding:0.5rem;">Travel</th><th style="padding:0.5rem;">Distance</th><th style="padding:0.5rem;">Electricity</th><th style="padding:0.5rem;">Food</th>';
        html += '</tr></thead><tbody>';
        data.recent_entries.forEach(e => {
          html += `<tr style="border-bottom:1px solid var(--border-color);">`;
          html += `<td style="padding:0.5rem;">${e.entry_date}</td>`;
          html += `<td style="padding:0.5rem;">${modeEmojis[e.travel_mode] || ''} ${e.travel_mode}</td>`;
          html += `<td style="padding:0.5rem;">${e.distance} km</td>`;
          html += `<td style="padding:0.5rem;">${e.electricity_usage} units</td>`;
          html += `<td style="padding:0.5rem;">${foodEmojis[e.food_habit] || ''} ${e.food_habit}</td>`;
          html += `</tr>`;
        });
        html += '</tbody></table>';
        entriesEl.innerHTML = html;
      }

    } catch (err) {
      console.error('Dashboard load error:', err);
      GreenTrack.toast('Failed to load dashboard data', 'error');
    }
  }

  loadDashboard();

  // ── Entry form submit ──────────────────────────
  const entryForm = document.getElementById('entryForm');
  if (entryForm) {
    entryForm.addEventListener('submit', async (e) => {
      e.preventDefault();
      const travelMode = document.getElementById('travelMode').value;
      const distance = document.getElementById('distance').value;
      const electricity = document.getElementById('electricity').value;
      const foodHabit = document.getElementById('foodHabit').value;

      if (!travelMode || !distance || !electricity || !foodHabit) {
        GreenTrack.toast('Please fill in all fields', 'error');
        return;
      }

      const btn = document.getElementById('entryBtn');
      btn.disabled = true;
      btn.textContent = 'Saving...';

      try {
        const res = await GreenTrack.api('/api/add-entry', {
          method: 'POST',
          body: JSON.stringify({
            travel_mode: travelMode,
            distance: parseFloat(distance),
            electricity_usage: parseFloat(electricity),
            food_habit: foodHabit,
          }),
        });

        if (res.ok) {
          const data = await res.json();
          GreenTrack.toast(`Entry logged! Total: ${data.emissions.total_emission} kg CO₂`, 'success');
          entryForm.reset();
          loadDashboard();
        } else {
          const err = await res.json();
          GreenTrack.toast(err.error || 'Failed to add entry', 'error');
        }
      } catch (error) {
        GreenTrack.toast('Network error. Please try again.', 'error');
      } finally {
        btn.disabled = false;
        btn.textContent = '📝 Log Entry';
      }
    });
  }

  // ── Logout ─────────────────────────────────────
  const logoutBtn = document.getElementById('logoutBtn');
  if (logoutBtn) {
    logoutBtn.addEventListener('click', async (e) => {
      e.preventDefault();
      try {
        await GreenTrack.api('/api/logout', { method: 'POST' });
      } catch (_) {}
      localStorage.removeItem('greentrack_user');
      GreenTrack.toast('Logged out successfully', 'info');
      setTimeout(() => window.location.href = 'login.html', 600);
    });
  }
});
