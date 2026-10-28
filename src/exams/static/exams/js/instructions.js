(function () {
  'use strict';
  var root = document.querySelector('.ins');
  function show(step) {
    root.setAttribute('data-step', step);
    root.querySelector('.ins__scroll').scrollTop = 0;
  }
  document.querySelectorAll('[data-goto]').forEach(function (btn) {
    btn.addEventListener('click', function () { show(btn.getAttribute('data-goto')); });
  });
  var form = document.getElementById('start-form');
  form.addEventListener('submit', function () {
    document.getElementById('begin').disabled = true;
  });
})();
