/* login.js – Auth Logic */
document.addEventListener('DOMContentLoaded', () => {
    'use strict';
    const tabLogin = document.getElementById('tabLogin');
    const tabSignup = document.getElementById('tabSignup');
    const loginForm = document.getElementById('loginForm');
    const signupForm = document.getElementById('signupForm');
    const authTitle = document.getElementById('authTitle');
    const authSubtitle = document.getElementById('authSubtitle');

    function showTab(tab) {
        if (tab === 'login') {
            tabLogin.classList.add('active');
            tabSignup.classList.remove('active');
            loginForm.classList.remove('hidden');
            signupForm.classList.add('hidden');
            authTitle.textContent = 'Welcome Back 👋';
            authSubtitle.textContent = 'Sign in to your GreenTrack account';
        } else {
            tabSignup.classList.add('active');
            tabLogin.classList.remove('active');
            signupForm.classList.remove('hidden');
            loginForm.classList.add('hidden');
            authTitle.textContent = 'Join GreenTrack 🌱';
            authSubtitle.textContent = 'Create your account and start tracking';
        }
    }

    if(tabLogin) tabLogin.addEventListener('click', () => showTab('login'));
    if(tabSignup) tabSignup.addEventListener('click', () => showTab('signup'));

    // Check URL hash
    if (window.location.hash === '#signup') showTab('signup');

    // ── Login ─────────────────────────────────────
    if(loginForm) {
      loginForm.addEventListener('submit', async (e) => {
          e.preventDefault();
          const username = document.getElementById('loginUsername').value.trim();
          const password = document.getElementById('loginPassword').value;

          if (!username || !password) {
              GreenTrack.toast('Please fill in all fields', 'error');
              return;
          }

          const btn = document.getElementById('loginBtn');
          btn.disabled = true;
          btn.textContent = 'Signing in...';

          try {
              const res = await GreenTrack.api('/api/login', {
                  method: 'POST',
                  body: JSON.stringify({ username, password }),
              });

              if (res.ok) {
                  const data = await res.json();
                  localStorage.setItem('greentrack_user', JSON.stringify(data.user));
                  GreenTrack.toast('Login successful!', 'success');
                  setTimeout(() => window.location.href = 'dashboard.html', 800);
              } else {
                  const err = await res.json();
                  GreenTrack.toast(err.error || 'Login failed', 'error');
              }
          } catch (error) {
              GreenTrack.toast('Network error. Please try again.', 'error');
          } finally {
              btn.disabled = false;
              btn.textContent = 'Sign In →';
          }
      });
    }

    // ── Signup ────────────────────────────────────
    if(signupForm) {
      signupForm.addEventListener('submit', async (e) => {
          e.preventDefault();
          const username = document.getElementById('signupUsername').value.trim();
          const email = document.getElementById('signupEmail').value.trim();
          const password = document.getElementById('signupPassword').value;
          const confirm = document.getElementById('signupConfirm').value;

          // Client-side validation
          let hasError = false;

          if (username.length < 3 || !/^[a-zA-Z0-9_]+$/.test(username)) {
              GreenTrack.showFieldError('signupUsernameError', 'Username must be 3+ chars (letters, numbers, underscores)');
              hasError = true;
          } else {
              GreenTrack.hideFieldError('signupUsernameError');
          }

          const emailPattern = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
          if (!emailPattern.test(email)) {
              GreenTrack.showFieldError('signupEmailError', 'Please enter a valid email');
              hasError = true;
          } else {
              GreenTrack.hideFieldError('signupEmailError');
          }

          if (password.length < 8 || !/[A-Za-z]/.test(password) || !/\d/.test(password)) {
              GreenTrack.showFieldError('signupPasswordError', 'Min 8 chars with at least 1 letter and 1 number');
              hasError = true;
          } else {
              GreenTrack.hideFieldError('signupPasswordError');
          }

          if (password !== confirm) {
              GreenTrack.showFieldError('signupConfirmError', 'Passwords do not match');
              hasError = true;
          } else {
              GreenTrack.hideFieldError('signupConfirmError');
          }

          if (hasError) return;

          const btn = document.getElementById('signupBtn');
          btn.disabled = true;
          btn.textContent = 'Creating account...';

          try {
              const res = await GreenTrack.api('/api/register', {
                  method: 'POST',
                  body: JSON.stringify({ username, email, password }),
              });

              if (res.ok) {
                  GreenTrack.toast('Account created! Please sign in.', 'success');
                  setTimeout(() => showTab('login'), 1000);
              } else {
                  const err = await res.json();
                  GreenTrack.toast(err.error || 'Registration failed', 'error');
              }
          } catch (error) {
              GreenTrack.toast('Network error. Please try again.', 'error');
          } finally {
              btn.disabled = false;
              btn.textContent = 'Create Account 🌱';
          }
      });
    }
});
