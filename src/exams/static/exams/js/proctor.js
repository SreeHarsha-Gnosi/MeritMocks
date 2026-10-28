/*
 * MeritMocks proctor: exam-hall discipline in the browser.
 *
 * A browser cannot truly stop screenshots or a determined attacker. What it
 * can do is make casual copying impossible, hide questions whenever the window
 * loses focus (which is what the OS snipping tools and screen recorders do
 * first), stamp every screen with a watermark that identifies the attempt,
 * and report every suspicious action to the server, which owns the
 * consequences (warnings, auto-submit). The real protections — answers never
 * sent to the client, one question per request, a server-side clock — live on
 * the server.
 */
(function () {
  'use strict';

  var BLOCKED_COMBOS = ['c', 'x', 'v', 'a', 's', 'p', 'u', 'f', 'g', 'j', 'k', 'i', 'h', 'o', 'e', 'd'];

  function Proctor(opts) {
    this.report = opts.report;            // function(kind)
    this.toast = opts.toast;              // function(message)
    this.gate = document.getElementById('gate');
    this.gateText = document.getElementById('gate-text');
    this.shield = document.getElementById('shield');
    this.watermark = document.getElementById('watermark');
    this.label = opts.label;
    this.active = false;
    this.lastFocusReport = 0;
    this.lastToast = 0;
    this.canFullscreen = !!(document.documentElement.requestFullscreen && document.fullscreenEnabled !== false);
  }

  Proctor.prototype.start = function () {
    this.active = true;
    this.drawWatermark();
    this.guardWatermark();
    this.blockClipboard();
    this.blockKeys();
    this.watchFocus();
    this.watchFullscreen();
    this.trapNavigation();
    if (this.canFullscreen && !document.fullscreenElement) {
      this.showGate(false);
    }
  };

  Proctor.prototype.stop = function () {
    this.active = false;
    window.onbeforeunload = null;
    if (document.fullscreenElement && document.exitFullscreen) {
      document.exitFullscreen().catch(function () {});
    }
  };

  Proctor.prototype.notify = function (message) {
    var now = Date.now();
    if (now - this.lastToast > 1500) {
      this.toast(message);
      this.lastToast = now;
    }
  };

  // ------------------------------------------------------------- watermark
  Proctor.prototype.drawWatermark = function () {
    var canvas = document.createElement('canvas');
    var ratio = window.devicePixelRatio || 1;
    var w = 360, h = 220;
    canvas.width = w * ratio;
    canvas.height = h * ratio;
    var ctx = canvas.getContext('2d');
    ctx.scale(ratio, ratio);
    ctx.translate(w / 2, h / 2);
    ctx.rotate(-Math.PI / 7);
    ctx.textAlign = 'center';
    ctx.fillStyle = 'rgba(22, 48, 92, 0.075)';
    ctx.font = '600 15px "Segoe UI", system-ui, sans-serif';
    ctx.fillText(this.label, 0, -6);
    ctx.font = '500 12px "Segoe UI", system-ui, sans-serif';
    ctx.fillText('MeritMocks · ' + new Date().toLocaleDateString('en-IN'), 0, 14);
    this.watermarkUrl = canvas.toDataURL('image/png');
    this.applyWatermarkStyle();
    this.watermarkCss = this.watermark.style.cssText;
  };

  // CSSOM writes (unlike style attributes) are allowed by our CSP.
  Proctor.prototype.applyWatermarkStyle = function () {
    var s = this.watermark.style;
    s.cssText = '';
    s.backgroundImage = 'url(' + this.watermarkUrl + ')';
    s.backgroundSize = '360px 220px';
  };

  Proctor.prototype.ensureWatermark = function () {
    var wm = this.watermark;
    if (!document.body.contains(wm)) { document.body.appendChild(wm); }
    // Only write when something changed, otherwise our own write re-triggers the observer.
    if (wm.hidden) { wm.hidden = false; }
    if (wm.className !== 'xm-watermark') { wm.className = 'xm-watermark'; }
    if (wm.style.cssText !== this.watermarkCss) { this.applyWatermarkStyle(); }
  };

  Proctor.prototype.guardWatermark = function () {
    // Removing or hiding the watermark from devtools puts it straight back.
    var ensure = this.ensureWatermark.bind(this);
    new MutationObserver(ensure).observe(document.body, { childList: true });
    new MutationObserver(ensure).observe(this.watermark, { attributes: true, attributeFilter: ['style', 'class', 'hidden'] });
  };

  // ------------------------------------------------------------- clipboard
  Proctor.prototype.blockClipboard = function () {
    var self = this;
    function isField(t) { return t && (t.tagName === 'INPUT' || t.tagName === 'TEXTAREA'); }
    ['copy', 'cut', 'paste'].forEach(function (type) {
      document.addEventListener(type, function (e) {
        e.preventDefault();
        if (e.clipboardData) { e.clipboardData.setData('text/plain', ''); }
        self.report(type === 'paste' ? 'paste' : 'copy');
        self.notify('Copying and pasting are disabled during the test.');
      }, true);
    });
    document.addEventListener('contextmenu', function (e) {
      e.preventDefault();
      self.report('context_menu');
      self.notify('Right-click is disabled during the test.');
    }, true);
    document.addEventListener('selectstart', function (e) { if (!isField(e.target)) { e.preventDefault(); } }, true);
    document.addEventListener('dragstart', function (e) { e.preventDefault(); }, true);
    document.addEventListener('drop', function (e) { e.preventDefault(); }, true);
    window.addEventListener('beforeprint', function () {
      self.report('print');
      self.notify('Printing is disabled during the test.');
    });
  };

  // ------------------------------------------------------------------ keys
  Proctor.prototype.blockKeys = function () {
    var self = this;
    document.addEventListener('keydown', function (e) {
      var key = (e.key || '').toLowerCase();
      var mod = e.ctrlKey || e.metaKey;
      if (key === 'f12' || (mod && e.shiftKey && 'ijck'.indexOf(key) !== -1) || (e.metaKey && e.altKey && 'ijcu'.indexOf(key) !== -1)) {
        e.preventDefault();
        self.report('devtools_key');
        self.notify('Developer tools are not allowed during the test.');
        return;
      }
      // macOS screenshot shortcuts (Cmd+Shift+3/4/5).
      if (e.metaKey && e.shiftKey && '345'.indexOf(key) !== -1) {
        e.preventDefault();
        self.flashShield();
        self.report('print_screen');
        return;
      }
      if (mod && BLOCKED_COMBOS.indexOf(key) !== -1) {
        e.preventDefault();
        var kind = key === 'p' ? 'print' : key === 'a' ? 'select_all' : (key === 'u' || key === 's') ? 'devtools_key' : 'copy';
        self.report(kind);
        self.notify('That shortcut is disabled during the test.');
        return;
      }
      if (key === 'printscreen') {
        e.preventDefault();
        self.onPrintScreen();
      }
      if (key === 'f5' || (mod && key === 'r')) {
        e.preventDefault();
        self.notify('Refreshing is disabled. Your timer keeps running on the server.');
      }
    }, true);
    // Windows only fires keyup for PrintScreen.
    document.addEventListener('keyup', function (e) {
      if ((e.key || '').toLowerCase() === 'printscreen') { self.onPrintScreen(); }
    }, true);
  };

  Proctor.prototype.onPrintScreen = function () {
    this.flashShield();
    this.report('print_screen');
    this.notify('Screenshots are not allowed. This attempt is watermarked.');
    if (navigator.clipboard && navigator.clipboard.writeText) {
      navigator.clipboard.writeText('').catch(function () {});
    }
  };

  // ----------------------------------------------------------------- focus
  Proctor.prototype.setShield = function (on) {
    document.body.classList.toggle('is-shielded', on);
  };

  Proctor.prototype.flashShield = function () {
    var self = this;
    this.setShield(true);
    setTimeout(function () { if (document.hasFocus()) { self.setShield(false); } }, 1200);
  };

  Proctor.prototype.focusLost = function () {
    if (!this.active) { return; }
    this.setShield(true);
    var now = Date.now();
    if (now - this.lastFocusReport > 2000) {
      this.lastFocusReport = now;
      this.report('focus_lost');
    }
  };

  Proctor.prototype.watchFocus = function () {
    var self = this;
    window.addEventListener('blur', function () { self.focusLost(); });
    document.addEventListener('visibilitychange', function () {
      if (document.visibilityState === 'hidden') { self.focusLost(); }
    });
    window.addEventListener('focus', function () { self.setShield(false); });
    if (!document.hasFocus()) { this.setShield(true); }
  };

  // ------------------------------------------------------------ fullscreen
  Proctor.prototype.showGate = function (violation) {
    this.gateText.textContent = violation
      ? 'You left full-screen mode. This has been recorded as a violation. Your timer is still running.'
      : 'This test runs in full-screen mode, just like the exam centre. Your timer is running.';
    this.gate.classList.add('is-open');
  };

  Proctor.prototype.watchFullscreen = function () {
    var self = this;
    if (!this.canFullscreen) { return; }
    document.getElementById('gate-btn').addEventListener('click', function () {
      document.documentElement.requestFullscreen({ navigationUI: 'hide' }).then(function () {
        self.gate.classList.remove('is-open');
      }).catch(function () {
        self.notify('Your browser blocked full-screen mode. Please allow it to continue.');
      });
    });
    document.addEventListener('fullscreenchange', function () {
      if (!self.active) { return; }
      if (document.fullscreenElement) {
        self.gate.classList.remove('is-open');
      } else {
        self.showGate(true);
        self.report('fullscreen_exit');
      }
    });
  };

  // ------------------------------------------------------------ navigation
  Proctor.prototype.trapNavigation = function () {
    var self = this;
    history.pushState({ exam: true }, '', location.href);
    window.addEventListener('popstate', function () {
      if (!self.active) { return; }
      history.pushState({ exam: true }, '', location.href);
      self.notify('Use the Submit button to finish the test.');
    });
    window.onbeforeunload = function (e) {
      if (!self.active) { return undefined; }
      e.preventDefault();
      e.returnValue = '';
      return '';
    };
  };

  window.MMProctor = Proctor;
})();
