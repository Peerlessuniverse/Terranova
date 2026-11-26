// TERRA NOVA — opening cinematic web player.
// The film is drawn in real time on a 2D canvas from WebP stills (scenes.js), clocked by one AAC audio track.
// Every frame is a pure function of time, so pause/seek/skip are exact and nothing heavy is downloaded.
import { W, H, loadImage } from './engine.js';
import { SCENES } from './scenes.js';

const DURATION = 120;
const $ = (id) => document.getElementById(id);
const app = $('app'), canvas = $('film'), ctx = canvas.getContext('2d', { alpha: false });
const buf = document.createElement('canvas'), bctx = buf.getContext('2d', { alpha: false });
const audio = new Audio();
audio.preload = 'auto';
audio.src = 'audio/opening.m4a';
const acceptAudio = new Audio();
acceptAudio.preload = 'none';
acceptAudio.src = 'audio/accept.m4a';

const store = {
  get(k) { try { return localStorage.getItem(k); } catch { return null; } },
  set(k, v) { try { localStorage.setItem(k, v); } catch { /* private mode */ } },
};
const reducedPref = window.matchMedia('(prefers-reduced-motion: reduce)');
const state = {
  started: false, playing: false, ended: false, buffering: false,
  reduced: store.get('tn_motion') ? store.get('tn_motion') === 'reduced' : reducedPref.matches,
  cc: store.get('tn_cc') || 'id',           // 'id' | 'en' | 'off'
  clockStart: 0, clockOffset: 0, audioOk: true,
  quality: 1, slow: 0, fast: 0, lastFrame: 0,
};

// ---------------------------------------------------------------- assets (loaded in timeline order)
const images = new Map();          // url -> HTMLImageElement
const pending = new Map();         // url -> Promise
SCENES.forEach((s) => { s.loaded = {}; s.urls = Object.entries(s.assets || {}); });
function want(url) {
  if (images.has(url)) return Promise.resolve(images.get(url));
  if (!pending.has(url)) {
    pending.set(url, loadImage(url).then((img) => { images.set(url, img); return img; })
      .catch(() => new Promise((r) => setTimeout(r, 1500)).then(() => { pending.delete(url); return want(url); })));
  }
  return pending.get(url);
}
function sceneReady(s) {
  for (const [k, url] of s.urls) {
    const img = images.get(url);
    if (!img) return false;
    s.loaded[k] = img;
  }
  return true;
}
const allUrls = [...new Set(SCENES.flatMap((s) => s.urls.map(([, u]) => u)))];
let loadedCount = 0;
async function preload() {
  const queue = allUrls.slice();
  const worker = async () => {
    while (queue.length) {
      await want(queue.shift());
      loadedCount++;
      $('load-fill').style.width = `${Math.round((loadedCount / allUrls.length) * 100)}%`;
      updateStartButton();
    }
  };
  await Promise.all([worker(), worker(), worker()]);
}
let audioReady = false;
audio.addEventListener('canplay', () => { audioReady = true; updateStartButton(); }, { once: true });
audio.addEventListener('error', () => { state.audioOk = false; audioReady = true; updateStartButton(); });
function firstScenesReady() { return SCENES.filter((s) => s.start < 24).every(sceneReady); }
function updateStartButton() {
  const btn = $('btn-start');
  if (firstScenesReady() && audioReady) {
    btn.disabled = false;
    btn.querySelector('.btn-label').textContent = 'Mulai cinematic';
    if (AUTOSTART) tryAutostart();
  }
}
// ?autostart=1 (after sign-up on the landing page): no start button, play as soon as the first shots are ready.
// If the browser blocks audio autoplay (mostly Safari/iOS), fall back to a single play button.
const AUTOSTART = new URLSearchParams(location.search).has('autostart');
let autoTried = false;
if (AUTOSTART) app.classList.add('autostart');
async function tryAutostart() {
  if (autoTried || state.started) return;
  autoTried = true;
  try {
    await audio.play();
    audio.pause();
    start();
  } catch {
    app.classList.remove('autostart');
    $('btn-start').querySelector('.btn-label').textContent = 'Putar cinematic';
  }
}

