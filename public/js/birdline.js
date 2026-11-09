(function () {
"use strict";
// ROCS = campaign revenue / (production cost + ad spend); ROPS = campaign revenue / production cost. Takes the three amounts as digit strings and returns everything the calculator shows.
function calcView(spendDigits, adsDigits, revenueDigits) {
  var spend = Number(spendDigits) || 0, ads = Number(adsDigits) || 0, revenue = Number(revenueDigits) || 0;
  var group = function (n) { return '$' + Math.round(n).toLocaleString('en-US'); };
  var x = function (r) { return r >= 999500 ? '1M×+' : r >= 9999.5 ? Math.round(r / 1000) + 'K×' : r >= 999.95 ? Math.round(r) + '×' : r >= 99.995 ? r.toFixed(1) + '×' : r.toFixed(r >= 10 ? 1 : 2) + '×'; };
  var rocs = spend + ads > 0 ? revenue / (spend + ads) : 0, rops = spend > 0 ? revenue / spend : 0;
  var verdict, tone;
  if (spend <= 0) { verdict = 'Enter your production cost to see your ROCS\u2122 and ROPS\u2122.'; tone = ''; }
  else if (rops >= 10) { verdict = 'Outperformer — productions like this should scale.'; tone = ''; }
  else if (rops >= 3) { verdict = 'Healthy — worth iterating on with the next brief.'; tone = 'is-mid'; }
  else { verdict = 'Under water — rethink the concept before the next shoot.'; tone = 'is-low'; }
  return {
    spendInput: spendDigits === '' ? '' : group(spend).slice(1),
    adsInput: adsDigits === '' ? '' : group(ads).slice(1),
    revenueInput: revenueDigits === '' ? '' : group(revenue).slice(1),
    rocsText: spend + ads > 0 ? x(rocs) : '—',
    ropsText: spend > 0 ? x(rops) : '—',
    rocsSub: group(revenue) + ' on ' + group(spend + ads),
    ropsSub: group(revenue) + ' on ' + group(spend),
    verdict: verdict, tone: tone
  };
}
function digitsOnly(value) {
  return String(value).replace(/[^0-9]/g, '').replace(/^0+(?=[0-9])/, '').slice(0, 8);
}
// Starts the parts of the page that move: the menu bar turning from clear to white as the page leaves its top, the menu on small screens,
// the tour advancing along its line, and the once-only moments when a module is first seen. Everything it touches is complete without it.
function enhance(doc) {
  var win = doc.defaultView, root = doc.documentElement;
  var matches = function (query) { return !!(win.matchMedia && win.matchMedia(query).matches); };
  // nothing plays under reduced motion, or in a frame that cannot scroll (a design board shows the finished state)
  var still = matches('(prefers-reduced-motion: reduce)') || root.scrollHeight - win.innerHeight < 200;
  var undo = [];
  var listen = function (type, fn) { doc.addEventListener(type, fn, true); undo.push(function () { doc.removeEventListener(type, fn, true); }); };
  if (!still) root.classList.add('js-on');

  // the menu bar is clear while the short marker at the top of the page is on screen, and the white bar once it has scrolled away.
  var bar = null, mark = null, markWatch = null, solid = false;
  function paintBar() {
    if (bar) bar.classList.toggle('is-solid', solid);
    root.classList.toggle('bar-open', !!(bar && bar.classList.contains('is-open')));
  }
  function bindBar() {
    var nextMark = doc.querySelector('[data-bar-mark]');
    bar = doc.querySelector('[data-bar]');
    if (nextMark !== mark) {
      if (markWatch) { markWatch.disconnect(); markWatch = null; }
      mark = nextMark;
      if (mark && win.IntersectionObserver) {
        markWatch = new win.IntersectionObserver(function (entries) { solid = !entries[entries.length - 1].isIntersecting; paintBar(); });
        markWatch.observe(mark);
      } else solid = true;
    }
    paintBar();
  }
  // the menu on small screens
  function setMenu(open) {
    if (!bar) return;
    var btn = bar.querySelector('[data-menu]');
    bar.classList.toggle('is-open', open);
    if (btn) btn.setAttribute('aria-expanded', open ? 'true' : 'false');
    paintBar();
  }
  listen('click', function (e) {
    var btn = e.target && e.target.closest ? e.target.closest('[data-menu]') : null;
    if (btn) { setMenu(!bar.classList.contains('is-open')); return; }
    if (bar && bar.classList.contains('is-open') && e.target.closest && e.target.closest('.nav a')) setMenu(false);
  });
  listen('keydown', function (e) { if (e.key === 'Escape' && bar && bar.classList.contains('is-open')) setMenu(false); });


  // numbers count up to the figure already written in the page
  function count(el) {
    var end = parseFloat(el.getAttribute('data-count')), decimals = Number(el.getAttribute('data-decimals') || 0), finalText = el.textContent;
    if (!isFinite(end) || !el.animate) return;
    var clock = el.animate([{ opacity: 1 }, { opacity: 1 }], { duration: 900 });
    function frame() {
      var t = clock.currentTime;
      var p = clock.playState !== 'running' || t === null ? 1 : Math.min(Number(t) / 900, 1);
      el.textContent = p < 1 ? (end * (1 - Math.pow(1 - p, 3))).toFixed(decimals) : finalText;
      if (p < 1) win.requestAnimationFrame(frame);
    }
    win.requestAnimationFrame(frame);
  }
  function arrive(el) {
    if (el.classList.contains('is-in')) return;
    el.classList.add('is-in');
    if (!still) Array.prototype.forEach.call(el.querySelectorAll('[data-count]'), count);
  }
  // "armed" while a module is just below the screen, "in" once a fifth of it shows
  var armed = win.IntersectionObserver && !still ? new win.IntersectionObserver(function (entries) {
    entries.forEach(function (entry) { if (entry.isIntersecting) { armed.unobserve(entry.target); entry.target.classList.add('is-armed'); } });
  }, { rootMargin: '0px 0px 240px 0px' }) : null;
  var seen = armed ? new win.IntersectionObserver(function (entries) {
    entries.forEach(function (entry) { if (entry.isIntersecting) { seen.unobserve(entry.target); arrive(entry.target); } });
  }, { threshold: 0.2 }) : null;

  // the tour plays through once, only where a pointer can hold it by hovering, and only until someone picks a part themselves
  var tour = null, watch = null, auto = !still && matches('(hover: hover) and (pointer: fine)');
  function bindTour() {
    var el = doc.querySelector('[data-tour]');
    if (el === tour) return;
    if (watch) { watch.disconnect(); watch = null; }
    tour = el;
    if (!tour || !auto || !win.IntersectionObserver) return;
    watch = new win.IntersectionObserver(function (entries) {
      entries.forEach(function (entry) { if (tour) tour.classList.toggle('is-playing', auto && entry.isIntersecting); });
    }, { threshold: 0.5 });
    watch.observe(tour);
  }
  function stopTour() { auto = false; if (tour) tour.classList.remove('is-playing'); }
  var inTour = function (node) { return !!(tour && node && node.nodeType === 1 && tour.contains(node)); };
  var segStarted = 0;
  listen('animationstart', function (e) { if (e.animationName === 'seg-fill' && inTour(e.target)) segStarted = win.performance.now(); });
  listen('animationend', function (e) {
    if (e.animationName !== 'seg-fill' || !auto || !inTour(e.target)) return;
    if (win.performance.now() - segStarted < 7000) { stopTour(); return; }
    var inputs = tour.querySelectorAll('input[name="tour"]'), current = 0;
    Array.prototype.forEach.call(inputs, function (input, i) { if (input.checked) current = i; });
    if (current >= inputs.length - 1) { stopTour(); return; }
    inputs[current + 1].checked = true;
  });
  listen('change', function (e) { if (inTour(e.target) && e.target.name === 'tour') stopTour(); });
  listen('pointerdown', function (e) { if (inTour(e.target) && e.target.closest('.rail')) stopTour(); });

  // links to a section on this page glide there (plain jumps under reduced motion or without script)
  if (!still) listen('click', function (e) {
    if (e.defaultPrevented || e.button || e.metaKey || e.ctrlKey || e.shiftKey || e.altKey) return;
    // a link to a place on this page: href="#id", or "/#id" from a page at "/" (the site's shared header writes it that way)
    var link = e.target && e.target.closest ? e.target.closest('a[href*="#"]') : null;
    if (!link || !link.hash || link.origin !== location.origin || link.pathname !== location.pathname) return;
    var target = doc.getElementById(decodeURIComponent(link.hash.slice(1)));
    if (!target) return;
    e.preventDefault();
    target.scrollIntoView({ behavior: 'smooth', block: 'start' });
    if (!target.hasAttribute('tabindex')) target.setAttribute('tabindex', '-1');
    target.focus({ preventScroll: true });
  });

  // one item at a time takes a turn: the "is-on" class moves through a group's items. Pointing at the group pauses it; pointing at an item gives it the turn.
  // Without this (no script, reduced motion) each group rests on its first item.
  var cycleTimers = [];
  function bindCycles() {
    Array.prototype.forEach.call(doc.querySelectorAll('[data-cycle]:not(.is-cycling)'), function (group) {
      var items = group.querySelectorAll('[data-cycle-item]');
      if (items.length < 2) return;
      group.classList.add('is-cycling');
      var every = Number(group.getAttribute('data-cycle')) || 2000, offset = Number(group.getAttribute('data-cycle-offset')) || 0;
      var at = 0, paused = false, timer = 0;
      function show(n) { at = n; Array.prototype.forEach.call(items, function (el, k) { el.classList.toggle('is-on', k === at); }); }
      show(0);
      if (still) return;
      root.classList.add('js-cycle');
      group.addEventListener('pointerenter', function () { paused = true; });
      group.addEventListener('pointerleave', function () { paused = false; });
      group.addEventListener('pointerover', function (e) {
        var item = e.target && e.target.closest ? e.target.closest('[data-cycle-item]') : null;
        if (item && group.contains(item)) show(Array.prototype.indexOf.call(items, item));
      });
      function tick() { if (!paused) show((at + 1) % items.length); timer = win.setTimeout(tick, every); }
      timer = win.setTimeout(tick, every + offset);
      cycleTimers.push(function () { win.clearTimeout(timer); });
    });
  }

  // the testimonial row: the buttons scroll it by one card
  listen('click', function (e) {
    var btn = e.target && e.target.closest ? e.target.closest('[data-carousel-prev],[data-carousel-next]') : null;
    if (!btn) return;
    var car = btn.closest('[data-carousel]'), track = car && car.querySelector('[data-carousel-track]');
    if (!track) return;
    var card = track.firstElementChild, step = card ? card.getBoundingClientRect().width + 20 : track.clientWidth;
    track.scrollBy({ left: btn.hasAttribute('data-carousel-next') ? step : -step, behavior: still ? 'auto' : 'smooth' });
  });

  // Booking. Every "Book a call" button ([data-book]) opens the modal: the short form, then Calendly inline. The homepage form
  // ([data-lead] at the close) is the same form laid into the page; a valid submit sends the details to /api/book (the Next.js
  // site emails them to the team; on the static site the request simply fails and the flow carries on) and opens the calendar.
  var CALENDLY = 'https://calendly.com/birdlinestudios/birdline-exploratory-call';
  var PERSONAL = /^(gmail|googlemail|yahoo|ymail|rocketmail|hotmail|outlook|live|msn|icloud|me|mac|aol|protonmail|proton|pm|gmx|mail|zoho|yandex|fastmail|hey|duck|comcast|att|verizon|sbcglobal|cox|qq|163|126)\./i;
  var WORK_EMAIL_HINT = 'Please use your company email. Personal email providers aren’t accepted.';
  function emailDomain(value) { var m = /^[^\s@]+@([^\s@]+\.[^\s@]+)$/.exec(String(value).trim()); return m ? m[1].toLowerCase() : ''; }
  function isWorkEmail(value) { var d = emailDomain(value); return !!d && !PERSONAL.test(d); }
  function field(form, name) { return form.querySelector('[name="' + name + '"]'); }
  function value(form, name) { var f = field(form, name); return f ? f.value.trim() : ''; }
  function firstName(name) { return name.trim().split(/\s+/)[0] || ''; }
  // checks a lead form; returns the first bad field or null, and writes the message
  function check(form) {
    var msg = form.querySelector('[data-lead-msg]'), bad = null, text = '';
    Array.prototype.forEach.call(form.querySelectorAll('[required],[data-work-email]'), function (f) {
      var v = f.value.trim(), wrong = false;
      if (f.hasAttribute('required') && !v) { wrong = true; text = text || 'Please fill in every field marked with an asterisk.'; }
      else if (f.type === 'email' && v && !emailDomain(v)) { wrong = true; text = text || 'That email address doesn’t look complete.'; }
      else if (f.hasAttribute('data-work-email') && v && !isWorkEmail(v)) { wrong = true; text = text || WORK_EMAIL_HINT; }
      f.setAttribute('aria-invalid', wrong ? 'true' : 'false');
      if (wrong && !bad) bad = f;
    });
    if (msg) { msg.textContent = bad ? text : ''; msg.classList.toggle('is-error', !!bad); }
    return bad;
  }
  function leadData(form) {
    var source = value(form, 'source'), other = value(form, 'source_other');
    return { name: value(form, 'name'), email: value(form, 'email'), company: value(form, 'company'), size: value(form, 'size'),
             source: source === 'Other' && other ? 'Other: ' + other : (source || other), website: value(form, 'website'),
             page: win.location.pathname + win.location.hash, referrer: doc.referrer || '' };
  }
  // sends the details; always calls done, because the calendar must open whether or not the email went out
  function sendLead(form, done) {
    var btn = form.querySelector('button[type="submit"]'), label = btn ? btn.textContent : '';
    if (btn) { btn.disabled = true; btn.textContent = 'One moment…'; }
    var finish = function (res) { if (btn) { btn.disabled = false; btn.textContent = label; } done(res || {}); };
    var payload = leadData(form);
    if (!win.fetch) return finish({ ok: false });
    win.fetch('/api/book', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(payload) })
      .then(function (r) { return r.json().then(function (j) { return j; }, function () { return { ok: r.ok }; }); })
      .then(finish, function () { finish({ ok: false }); });
  }
  var bookDialog = null, bookForm = null;
  function bindBook() {
    bookDialog = doc.querySelector('[data-book-dialog]');
    bookForm = bookDialog ? bookDialog.querySelector('[data-book-form]') : null;
  }
  function bookStep(name) {
    if (!bookDialog) return;
    Array.prototype.forEach.call(bookDialog.querySelectorAll('[data-book-step]'), function (s) { s.hidden = s.getAttribute('data-book-step') !== name; });
    var card = bookDialog.querySelector('.book-card'); if (card) card.scrollTop = 0;
  }
  function openBook(step, lead) {
    if (!bookDialog || typeof bookDialog.showModal !== 'function') return false;
    if (step === 'calendar' && lead) {
      var first = bookDialog.querySelector('[data-book-first]'), frame = bookDialog.querySelector('[data-book-cal]'), link = bookDialog.querySelector('[data-book-cal-link]');
      var url = CALENDLY + '?hide_gdpr_banner=1&embed_type=Inline&embed_domain=' + encodeURIComponent(win.location.hostname) +
                '&name=' + encodeURIComponent(lead.name) + '&email=' + encodeURIComponent(lead.email) + '&utm_source=website&utm_medium=book-a-call' +
                '&primary_color=2547d0&text_color=0b1220&background_color=ffffff';
      if (first) first.textContent = lead.name ? ', ' + firstName(lead.name) : '';
      if (frame && frame.getAttribute('src') !== url) frame.setAttribute('src', url);
      if (link) link.setAttribute('href', CALENDLY + '?name=' + encodeURIComponent(lead.name) + '&email=' + encodeURIComponent(lead.email));
    }
    bookStep(step);
    if (!bookDialog.open) bookDialog.showModal();
    root.classList.add('book-open');
    if (step === 'form' && bookForm) { var f = field(bookForm, 'name'); if (f && !f.value) setTimeout(function () { f.focus(); }, 50); }
    return true;
  }
  function closeBook() { if (bookDialog && bookDialog.open) bookDialog.close(); }
  listen('close', function (e) { if (e.target === bookDialog) root.classList.remove('book-open'); });
  listen('click', function (e) {
    var t = e.target;
    if (!t || !t.closest) return;
    var open = t.closest('[data-book]');
    if (open) { if (openBook('form')) e.preventDefault(); return; }
    if (t.closest('[data-book-close]')) { closeBook(); return; }
    if (bookDialog && t === bookDialog && bookDialog.open) closeBook();   // the backdrop
  });
  listen('change', function (e) {
    var sel = e.target && e.target.closest ? e.target.closest('[data-source]') : null;
    if (!sel) return;
    var other = sel.closest('form').querySelector('.book-other');
    if (other) { other.hidden = sel.value !== 'Other'; if (!other.hidden) { var i = other.querySelector('input'); if (i) i.focus(); } }
  });
  listen('submit', function (e) {
    var form = e.target && e.target.closest ? e.target.closest('[data-lead]') : null;
    if (!form) return;
    e.preventDefault();
    var bad = check(form);
    if (bad) { bad.focus(); return; }
    var lead = leadData(form), msg = form.querySelector('[data-lead-msg]');
    sendLead(form, function () {
      if (!openBook('calendar', lead)) { win.open(CALENDLY + '?name=' + encodeURIComponent(lead.name) + '&email=' + encodeURIComponent(lead.email), '_blank', 'noopener'); }
      if (msg && !form.hasAttribute('data-book-form')) { msg.textContent = 'Thanks, ' + firstName(lead.name) + '. Pick a time in the calendar.'; msg.classList.remove('is-error'); }
    });
  });
  // the email field explains itself as soon as a personal address is typed
  listen('blur', function (e) {
    var f = e.target && e.target.closest ? e.target.closest('[data-work-email]') : null;
    if (!f || !f.value.trim()) return;
    var ok = isWorkEmail(f.value);
    f.setAttribute('aria-invalid', ok ? 'false' : 'true');
    var msg = f.closest('form') && f.closest('form').querySelector('[data-lead-msg]');
    if (msg && !ok) { msg.textContent = WORK_EMAIL_HINT; msg.classList.add('is-error'); }
    else if (msg && msg.textContent === WORK_EMAIL_HINT) { msg.textContent = ''; msg.classList.remove('is-error'); }
  });

  // the stack of deliverables: every few seconds the front frame drops out and goes to the back, so the pile never ends
  var stackTimers = [];
  function bindStacks() {
    Array.prototype.forEach.call(doc.querySelectorAll('[data-stack]:not(.is-stacking)'), function (stack) {
      stack.classList.add('is-stacking');
      if (still) return;
      var timer = win.setInterval(function () {
        var front = stack.firstElementChild;
        if (!front) return;
        front.classList.add('is-out');
        win.setTimeout(function () { front.classList.remove('is-out'); stack.appendChild(front); }, 600);
      }, 2600);
      stackTimers.push(function () { win.clearInterval(timer); });
    });
  }

  // the workspace switch: three screens, one shown at a time; picking one stops the auto-advance below
  listen('click', function (e) {
    var tab = e.target && e.target.closest ? e.target.closest('[data-ws-tab]') : null;
    if (!tab) return;
    var stage = tab.closest('.hc-stage, [data-ws-stage]'), key = tab.getAttribute('data-ws-tab');
    if (!stage) return;
    stage.__wsStopped = true;
    Array.prototype.forEach.call(stage.querySelectorAll('[data-ws-tab]'), function (b) { var on = b === tab; b.classList.toggle('is-on', on); b.setAttribute('aria-selected', on ? 'true' : 'false'); });
    Array.prototype.forEach.call(stage.querySelectorAll('[data-ws-screen]'), function (img) { img.classList.toggle('is-on', img.getAttribute('data-ws-screen') === key); });
  });

  // the homepage's workspace card advances through its pages every few seconds (data-ws-cycle, in ms) until someone picks one; it rests under the pointer
  var wsTimers = [];
  function bindWsCycles() {
    Array.prototype.forEach.call(doc.querySelectorAll('[data-ws-cycle]:not(.is-ws-cycling)'), function (stage) {
      stage.classList.add('is-ws-cycling');
      if (still) return;
      var every = Number(stage.getAttribute('data-ws-cycle')) || 4000, paused = false;
      stage.addEventListener('pointerenter', function () { paused = true; });
      stage.addEventListener('pointerleave', function () { paused = false; });
      var timer = win.setInterval(function () {
        if (paused || stage.__wsStopped || !doc.contains(stage)) return;
        var tabs = stage.querySelectorAll('[data-ws-tab]'), at = 0;
        Array.prototype.forEach.call(tabs, function (b, k) { if (b.classList.contains('is-on')) at = k; });
        var next = tabs[(at + 1) % tabs.length], key = next.getAttribute('data-ws-tab');
        Array.prototype.forEach.call(tabs, function (b) { var on = b === next; b.classList.toggle('is-on', on); b.setAttribute('aria-selected', on ? 'true' : 'false'); });
        Array.prototype.forEach.call(stage.querySelectorAll('[data-ws-screen]'), function (img) { img.classList.toggle('is-on', img.getAttribute('data-ws-screen') === key); });
      }, every);
      wsTimers.push(function () { win.clearInterval(timer); });
    });
  }

  function scan() {
    bindCycles();
    bindStacks();
    bindWsCycles();
    Array.prototype.forEach.call(doc.querySelectorAll('[data-inview]:not(.is-in)'), function (el) {
      if (!seen) { arrive(el); return; }
      if (!el.classList.contains('is-armed')) armed.observe(el);
      seen.observe(el);
    });
    bindBar();
    bindBook();
    bindTour();
  }
  scan();
  return {
    scan: scan,
    destroy: function () {
      undo.forEach(function (off) { off(); });
      cycleTimers.forEach(function (stop) { stop(); });
      stackTimers.forEach(function (stop) { stop(); });
      root.classList.remove('js-cycle');
      if (armed) armed.disconnect();
      if (seen) seen.disconnect();
      if (watch) watch.disconnect();
      if (markWatch) markWatch.disconnect();
      if (bar) { bar.classList.remove('is-solid'); bar.classList.remove('is-open'); }
      if (tour) tour.classList.remove('is-playing');
      root.classList.remove('js-on');
      root.classList.remove('bar-open');
    }
  };
}

/* The calculator: three amounts in, two results out. bindCalc wires every calculator under root that is not wired yet; kept on window so a
   page that swaps its content in (the artifact's router) can wire a calculator that arrives later. */
function bindCalc(root) {
  Array.prototype.forEach.call(root.querySelectorAll('[data-calc-form]:not(.is-bound)'), function (form) {
    form.classList.add('is-bound');
    var q = function (k) { return form.querySelector('[data-calc="' + k + '"]'); };
    var spend = q('spend-input'), ads = q('ads-input'), revenue = q('revenue-input');
    if (!spend || !ads || !revenue) return;
    form.addEventListener('submit', function (e) { e.preventDefault(); });
    var state = { spend: digitsOnly(spend.value), ads: digitsOnly(ads.value), revenue: digitsOnly(revenue.value) };
    function render() {
      var v = calcView(state.spend, state.ads, state.revenue);
      if (spend.value !== v.spendInput) spend.value = v.spendInput;
      if (ads.value !== v.adsInput) ads.value = v.adsInput;
      if (revenue.value !== v.revenueInput) revenue.value = v.revenueInput;
      q('rocs').textContent = v.rocsText;
      q('rops').textContent = v.ropsText;
      q('rocs-sub').textContent = v.rocsSub;
      q('rops-sub').textContent = v.ropsSub;
      var s = q('summary');
      s.lastChild.nodeValue = v.verdict;
      s.classList.remove('is-mid'); s.classList.remove('is-low');
      if (v.tone) s.classList.add(v.tone);
    }
    spend.addEventListener('input', function () { state.spend = digitsOnly(spend.value); render(); });
    ads.addEventListener('input', function () { state.ads = digitsOnly(ads.value); render(); });
    revenue.addEventListener('input', function () { state.revenue = digitsOnly(revenue.value); render(); });
    render();
  });
}
window.__birdlineCalc = bindCalc;
bindCalc(document);
try { window.__birdline = enhance(document); } catch (err) { console.error(err); }
})();

