/* ═══════════════════════════════════════════════════════════════
   GreenTrack – Frontend Application Logic
   Shared utilities: API layer, auth, theme toggle, toasts, nav
   ═══════════════════════════════════════════════════════════════ */

const GreenTrack = (() => {
  'use strict';

  const API_BASE = '';  // Same-origin — Flask serves frontend

  // ── API Helper ──────────────────────────────────────────
  async function api(path, options = {}) {
    const defaults = {
      headers: { 'Content-Type': 'application/json' },
      credentials: 'same-origin',   // Send cookies
    };
    const config = { ...defaults, ...options };
    if (options.headers) {
      config.headers = { ...defaults.headers, ...options.headers };
    }
    return fetch(API_BASE + path, config);
  }

  // ── Toast Notifications ─────────────────────────────────
  function toast(message, type = 'info') {
    const container = document.getElementById('toastContainer');
    if (!container) return;

    const el = document.createElement('div');
    el.className = `toast ${type}`;
    const icons = { success: '✓', error: '✗', info: 'ℹ' };
    el.innerHTML = `<span>${icons[type] || 'ℹ'}</span> ${escapeHtml(message)}`;
    container.appendChild(el);

    setTimeout(() => {
      el.classList.add('exit');
      setTimeout(() => el.remove(), 300);
    }, 3500);
  }

  // ── HTML Escaping (XSS prevention) ──────────────────────
  function escapeHtml(str) {
    if (typeof str !== 'string') return '';
    const map = { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' };
    return str.replace(/[&<>"']/g, c => map[c]);
  }

  // ── Form Error Helpers ──────────────────────────────────
  function showFieldError(id, msg) {
    const el = document.getElementById(id);
    if (el) {
      el.textContent = msg;
      el.classList.remove('hidden');
      el.previousElementSibling?.classList.add('error');
    }
  }

  function hideFieldError(id) {
    const el = document.getElementById(id);
    if (el) {
      el.textContent = '';
      el.classList.add('hidden');
      el.previousElementSibling?.classList.remove('error');
    }
  }

  // ── Theme Toggle ────────────────────────────────────────
  function initTheme() {
    const saved = localStorage.getItem('greentrack_theme');
    if (saved === 'dark') {
      document.documentElement.setAttribute('data-theme', 'dark');
    }
    updateThemeIcon();
  }

  function toggleTheme() {
    const current = document.documentElement.getAttribute('data-theme');
    const next = current === 'dark' ? 'light' : 'dark';
    document.documentElement.setAttribute('data-theme', next === 'dark' ? 'dark' : '');
    if (next === 'dark') {
      document.documentElement.setAttribute('data-theme', 'dark');
    } else {
      document.documentElement.removeAttribute('data-theme');
    }
    localStorage.setItem('greentrack_theme', next);
    updateThemeIcon();
  }

  function updateThemeIcon() {
    const btn = document.getElementById('themeToggle');
    if (!btn) return;
    const isDark = document.documentElement.getAttribute('data-theme') === 'dark';
    btn.textContent = isDark ? '☀️' : '🌙';
  }

  // ── Mobile Nav Toggle ───────────────────────────────────
  function initNav() {
    const toggle = document.getElementById('navToggle');
    const links = document.getElementById('navLinks');
    if (toggle && links) {
      toggle.addEventListener('click', () => {
        links.classList.toggle('open');
      });
      // Close on link click
      links.querySelectorAll('a').forEach(a => {
        a.addEventListener('click', () => links.classList.remove('open'));
      });
    }
  }

  // ── Scroll Navbar Shadow ────────────────────────────────
  function initScrollShadow() {
    const nav = document.getElementById('main-nav');
    if (!nav) return;
    window.addEventListener('scroll', () => {
      if (window.scrollY > 10) {
        nav.style.boxShadow = '0 4px 20px rgba(0,0,0,0.08)';
      } else {
        nav.style.boxShadow = 'none';
      }
    }, { passive: true });
  }

  // ── Initialize ──────────────────────────────────────────
  function init() {
    initTheme();
    initNav();
    initScrollShadow();

    // Theme toggle button
    const themeBtn = document.getElementById('themeToggle');
    if (themeBtn) {
      themeBtn.addEventListener('click', toggleTheme);
    }
  }

  // Run on DOM ready
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }

  // ── Public API ──────────────────────────────────────────
  return {
    api,
    toast,
    escapeHtml,
    showFieldError,
    hideFieldError,
    toggleTheme,
  };
})();
