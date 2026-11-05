/* The artifact's router. The artifact viewer shows one document and does not follow links to the other published pages, so here the
   whole site lives in this one document: #work, #case-studies, #cs-<slug>, #packages, #about, #workspace, #all-services and #svc-<slug>
   name the other pages, whose content is fetched from the files published alongside this one (portfolio.html, case-studies/<slug>.html,
   services/<slug>.html and so on) and swapped in for <main>.
   The homepage's own <main> is kept, not rebuilt, so the calculator and everything else bound to it keep working.
   Any other hash (#services, #faq, #top) is a place on the homepage. The site folder has no need of this: there the pages are real. */
(function () {
  "use strict";
  window.__artifact = true;
  var home = document.querySelector('.page > main');
  if (!home || !window.fetch || !window.DOMParser) return;
  var holder = home.parentNode, homeTitle = document.title, cache = {}, started = false;
  var base = new URL('.', document.baseURI);

  function fileFor(key) {
    if (key === 'work') return 'portfolio.html';
    if (key === 'case-studies') return 'case-studies.html';
    if (key === 'packages') return 'packages.html';
    if (key === 'about') return 'about.html';
    if (key === 'workspace') return 'workspace.html';
    if (key === 'all-services') return 'services.html';
    if (key === 'why-us') return 'why-us.html';
    if (key === 'rops') return 'rops.html';
    if (/^cs-[a-z0-9-]+$/.test(key)) return 'case-studies/' + key.slice(3) + '.html';
    if (/^svc-[a-z0-9-]+$/.test(key)) return 'services/' + key.slice(4) + '.html';
    return null;
  }
  // a link to one of the site's pages becomes a hash; anything else keeps its address
  function hashFor(u) {
    if (u.origin !== base.origin || u.pathname.indexOf(base.pathname) !== 0) return null;
    var rel = u.pathname.slice(base.pathname.length), m;
    if (rel === 'portfolio.html') return '#work';
    if (rel === 'case-studies.html') return '#case-studies';
    if (rel === 'packages.html') return '#packages' + (u.hash === '#plans' ? '' : '');
    if (rel === 'about.html') return '#about';
    if (rel === 'workspace.html') return '#workspace';
    if (rel === 'services.html') return '#all-services';
    if (rel === 'why-us.html') return '#why-us';
    if (rel === 'rops.html') return '#rops';
    if ((m = rel.match(/^case-studies\/([a-z0-9-]+)\.html$/))) return '#cs-' + m[1];
    if ((m = rel.match(/^services\/([a-z0-9-]+)\.html$/))) return '#svc-' + m[1];
    if (rel === 'index.html' || rel === '') return u.hash || '#top';
    return null;
  }
  // the fetched page's <main>, with its images and links made to work from this document
  function adopt(doc, pageURL) {
    var m = doc.querySelector('main');
    if (!m) return null;
    // every page-relative media reference: src, a video's poster, and the data-* URLs the lightbox player reads
    var MEDIA = ['src', 'poster', 'data-src', 'data-poster'];
    Array.prototype.forEach.call(m.querySelectorAll('[src],[poster],[data-src],[data-poster],[srcset]'), function (el) {
      MEDIA.forEach(function (name) {
        var v = el.getAttribute(name);
        if (v && !/^(https?:|data:|blob:)/i.test(v)) el.setAttribute(name, new URL(v, pageURL).href);
      });
      var ss = el.getAttribute('srcset');
      if (ss) el.setAttribute('srcset', ss.split(',').map(function (c) {
        var p = c.trim().split(/\s+/);
        if (p[0] && !/^(https?:|data:|blob:)/i.test(p[0])) p[0] = new URL(p[0], pageURL).href;
        return p.join(' ');
      }).join(', '));
    });
    Array.prototype.forEach.call(m.querySelectorAll('a[href]'), function (a) {
      var v = a.getAttribute('href');
      if (!v || /^(https?:|mailto:|tel:|#)/i.test(v)) return;
      var u = new URL(v, pageURL), h = hashFor(u);
      if (h) { a.setAttribute('href', h); a.removeAttribute('target'); }
      else a.setAttribute('href', u.href);
    });
    // "top" belongs to the homepage's hero, so a sub-page's hero gives it up: #top then always leads home
    Array.prototype.forEach.call(m.querySelectorAll('[id="top"]'), function (el) { el.id = 'page-top'; });
    return { main: m, title: doc.title };
  }
  function load(key) {
    var file = fileFor(key), pageURL = new URL(file, document.baseURI);
    return fetch(file, { credentials: 'same-origin' }).then(function (r) { if (!r.ok) throw new Error(r.status); return r.text(); })
      .then(function (text) { cache[key] = adopt(new DOMParser().parseFromString(text, 'text/html'), pageURL); });
  }
  var pending = 0;
  function show(key, frag, initial) {
    var target = key ? cache[key] : { main: home, title: homeTitle };
    if (!target) {
      var n = ++pending;
      load(key).then(function () { if (n === pending) show(key, frag, initial); }).catch(function () { if (n === pending) show('', '', initial); });
      return;
    }
    var cur = holder.querySelector(':scope > main');
    if (cur !== target.main) {
      holder.replaceChild(target.main, cur);
      document.title = target.title;
    }
    if (window.__birdline && window.__birdline.scan) window.__birdline.scan();
    if (window.__siteMasonry) window.__siteMasonry(target.main);
    if (window.__birdlineCalc) window.__birdlineCalc(target.main);
    if (window.__siteVideo) window.__siteVideo(target.main);
    if (window.__siteWs) window.__siteWs(target.main);
    if (window.__siteFloat) window.__siteFloat(target.main);
    if (window.__siteTv) window.__siteTv(target.main);
    if (window.__siteTl) window.__siteTl(target.main);
    var el = frag ? document.getElementById(frag) : null;
    if (el) el.scrollIntoView();
    else if (!initial || key) window.scrollTo(0, 0);
  }
  function route(initial) {
    var h = decodeURIComponent(location.hash.slice(1));
    if (fileFor(h)) { show(h, '', initial); return; }
    // a place on the page already showing (a sub-page's own #plans, say) is just scrolled to; anything else is a place on the homepage
    var el = h ? document.getElementById(h) : null, cur = holder.querySelector(':scope > main');
    if (el && cur !== home && cur.contains(el)) { el.scrollIntoView(); return; }
    show('', h, initial);
  }
  window.addEventListener('hashchange', function () { route(false); });
  route(true);
})();