/* The lightbox on the Work, case-study and service pages. A tile opens its media over the page and the arrows, the keyboard
   (left and right) or a swipe move through the rest of that gallery, with a rail of thumbnails along the bottom. A self-hosted
   video (data-src) plays in the site's own player; a Vimeo one in Vimeo's; a photo opens at full size. Without script (or without
   <dialog>) every tile is a plain link. Inside the artifact viewer (window.__artifact) Vimeo cannot be embedded, so there a Vimeo
   tile opens Vimeo in a new tab and the rail skips those. */
(function () {
  "use strict";
  var dlg = document.querySelector('[data-lb-dialog]');
  if (!dlg || typeof dlg.showModal !== 'function') return;
  var stage = dlg.querySelector('[data-lb-body]'), title = dlg.querySelector('[data-lb-title]'),
      kind = dlg.querySelector('[data-lb-kind]'), count = dlg.querySelector('[data-lb-count]'), rail = dlg.querySelector('[data-lb-rail]'),
      prev = dlg.querySelector('[data-lb-prev]'), next = dlg.querySelector('[data-lb-next]');
  var items = [], at = 0;
  function usable(link) { return !(window.__artifact && link.getAttribute('data-vimeo')); }
  function visible(link) { var t = link.closest('.gi, .tv-tile, li'); return !(t && t.classList.contains('is-hidden')); }
  function gallery(link) {
    var root = link.closest('[data-masonry], [data-carousel-track], .cs-quotes, section') || document;
    var seen = {}, out = [];
    Array.prototype.forEach.call(root.querySelectorAll('a[data-lb]'), function (l) {
      if (!usable(l) || !visible(l)) return;
      var key = l.getAttribute('data-src') || l.getAttribute('data-vimeo') || l.getAttribute('href');
      if (key in seen) { if (l === link) out[seen[key]] = l; return; }  // the hero's looping track repeats its tiles
      seen[key] = out.length; out.push(l);
    });
    return out;
  }
  function clear() {
    var v = stage.querySelector('video'); if (v) { v.pause(); v.removeAttribute('src'); v.load(); }
    stage.innerHTML = '';
    dlg.classList.remove('lb--video'); dlg.classList.remove('lb--img'); dlg.classList.remove('lb--tall'); dlg.classList.remove('lb--square');
  }
  function render() {
    var link = items[at];
    clear();
    var k = link.getAttribute('data-lb'), href = link.getAttribute('href'), shape = link.getAttribute('data-shape') || 'wide';
    dlg.style.setProperty('--lb-asp', link.getAttribute('data-asp') || (shape === 'tall' ? '0.5625' : shape === 'square' ? '1' : '1.7778'));
    if (k === 'video') {
      dlg.classList.add('lb--video');
      if (shape === 'tall') dlg.classList.add('lb--tall'); else if (shape === 'square') dlg.classList.add('lb--square');
      if (link.getAttribute('data-src')) {
        var v = document.createElement('video');
        v.src = link.getAttribute('data-src'); v.controls = true; v.autoplay = true; v.playsInline = true; v.preload = 'auto';
        v.setAttribute('title', link.getAttribute('data-title') || 'Video');
        // a file that is not in the store yet (or a network hiccup): try the file's fallback (the original upload), then show its still instead of a black player
        var poster = link.getAttribute('data-poster') || (link.querySelector('video') && link.querySelector('video').getAttribute('poster')) || (link.querySelector('img') && link.querySelector('img').getAttribute('src'));
        if (poster) v.poster = poster;
        var fallback = link.getAttribute('data-fallback');
        v.addEventListener('error', function () {
          if (!v.parentNode) return;
          if (fallback) { var f = fallback; fallback = null; v.src = f; v.load(); var pp = v.play(); if (pp && pp.catch) pp.catch(function () {}); return; }
          var holder = document.createElement('div'); holder.className = 'lb-missing';
          if (poster) { var im = document.createElement('img'); im.src = poster; im.alt = ''; holder.appendChild(im); }
          var note = document.createElement('p'); note.textContent = 'This video isn’t available yet. Check back soon.'; holder.appendChild(note);
          stage.replaceChild(holder, v);
        });
        stage.appendChild(v);
      } else {
        var frame = document.createElement('iframe');
        frame.src = 'https://player.vimeo.com/video/' + link.getAttribute('data-vimeo') + '?autoplay=1&title=0&byline=0&portrait=0&dnt=1';
        frame.setAttribute('allow', 'autoplay; fullscreen; picture-in-picture'); frame.setAttribute('allowfullscreen', '');
        frame.setAttribute('title', link.getAttribute('data-title') || 'Video');
        stage.appendChild(frame);
      }
    } else {
      dlg.classList.add('lb--img');
      var img = document.createElement('img'); img.src = href; img.alt = link.getAttribute('data-title') || '';
      stage.appendChild(img);
    }
    title.textContent = link.getAttribute('data-title') || '';
    kind.textContent = link.getAttribute('data-kind') || (k === 'video' ? 'Video' : 'Photo');
    count.textContent = items.length > 1 ? (at + 1) + ' / ' + items.length : '';
    dlg.classList.toggle('lb--one', items.length < 2);
    Array.prototype.forEach.call(rail.children, function (b, i) {
      var on = i === at; b.classList.toggle('is-on', on); b.setAttribute('aria-current', on ? 'true' : 'false');
      if (on && b.scrollIntoView) b.scrollIntoView({ block: 'nearest', inline: 'center', behavior: 'smooth' });
    });
  }
  function thumb(link, i) {
    var b = document.createElement('button'); b.type = 'button'; b.className = 'lb-thumb'; b.setAttribute('aria-label', (link.getAttribute('data-title') || 'Item') + ', ' + (i + 1));
    var img = link.querySelector('img'), vid = link.querySelector('video');
    if (img) { var t = document.createElement('img'); t.src = img.currentSrc || img.src; t.alt = ''; b.appendChild(t); }
    else if (vid && vid.poster) { var pt = document.createElement('img'); pt.src = vid.poster; pt.alt = ''; b.appendChild(pt); }
    else if (vid) {
      // a frame of the tile's own video, drawn once it has one; a play glyph until then
      var c = document.createElement('canvas'); c.width = 96; c.height = 96; b.appendChild(c);
      var draw = function () {
        try {
          var w = vid.videoWidth, h = vid.videoHeight; if (!w || !h) return;
          var s = Math.max(96 / w, 96 / h), ctx = c.getContext('2d');
          ctx.drawImage(vid, (96 - w * s) / 2, (96 - h * s) / 2, w * s, h * s);
        } catch (e) {}
      };
      if (vid.readyState >= 2) draw(); else vid.addEventListener('loadeddata', draw, { once: true });
    }
    if (link.getAttribute('data-lb') === 'video') { var p = document.createElement('i'); p.className = 'lb-thumb-play'; b.appendChild(p); }
    b.addEventListener('click', function () { at = i; render(); });
    return b;
  }
  function show(link) {
    items = gallery(link);
    if (items.indexOf(link) < 0) items = [link];
    at = items.indexOf(link);
    rail.innerHTML = '';
    if (items.length > 1) items.forEach(function (l, i) { rail.appendChild(thumb(l, i)); });
    // the dialog opens first, so the media renders into a laid-out stage (and a hiccup in rendering never leaves it closed)
    if (!dlg.open) dlg.showModal();
    try { render(); } catch (err) { if (window.console) console.error(err); }
  }
  function step(d) { if (items.length < 2) return; at = (at + d + items.length) % items.length; render(); }
  document.addEventListener('click', function (e) {
    if (e.defaultPrevented || e.button || e.metaKey || e.ctrlKey || e.shiftKey || e.altKey) return;
    var link = e.target && e.target.closest ? e.target.closest('a[data-lb]') : null;
    if (link) {
      if (!usable(link)) return;
      e.preventDefault(); show(link); return;
    }
    if (e.target.closest && e.target.closest('[data-lb-close]')) { dlg.close(); return; }
    if (e.target.closest && e.target.closest('[data-lb-prev]')) { step(-1); return; }
    if (e.target.closest && e.target.closest('[data-lb-next]')) { step(1); return; }
    // a click on the backdrop (outside the media) closes it
    if (dlg.open && e.target === dlg) dlg.close();
  });
  dlg.addEventListener('keydown', function (e) {
    if (e.key === 'ArrowLeft') { e.preventDefault(); step(-1); }
    if (e.key === 'ArrowRight') { e.preventDefault(); step(1); }
  });
  var tx = null;
  dlg.addEventListener('touchstart', function (e) { tx = e.touches[0].clientX; }, { passive: true });
  dlg.addEventListener('touchend', function (e) { if (tx === null) return; var dx = e.changedTouches[0].clientX - tx; tx = null; if (Math.abs(dx) > 48) step(dx < 0 ? 1 : -1); }, { passive: true });
  dlg.addEventListener('close', function () { clear(); rail.innerHTML = ''; items = []; });
})();