// ---------------------------------------------------------------- clock
function now() {
  if (state.audioOk && !audio.paused && audio.readyState >= 2) return audio.currentTime;
  if (state.audioOk && audio.paused) return audio.currentTime;
  return state.playing ? state.clockOffset + (performance.now() - state.clockStart) / 1000 : state.clockOffset;
}
function seek(t) {
  t = Math.max(0, Math.min(DURATION, t));
  if (state.audioOk) audio.currentTime = t;
  state.clockOffset = t; state.clockStart = performance.now();
  if (state.ended && t < DURATION) { state.ended = false; app.classList.remove('is-ended'); $('ending').hidden = true; }
  draw(t);
}
async function play() {
  if (state.ended) return;
  state.playing = true;
  app.classList.remove('paused');
  state.clockStart = performance.now();
  if (state.audioOk) {
    try { await audio.play(); } catch { state.audioOk = false; state.clockOffset = audio.currentTime || state.clockOffset; }
  }
  loop();
}
function pause() {
  if (!state.playing) return;
  state.clockOffset = now();
  state.playing = false;
  app.classList.add('paused');
  audio.pause();
}

// ---------------------------------------------------------------- rendering
function resize() {
  const rect = canvas.getBoundingClientRect();
  const dpr = Math.min(window.devicePixelRatio || 1, 2);
  const base = Math.min(1, Math.max(0.35, (rect.width * dpr) / W));
  const s = Math.max(0.3, base * state.quality);
  const w = Math.round(W * s), h = Math.round(H * s);
  if (canvas.width !== w || canvas.height !== h) {
    canvas.width = w; canvas.height = h; buf.width = w; buf.height = h;
  }
  state.scale = s;
  if (!state.playing) draw(now());
}
function sceneIndexAt(t) {
  let i = 0;
  for (let k = 0; k < SCENES.length; k++) if (SCENES[k].start <= t) i = k;
  return i;
}
function renderScene(c, s, t) {
  c.setTransform(state.scale, 0, 0, state.scale, 0, 0);
  c.globalAlpha = 1;
  c.globalCompositeOperation = 'source-over';
  c.fillStyle = '#030808';
  c.fillRect(0, 0, W, H);
  if (!sceneReady(s)) return false;
  let local = Math.min(s.total, Math.max(0, t - s.start));
  if (state.reduced) local = Math.min(s.total * 0.55, 2.4);   // static frame per shot
  s.render(c, local, s.total, s.loaded);
  return true;
}
function draw(t) {
  const i = sceneIndexAt(t);
  const s = SCENES[i];
  let ok;
  if (i > 0 && s.fade > 0 && t < s.start + s.fade && sceneReady(SCENES[i - 1])) {
    // crossfade: previous shot underneath, current shot fades in on top
    renderScene(ctx, SCENES[i - 1], t);
    ok = renderScene(bctx, s, t);
    if (ok) {
      ctx.setTransform(1, 0, 0, 1, 0, 0);
      ctx.globalAlpha = Math.max(0, Math.min(1, (t - s.start) / s.fade));
      ctx.drawImage(buf, 0, 0);
      ctx.globalAlpha = 1;
    }
  } else {
    ok = renderScene(ctx, s, t);
  }
  setBuffering(!ok);
  updateCaptions(t);
  updateProgress(t);
  return ok;
}
let raf = 0;
function loop() {
  cancelAnimationFrame(raf);
  raf = requestAnimationFrame(function frame(ms) {
    if (!state.playing) return;
    const t = now();
    if (t >= DURATION - 0.02) { finish(false); return; }
    const t0 = performance.now();
    const ok = draw(t);
    if (!ok) {                       // a shot's image is still downloading: hold the clock
      if (!audio.paused) audio.pause();
      state.clockOffset = t; state.clockStart = performance.now();
      const s = SCENES[sceneIndexAt(t)];
      Promise.all(s.urls.map(([, u]) => want(u))).then(() => {
        if (state.playing && state.audioOk) audio.play().catch(() => {});
      });
    }
    adaptQuality(performance.now() - t0, ms);
    raf = requestAnimationFrame(frame);
  });
}
// lower the canvas resolution if the device cannot keep up, raise it again when there is headroom
function adaptQuality(cost) {
  if (cost > 22) { state.slow++; state.fast = 0; } else if (cost < 9) { state.fast++; state.slow = Math.max(0, state.slow - 1); }
  if (state.slow > 30 && state.quality > 0.5) { state.quality = Math.max(0.5, state.quality - 0.15); state.slow = 0; resize(); }
  if (state.fast > 240 && state.quality < 1) { state.quality = Math.min(1, state.quality + 0.1); state.fast = 0; resize(); }
}
function setBuffering(on) {
  if (on === state.buffering) return;
  state.buffering = on;
  $('spinner').hidden = !on;
}

