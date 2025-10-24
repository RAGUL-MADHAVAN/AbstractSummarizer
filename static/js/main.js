// Global JS for small UX improvements
(function () {
  document.addEventListener('DOMContentLoaded', function () {
    // Enable Bootstrap tooltips
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function (tooltipTriggerEl) {
      return new bootstrap.Tooltip(tooltipTriggerEl);
    });

    // Theme handling (Bootstrap 5.3)
    const root = document.documentElement;
    const toggleBtn = document.getElementById('themeToggle');

    function applyTheme(theme) {
      root.setAttribute('data-bs-theme', theme);
      if (toggleBtn) {
        const icon = toggleBtn.querySelector('i');
        const label = toggleBtn.querySelector('span');
        if (theme === 'dark') {
          if (icon) icon.className = 'far fa-sun me-1';
          if (label) label.textContent = 'Light';
          toggleBtn.classList.remove('btn-outline-light');
          toggleBtn.classList.add('btn-light');
        } else {
          if (icon) icon.className = 'far fa-moon me-1';
          if (label) label.textContent = 'Dark';
          toggleBtn.classList.remove('btn-light');
          toggleBtn.classList.add('btn-outline-light');
        }
      }
    }

    // Determine initial theme
    const stored = localStorage.getItem('theme');
    const prefersDark = window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches;
    const initialTheme = stored || (prefersDark ? 'dark' : 'light');
    applyTheme(initialTheme);

    // Toggle handler
    if (toggleBtn) {
      toggleBtn.addEventListener('click', function () {
        const current = root.getAttribute('data-bs-theme') === 'dark' ? 'dark' : 'light';
        const next = current === 'dark' ? 'light' : 'dark';
        localStorage.setItem('theme', next);
        applyTheme(next);
      });
    }
  });
})();