/* A tile's video that is not in the store yet (data-fallback names the original upload) loads the fallback instead. Media errors
   do not bubble, so this listens in the capture phase. */
(function () {
  "use strict";
  function swap(v) {
    var f = v.getAttribute('data-fallback');
    if (!f) return;
    v.removeAttribute('data-fallback');
    v.setAttribute('src', f); v.load();
  }
  document.addEventListener('error', function (e) {
    var v = e.target;
    if (v && v.tagName === 'VIDEO') swap(v);
  }, true);
  // the videos that failed before this ran (they start loading with the page; this script comes after it)
  function sweep() {
    Array.prototype.forEach.call(document.querySelectorAll('video[data-fallback]'), function (v) { if (v.error) swap(v); });
  }
  sweep();
  window.addEventListener('load', sweep);
  window.__siteFallbacks = sweep;
})();

/* Video tiles: the frame they show is the video's own; pointing at one plays it quietly, leaving it puts it back. */
(function () {
  "use strict";
  if (!window.matchMedia || !window.matchMedia('(hover: hover)').matches) return;
  var still = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  if (still) return;
  document.addEventListener('pointerenter', function (e) {
    var a = e.target && e.target.closest ? e.target.closest('.gi--video a') : null; if (!a) return;
    var v = a.querySelector('video'); if (!v) return;
    var p = v.play(); if (p && p.catch) p.catch(function () {});
  }, true);
  document.addEventListener('pointerleave', function (e) {
    var a = e.target && e.target.closest ? e.target.closest('.gi--video a') : null; if (!a) return;
    var v = a.querySelector('video'); if (!v) return;
    v.pause(); try { if (v.poster) v.load(); else v.currentTime = 0.8; } catch (x) {}
  }, true);
})();