// ---------------------------------------------------------------- captions
let CAPTIONS = [];
fetch('captions.json').then((r) => r.json()).then((c) => { CAPTIONS = c; }).catch(() => {});
let capKey = '';
const capEl = $('captions');
function updateCaptions(t) {
  const c = state.cc === 'off' ? null : CAPTIONS.find((x) => t >= x.start && t <= x.end);
  const key = c ? `${c.start}|${state.cc}` : '';
  if (key === capKey) return;
  capKey = key;
  capEl.textContent = '';
  if (!c) return;
  const span = document.createElement('span');
  span.className = `cap${c.speaker === 'Gaia' ? ' gaia' : ''}`;
  span.lang = state.cc;
  span.textContent = c[state.cc];
  capEl.appendChild(span);
  requestAnimationFrame(() => span.classList.add('on'));
}
function setCC(mode) {
  state.cc = mode; store.set('tn_cc', mode); capKey = '#';
  const label = { id: 'ID', en: 'EN', off: 'CC' }[mode];
  const btn = $('btn-cc');
  btn.textContent = label;
  btn.setAttribute('aria-label', `Subtitle: ${{ id: 'Indonesia', en: 'English', off: 'mati' }[mode]}`);
  btn.style.opacity = mode === 'off' ? 0.55 : 1;
  updateCaptions(now());
}

// ---------------------------------------------------------------- progress / time
const fmt = (t) => `${Math.floor(t / 60)}:${String(Math.floor(t % 60)).padStart(2, '0')}`;
function updateProgress(t) {
  $('progress-fill').style.width = `${(t / DURATION) * 100}%`;
  $('progress').setAttribute('aria-valuenow', Math.round(t));
  $('time').textContent = `${fmt(t)} / ${fmt(DURATION)}`;
}
function seekFromPointer(e) {
  const r = $('progress').getBoundingClientRect();
  seek(((e.clientX - r.left) / r.width) * DURATION);
}
$('progress').addEventListener('pointerdown', (e) => {
  seekFromPointer(e);
  const move = (ev) => seekFromPointer(ev);
  const up = () => { window.removeEventListener('pointermove', move); window.removeEventListener('pointerup', up); };
  window.addEventListener('pointermove', move); window.addEventListener('pointerup', up);
});

// ---------------------------------------------------------------- ending (H02) & game handoff
function emit(type, detail = {}) {
  window.dispatchEvent(new CustomEvent(type, { detail }));
  try { if (window.parent !== window) window.parent.postMessage({ type, ...detail }, '*'); } catch { /* cross-origin */ }
}
function finish(skipped) {
  pause();
  cancelAnimationFrame(raf);
  state.ended = true;
  app.classList.add('is-ended');
  app.classList.remove('idle');
  capEl.textContent = ''; capKey = '';
  $('ending').hidden = false;
  $('btn-accept').focus({ preventScroll: true });
  store.set('tn_intro_seen_at', new Date().toISOString());
  emit('terranova:intro-ended', { skipped, at: Math.round(now()) });
}
$('btn-accept').addEventListener('click', () => {
  const p = $('accepted');
  p.textContent = '“Terima kasih, manusia terpilih. Perjalananmu kini dimulai. Pergilah ke kotamu. Aku akan selalu menyertaimu.”';
  p.hidden = false;
  $('ending-actions').hidden = true;
  emit('terranova:intro-accepted');
  // tell the game shell when Gaia's thank-you line is over (or right away if muted / blocked)
  let doneSent = false;
  const done = () => { if (!doneSent) { doneSent = true; emit('terranova:intro-done'); } };
  if (!audio.muted) {
    acceptAudio.currentTime = 0;
    acceptAudio.onended = () => setTimeout(done, 600);
    acceptAudio.play().catch(() => setTimeout(done, 2500));
    setTimeout(done, 12000);
  } else {
    setTimeout(done, 3500);
  }
});
$('btn-replay').addEventListener('click', () => {
  acceptAudio.pause();
  $('ending').hidden = true; $('accepted').hidden = true; $('ending-actions').hidden = false;
  state.ended = false; app.classList.remove('is-ended');
  app.classList.add('is-playing');
  seek(0); play();
});
const loginUrl = new URLSearchParams(location.search).get('login') || app.dataset.loginUrl;
$('login-link').href = loginUrl;
// ?embed=1: running inside the game sign-up flow, so the player is already signed in (no login link)
if (new URLSearchParams(location.search).has('embed')) $('login-link').hidden = true;

