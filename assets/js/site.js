/* ==========================================================================
   Digital Autonomous — site behaviour
   No dependencies, no third-party network calls.
   ========================================================================== */
(function () {
  'use strict';

  var reduceMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  var $  = function (s, r) { return (r || document).querySelector(s); };
  var $$ = function (s, r) { return Array.prototype.slice.call((r || document).querySelectorAll(s)); };

  /* ------------------------------------------------------------------ *
   * Conversion tracking
   *
   * Privacy-conscious by construction: this ships NO third-party script
   * and sets NO cookies. Every event is pushed to window.dataLayer and
   * re-dispatched as a DOM CustomEvent ('da:track').
   *
   * To connect an analytics provider later, subscribe to that event —
   * e.g. for Plausible (cookieless):
   *   addEventListener('da:track', e => plausible(e.detail.event, {props: e.detail}));
   * ------------------------------------------------------------------ */
  window.dataLayer = window.dataLayer || [];

  function track(eventName, props) {
    var payload = Object.assign({ event: eventName }, props || {});
    try {
      window.dataLayer.push(payload);
      window.dispatchEvent(new CustomEvent('da:track', { detail: payload }));
    } catch (err) { /* tracking must never break the page */ }
  }
  window.daTrack = track;

  // Declarative tracking: data-track="name" plus optional data-track-* props.
  document.addEventListener('click', function (e) {
    var el = e.target.closest ? e.target.closest('[data-track]') : null;
    if (el) {
      var props = { location: el.getAttribute('data-track-location') || 'page' };
      if (el.getAttribute('data-track-label')) props.label = el.getAttribute('data-track-label');
      track(el.getAttribute('data-track'), props);
      return;
    }
    // Untagged contact links still count.
    var a = e.target.closest ? e.target.closest('a[href^="mailto:"], a[href^="tel:"]') : null;
    if (a) {
      var href = a.getAttribute('href');
      track(href.indexOf('tel:') === 0 ? 'telephone_click' : 'email_click', { value: href });
    }
  }, true);

  /* ------------------------------------------------------------------ *
   * Header
   * ------------------------------------------------------------------ */
  var hdr = $('#hdr');
  if (hdr) {
    var onScroll = function () { hdr.classList.toggle('scrolled', window.scrollY > 8); };
    addEventListener('scroll', onScroll, { passive: true });
    onScroll();
  }

  /* ------------------------------------------------------------------ *
   * Mobile drawer
   * ------------------------------------------------------------------ */
  var menuBtn = $('#menuBtn');
  var menu = $('#mobileMenu');
  if (menuBtn && menu) {
    var setMenu = function (open) {
      menu.classList.toggle('open', open);
      menuBtn.setAttribute('aria-expanded', String(open));
      document.body.classList.toggle('no-scroll', open);
    };
    menuBtn.addEventListener('click', function () {
      setMenu(!menu.classList.contains('open'));
    });
    $$('a', menu).forEach(function (a) {
      a.addEventListener('click', function () { setMenu(false); });
    });
    addEventListener('keydown', function (e) {
      if (e.key === 'Escape' && menu.classList.contains('open')) {
        setMenu(false);
        menuBtn.focus();
      }
    });
    // A resize past the desktop breakpoint must not leave the body locked.
    addEventListener('resize', function () {
      if (window.innerWidth > 820 && menu.classList.contains('open')) setMenu(false);
    });
  }

  /* ------------------------------------------------------------------ *
   * Desktop nav dropdowns — pointer and keyboard
   * ------------------------------------------------------------------ */
  var navItems = $$('.nav-item');
  navItems.forEach(function (item) {
    var btn = $('button', item);
    if (!btn) return;
    var closeTimer;

    var open = function (state) {
      item.classList.toggle('open', state);
      btn.setAttribute('aria-expanded', String(state));
    };

    btn.addEventListener('click', function (e) {
      e.stopPropagation();
      var isOpen = item.classList.contains('open');
      navItems.forEach(function (o) { if (o !== item) o.classList.remove('open'); });
      open(!isOpen);
    });
    item.addEventListener('mouseenter', function () { clearTimeout(closeTimer); open(true); });
    item.addEventListener('mouseleave', function () {
      closeTimer = setTimeout(function () { open(false); }, 140);
    });
    item.addEventListener('focusout', function (e) {
      if (!item.contains(e.relatedTarget)) open(false);
    });
    item.addEventListener('keydown', function (e) {
      if (e.key === 'Escape') { open(false); btn.focus(); }
    });
  });
  document.addEventListener('click', function () {
    navItems.forEach(function (o) { o.classList.remove('open'); });
  });

  /* ------------------------------------------------------------------ *
   * Reveal on scroll
   * ------------------------------------------------------------------ */
  var reveals = $$('.reveal');
  if (reduceMotion || !('IntersectionObserver' in window)) {
    reveals.forEach(function (el) { el.classList.add('in'); });
  } else {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (e, i) {
        if (!e.isIntersecting) return;
        var delay = Math.min(i, 4) * 70;
        setTimeout(function () { e.target.classList.add('in'); }, delay);
        io.unobserve(e.target);
      });
    }, { threshold: 0.12, rootMargin: '0px 0px -40px 0px' });
    reveals.forEach(function (el) { io.observe(el); });
  }

  /* ------------------------------------------------------------------ *
   * Hero panel — illustrative pipeline
   * One clock drives the pulse and the nodes: the line fills to each
   * circle and the circle lights the moment the pulse arrives.
   * ------------------------------------------------------------------ */
  (function heroPipeline() {
    var flowLine = $('.flow-line');
    var fillLine = $('.flow-fill');
    var steps = $$('.flow .step');
    if (!flowLine || !fillLine || !steps.length) return;

    if (reduceMotion) {
      fillLine.style.height = '100%';
      steps.forEach(function (s) { s.classList.add('on'); });
      return;
    }

    var TRAVEL = 850; // matches the CSS transition on .flow-fill
    var wait = function (ms) { return new Promise(function (r) { setTimeout(r, ms); }); };
    // Stop at the circle's top edge, not its centre, so the fill meets each
    // node instead of ending inside it.
    var nodeY = function (step) {
      var lr = flowLine.getBoundingClientRect();
      var nr = step.querySelector('.node').getBoundingClientRect();
      return Math.max(0, nr.top - lr.top);
    };

    var running = true;
    document.addEventListener('visibilitychange', function () {
      running = !document.hidden;
    });

    async function run() {
      while (true) {
        if (!running) { await wait(400); continue; }
        for (var k = 0; k < steps.length; k++) {
          fillLine.style.height = nodeY(steps[k]) + 'px';
          await wait(TRAVEL);
          steps[k].classList.add('on');
          await wait(650);
        }
        await wait(1400);
        fillLine.style.height = '0px';
        steps.forEach(function (s) { s.classList.remove('on'); });
        await wait(950);
      }
    }
    requestAnimationFrame(function () { requestAnimationFrame(run); });
  })();

  /* ------------------------------------------------------------------ *
   * "See Automation in Action" — visitor-driven demo player
   * ------------------------------------------------------------------ */
  (function demoPlayer() {
    var stage = $('#demoStage');
    if (!stage) return;

    var steps    = $$('.dstep', stage);
    var bar      = $('#demoProgress');
    var playBtn  = $('#demoPlay');
    var resetBtn = $('#demoReset');
    if (!steps.length) return;

    var idx = -1, timer = null, playing = false;
    var STEP_MS = 1900;

    function render() {
      steps.forEach(function (s, i) {
        s.classList.toggle('active', i === idx);
        s.classList.toggle('done', i < idx);
      });
      if (bar) bar.style.width = ((idx + 1) / steps.length * 100) + '%';
      if (playBtn) {
        playBtn.setAttribute('aria-pressed', String(playing));
        $('.label', playBtn).textContent = playing ? 'Pause' : (idx >= steps.length - 1 ? 'Replay' : 'Play');
        $('.icon-play', playBtn).style.display  = playing ? 'none' : '';
        $('.icon-pause', playBtn).style.display = playing ? '' : 'none';
      }
    }

    function advance() {
      if (idx >= steps.length - 1) { stop(); return; }
      idx += 1;
      render();
      timer = setTimeout(advance, STEP_MS);
    }
    function stop() {
      playing = false;
      clearTimeout(timer);
      timer = null;
      render();
    }
    function play() {
      if (idx >= steps.length - 1) idx = -1;
      playing = true;
      render();
      advance();
      track('demo_interaction', { action: 'play' });
    }
    function reset() {
      stop();
      idx = -1;
      render();
      track('demo_interaction', { action: 'reset' });
    }

    if (playBtn) playBtn.addEventListener('click', function () { playing ? stop() : play(); });
    if (resetBtn) resetBtn.addEventListener('click', reset);

    // Clicking a step jumps to it.
    steps.forEach(function (s, i) {
      s.addEventListener('click', function () {
        stop(); idx = i; render();
        track('demo_interaction', { action: 'step', label: String(i + 1) });
      });
      s.addEventListener('keydown', function (e) {
        if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); s.click(); }
      });
    });

    if (reduceMotion) {
      idx = steps.length - 1;
      steps.forEach(function (s) { s.classList.add('done'); });
      render();
      return;
    }

    render();

    // Autoplay once, when the section first scrolls into view.
    if ('IntersectionObserver' in window) {
      var started = false;
      var dio = new IntersectionObserver(function (entries) {
        entries.forEach(function (e) {
          if (e.isIntersecting && !started) { started = true; play(); dio.disconnect(); }
        });
      }, { threshold: 0.4 });
      dio.observe(stage);
    }
  })();

  /* ------------------------------------------------------------------ *
   * Forms
   *
   * One handler drives every form on the site. It reads its rules from
   * the markup — a field is required if it carries `required`, and how it
   * is validated comes from its `type` — so adding a field needs no code.
   *
   * Static hosting has no server to post to, so a validated form hands
   * off to the visitor's mail client. Setting `data-endpoint` on the form
   * switches it to a real POST instead; nothing else has to change.
   * ------------------------------------------------------------------ */
  function labelFor(input, form) {
    var el = form.querySelector('label[for="' + input.id + '"]');
    return el ? el.textContent.replace('*', '').trim() : (input.name || input.id);
  }

  function validate(input) {
    var v = input.value.trim();
    if (!input.hasAttribute('required') && !v) return true;
    if (input.type === 'email') return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(v);
    if (input.type === 'tel') return (v.replace(/[^\d]/g, '').length >= 7);
    if (input.tagName === 'TEXTAREA') return v.length > 4;
    return v.length > 1;
  }

  function wireForm(formId, opts) {
    var form = $('#' + formId);
    if (!form) return;

    opts = opts || {};
    var status = $('.form-status', form);
    var fields = $$('.field input, .field textarea', form);

    // Clear a field's error as soon as it becomes valid again.
    fields.forEach(function (f) {
      f.addEventListener('input', function () {
        if (f.closest('.field').classList.contains('invalid') && validate(f)) {
          f.closest('.field').classList.remove('invalid');
        }
      });
    });

    form.addEventListener('submit', function (e) {
      e.preventDefault();

      var bad = null;
      fields.forEach(function (f) {
        var ok = validate(f);
        f.closest('.field').classList.toggle('invalid', !ok);
        if (!ok && !bad) bad = f;
      });
      if (bad) { bad.focus(); return; }

      var payload = {};
      fields.forEach(function (f) { payload[f.name || f.id] = f.value.trim(); });
      track(opts.event || 'contact_form_submit', { location: opts.location || 'page' });

      var endpoint = form.getAttribute('data-endpoint');
      if (endpoint && endpoint.trim()) {
        status.className = 'form-status show';
        status.textContent = 'Sending…';
        fetch(endpoint, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify(payload)
        }).then(function (r) {
          if (!r.ok) throw new Error(r.status);
          status.className = 'form-status show ok';
          status.textContent = opts.sent ||
            'Thanks — we will come back to you within one working day.';
          form.reset();
        }).catch(function () {
          status.className = 'form-status show';
          status.textContent = 'Something went wrong. Please email ' + MAIL + ' directly.';
        });
        return;
      }

      // Mail-client hand-off: build a readable message from the fields.
      var lines = fields.map(function (f) {
        return labelFor(f, form) + ': ' + (f.value.trim() || '—');
      });
      var who = (payload.company || payload.name || '').trim();
      var subject = (opts.subject || 'Automation audit request') + (who ? ' — ' + who : '');

      window.location.href = 'mailto:' + MAIL +
        '?subject=' + encodeURIComponent(subject) +
        '&body=' + encodeURIComponent(lines.join('\n'));

      status.className = 'form-status show ok';
      status.textContent = 'Your email app should have opened with the details ready to send. ' +
        'If nothing happened, email ' + MAIL + ' directly.';
    });
  }

  var MAIL = 'hello@digitalautonomous.co.uk';

  wireForm('auditForm', {
    event: 'book_audit_submit', location: 'audit_section',
    subject: 'Free automation audit request',
    sent: 'Thanks — we will call you to arrange your audit within one working day.'
  });
  wireForm('contactForm', {
    event: 'contact_form_submit', location: 'contact_page',
    subject: 'Automation audit enquiry'
  });

  /* ------------------------------------------------------------------ *
   * Jumping to the audit form
   *
   * The form sits near the foot of a very long page. Smooth-scrolling the
   * ~12,000px from the hero takes about three seconds, which is a poor
   * response to the page's main call to action — so a long jump is
   * instant and only a short one animates. Either way the cursor lands
   * in the first field.
   * ------------------------------------------------------------------ */
  (function auditJump() {
    var section = $('#audit');
    if (!section) return;
    var first = $('#aName');

    function jump() {
      var pad = parseFloat(getComputedStyle(document.documentElement).scrollPaddingTop) || 88;
      var top = section.getBoundingClientRect().top + window.scrollY - pad;
      var far = Math.abs(top - window.scrollY) > window.innerHeight * 2;
      var instant = far || reduceMotion;

      // 'auto' defers to the CSS scroll-behavior (smooth); 'instant' overrides it.
      window.scrollTo({ top: Math.max(0, top), behavior: instant ? 'instant' : 'smooth' });
      if (!first) return;
      setTimeout(function () {
        try { first.focus({ preventScroll: true }); } catch (e) { first.focus(); }
      }, instant ? 60 : 520);
    }

    document.addEventListener('click', function (e) {
      var a = e.target.closest ? e.target.closest('a[href$="#audit"]') : null;
      if (!a) return;
      var href = a.getAttribute('href');
      // Only same-page jumps; a link from another page should navigate.
      if (href !== '#audit' && href !== location.pathname + '#audit') return;
      e.preventDefault();
      jump();
    });

    if (location.hash === '#audit') setTimeout(jump, 60);
  })();

  /* ------------------------------------------------------------------ *
   * Mark the current page in the nav
   * ------------------------------------------------------------------ */
  (function markCurrent() {
    var path = location.pathname.replace(/index\.html$/, '');
    if (path.length > 1 && path.slice(-1) !== '/') path += '/';
    $$('.nav-links a[href], .nav-panel a[href]').forEach(function (a) {
      var href = a.getAttribute('href');
      if (href && href.charAt(0) === '/' && href === path) {
        a.setAttribute('aria-current', 'page');
      }
    });
  })();
})();