/* The masonry: without script the tiles flow down CSS columns, which can leave one column short. With it, the tiles are dealt one at
   a time into the shortest column (their heights known from each image's width and height), so the columns end together.
   window.__siteMasonry(root) lays out any masonry under root that is new, for content added to the page later. The tiles stay in
   their own order (the lightbox walks them in it) and fill justified rows with no gaps: a row holds --cols slots, a wide frame takes
   two and anything else one, and the tiles in a row share one height, so a 16:9 sits at about half the width beside another 16:9 and
   wider beside a vertical or a square. */
(function () {
  "use strict";
  var lists = [];
  function layout(list, force) {
    var cs = getComputedStyle(list);
    var cap = parseInt(cs.getPropertyValue('--cols'), 10) || 1, gap = parseFloat(cs.getPropertyValue('--mgap')) || 0, W = list.clientWidth;
    if (!W) return;
    if (list.__cap === cap && list.__w === W && !force) return;
    var all = list.__items || (list.__items = Array.prototype.slice.call(list.querySelectorAll('.gi')));
    var items = all.filter(function (it) { return !it.classList.contains('is-hidden'); });
    list.__cap = cap; list.__w = W;
    list.classList.add('is-js');
    // each tile's proportions and how many of the row's slots it takes: a wide frame two, anything else one
    var tiles = items.map(function (it) {
      var m = it.querySelector('img, video'), w = m ? Number(m.getAttribute('width')) : 0, h = m ? Number(m.getAttribute('height')) : 0;
      var a = w && h ? w / h : 1;
      return { el: it, a: a, u: (cap > 1 && a >= 1.3) ? 2 : 1 };
    });
    var rows = [], row = [], units = 0;
    tiles.forEach(function (t) {
      if (units + t.u > cap) { rows.push(row); row = []; units = 0; }
      row.push(t); units += t.u;
      if (units === cap) { rows.push(row); row = []; units = 0; }
    });
    if (row.length) rows.push(row);
    rows.forEach(function (r, ri) {
      var sum = 0, i; r.forEach(function (t) { sum += t.a; });
      var u = 0; r.forEach(function (t) { u += t.u; });
      var inner = W - (r.length - 1) * gap, full = true;
      if (ri === rows.length - 1 && u < cap - 1) { sum += (cap - u); inner = W - (r.length - 1 + cap - u) * gap; full = false; }  // a short last row keeps its neighbours' scale
      var h = inner / sum, used = 0;
      r.forEach(function (t, i) {
        var w = Math.floor(t.a * h);
        if (full && i === r.length - 1) w = inner - used;  // the last tile closes the row to the pixel
        used += w;
        t.el.style.width = w + 'px';
      });
    });
  }
  function scan(root) {
    Array.prototype.forEach.call((root || document).querySelectorAll('[data-masonry]'), function (list) {
      if (lists.indexOf(list) < 0) lists.push(list);
      layout(list);
    });
  }
  window.__siteMasonry = scan;
  scan.relayout = function (list) { layout(list, true); };
  scan(document);
  var timer;
  window.addEventListener('resize', function () { clearTimeout(timer); timer = setTimeout(function () { lists.forEach(function (l) { layout(l); }); }, 150); });
})();

