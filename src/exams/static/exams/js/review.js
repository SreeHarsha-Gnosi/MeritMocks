/* Solutions page: filters, plus the same copy/print deterrents as the exam. */
(function () {
  'use strict';
  var sol = document.getElementById('sol');
  if (!sol) { return; }

  document.querySelectorAll('[data-filter]').forEach(function (btn) {
    btn.addEventListener('click', function () {
      var f = btn.getAttribute('data-filter');
      document.querySelectorAll('[data-filter]').forEach(function (b) { b.classList.toggle('is-on', b === btn); });
      sol.querySelectorAll('.sol-q').forEach(function (q) {
        q.hidden = f !== 'all' && q.getAttribute('data-outcome') !== f;
      });
    });
  });

  ['copy', 'cut'].forEach(function (type) {
    document.addEventListener(type, function (e) { e.preventDefault(); }, true);
  });
  document.addEventListener('contextmenu', function (e) { e.preventDefault(); }, true);
  document.addEventListener('dragstart', function (e) { e.preventDefault(); }, true);
  document.addEventListener('keydown', function (e) {
    var key = (e.key || '').toLowerCase();
    if ((e.ctrlKey || e.metaKey) && 'cxasup'.indexOf(key) !== -1) { e.preventDefault(); }
    if (key === 'f12' || ((e.ctrlKey || e.metaKey) && e.shiftKey && 'ijc'.indexOf(key) !== -1)) { e.preventDefault(); }
  }, true);

  var canvas = document.createElement('canvas');
  var ratio = window.devicePixelRatio || 1;
  canvas.width = 360 * ratio;
  canvas.height = 220 * ratio;
  var ctx = canvas.getContext('2d');
  ctx.scale(ratio, ratio);
  ctx.translate(180, 110);
  ctx.rotate(-Math.PI / 7);
  ctx.textAlign = 'center';
  ctx.fillStyle = 'rgba(22, 48, 92, 0.06)';
  ctx.font = '600 15px "Plus Jakarta Sans", system-ui, sans-serif';
  ctx.fillText(sol.getAttribute('data-label'), 0, -6);
  ctx.font = '500 12px system-ui, sans-serif';
  ctx.fillText('MeritMocks · solutions', 0, 14);
  var wm = document.getElementById('watermark');
  wm.style.backgroundImage = 'url(' + canvas.toDataURL('image/png') + ')';
  wm.style.backgroundSize = '360px 220px';
})();
