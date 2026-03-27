/* index.js – Homepage Animations */
(function() {
  'use strict';
  const container = document.getElementById('leavesContainer');
  const emojis = ['🍃', '🌿', '☘️', '🌱', '🍀'];
  if (!container) return;
  for (let i = 0; i < 12; i++) {
    const leaf = document.createElement('span');
    leaf.className = 'leaf';
    leaf.textContent = emojis[Math.floor(Math.random() * emojis.length)];
    leaf.style.left = Math.random() * 100 + '%';
    leaf.style.animationDuration = (8 + Math.random() * 12) + 's';
    leaf.style.animationDelay = Math.random() * 10 + 's';
    leaf.style.fontSize = (1 + Math.random() * 1.5) + 'rem';
    container.appendChild(leaf);
  }
})();