/* A looping product video stands still for anyone who asked for reduced motion. */
(function () {
  "use strict";
  var still = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  function scan(root) {
    if (!still) return;
    Array.prototype.forEach.call((root || document).querySelectorAll('video[autoplay]'), function (v) { v.removeAttribute('autoplay'); v.pause(); });
  }
  window.__siteVideo = scan;
  scan(document);
})();

/* A cover loop (the short silent clip over a case study's still) plays while it is on screen and rests off it, and stays on its
   still for anyone who asked for reduced motion. Autoplay alone is not enough everywhere: some browsers hold a clip that starts
   off screen until it is asked to play. */
(function () {
  "use strict";
  if (!('IntersectionObserver' in window)) return;
  var still = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  var io = new IntersectionObserver(function (entries) {
    entries.forEach(function (e) {
      var v = e.target;
      if (e.isIntersecting && !still) { var p = v.play(); if (p && p.catch) p.catch(function () {}); }
      else v.pause();
    });
  }, { rootMargin: '120px' });
  function scan(root) {
    Array.prototype.forEach.call((root || document).querySelectorAll('video.cover-loop'), function (v) { if (!v.__loop) { v.__loop = true; io.observe(v); } });
  }
  window.__siteLoops = scan;
  scan(document);
})();

/* A screen switch that advances on its own (data-ws-auto, in ms) until someone picks a page, and rests while pointed at. Its screens
   are the [data-ws-screen] elements (a key may appear twice, for a wide and a narrow copy); tabs ([data-ws-tab]) and arrows
   ([data-ws-prev], [data-ws-next]) pick one. */