// ---------------------------------------------------------------- UI wiring
function start() {
  if (state.started) return;
  state.started = true;
  app.classList.remove('is-intro');
  app.classList.add('is-playing');
  resize();
  seek(0);
  play();
  pokeIdle();
}
$('btn-start').addEventListener('click', start);
$('btn-skip-intro').addEventListener('click', () => { state.started = true; app.classList.remove('is-intro'); finish(true); });
$('btn-skip').addEventListener('click', () => finish(true));
$('btn-play').addEventListener('click', () => (state.playing ? pause() : play()));
$('btn-mute').addEventListener('click', () => {
  audio.muted = !audio.muted; acceptAudio.muted = audio.muted;
  app.classList.toggle('muted', audio.muted);
  $('btn-mute').setAttribute('aria-label', audio.muted ? 'Nyalakan suara' : 'Bisukan');
});
$('btn-cc').addEventListener('click', () => setCC({ id: 'en', en: 'off', off: 'id' }[state.cc]));
function setMotion(reduced) {
  state.reduced = reduced; store.set('tn_motion', reduced ? 'reduced' : 'full');
  $('btn-motion').textContent = reduced ? 'Statis' : 'Gerak';
  $('btn-motion').setAttribute('aria-label', reduced ? 'Mode statis (gerak dikurangi)' : 'Gerak penuh');
  draw(now());
}
$('btn-motion').addEventListener('click', () => setMotion(!state.reduced));
$('btn-fs').addEventListener('click', () => {
  const el = document.documentElement;
  if (document.fullscreenElement) document.exitFullscreen?.();
  else (el.requestFullscreen || el.webkitRequestFullscreen)?.call(el, { navigationUI: 'hide' })?.catch?.(() => {});
});
document.addEventListener('keydown', (e) => {
  if (e.target.closest('input, textarea')) return;
  if (!state.started && (e.key === 'Enter') && !$('btn-start').disabled) return;
  if (!state.started || state.ended) return;
  const k = e.key.toLowerCase();
  if (k === ' ' || k === 'k') { e.preventDefault(); state.playing ? pause() : play(); }
  else if (k === 'm') $('btn-mute').click();
  else if (k === 'c') $('btn-cc').click();
  else if (k === 'f') $('btn-fs').click();
  else if (k === 's' || k === 'escape') finish(true);
  else if (k === 'arrowright') seek(now() + 5);
  else if (k === 'arrowleft') seek(now() - 5);
  pokeIdle();
});
let idleTimer = 0;
function pokeIdle() {
  app.classList.remove('idle');
  clearTimeout(idleTimer);
  idleTimer = setTimeout(() => { if (state.playing) app.classList.add('idle'); }, 2600);
}
['pointermove', 'pointerdown', 'touchstart'].forEach((ev) => window.addEventListener(ev, pokeIdle, { passive: true }));
document.addEventListener('visibilitychange', () => { if (document.hidden) pause(); });
window.addEventListener('resize', resize);
window.addEventListener('pagehide', () => { pause(); cancelAnimationFrame(raf); });
audio.addEventListener('ended', () => finish(false));
audio.addEventListener('waiting', () => setBuffering(true));
audio.addEventListener('playing', () => setBuffering(false));

// small API for the game shell and QA: window.__terranova.seek(42), .play(), .pause(), .skip(), .time
window.__terranova = {
  seek, play, pause, start, skip: () => finish(true),
  get time() { return now(); }, get quality() { return state.quality; }, get scale() { return state.scale; },
};

// ---------------------------------------------------------------- boot
setCC(state.cc);
setMotion(state.reduced);
resize();
preload();
