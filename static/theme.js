/* ═══════════════════════════════════════════════════
   Theme Toggle – Light / Dark mode with localStorage
   ═══════════════════════════════════════════════════ */
(function () {
    const STORAGE_KEY = 'srm-attendance-theme';

    // Apply saved theme instantly (before paint) to avoid flash
    const saved = localStorage.getItem(STORAGE_KEY);
    if (saved) document.documentElement.setAttribute('data-theme', saved);

    document.addEventListener('DOMContentLoaded', function () {
        const btn = document.getElementById('themeToggle');
        if (!btn) return;

        function update() {
            const current = document.documentElement.getAttribute('data-theme');
            btn.textContent = current === 'dark' ? '☀️' : '🌙';
            btn.title       = current === 'dark' ? 'Switch to Light Mode' : 'Switch to Dark Mode';
        }

        btn.addEventListener('click', function () {
            const current = document.documentElement.getAttribute('data-theme');
            const next = current === 'dark' ? 'light' : 'dark';
            document.documentElement.setAttribute('data-theme', next);
            localStorage.setItem(STORAGE_KEY, next);
            update();
        });

        update();
    });
})();