(function () {
  "use strict";
  var still = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  function keysOf(stage) {
    var keys = [];
    Array.prototype.forEach.call(stage.querySelectorAll('[data-ws-screen]'), function (s) { var k = s.getAttribute('data-ws-screen'); if (keys.indexOf(k) < 0) keys.push(k); });
    return keys;
  }
  function current(stage, keys) {
    var at = 0;
    keys.forEach(function (k, i) { if (stage.querySelector('[data-ws-screen="' + k + '"].is-on')) at = i; });
    return at;
  }
  function show(stage, key) {
    Array.prototype.forEach.call(stage.querySelectorAll('[data-ws-screen]'), function (s) { s.classList.toggle('is-on', s.getAttribute('data-ws-screen') === key); });
    Array.prototype.forEach.call(stage.querySelectorAll('[data-ws-tab]'), function (t) {
      var on = t.getAttribute('data-ws-tab') === key; t.classList.toggle('is-on', on); t.setAttribute('aria-selected', on ? 'true' : 'false');
      // on phones the tabs sit in one row that scrolls: keep the chosen one in view
      var row = t.parentElement;
      if (on && row && row.scrollWidth > row.clientWidth + 1 && row.scrollTo) row.scrollTo({ left: t.offsetLeft - (row.clientWidth - t.offsetWidth) / 2, behavior: still ? 'auto' : 'smooth' });
    });
  }
  function step(stage, dir) {
    var keys = keysOf(stage);
    if (!keys.length) return;
    show(stage, keys[(current(stage, keys) + dir + keys.length) % keys.length]);
  }
  document.addEventListener('click', function (e) {
    var b = e.target && e.target.closest ? e.target.closest('[data-ws-prev],[data-ws-next]') : null;
    if (!b) return;
    var stage = b.closest('[data-ws-stage]');
    if (!stage) return;
    stage.__wsStopped = true;
    step(stage, b.hasAttribute('data-ws-next') ? 1 : -1);
  });
  function arm(stage) {
    if (stage.__armed) return;
    stage.__armed = true;
    if (still) return;
    var every = Number(stage.getAttribute('data-ws-auto')) || 4000, paused = false;
    stage.addEventListener('pointerenter', function () { paused = true; });
    stage.addEventListener('pointerleave', function () { paused = false; });
    stage.addEventListener('click', function (e) { if (e.target.closest && e.target.closest('[data-ws-tab]')) stage.__wsStopped = true; });
    stage.addEventListener('focusin', function () { paused = true; });
    stage.addEventListener('focusout', function () { paused = false; });
    var timer = setInterval(function () {
      if (stage.__wsStopped) { clearInterval(timer); return; }
      if (paused || !document.contains(stage)) return;
      step(stage, 1);
    }, every);
  }
  function scan(root) { Array.prototype.forEach.call((root || document).querySelectorAll('[data-ws-auto]'), arm); }
  window.__siteWs = scan;
  scan(document);
})();

