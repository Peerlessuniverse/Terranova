/* TERRA NOVA · warna karakter (Evaluasi 4: Setting Karakter sebelum prolog).
   Sprite pemain dibuat sekali (fal.ai) dengan jaket hijau & rambut coklat; warna lain diterapkan per piksel di canvas:
   jaket = piksel hijau, rambut = piksel coklat gelap di bagian atas sprite (bukan kulit atau sepatu).
   API: TN_AVATAR.warnai(img, {baju, rambut}, gender) -> canvas · TN_AVATAR.BAJU / RAMBUT (pilihan + swatch) */
(function () {
  const BAJU = { hijau: { h: null, sw: '#3f8f3a' }, biru: { h: 212, sw: '#2f6fc0' }, merah: { h: 356, sw: '#c23b32' },
    kuning: { h: 46, sw: '#d6a92a' }, ungu: { h: 276, sw: '#7d4cc0' }, coklat: { h: 28, s: 0.45, sw: '#8a5a32' } };
  const RAMBUT = { coklat: { sw: '#6b4024' }, hitam: { sw: '#231c18' }, pirang: { sw: '#d9b25a' }, merah: { sw: '#a8382a' } };

  function rgb2hsl(r, g, b) {
    r /= 255; g /= 255; b /= 255;
    const mx = Math.max(r, g, b), mn = Math.min(r, g, b), l = (mx + mn) / 2;
    if (mx === mn) return [0, 0, l];
    const d = mx - mn, s = l > 0.5 ? d / (2 - mx - mn) : d / (mx + mn);
    let h = mx === r ? (g - b) / d + (g < b ? 6 : 0) : mx === g ? (b - r) / d + 2 : (r - g) / d + 4;
    return [h * 60, s, l];
  }
  function hsl2rgb(h, s, l) {
    h = ((h % 360) + 360) % 360 / 360;
    if (s === 0) return [l * 255, l * 255, l * 255];
    const q = l < 0.5 ? l * (1 + s) : l + s - l * s, p = 2 * l - q;
    const f = t => { t = (t + 1) % 1; return t < 1 / 6 ? p + (q - p) * 6 * t : t < 1 / 2 ? q : t < 2 / 3 ? p + (q - p) * (2 / 3 - t) * 6 : p; };
    return [f(h + 1 / 3) * 255, f(h) * 255, f(h - 1 / 3) * 255];
  }

  const cache = new Map();
  function warnai(img, av, gender) {
    const baju = (av && av.baju) || 'hijau', rambut = (av && av.rambut) || 'coklat';
    if (!img || !(img.naturalWidth || img.width)) return img;
    if (baju === 'hijau' && rambut === 'coklat') return img;
    const key = img.src + '|' + baju + '|' + rambut;
    if (cache.has(key)) return cache.get(key);
    const w = img.naturalWidth || img.width, h = img.naturalHeight || img.height;
    const c = document.createElement('canvas'); c.width = w; c.height = h;
    const g = c.getContext('2d'); g.drawImage(img, 0, 0);
    let data;
    try { data = g.getImageData(0, 0, w, h); } catch { return img; }
    const px = data.data, B = BAJU[baju], batasRambut = h * (gender === 'wanita' ? 0.5 : 0.36);
    for (let i = 0; i < px.length; i += 4) {
      if (px[i + 3] < 20) continue;
      const y = Math.floor(i / 4 / w);
      let [H, S, L] = rgb2hsl(px[i], px[i + 1], px[i + 2]);
      let ubah = false;
      if (B.h !== null && H > 70 && H < 170 && S > 0.18 && L > 0.08 && L < 0.8) {     // jaket hijau
        H = B.h; if (B.s !== undefined) S = Math.min(S, B.s); ubah = true;
      } else if (rambut !== 'coklat' && y < batasRambut && H >= 5 && H <= 45 && S > 0.12 && L < 0.42) {   // rambut coklat
        if (rambut === 'hitam') { S *= 0.35; L *= 0.55; }
        else if (rambut === 'pirang') { H = 44; S = Math.min(1, S + 0.15); L = Math.min(0.82, L * 1.75 + 0.12); }
        else if (rambut === 'merah') { H = 8; S = Math.min(1, S + 0.25); L = Math.min(0.6, L * 1.15); }
        ubah = true;
      }
      if (ubah) { const [r, gg, b] = hsl2rgb(H, S, L); px[i] = r; px[i + 1] = gg; px[i + 2] = b; }
    }
    g.putImageData(data, 0, 0);
    cache.set(key, c);
    return c;
  }
  window.TN_AVATAR = { warnai, BAJU, RAMBUT };
})();
