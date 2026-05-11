/* =========================================================
   SIMON EXPRESS — site-wide behavior
   - Mobile nav toggle
   - Quote / Application modals (open from any [data-open-quote] or [data-open-apply] CTA)
   - Form submission via /api/submit-form (with mailto: fallback)
   - Scroll-reveal animations using IntersectionObserver
   - Active nav link highlight
   ========================================================= */
(function () {
  'use strict';

  // ===== MOBILE NAV =====
  function initNav() {
    var nav = document.querySelector('[data-nav]');
    var toggle = document.querySelector('[data-nav-toggle]');
    if (!nav || !toggle) return;
    toggle.addEventListener('click', function () {
      var open = nav.classList.toggle('is-open');
      toggle.setAttribute('aria-expanded', String(open));
    });
  }

  // ===== ACTIVE NAV LINK =====
  function initActiveNav() {
    var path = window.location.pathname.replace(/\/$/, '') || '/';
    var page = path.split('/').pop() || 'index.html';
    if (page === '') page = 'index.html';
    document.querySelectorAll('[data-nav-link]').forEach(function (a) {
      var href = a.getAttribute('href') || '';
      var hrefPage = href.split('/').pop();
      if (
        (page === 'index.html' && (href === '/' || href === 'index.html' || href === './' || href === '')) ||
        (hrefPage && hrefPage === page)
      ) {
        a.classList.add('active');
      }
    });
  }

  // ===== MODAL =====
  var lastFocus = null;
  function openModal(id) {
    var m = document.getElementById(id);
    if (!m) return;
    lastFocus = document.activeElement;
    m.classList.add('is-open');
    m.setAttribute('aria-hidden', 'false');
    document.body.style.overflow = 'hidden';
    var firstInput = m.querySelector('input, select, textarea, button');
    if (firstInput) setTimeout(function () { firstInput.focus(); }, 50);
  }
  function closeModal(m) {
    m.classList.remove('is-open');
    m.setAttribute('aria-hidden', 'true');
    document.body.style.overflow = '';
    if (lastFocus && lastFocus.focus) lastFocus.focus();
  }
  function initModals() {
    document.querySelectorAll('[data-open-quote]').forEach(function (b) {
      b.addEventListener('click', function (e) {
        e.preventDefault();
        openModal('modal-quote');
      });
    });
    document.querySelectorAll('[data-open-apply]').forEach(function (b) {
      b.addEventListener('click', function (e) {
        e.preventDefault();
        openModal('modal-apply');
      });
    });
    document.querySelectorAll('.modal-overlay').forEach(function (m) {
      m.addEventListener('click', function (e) {
        if (e.target === m) closeModal(m);
      });
      m.querySelectorAll('[data-modal-close]').forEach(function (b) {
        b.addEventListener('click', function () { closeModal(m); });
      });
    });
    document.addEventListener('keydown', function (e) {
      if (e.key === 'Escape') {
        var open = document.querySelector('.modal-overlay.is-open');
        if (open) closeModal(open);
      }
    });
  }

  // ===== FORMS =====
  // Submits to /api/submit-form (Vercel serverless function);
  // falls back to mailto: if the API isn't reachable.
  // Injects honeypot + timestamp fields into every form on the page.
  // Real users never see them. Bots fill the honeypot (they fill every input),
  // and bots without JS execution leave the timestamp empty/stale. Server
  // (api/submit-form.js) checks both and silently rejects matches.
  function injectBotDefense() {
    var now = String(Date.now());
    document.querySelectorAll('form[data-simon-form]').forEach(function (form) {
      if (form.querySelector('input[name="website"][data-bot-defense]')) return;
      var wrap = document.createElement('div');
      wrap.setAttribute('aria-hidden', 'true');
      wrap.style.cssText = 'position:absolute;left:-10000px;top:auto;width:1px;height:1px;overflow:hidden;';
      wrap.innerHTML =
        '<label for="hp-' + Math.random().toString(36).slice(2, 8) + '">Leave blank</label>' +
        '<input type="text" name="website" tabindex="-1" autocomplete="off" value="" data-bot-defense />';
      form.appendChild(wrap);
      var ts = document.createElement('input');
      ts.type = 'hidden';
      ts.name = '_t';
      ts.value = now;
      ts.setAttribute('data-bot-defense', '');
      form.appendChild(ts);
    });
  }
  function initForms() {
    injectBotDefense();
    document.querySelectorAll('form[data-simon-form]').forEach(function (form) {
      form.addEventListener('submit', function (e) {
        e.preventDefault();
        submitForm(form);
      });
    });
  }

  function submitForm(form) {
    // Validate required
    var ok = true;
    form.querySelectorAll('[required]').forEach(function (input) {
      var field = input.closest('.field');
      if (!input.value.trim()) {
        if (field) field.classList.add('has-error');
        ok = false;
      } else {
        if (field) field.classList.remove('has-error');
      }
    });
    if (!ok) {
      var first = form.querySelector('.field.has-error input, .field.has-error select, .field.has-error textarea');
      if (first) first.focus();
      return;
    }

    var status = form.querySelector('.form-status');
    var submitBtn = form.querySelector('button[type="submit"]');
    var originalLabel = submitBtn ? submitBtn.innerHTML : '';
    if (submitBtn) {
      submitBtn.disabled = true;
      submitBtn.innerHTML = 'Sending&hellip;';
    }
    if (status) {
      status.className = 'form-status';
      status.textContent = '';
    }

    var data = {};
    new FormData(form).forEach(function (v, k) { data[k] = v; });
    data.formType = form.getAttribute('data-simon-form') || 'general';
    data.submittedAt = new Date().toISOString();
    data.userAgent = navigator.userAgent;
    data.pageUrl = window.location.href;

    fetch('/api/submit-form', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(data),
    })
      .then(function (r) {
        if (!r.ok) throw new Error('API ' + r.status);
        return r.json();
      })
      .then(function () {
        if (status) {
          status.className = 'form-status success';
          status.textContent = "Thanks — we got it. Someone from Simon will be in touch within one business day. For urgent freight, call 801-260-7010.";
        }
        form.reset();
        if (submitBtn) {
          submitBtn.disabled = false;
          submitBtn.innerHTML = originalLabel;
        }
      })
      .catch(function () {
        // Fallback: mailto with body
        var subjectMap = {
          quote:   'Freight Quote Request',
          apply:   'Driver Application',
          contact: 'Website Contact'
        };
        var subject = subjectMap[data.formType] || 'Website Inquiry';
        var bodyLines = Object.keys(data)
          .filter(function (k) { return k !== 'userAgent' && k !== 'pageUrl' && k !== 'submittedAt'; })
          .map(function (k) { return k + ': ' + data[k]; });
        bodyLines.push('');
        bodyLines.push('— Submitted ' + data.submittedAt);
        bodyLines.push('Page: ' + data.pageUrl);
        var href = 'mailto:info@simonexpress.com'
          + '?subject=' + encodeURIComponent(subject)
          + '&body=' + encodeURIComponent(bodyLines.join('\n'));
        if (status) {
          status.className = 'form-status success';
          status.innerHTML = "We're routing this through your email app. Click <a href='" + href + "' style='color:inherit;text-decoration:underline;'>here</a> if it didn't open automatically, or call 801-260-7010.";
        }
        window.location.href = href;
        if (submitBtn) {
          submitBtn.disabled = false;
          submitBtn.innerHTML = originalLabel;
        }
      });
  }

  // ===== SCROLL REVEALS =====
  function initReveals() {
    if (!('IntersectionObserver' in window)) {
      document.querySelectorAll('.reveal, .reveal-stagger').forEach(function (el) {
        el.classList.add('is-visible');
      });
      return;
    }
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (entry.isIntersecting) {
          entry.target.classList.add('is-visible');
          io.unobserve(entry.target);
        }
      });
    }, { threshold: 0.12, rootMargin: '0px 0px -60px 0px' });

    document.querySelectorAll('.reveal, .reveal-stagger').forEach(function (el) {
      io.observe(el);
    });
  }

  // ===== INIT =====
  function init() {
    initNav();
    initActiveNav();
    initModals();
    initForms();
    initReveals();
    // Year stamp
    document.querySelectorAll('[data-year]').forEach(function (el) {
      el.textContent = new Date().getFullYear();
    });
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();