/* The logos floating beside the app page's headline drift, as the page scrolls, along the line from where each rests to the centre
   of the workspace: each tile's --k sets how fast it goes, and it fades out as its bottom reaches the workspace's top edge, so the
   workspace seems to take it in. Still for reduced motion. window.__siteFloat(root) arms any layer under root added later. */
(function () {
  "use strict";
  var still = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  var layers = [], ticking = false;
  function measure(layer) {
    var lr = layer.getBoundingClientRect(), top = lr.top + window.scrollY;
    var panel = layer.parentNode.querySelector('.ws-screens'), pr = panel ? panel.getBoundingClientRect() : null;
    var goal = pr ? { x: pr.left - lr.left + pr.width / 2, y: pr.top - lr.top + pr.height / 2, top: pr.top - lr.top } : { x: lr.width / 2, y: lr.height, top: lr.height };
    layer.__m = { top: top, goal: goal, tiles: Array.prototype.map.call(layer.querySelectorAll('.fl'), function (t) {
      return { el: t, k: parseFloat(getComputedStyle(t).getPropertyValue('--k')) || .5, x: t.offsetLeft + t.offsetWidth / 2, y: t.offsetTop + t.offsetHeight / 2, h: t.offsetHeight };
    }) };
  }
  function place(layer) {
    var m = layer.__m, s = Math.max(0, window.scrollY - m.top);
    m.tiles.forEach(function (t) {
      var dy = t.k * s, span = Math.max(1, m.goal.y - t.y), p = Math.min(1.5, dy / span), dx = (m.goal.x - t.x) * p;
      // gone by the time its bottom is 120px past the workspace's top edge; the fade starts 20px before it gets there
      var reach = (t.y + t.h / 2 + dy) - (m.goal.top - 20), op = reach <= 0 ? 1 : Math.max(0, 1 - reach / 140);
      t.el.style.setProperty('--tx', dx.toFixed(1) + 'px');
      t.el.style.setProperty('--ty', dy.toFixed(1) + 'px');
      t.el.style.setProperty('--op', op.toFixed(3));
    });
  }
  function update(remeasure) {
    layers.forEach(function (l) {
      if (!document.contains(l) || !l.offsetParent) return;
      if (remeasure || !l.__m) measure(l);
      place(l);
    });
  }
  function onScroll() { if (ticking) return; ticking = true; requestAnimationFrame(function () { ticking = false; update(false); }); }
  function scan(root) {
    Array.prototype.forEach.call((root || document).querySelectorAll('[data-float]'), function (l) { if (layers.indexOf(l) < 0) layers.push(l); l.__m = null; });
    if (!still) update(true);
  }
  window.__siteFloat = scan;
  scan(document);
  if (!still) {
    window.addEventListener('scroll', onScroll, { passive: true });
    window.addEventListener('resize', function () { update(true); });
    window.addEventListener('load', function () { update(true); });
  }
})();

/* The pill nav over the Work page's hero: each pill scrolls to a shelf (no hash, so the artifact's router stays put), and the pill
   for the shelf in view lights up as the page scrolls. */
(function () {
  "use strict";
  var still = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  document.addEventListener('click', function (e) {
    var b = e.target && e.target.closest ? e.target.closest('[data-tv-jump]') : null;
    if (!b) return;
    var id = b.getAttribute('data-tv-jump'), el = id === 'top' ? null : document.getElementById(id);
    if (el) el.scrollIntoView({ behavior: still ? 'auto' : 'smooth', block: 'start' });
    else window.scrollTo({ top: 0, behavior: still ? 'auto' : 'smooth' });
  });
  var seen = [];
  function arm(nav) {
    if (seen.indexOf(nav) >= 0 || !window.IntersectionObserver) return;
    seen.push(nav);
    var pills = Array.prototype.slice.call(nav.querySelectorAll('[data-tv-jump]')), hero = nav.closest('.tv-hero');
    function light(id) { pills.forEach(function (p) { p.classList.toggle('is-on', p.getAttribute('data-tv-jump') === id); }); }
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) {
        if (!en.isIntersecting) return;
        light(en.target === hero ? 'top' : en.target.id);
      });
    }, { rootMargin: '-40% 0px -55% 0px' });
    if (hero) io.observe(hero);
    pills.forEach(function (p) { var el = document.getElementById(p.getAttribute('data-tv-jump')); if (el && el !== hero) io.observe(el); });
  }
  function scan(root) { Array.prototype.forEach.call((root || document).querySelectorAll('.tv-nav'), arm); }
  window.__siteTv = scan;
  scan(document);
})();

/* Client stories on the About page: the faces pick a story, the arrows step through them. Delegated, so it works on a page the
   artifact's router swaps in. */
(function () {
  "use strict";
  function pick(root, i) {
    var tabs = root.querySelectorAll('[data-story-tab]'), panels = root.querySelectorAll('[data-story-panel]'), n = tabs.length;
    if (!n) return;
    i = ((i % n) + n) % n;
    Array.prototype.forEach.call(tabs, function (t, k) { var on = k === i; t.classList.toggle('is-on', on); t.setAttribute('aria-selected', on ? 'true' : 'false'); });
    Array.prototype.forEach.call(panels, function (p, k) { var on = k === i; p.classList.toggle('is-on', on); p.hidden = !on; });
    root.setAttribute('data-story-at', i);
  }
  document.addEventListener('click', function (e) {
    var t = e.target && e.target.closest ? e.target.closest('[data-story-tab],[data-story-prev],[data-story-next]') : null;
    if (!t) return;
    var root = t.closest('[data-stories]');
    if (!root) return;
    var at = parseInt(root.getAttribute('data-story-at') || '0', 10);
    if (t.hasAttribute('data-story-tab')) pick(root, parseInt(t.getAttribute('data-story-tab'), 10));
    else pick(root, at + (t.hasAttribute('data-story-next') ? 1 : -1));
  });
})();

/* The content-library board on the Why Us page: productions on the left, the campaigns cut from them on the right, and lines
   between them drawn from the cards' positions. Pointing at or tapping a card lights what it fed or drew on; the board walks through
   the year on its own while on screen until someone takes over. Clicks are delegated; scan() draws and arms (the artifact's router
   calls it after swapping a page in). */
