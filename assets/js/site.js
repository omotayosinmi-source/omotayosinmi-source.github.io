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
   * Submissions POST as JSON to the form's `data-endpoint` and the result
   * is confirmed in place; the visitor is never redirected and no mail
   * client is opened. If the endpoint is missing or the request fails,
   * the form falls back to a mail-client hand-off so an enquiry is never
   * silently lost.
   * ------------------------------------------------------------------ */
  var MAIL = 'hello@digitalautonomous.co.uk';

  function labelFor(input, form) {
    var el = form.querySelector('label[for="' + input.id + '"]');
    if (!el) return input.name || input.id;
    return el.textContent.replace('*', '').replace(/\s+/g, ' ').trim();
  }

  // Countries that keep the national trunk "0" when dialled from abroad.
  // Almost everywhere drops it; Italy is the notable exception.
  var KEEPS_TRUNK_ZERO = { '+39': true };

  // Join a dialling code to a number the way it would actually be dialled,
  // whichever way the visitor typed it: 07380 892559, 7380892559,
  // +44 7380 892559 and 0044 7380892559 all come out the same.
  function formatPhone(raw, code) {
    var cc = String(code).replace(/\D/g, '');
    var trimmed = String(raw).trim();
    var digits = trimmed.replace(/\D/g, '');

    // Only treat the entry as international when the visitor said so, so a
    // plain national number is never mistaken for a repeated country code.
    var international = trimmed.charAt(0) === '+' || /^00\d/.test(digits);
    if (international) {
      if (digits.indexOf('00') === 0) digits = digits.slice(2);
      if (cc && digits.indexOf(cc) === 0) digits = digits.slice(cc.length);
    }

    if (!KEEPS_TRUNK_ZERO[code]) digits = digits.replace(/^0+/, '');
    return digits ? code + ' ' + digits : code;
  }

  function validate(field) {
    var v = (field.value || '').trim();
    if (!field.hasAttribute('required') && !v) return true;
    if (field.tagName === 'SELECT') return v !== '';
    if (field.type === 'email') return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(v);
    if (field.type === 'tel') return v.replace(/[^\d]/g, '').length >= 6;
    if (field.tagName === 'TEXTAREA') return v.length > 4;
    return v.length > 1;
  }

  function wireForm(formId, opts) {
    var form = $('#' + formId);
    if (!form) return;

    opts = opts || {};
    var status = $('.form-status', form);
    var submit = $('button[type="submit"]', form);
    var dial = $('select[name="dial_code"]', form);
    var trap = $('input[name="website"]', form);   // honeypot: only a bot fills this
    // The dial-code picker is read as part of the telephone number, not
    // validated on its own.
    var fields = $$('.field input, .field textarea, .field select', form)
      .filter(function (f) { return f.name !== 'dial_code'; });
    var sending = false;

    function shown(f) {
      var wrap = f.closest('.field');
      return !(wrap && wrap.hasAttribute('hidden'));
    }
    function setError(f, on) { f.closest('.field').classList.toggle('invalid', on); }

    /* -- "Something else" reveals a box to type the real answer ---------- */
    var picker = $('select[data-other]', form);
    if (picker) {
      var otherWrap = $('#' + picker.getAttribute('data-other') + 'Wrap', form);
      var otherInput = $('#' + picker.getAttribute('data-other'), form);
      var otherValue = picker.getAttribute('data-other-value');

      var syncOther = function (focus) {
        var on = picker.value === otherValue;
        otherWrap.hidden = !on;
        if (on) {
          otherInput.setAttribute('required', 'required');
          if (focus) otherInput.focus();
        } else {
          otherInput.removeAttribute('required');
          otherInput.value = '';
          setError(otherInput, false);
        }
      };
      picker.addEventListener('change', function () { syncOther(true); });
      syncOther(false);
    }

    fields.forEach(function (f) {
      var ev = (f.tagName === 'SELECT') ? 'change' : 'input';
      f.addEventListener(ev, function () {
        if (f.closest('.field').classList.contains('invalid') && validate(f)) setError(f, false);
      });
    });

    function say(text, ok) {
      status.className = 'form-status show' + (ok ? ' ok' : '');
      status.textContent = text;
    }

    function valueOf(f) {
      var v = (f.value || '').trim();
      return (f.type === 'tel' && dial) ? formatPhone(v, dial.value) : v;
    }

    // If sending fails we do not hijack the visitor with a mail-client popup.
    // We offer one prefilled link instead, so the enquiry is one click away.
    function offerMailLink(readable) {
      var lines = Object.keys(readable).filter(function (k) { return k.charAt(0) !== '_'; })
        .map(function (k) { return k + ': ' + (readable[k] || '—'); });
      var href = 'mailto:' + MAIL +
        '?subject=' + encodeURIComponent(readable._subject || 'Enquiry') +
        '&body=' + encodeURIComponent(lines.join('\n'));

      status.className = 'form-status show warn';
      status.textContent = 'That did not send. Nothing is lost — ';
      var a = document.createElement('a');
      a.href = href;
      a.textContent = 'send it as an email instead';
      status.appendChild(a);
      status.appendChild(document.createTextNode(', or write to ' + MAIL + '.'));
    }

    form.addEventListener('submit', function (e) {
      e.preventDefault();
      if (sending) return;

      var live = fields.filter(shown);
      var bad = null;
      live.forEach(function (f) {
        var ok = validate(f);
        setError(f, !ok);
        if (!ok && !bad) bad = f;
      });
      if (bad) { bad.focus(); return; }

      // Two shapes: one a person reads in an email, one a spreadsheet can
      // put in columns.
      var readable = {};
      var record = { form: opts.label || formId, page: location.pathname };
      live.forEach(function (f) {
        var v = valueOf(f);
        readable[labelFor(f, form)] = v;
        record[f.name || f.id] = v;
      });
      // Fold the free-text answer into the company type so the sheet has one
      // column that is always meaningful.
      if (record.company_type_other) {
        record.company_type = record.company_type_other;
        delete record.company_type_other;
      }
      record.referrer = document.referrer || '';
      record.token = form.getAttribute('data-token') || '';
      record.website = trap ? trap.value : '';       // the script rejects a filled trap
      readable._subject = (opts.subject || 'Website enquiry') +
        (record.company ? ' — ' + record.company : '');
      readable._template = 'table';

      track(opts.event || 'contact_form_submit', { location: opts.location || 'page' });

      var jobs = [];
      var mailEndpoint = form.getAttribute('data-endpoint');
      var sheetEndpoint = form.getAttribute('data-sheet');

      if (mailEndpoint && mailEndpoint.trim()) {
        jobs.push(fetch(mailEndpoint, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json', 'Accept': 'application/json' },
          body: JSON.stringify(readable)
        }).then(function (r) {
          if (!r.ok) throw new Error(r.status);
          return r.json().catch(function () { return {}; });
        }).then(function (d) {
          if (d && d.success === 'false') throw new Error(d.message || 'rejected');
          return 'mail';
        }));
      }

      if (sheetEndpoint && sheetEndpoint.trim()) {
        // text/plain keeps this a "simple" request, so the browser skips the
        // preflight that Apps Script does not answer.
        jobs.push(fetch(sheetEndpoint, {
          method: 'POST',
          headers: { 'Content-Type': 'text/plain;charset=utf-8' },
          body: JSON.stringify(record)
        }).then(function (r) {
          if (!r.ok) throw new Error(r.status);
          return 'sheet';
        }));
      }

      if (!jobs.length) { offerMailLink(readable); return; }

      sending = true;
      if (submit) submit.disabled = true;
      say('Sending…');

      // Settle every job, then succeed if any route got through: an enquiry
      // that reached the inbox is not a failure because the log was down.
      Promise.all(jobs.map(function (j) {
        return j.then(function (v) { return { ok: true, v: v }; },
                      function (e) { return { ok: false, e: e }; });
      })).then(function (results) {
        var delivered = results.filter(function (r) { return r.ok; });
        if (!delivered.length) { offerMailLink(readable); return; }

        say(opts.sent || 'Thanks — we have got your details and will come back to you within one working day.', true);
        form.reset();
        if (dial) dial.selectedIndex = 0;
        if (picker) picker.dispatchEvent(new Event('change'));
        track((opts.event || 'contact_form_submit') + '_success',
              { location: opts.location || 'page', label: delivered.map(function (r) { return r.v; }).join('+') });
      }).then(function () {
        sending = false;
        if (submit) submit.disabled = false;
      });
    });
  }

  wireForm('auditForm', {
    label: 'Audit form',
    event: 'book_audit_submit', location: 'audit_section',
    subject: 'Free automation audit request',
    sent: 'Thanks — your request is with us. We will call to arrange your audit within one working day.'
  });
  wireForm('contactForm', {
    label: 'Contact page',
    event: 'contact_form_submit', location: 'contact_page',
    subject: 'Website enquiry'
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
