/*
 * MeritMocks exam client. The server is the source of truth for the clock,
 * the open section and every response; this file only renders that state and
 * sends the candidate's actions.
 */
(function () {
  'use strict';

  var cfg = JSON.parse(document.getElementById('exam-config').textContent);
  var csrf = document.querySelector('input[name=csrfmiddlewaretoken]').value;
  var $ = function (id) { return document.getElementById(id); };

  var STATUS_LABELS = {
    answered: 'Answered',
    not_answered: 'Not Answered',
    not_visited: 'Not Visited',
    marked: 'Marked for Review',
    answered_marked: 'Answered & Marked for Review'
  };

  var S = {
    state: null,
    q: null,
    selected: null,
    sectionIndex: null,
    warnings: null,
    deadline: 0,
    expiring: false,
    busy: false,
    done: false,
    passageId: null
  };

  // ------------------------------------------------------------------ utils
  function toast(message) {
    var el = $('toast');
    el.textContent = message;
    el.classList.add('is-open');
    clearTimeout(toast.t);
    toast.t = setTimeout(function () { el.classList.remove('is-open'); }, 3200);
  }

  function el(tag, cls, text) {
    var node = document.createElement(tag);
    if (cls) { node.className = cls; }
    if (text !== undefined) { node.textContent = text; }
    return node;
  }

  function pad(n) { return (n < 10 ? '0' : '') + n; }

  function openModal(id) { $(id).hidden = false; }
  function closeModal(id) { $(id).hidden = true; }

  // -------------------------------------------------------------------- api
  function api(name, body) {
    return fetch(cfg.urls[name], {
      method: 'POST',
      credentials: 'same-origin',
      cache: 'no-store',
      headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': csrf,
        'X-Exam-Window': cfg.token
      },
      body: JSON.stringify(body || {})
    }).then(function (res) {
      return res.json().catch(function () { return {}; }).then(function (data) {
        if (data.state) { applyState(data.state); }
        if (data.redirect) { finish(data.redirect); }
        if (!res.ok) {
          handleError(res.status, data);
          throw data;
        }
        return data;
      });
    }, function (err) {
      toast('Connection problem — your answers are safe. Retrying…');
      throw err;
    });
  }

  function handleError(status, data) {
    switch (data.error) {
      case 'another_window':
        lock('Test closed in this window',
          'This test was opened in another window or tab. It can only be active in one place at a time.');
        break;
      case 'submitted':
        break;
      case 'section_locked':
      case 'section_closed':
        toast('That section is closed.');
        refresh();
        break;
      case 'rate_limited':
        toast('Too many requests. Please slow down.');
        break;
      case 'not_last_section':
        toast('You can submit only in the last section.');
        break;
      default:
        toast(status === 403 ? 'Your session has expired. Please reload the page.' : 'Something went wrong. Please try again.');
    }
  }

  function refresh() {
    return api('state').catch(function () {});
  }

  function finish(url) {
    if (S.done) { return; }
    S.done = true;
    proctor.stop();
    document.body.classList.add('is-finishing');
    location.replace(url);
  }

  function lock(title, text) {
    S.done = true;
    proctor.stop();
    $('lock-title').textContent = title;
    $('lock-text').textContent = text;
    $('lock-btn').href = location.href;
    $('lock').hidden = false;
  }

  // ------------------------------------------------------------------ state
  function applyState(st) {
    var previous = S.sectionIndex;
    S.state = st;
    S.deadline = performance.now() + st.remaining * 1000;
    S.expiring = false;
    if (st.status !== 'in_progress') { return; }

    renderSections(st);
    renderPalette(st);
    renderCounts(st);

    var last = st.section_index === st.sections.length - 1;
    $('btn-submit').disabled = !last;
    $('submit-hint').hidden = last;

    if (S.warnings !== null && st.warnings > S.warnings) { showWarning(st); }
    S.warnings = st.warnings;

    S.sectionIndex = st.section_index;
    if (previous !== null && previous !== st.section_index) {
      toast('Time for ' + st.sections[previous].name + ' is over. ' + st.sections[st.section_index].name + ' has started.');
      S.passageId = null;
      loadQuestion(st.palette[0].n);
    }
  }

  function renderSections(st) {
    var nav = $('sections');
    nav.textContent = '';
    st.sections.forEach(function (s) {
      var tab = el('div', 'xm-tab xm-tab--' + s.state);
      tab.appendChild(el('span', 'xm-tab__name', s.name));
      var badge = el('span', 'xm-tab__badge');
      badge.textContent = s.state === 'done' ? '✓' : s.state === 'upcoming' ? s.minutes + 'm' : 'ⓘ';
      tab.appendChild(badge);
      if (s.state === 'active') {
        tab.setAttribute('aria-current', 'step');
        var tip = el('div', 'xm-tab__tip');
        var counts = countStatuses(st.palette);
        Object.keys(STATUS_LABELS).forEach(function (key) {
          var row = el('div', 'xm-tab__tiprow');
          row.appendChild(el('span', 'st st--' + key, String(counts[key])));
          row.appendChild(el('span', '', STATUS_LABELS[key]));
          tip.appendChild(row);
        });
        tab.appendChild(tip);
      } else {
        tab.title = s.state === 'done' ? 'This section is over' : 'Opens after the current section';
      }
      nav.appendChild(tab);
    });
    $('pal-section').textContent = st.sections[st.section_index].name;
  }

  function countStatuses(palette) {
    var counts = { answered: 0, not_answered: 0, not_visited: 0, marked: 0, answered_marked: 0 };
    palette.forEach(function (p) { counts[p.s] += 1; });
    return counts;
  }

  function renderCounts(st) {
    var counts = countStatuses(st.palette);
    document.querySelectorAll('#legend .st').forEach(function (node) {
      var key = node.className.replace('st st--', '');
      node.textContent = counts[key];
    });
  }

  function renderPalette(st) {
    var grid = $('palette');
    grid.textContent = '';
    var current = S.q ? S.q.n : st.current;
    st.palette.forEach(function (p) {
      var btn = el('button', 'st st--' + p.s + (p.n === current ? ' is-current' : ''), String(p.n));
      btn.type = 'button';
      btn.setAttribute('aria-label', 'Question ' + p.n + ', ' + STATUS_LABELS[p.s]);
      btn.addEventListener('click', function () {
        if (S.q && S.q.n === p.n) { return; }
        loadQuestion(p.n);
        closeDrawer();
      });
      grid.appendChild(btn);
    });
  }

  // --------------------------------------------------------------- question
  function loadQuestion(n) {
    if (S.done) { return; }
    $('qbody').classList.add('is-loading');
    return api('question', { n: n }).then(function (data) {
      renderQuestion(data.question);
    }).catch(function () {}).then(function () {
      $('qbody').classList.remove('is-loading');
      document.body.classList.remove('is-booting');
    });
  }

  function renderQuestion(q) {
    S.q = q;
    S.selected = q.selected;
    $('qno').textContent = q.n;
    $('mpos').textContent = '+' + q.marks.positive;
    $('mneg').textContent = '−' + q.marks.negative;

    var body = $('qbody');
    var passage = $('passage');
    var inlineDir = $('inline-dir');
    var p = q.passage;
    var split = p && p.layout === 'split';
    body.classList.toggle('is-split', !!split);
    passage.hidden = !split;
    inlineDir.hidden = !(p && !split);

    // Staff-authored HTML from our own database; the CSP blocks any script in it.
    if (split) {
      if (S.passageId !== p.id) {
        $('passage-dir').innerHTML = p.directions;
        $('passage-body').innerHTML = p.body;
        passage.scrollTop = 0;
      }
    } else if (p) {
      inlineDir.innerHTML = '<div class="xm-inline-dir__d">' + p.directions + '</div>' + (p.body ? '<div class="xm-inline-dir__b">' + p.body + '</div>' : '');
    }
    S.passageId = p ? p.id : null;

    $('qtext').innerHTML = q.text;
    var opts = $('options');
    opts.textContent = '';
    q.options.forEach(function (o) {
      var label = el('label', 'xm-opt' + (o.i === S.selected ? ' is-selected' : ''));
      var input = el('input');
      input.type = 'radio';
      input.name = 'opt';
      input.value = o.i;
      input.checked = o.i === S.selected;
      input.addEventListener('change', function () {
        S.selected = o.i;
        opts.querySelectorAll('.xm-opt').forEach(function (n) { n.classList.remove('is-selected'); });
        label.classList.add('is-selected');
      });
      label.appendChild(input);
      label.appendChild(el('span', 'xm-opt__dot'));
      label.appendChild(el('span', 'xm-opt__text', o.text));
      opts.appendChild(label);
    });
    document.querySelector('.xm-question').scrollTop = 0;

    document.querySelectorAll('#palette .st').forEach(function (b) {
      b.classList.toggle('is-current', b.textContent === String(q.n));
    });
  }

  function nextNumber() {
    var list = S.state.palette.map(function (p) { return p.n; });
    var i = list.indexOf(S.q.n);
    return list[(i + 1) % list.length];
  }

  function act(action) {
    if (S.busy || !S.q || S.done) { return; }
    S.busy = true;
    var n = S.q.n;
    var option = action === 'clear' ? null : S.selected;
    api('answer', { n: n, action: action, option: option }).then(function () {
      if (action === 'clear') {
        S.selected = null;
        S.q.selected = null;
        $('options').querySelectorAll('input').forEach(function (i) { i.checked = false; });
        $('options').querySelectorAll('.xm-opt').forEach(function (l) { l.classList.remove('is-selected'); });
        return null;
      }
      return loadQuestion(nextNumber());
    }).catch(function () {}).then(function () { S.busy = false; });
  }

  // ------------------------------------------------------------------ timer
  function tick() {
    if (S.done || !S.state) { return; }
    var remaining = Math.max(0, Math.ceil((S.deadline - performance.now()) / 1000));
    var h = Math.floor(remaining / 3600);
    var m = Math.floor((remaining % 3600) / 60);
    var s = remaining % 60;
    $('timer').textContent = (h ? h + ':' + pad(m) : pad(m)) + ':' + pad(s);
    var box = $('timer-box');
    box.classList.toggle('is-warn', remaining <= 300 && remaining > 60);
    box.classList.toggle('is-danger', remaining <= 60);
    if (remaining === 0 && !S.expiring) {
      S.expiring = true;
      setTimeout(refresh, 700);
    }
  }

  // ------------------------------------------------------------- warnings
  function showWarning(st) {
    var max = st.max_warnings;
    $('warn-count').textContent = max ? st.warnings + ' of ' + max : st.warnings;
    $('warn-text').textContent = 'You moved away from the test window or left full-screen mode. This has been recorded.' +
      (max ? ' At ' + max + ' warnings your test will be submitted automatically.' : '');
    openModal('warn-modal');
  }

  // ----------------------------------------------------------------- submit
  function openSummary() {
    if (S.busy) { return; }
    api('summary').then(function (data) {
      var tbody = $('summary-body');
      tbody.textContent = '';
      data.summary.forEach(function (row) {
        var tr = el('tr');
        [row.name, row.total, row.answered, row.not_answered, row.marked, row.answered_marked, row.not_visited]
          .forEach(function (v) { tr.appendChild(el('td', '', String(v))); });
        tbody.appendChild(tr);
      });
      openModal('submit-modal');
    }).catch(function () {});
  }

  function confirmSubmit() {
    var btn = $('confirm-submit');
    btn.disabled = true;
    api('submit').catch(function () { btn.disabled = false; });
  }

  // ----------------------------------------------------------------- layout
  function closeDrawer() { $('xm').classList.remove('is-drawer-open'); }

  function bind() {
    $('btn-save').addEventListener('click', function () { act('save'); });
    $('btn-mark').addEventListener('click', function () { act('mark'); });
    $('btn-clear').addEventListener('click', function () { act('clear'); });
    $('btn-submit').addEventListener('click', openSummary);
    $('confirm-submit').addEventListener('click', confirmSubmit);
    $('side-toggle').addEventListener('click', function () {
      var xm = $('xm');
      var mobile = window.matchMedia('(max-width: 860px)').matches;
      var cls = mobile ? 'is-drawer-open' : 'is-collapsed';
      xm.classList.toggle(cls);
      this.setAttribute('aria-expanded', String(mobile ? xm.classList.contains(cls) : !xm.classList.contains(cls)));
    });
    document.querySelectorAll('[data-open]').forEach(function (b) {
      b.addEventListener('click', function () { openModal(b.getAttribute('data-open')); });
    });
    document.querySelectorAll('[data-close]').forEach(function (b) {
      b.addEventListener('click', function () {
        b.closest('.xm-modal').hidden = true;
        $('confirm-submit').disabled = false;
      });
    });
    document.addEventListener('visibilitychange', function () {
      if (document.visibilityState === 'visible') { refresh(); }
    });
  }

  // ------------------------------------------------------------------- boot
  var proctor = new window.MMProctor({
    label: cfg.candidate + ' · ' + cfg.attemptId,
    toast: toast,
    report: function (kind) {
      if (S.done) { return; }
      api('event', { kind: kind }).catch(function () {});
    }
  });

  $('cand-name').textContent = cfg.candidate;
  $('cand-id').textContent = cfg.attemptId;
  bind();
  proctor.start();

  api('state').then(function (data) {
    var st = data.state;
    if (st.status !== 'in_progress') { return; }
    loadQuestion(st.current || st.palette[0].n);
  }).catch(function () {});

  setInterval(tick, 250);
  setInterval(refresh, 30000);
})();