(function () {
  "use strict";
  var still = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  var NS = 'http://www.w3.org/2000/svg';
  function links(root) {
    var out = [];
    Array.prototype.forEach.call(root.querySelectorAll('[data-node][data-from]'), function (c) {
      c.getAttribute('data-from').split(' ').forEach(function (f) { if (f) out.push([f, c.getAttribute('data-node')]); });
    });
    return out;
  }
  function draw(root) {
    var svg = root.querySelector('.cl-svg'), board = root.querySelector('.cl-board');
    if (!svg || !board || getComputedStyle(svg).display === 'none' || !board.offsetParent) return;
    var br = board.getBoundingClientRect();
    svg.setAttribute('viewBox', '0 0 ' + Math.round(br.width) + ' ' + Math.round(br.height));
    while (svg.firstChild) svg.removeChild(svg.firstChild);
    links(root).forEach(function (l) {
      var a = root.querySelector('[data-node="' + l[0] + '"]'), b = root.querySelector('[data-node="' + l[1] + '"]');
      if (!a || !b) return;
      var ar = a.getBoundingClientRect(), bb = b.getBoundingClientRect();
      var x1 = ar.right - br.left, y1 = ar.top + ar.height / 2 - br.top, x2 = bb.left - br.left, y2 = bb.top + bb.height / 2 - br.top, mx = (x1 + x2) / 2;
      var path = document.createElementNS(NS, 'path');
      path.setAttribute('d', 'M' + x1.toFixed(1) + ' ' + y1.toFixed(1) + ' C ' + mx.toFixed(1) + ' ' + y1.toFixed(1) + ', ' + mx.toFixed(1) + ' ' + y2.toFixed(1) + ', ' + x2.toFixed(1) + ' ' + y2.toFixed(1));
      path.setAttribute('data-from', l[0]); path.setAttribute('data-to', l[1]);
      svg.appendChild(path);
    });
    light(root, root.getAttribute('data-flow-active') || '');
  }
  function light(root, key) {
    var cards = root.querySelectorAll('[data-node]'), paths = root.querySelectorAll('.cl-svg path'), cap = root.querySelector('[data-flow-cap]');
    var on = key ? root.querySelector('[data-node="' + key + '"]') : null;
    var linked = {};
    if (on) {
      links(root).forEach(function (l) { if (l[0] === key) linked[l[1]] = 1; if (l[1] === key) linked[l[0]] = 1; });
    }
    root.classList.toggle('has-active', !!on);
    if (key) root.setAttribute('data-flow-active', key); else root.removeAttribute('data-flow-active');
    Array.prototype.forEach.call(cards, function (c) {
      var k = c.getAttribute('data-node');
      c.classList.toggle('is-on', k === key);
      c.classList.toggle('is-linked', !!linked[k]);
      Array.prototype.forEach.call(c.querySelectorAll('[data-ref]'), function (r) { r.classList.toggle('is-on', !!on && (r.getAttribute('data-ref') === key || k === key)); });
    });
    Array.prototype.forEach.call(paths, function (p) { p.classList.toggle('is-on', !!on && (p.getAttribute('data-from') === key || p.getAttribute('data-to') === key)); });
    if (cap) cap.textContent = on ? on.getAttribute('data-caption') : cap.getAttribute('data-flow-default');
  }
  function stop(root) { root.setAttribute('data-flow-stopped', '1'); }
  document.addEventListener('click', function (e) {
    var c = e.target && e.target.closest ? e.target.closest('[data-flow] [data-node]') : null;
    if (!c) return;
    var root = c.closest('[data-flow]');
    stop(root);
    light(root, c.getAttribute('data-node'));
  });
  document.addEventListener('mouseover', function (e) {
    var c = e.target && e.target.closest ? e.target.closest('[data-flow] [data-node]') : null;
    if (!c) return;
    var root = c.closest('[data-flow]');
    stop(root);
    light(root, c.getAttribute('data-node'));
  });
  function arm(root) {
    if (root.__flow) return;
    root.__flow = true;
    if (still || !window.IntersectionObserver) return;
    var order = Array.prototype.map.call(root.querySelectorAll('[data-node]'), function (c) { return c; });
    order.sort(function (a, b) { return (parseInt(a.getAttribute('data-order'), 10) || 0) - (parseInt(b.getAttribute('data-order'), 10) || 0); });
    order = order.map(function (c) { return c.getAttribute('data-node'); });
    var at = -1, timer = null, every = parseInt(root.getAttribute('data-flow-auto') || '3600', 10);
    function tick() {
      if (root.getAttribute('data-flow-stopped') || !document.contains(root)) { if (timer) { window.clearInterval(timer); timer = null; } return; }
      at = (at + 1) % order.length;
      light(root, order[at]);
    }
    var io = new window.IntersectionObserver(function (entries) {
      entries.forEach(function (en) {
        if (en.isIntersecting) { if (!timer && !root.getAttribute('data-flow-stopped')) { tick(); timer = window.setInterval(tick, every); } }
        else if (timer) { window.clearInterval(timer); timer = null; }
      });
    }, { threshold: 0.4 });
    io.observe(root);
  }
  var roots = [];
  function scan(r) {
    Array.prototype.forEach.call((r || document).querySelectorAll('[data-flow]'), function (root) { if (roots.indexOf(root) < 0) roots.push(root); draw(root); arm(root); });
  }
  window.__siteTl = scan;
  scan(document);
  window.addEventListener('resize', function () { roots.forEach(draw); });
  window.addEventListener('load', function () { roots.forEach(draw); });
})();

/* The radio spots on a case study: one reel in an <audio>, a list of spots that each play their own stretch of it. The list is left
   alone until a spot is tapped, so pages the router keeps in memory cost nothing; any other media starting pauses the radio. */
(function () {
  "use strict";
  function arm(box) {
    if (box.__radio) return box.__radio;
    var audio = box.querySelector('audio'), cur = null, raf = 0;
    function paint() {
      if (!cur) return;
      var s = +cur.getAttribute('data-start'), e = +cur.getAttribute('data-end');
      var p = Math.min(1, Math.max(0, (audio.currentTime - s) / (e - s)));
      cur.style.setProperty('--p', p.toFixed(4));
      if (audio.currentTime >= e - 0.08) { audio.pause(); done(); return; }
      raf = requestAnimationFrame(paint);
    }
    function done() {
      cancelAnimationFrame(raf);
      if (cur) { cur.classList.remove('is-on', 'is-paused'); cur.setAttribute('aria-pressed', 'false'); cur.style.setProperty('--p', 0); }
      cur = null;
    }
    function start(btn) {
      if (cur && cur !== btn) done();
      cur = btn; btn.classList.add('is-on'); btn.classList.remove('is-paused'); btn.setAttribute('aria-pressed', 'true');
      var go = function () {
        try { audio.currentTime = +btn.getAttribute('data-start'); } catch (err) {}
        var p = audio.play(); if (p && p.catch) p.catch(function () { done(); });
      };
      if (audio.readyState >= 1) go(); else { audio.addEventListener('loadedmetadata', go, { once: true }); audio.load(); }
    }
    audio.addEventListener('play', function () { if (cur) { cur.classList.remove('is-paused'); cancelAnimationFrame(raf); raf = requestAnimationFrame(paint); } });
    audio.addEventListener('pause', function () { cancelAnimationFrame(raf); if (cur) cur.classList.add('is-paused'); });
    audio.addEventListener('ended', done);
    box.__radio = { toggle: function (btn) {
      if (cur === btn) { if (audio.paused) audio.play(); else audio.pause(); return; }
      start(btn);
    }, stop: function () { audio.pause(); done(); }, audio: audio };
    return box.__radio;
  }
  document.addEventListener('click', function (e) {
    var btn = e.target && e.target.closest ? e.target.closest('[data-radio-play]') : null;
    if (!btn) return;
    var box = btn.closest('[data-radio]'); if (!box) return;
    e.preventDefault(); arm(box).toggle(btn);
  });
  document.addEventListener('play', function (e) {  // another video or audio starting pauses the radio
    Array.prototype.forEach.call(document.querySelectorAll('[data-radio]'), function (box) {
      if (box.__radio && e.target !== box.__radio.audio && !box.__radio.audio.paused) box.__radio.stop();
    });
  }, true);
})();
