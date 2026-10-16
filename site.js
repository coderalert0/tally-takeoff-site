// Tally support site: the support address, searching the guide and the questions, the guide's contents, the screen map,
// a full-size view of each screenshot, and back to top. Every page reads fine without it.
(function () {
  // The support address is written here, not in the pages, so it isn't sitting in the source for scrapers.
  var user = 'laddothis', domain = 'gmail.com';
  var mailto = 'ma' + 'ilto:' + user + '@' + domain + '?subject=Construction%20Takeoff%20-%20Tally';
  document.querySelectorAll('.email').forEach(function (el) {
    var a = document.createElement('a');
    a.href = mailto;
    a.textContent = user + '@' + domain;
    el.replaceChildren(a);
  });
  document.querySelectorAll('a.mail').forEach(function (a) { a.href = mailto; });

  // Screenshots open full size.
  var viewer = document.createElement('dialog');
  viewer.className = 'viewer';
  var big = document.createElement('img');
  viewer.appendChild(big);
  document.body.appendChild(viewer);
  viewer.addEventListener('click', function () { viewer.close(); });
  document.querySelectorAll('a.zoom').forEach(function (a) {
    a.addEventListener('click', function (e) {
      if (typeof viewer.showModal !== 'function') return;
      e.preventDefault();
      var img = a.querySelector('img');
      big.src = a.href;
      big.alt = img ? img.alt : '';
      viewer.showModal();
    });
  });

  // The screen map: a number in the list and its pin on the screenshot light up together.
  document.querySelectorAll('.legend li[data-pin]').forEach(function (li) {
    var pin = document.querySelector('.pin[data-pin="' + li.dataset.pin + '"]');
    if (!pin) return;
    var on = function () { li.classList.add('on'); pin.classList.add('on'); };
    var off = function () { li.classList.remove('on'); pin.classList.remove('on'); };
    li.addEventListener('mouseenter', on); li.addEventListener('mouseleave', off);
    pin.addEventListener('mouseenter', on); pin.addEventListener('mouseleave', off);
  });

  // The guide's contents follow the reader.
  var tocLinks = Array.prototype.slice.call(document.querySelectorAll('.sidebar .toc a[href^="#"]'));
  if (tocLinks.length && 'IntersectionObserver' in window) {
    var byId = {};
    tocLinks.forEach(function (a) { byId[a.getAttribute('href').slice(1)] = a; });
    var observer = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (!entry.isIntersecting) return;
        tocLinks.forEach(function (a) { a.classList.remove('active'); });
        var link = byId[entry.target.id];
        if (link) link.classList.add('active');
      });
    }, { rootMargin: '-15% 0px -75% 0px' });
    document.querySelectorAll('.g-section[id]').forEach(function (s) { observer.observe(s); });
  }
  // On a phone, the contents close once a section is picked.
  document.querySelectorAll('.mtoc a').forEach(function (a) {
    a.addEventListener('click', function () { var d = a.closest('details'); if (d) d.open = false; });
  });

  // Search: hides what doesn't mention every word typed and marks the words in what's left.
  function words(value) { return value.toLowerCase().trim().split(/\s+/).filter(Boolean); }
  function mark(blocks, terms) {
    if (!window.CSS || !CSS.highlights || typeof Highlight !== 'function') return;
    CSS.highlights.delete('hit');
    if (!terms.length) return;
    var ranges = [];
    blocks.forEach(function (block) {
      var walker = document.createTreeWalker(block, NodeFilter.SHOW_TEXT);
      for (var node = walker.nextNode(); node; node = walker.nextNode()) {
        var text = node.nodeValue.toLowerCase();
        terms.forEach(function (t) {
          for (var i = text.indexOf(t); i !== -1; i = text.indexOf(t, i + t.length)) {
            var r = new Range();
            r.setStart(node, i); r.setEnd(node, i + t.length);
            ranges.push(r);
          }
        });
      }
    });
    CSS.highlights.set('hit', new Highlight(...ranges));
  }
  function searchable(input, blocks, opts) {
    if (!input) return;
    var status = document.getElementById(opts.status);
    var empty = document.getElementById(opts.empty);
    var run = function () {
      var terms = words(input.value);
      var shown = [];
      blocks.forEach(function (b) {
        var text = (b.textContent + ' ' + (b.dataset.k || '')).toLowerCase();
        var hit = terms.every(function (t) { return text.indexOf(t) !== -1; });
        b.hidden = !hit;
        if (hit) shown.push(b);
        if (opts.each) opts.each(b, hit, terms.length > 0);
      });
      if (opts.after) opts.after(terms.length > 0);
      mark(shown, terms);
      if (empty) empty.hidden = shown.length > 0;
      if (status) {
        if (!terms.length) status.textContent = '';
        else if (!shown.length) status.textContent = 'Nothing matches “' + input.value.trim() + '”.';
        else {
          status.textContent = shown.length + ' ' + (shown.length === 1 ? opts.one : opts.many) + ' — ';
          var go = document.createElement('a');
          go.href = '#' + shown[0].id;
          go.textContent = 'go to the first';
          status.appendChild(go);
        }
      }
      return shown;
    };
    input.addEventListener('input', run);
    input.addEventListener('keydown', function (e) {
      if (e.key === 'Enter') {
        e.preventDefault();
        var shown = run();
        if (shown.length) shown[0].scrollIntoView({ block: 'start' });
      } else if (e.key === 'Escape') {
        input.value = ''; run();
      }
    });
    var q = new URLSearchParams(location.search).get('q');
    if (q) { input.value = q; run(); }
  }

  // The guide: sections, with their entries in the contents dimmed when they don't match.
  var sections = Array.prototype.slice.call(document.querySelectorAll('.g-section'));
  searchable(document.getElementById('guide-search'), sections, {
    status: 'search-status', empty: 'no-results', one: 'section matches', many: 'sections match',
    each: function (s, hit) {
      document.querySelectorAll('.toc a[href="#' + s.id + '"]').forEach(function (a) { a.classList.toggle('dim', !hit); });
    }
  });

  // The questions: matching ones open, groups with none left hide.
  var questions = Array.prototype.slice.call(document.querySelectorAll('details.qa'));
  searchable(document.getElementById('faq-search'), questions, {
    status: 'faq-status', empty: 'faq-empty', one: 'answer matches', many: 'answers match',
    each: function (d, hit, searching) { if (searching) d.open = hit; else d.open = false; },
    after: function () {
      document.querySelectorAll('.faq-group').forEach(function (g) {
        g.hidden = !g.querySelector('details.qa:not([hidden])');
      });
    }
  });
  // A link to a question opens it.
  function openHash() {
    var id = decodeURIComponent(location.hash.slice(1));
    var target = id && document.getElementById(id);
    if (target && target.tagName === 'DETAILS') target.open = true;
  }
  window.addEventListener('hashchange', openHash);
  openHash();

  // Back to top.
  var top = document.querySelector('.totop');
  if (top) {
    var onScroll = function () { top.classList.toggle('show', window.scrollY > 900); };
    window.addEventListener('scroll', onScroll, { passive: true });
    top.addEventListener('click', function () { window.scrollTo({ top: 0 }); });
    onScroll();
  }
})();
