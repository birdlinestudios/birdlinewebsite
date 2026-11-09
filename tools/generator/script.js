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
  var each = function (list, fn) { Array.prototype.forEach.call(list, fn); };
  function setAccordion(item, open) {
    item.classList.toggle('is-open', open);
    var head = item.querySelector('.nav-acc');
    if (head) head.setAttribute('aria-expanded', open ? 'true' : 'false');
  }
  function setMenu(open) {
    if (!bar) return;
    var btn = bar.querySelector('[data-menu]');
    bar.classList.toggle('is-open', open);
    if (btn) btn.setAttribute('aria-expanded', open ? 'true' : 'false');
    if (!open) each(bar.querySelectorAll('.nav-item.is-open'), function (it) { setAccordion(it, false); });
    paintBar();
  }
  listen('click', function (e) {
    var btn = e.target && e.target.closest ? e.target.closest('[data-menu]') : null;
    if (btn) { setMenu(!bar.classList.contains('is-open')); return; }
    if (!(bar && bar.classList.contains('is-open') && e.target.closest)) return;
    // in the phone sheet, Work and Services are accordion buttons; their pages are the rows inside
    var head = e.target.closest('.nav-acc');
    if (head) {
      var item = head.parentNode, open = !item.classList.contains('is-open');
      each(bar.querySelectorAll('.nav-item.is-open'), function (it) { if (it !== item) setAccordion(it, false); });
      setAccordion(item, open);
      if (open) win.setTimeout(function () {
        var sheet = bar.querySelector('.nav');
        if (sheet) sheet.scrollTo({ top: head.offsetTop - 4, behavior: 'smooth' });
      }, 60);
      return;
    }
    if (e.target.closest('.nav a')) setMenu(false);
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
