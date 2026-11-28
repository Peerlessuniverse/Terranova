/* TERRA NOVA · gambar alat/mesin isometrik prosedural (Evaluasi 3 #6).
   307 item katalog dipetakan ke ±20 bentuk dasar lewat nama & kategori, digambar dengan canvas (tanpa aset tambahan).
   API: TN_MESIN.jenis(nama, kategori) -> {key, pal}, TN_MESIN.gambar(g, jenis, x, y, r, t), TN_MESIN.ikon(nama, kategori) -> dataURL */
(function () {
  const PAL = {
    organik: { a: '#5f9a3c', b: '#3f6e27', c: '#2c4f1b', x: '#a5d36b' },
    plastik: { a: '#3f86c6', b: '#2b6198', c: '#1f476f', x: '#9fd2ff' },
    kertas: { a: '#c49a5a', b: '#946f3b', c: '#6e5129', x: '#f1d9a6' },
    logam: { a: '#8f9aa4', b: '#66707a', c: '#4a525a', x: '#d8e0e6' },
    tekstil: { a: '#b0648f', b: '#824769', c: '#5e324c', x: '#f0b6d6' },
    khusus: { a: '#d0a12f', b: '#9b741b', c: '#6f5212', x: '#ffe08a' },
    energi: { a: '#4a9d8f', b: '#337066', c: '#24514a', x: '#a6f0e2' },
    surya: { a: '#2f5fb0', b: '#21447f', c: '#17305b', x: '#8fc2ff' },
    hidro: { a: '#3aa0c0', b: '#277189', c: '#1c5263', x: '#a8ecff' },
    wte: { a: '#a86a3a', b: '#7a4b27', c: '#58361b', x: '#ffc58a' },
    umum: { a: '#7d8c74', b: '#5a6653', c: '#414a3c', x: '#d5e4cb' },
  };
  function palDari(kat) {
    const k = String(kat || '').toLowerCase();
    if (/organik|kompos/.test(k)) return PAL.organik;
    if (/plastik/.test(k)) return PAL.plastik;
    if (/kertas/.test(k)) return PAL.kertas;
    if (/logam|kaca/.test(k)) return PAL.logam;
    if (/tekstil|kayu|karet/.test(k)) return PAL.tekstil;
    if (/jelantah|elektronik|khusus/.test(k)) return PAL.khusus;
    if (/surya/.test(k)) return PAL.surya;
    if (/hidro/.test(k)) return PAL.hidro;
    if (/waste|wte/.test(k)) return PAL.wte;
    if (/energi|angin|panas|penyimpanan|rumah tangga/.test(k)) return PAL.energi;
    return PAL.umum;
  }
  // urutan penting: pola yang lebih khusus lebih dulu
  const ATURAN = [
    ['gerobak', /gerobak dorong/],
    ['tong3', /tong sampah terpilah/],
    ['biopori', /biopori/],
    ['drum', /komposter putar|trommel|windrow/],
    ['ember', /ember|takakura/],
    ['komposter', /komposter|vermikompos|bak penampung|bak float|bak pengendap/],
    ['jeriken', /jeriken|drop box|penyimpanan baterai/],
    ['timbangan', /timbangan gantung|jembatan timbang/],
    ['jahit', /mesin jahit|obras/],
    ['meja', /meja|timbangan digital|pemotong (kertas|kain|kabel)|stasiun (cuci|inspeksi)|gergaji|bengkel/],
    ['rak', /rak|modul bsf|pemisah maggot/],
    ['surya', /surya|solar|plts|panel fleksibel/],
    ['angin', /hawt|savonius|darrieus|vawt|anemometer|turbin angin/],
    ['kincir', /hidro|kincir|pelton|turgo|crossflow|francis|kaplan|propeller|archimedes|hidrokinetik|pasang surut|gelombang/],
    ['kabinet', /baterai|inverter|controller|mppt|meter|panel (distribusi|proteksi)|ems\b|energy management|proteksi|transformer|kontrol|stasiun pengisian|monitoring|sensor|smart|audit kit|weather/],
    ['tungku', /insinerator|furnace|kiln|smelter|boiler|pengering|dryer|pirolisis|gasifier|oven|biochar|refinery|grate|fluidized|flare/],
    ['genset', /genset|generator|chp|engine|fuel cell|teg\b|teg |stirling|orc|rankine|steam turbine|turbine/],
    ['tangki', /digester|tangki|bunker|gas holder|penampung|ipal|pemurni|scrubber|baghouse|filter|condenser|cooling|water|pompa|karbon aktif|dewatering|h2s|adsorpsi|reuse/],
    ['press', /press|baler|briket|compression|molding|cetak|tray/],
    ['conveyor', /conveyor|lini|separator|sorter|screen|classifier|washer|wash|line\b|pengayak|robot|optical|deinking|nonwoven|benang|machine|lembaran/],
    ['cacah', /cacah|shredder|granulator|crusher|chipper|mill|debeader|giling|penggiling|mixer|densifier|agglomerator|opener|shear|pulper|hydrapulper|extruder|pengemas|label|centrifugal|depackager|pulping/],
    ['lab', /lab|riset|pusat|cems|survei|commissioning|kajian|mitra|audit/],
  ];
  function jenis(nama, kategori) {
    const n = String(nama || '').toLowerCase();
    const key = (ATURAN.find(([, re]) => re.test(n)) || ['mesin'])[0];
    return { key, pal: palDari(kategori) };
  }

  // ---- primitives (k = skala; koordinat dasar: tengah-bawah)
  function poly(g, pts, fill, stroke) {
    g.beginPath(); pts.forEach(([a, b], i) => (i ? g.lineTo(a, b) : g.moveTo(a, b))); g.closePath();
    g.fillStyle = fill; g.fill();
    if (stroke) { g.strokeStyle = stroke; g.lineWidth = 1; g.stroke(); }
  }
  // kotak isometrik: pusat alas (x, y), setengah lebar u (ke kanan-bawah) & v (ke kiri-bawah), tinggi h, z0 = dasar
  function kotak(g, x, y, u, v, h, top, kiri, kanan, z0 = 0) {
    const P = (a, b, z) => [x + a - b, y + (a + b) / 2 - z - z0];
    poly(g, [P(-u, v, 0), P(u, v, 0), P(u, v, h), P(-u, v, h)], kiri, 'rgba(0,0,0,.25)');
    poly(g, [P(u, v, 0), P(u, -v, 0), P(u, -v, h), P(u, v, h)], kanan, 'rgba(0,0,0,.25)');
    poly(g, [P(-u, -v, h), P(u, -v, h), P(u, v, h), P(-u, v, h)], top, 'rgba(255,255,255,.18)');
    return P;
  }
  function silinder(g, x, y, r, h, warna, gelap, tutup) {
    const ry = r * 0.5;
    const gr = g.createLinearGradient(x - r, 0, x + r, 0);
    gr.addColorStop(0, gelap); gr.addColorStop(0.45, warna); gr.addColorStop(1, gelap);
    g.fillStyle = gr;
    g.beginPath(); g.moveTo(x - r, y - h); g.lineTo(x - r, y); g.ellipse(x, y, r, ry, 0, Math.PI, 0, true); g.lineTo(x + r, y - h); g.closePath(); g.fill();
    g.fillStyle = tutup || warna; g.beginPath(); g.ellipse(x, y - h, r, ry, 0, 0, Math.PI * 2); g.fill();
    g.strokeStyle = 'rgba(0,0,0,.3)'; g.lineWidth = 1; g.stroke();
  }
  function bayang(g, x, y, r) { g.fillStyle = 'rgba(0,0,0,.28)'; g.beginPath(); g.ellipse(x, y + 2, r * 1.15, r * 0.55, 0, 0, Math.PI * 2); g.fill(); }
  function asap(g, x, y, k, t) {
    for (let i = 0; i < 3; i++) {
      const f = ((t / 60 + i / 3) % 1);
      g.fillStyle = `rgba(225,225,225,${0.45 * (1 - f)})`;
      g.beginPath(); g.arc(x + Math.sin(f * 4 + i) * 4 * k, y - f * 34 * k, (3 + f * 7) * k, 0, Math.PI * 2); g.fill();
    }
  }

  const GAMBAR = {
    tong3(g, x, y, k, P) {
      [['#2f8f46', '#1d5f2e', -15], ['#d9b425', '#9a7f12', 0], ['#c8452f', '#86291b', 15]].forEach(([c, d, dx]) => {
        silinder(g, x + dx * k, y - Math.abs(dx) * 0.15 * k, 7 * k, 17 * k, c, d, c);
        g.fillStyle = '#fff'; g.font = `${7 * k}px system-ui`; g.textAlign = 'center'; g.fillText('♻', x + dx * k, y - 9 * k);
      });
    },
    komposter(g, x, y, k, P) {
      silinder(g, x, y, 13 * k, 26 * k, P.a, P.c, P.b);
      g.fillStyle = 'rgba(0,0,0,.35)';
      for (let i = 0; i < 3; i++) for (let j = 0; j < 2; j++) { g.beginPath(); g.arc(x - 6 * k + i * 6 * k, y - 8 * k - j * 7 * k, 1.3 * k, 0, 7); g.fill(); }
      g.fillStyle = P.c; g.fillRect(x - 3 * k, y - 31 * k, 6 * k, 3 * k);
      g.fillStyle = '#fff'; g.font = `bold ${9 * k}px system-ui`; g.textAlign = 'center'; g.fillText('♻', x, y - 15 * k);
    },
    ember(g, x, y, k, P) {
      silinder(g, x, y, 11 * k, 11 * k, P.b, P.c, P.a);
      silinder(g, x, y - 11 * k, 10 * k, 10 * k, P.a, P.b, P.a);
      silinder(g, x, y - 21 * k, 9 * k, 6 * k, P.x, P.b, P.a);
    },
    drum(g, x, y, k, P, t) {
      kotak(g, x - 12 * k, y, 2 * k, 2 * k, 16 * k, '#555', '#444', '#333'); kotak(g, x + 12 * k, y, 2 * k, 2 * k, 16 * k, '#555', '#444', '#333');
      g.save(); g.translate(x, y - 20 * k); g.scale(1, 0.62);
      const gr = g.createLinearGradient(0, -14 * k, 0, 14 * k); gr.addColorStop(0, P.x); gr.addColorStop(0.5, P.a); gr.addColorStop(1, P.c);
      g.fillStyle = gr; g.beginPath(); g.roundRect(-18 * k, -14 * k, 36 * k, 28 * k, 12 * k); g.fill();
      g.strokeStyle = 'rgba(0,0,0,.35)'; g.lineWidth = 2;
      const off = (t / 6) % 8;
      for (let i = -16; i < 18; i += 8) { g.beginPath(); g.moveTo((i + off) * k, -14 * k); g.lineTo((i + off) * k, 14 * k); g.stroke(); }
      g.restore();
    },
    biopori(g, x, y, k) {
      g.fillStyle = '#5a3b22'; g.beginPath(); g.ellipse(x, y - 2 * k, 12 * k, 6 * k, 0, 0, 7); g.fill();
      g.fillStyle = '#9aa0a6'; g.beginPath(); g.ellipse(x, y - 3 * k, 8 * k, 4 * k, 0, 0, 7); g.fill();
      g.fillStyle = '#1d140c'; g.beginPath(); g.ellipse(x, y - 3 * k, 5 * k, 2.5 * k, 0, 0, 7); g.fill();
    },
    jeriken(g, x, y, k, P) {
      kotak(g, x, y, 9 * k, 6 * k, 20 * k, P.x, P.a, P.b);
      kotak(g, x + 3 * k, y - 2 * k, 2 * k, 2 * k, 4 * k, '#333', '#222', '#111', 20 * k);
      g.fillStyle = '#222'; g.font = `bold ${8 * k}px system-ui`; g.textAlign = 'center'; g.fillText('⚠', x - 2 * k, y - 6 * k);
    },
    timbangan(g, x, y, k, P) {
      kotak(g, x, y, 16 * k, 12 * k, 3 * k, '#9aa3ab', '#6b737a', '#555c62');
      kotak(g, x - 12 * k, y - 4 * k, 2 * k, 2 * k, 26 * k, '#666', '#555', '#444');
      g.fillStyle = '#e8eef2'; g.beginPath(); g.arc(x - 12 * k, y - 34 * k, 6 * k, 0, 7); g.fill();
      g.strokeStyle = '#c33'; g.lineWidth = 1.5; g.beginPath(); g.moveTo(x - 12 * k, y - 34 * k); g.lineTo(x - 9 * k, y - 37 * k); g.stroke();
    },
    meja(g, x, y, k, P) {
      [[-14, -6], [14, -6], [-14, 6], [14, 6]].forEach(([a, b]) => kotak(g, x + (a - b) * k, y + (a + b) / 2 * k, 1.2 * k, 1.2 * k, 14 * k, '#5a4026', '#4a321c', '#3a2614'));
      kotak(g, x, y, 17 * k, 8 * k, 3 * k, '#b98a55', '#8c6235', '#6e4c27', 14 * k);
      kotak(g, x - 6 * k, y - 2 * k, 4 * k, 4 * k, 5 * k, P.x, P.a, P.b, 17 * k);
      kotak(g, x + 7 * k, y + 1 * k, 4 * k, 4 * k, 4 * k, '#e7c96a', '#c09a36', '#9a7a24', 17 * k);
    },
    jahit(g, x, y, k, P) {
      GAMBAR.meja(g, x, y, k, P);
      kotak(g, x, y - 1 * k, 6 * k, 3 * k, 8 * k, '#f2f2f2', '#c9c9c9', '#a8a8a8', 17 * k);
    },
    rak(g, x, y, k, P) {
      kotak(g, x, y, 16 * k, 6 * k, 34 * k, 'rgba(0,0,0,0)', 'rgba(60,60,60,.35)', 'rgba(40,40,40,.4)');
      for (let z = 0; z <= 30; z += 11) kotak(g, x, y, 16 * k, 6 * k, 1.5 * k, '#9aa3ab', '#6b737a', '#555c62', z * k);
      [[-9, 2, P.a], [3, 2, '#c49a5a'], [-4, 13, '#c49a5a'], [8, 13, P.x], [-8, 24, P.b]].forEach(([dx, z, c]) => kotak(g, x + dx * k, y + dx * 0.2 * k, 4 * k, 4 * k, 7 * k, c, c, 'rgba(0,0,0,.25)', (z + 1.5) * k));
    },
    surya(g, x, y, k, P) {
      kotak(g, x - 14 * k, y - 1 * k, 1.5 * k, 1.5 * k, 9 * k, '#777', '#555', '#444'); kotak(g, x + 14 * k, y - 1 * k, 1.5 * k, 1.5 * k, 33 * k, '#777', '#555', '#444');
      const A = [x - 22 * k, y - 4 * k], B = [x + 6 * k, y - 18 * k], C = [x + 22 * k, y - 22 * k], D = [x - 6 * k, y - 8 * k];
      const L = (p, q, f) => [p[0] + (q[0] - p[0]) * f, p[1] + (q[1] - p[1]) * f];
      const pa = [A[0], A[1] - 4 * k], pd = [D[0], D[1] - 4 * k], pc = [C[0], C[1] - 14 * k], pb = [B[0], B[1] - 14 * k];
      poly(g, [pa, pd, pc, pb], P.a, '#d9e8ff');
      g.strokeStyle = 'rgba(200,230,255,.6)'; g.lineWidth = 1;
      for (let i = 1; i < 4; i++) { const p = L(pa, pb, i / 4), q = L(pd, pc, i / 4); g.beginPath(); g.moveTo(p[0], p[1]); g.lineTo(q[0], q[1]); g.stroke(); }
      for (let i = 1; i < 2; i++) { const p = L(pa, pd, i / 2), q = L(pb, pc, i / 2); g.beginPath(); g.moveTo(p[0], p[1]); g.lineTo(q[0], q[1]); g.stroke(); }
      g.fillStyle = 'rgba(255,255,255,.22)'; poly(g, [pa, L(pa, pd, .35), L(pb, pc, .35), pb], 'rgba(255,255,255,.18)');
    },
    angin(g, x, y, k, P, t, nama) {
      const vawt = /savonius|darrieus|vawt/.test(nama), ane = /anemometer/.test(nama);
      kotak(g, x, y, 5 * k, 5 * k, 3 * k, '#888', '#666', '#555');
      g.fillStyle = '#d7dde2'; g.fillRect(x - 1.5 * k, y - 46 * k, 3 * k, 44 * k);
      const hy = y - 48 * k, a = t / 9;
      if (ane) { for (let i = 0; i < 3; i++) { const ang = a + i * 2.09; g.fillStyle = '#e4e4e4'; g.beginPath(); g.arc(x + Math.cos(ang) * 8 * k, hy + Math.sin(ang) * 3 * k, 3 * k, 0, 7); g.fill(); } return; }
      if (vawt) {
        const w = Math.cos(a) * 9 * k;
        g.fillStyle = P.x; g.beginPath(); g.ellipse(x - w / 2, hy, Math.abs(w) / 2 + 2 * k, 13 * k, 0, 0, 7); g.fill();
        g.fillStyle = P.a; g.beginPath(); g.ellipse(x + w / 2, hy, Math.abs(w) / 2 + 2 * k, 13 * k, 0, 0, 7); g.fill();
        return;
      }
      kotak(g, x, hy + 2 * k, 5 * k, 2 * k, 4 * k, '#eee', '#ccc', '#aaa');
      g.save(); g.translate(x - 4 * k, hy); g.fillStyle = '#f4f6f8'; g.strokeStyle = 'rgba(0,0,0,.25)';
      for (let i = 0; i < 3; i++) { g.save(); g.rotate(a + i * 2.094); g.beginPath(); g.ellipse(0, -13 * k, 2.4 * k, 13 * k, 0, 0, 7); g.fill(); g.stroke(); g.restore(); }
      g.fillStyle = '#bbb'; g.beginPath(); g.arc(0, 0, 2.5 * k, 0, 7); g.fill(); g.restore();
    },
    kincir(g, x, y, k, P, t) {
      g.fillStyle = '#2b6f8a'; g.beginPath(); g.ellipse(x, y - 1 * k, 20 * k, 7 * k, 0, 0, 7); g.fill();
      g.fillStyle = 'rgba(190,240,255,.6)'; for (let i = 0; i < 3; i++) g.fillRect(x - 14 * k + ((t / 2 + i * 10) % 28) * k, y - 2 * k + i * 2 * k, 5 * k, 1);
      kotak(g, x - 10 * k, y, 2 * k, 2 * k, 18 * k, '#7a5634', '#5d4026', '#47301c'); kotak(g, x + 10 * k, y, 2 * k, 2 * k, 18 * k, '#7a5634', '#5d4026', '#47301c');
      g.save(); g.translate(x, y - 18 * k); g.scale(0.55, 1); g.rotate(t / 25);
      g.strokeStyle = '#6e4c2a'; g.lineWidth = 3 * k; g.beginPath(); g.arc(0, 0, 16 * k, 0, 7); g.stroke();
      g.lineWidth = 2 * k; for (let i = 0; i < 8; i++) { g.save(); g.rotate(i * Math.PI / 4); g.beginPath(); g.moveTo(0, 0); g.lineTo(0, -16 * k); g.stroke(); g.fillStyle = P.a; g.fillRect(-3 * k, -19 * k, 6 * k, 5 * k); g.restore(); }
      g.restore();
    },
    kabinet(g, x, y, k, P, t) {
      kotak(g, x, y, 9 * k, 6 * k, 26 * k, P.b, P.a, P.c);
      g.fillStyle = '#0d2a1f'; poly(g, [[x - 13 * k, y - 18 * k], [x - 3 * k, y - 13 * k], [x - 3 * k, y - 19 * k], [x - 13 * k, y - 24 * k]], '#0d2a1f');
      const on = Math.floor(t / 30) % 2;
      g.fillStyle = on ? '#7bff8f' : '#2f7a3d'; g.beginPath(); g.arc(x - 10 * k, y - 10 * k, 1.6 * k, 0, 7); g.fill();
      g.fillStyle = '#ffd34d'; g.beginPath(); g.arc(x - 6 * k, y - 8 * k, 1.6 * k, 0, 7); g.fill();
      g.fillStyle = '#ffe14d'; g.font = `bold ${9 * k}px system-ui`; g.textAlign = 'center'; g.fillText('⚡', x + 5 * k, y - 10 * k);
    },
    tungku(g, x, y, k, P, t) {
      kotak(g, x, y, 13 * k, 10 * k, 20 * k, '#8c5a3c', '#a5603a', '#7a4325');
      g.fillStyle = '#ff9d2e'; g.beginPath(); g.roundRect(x - 13 * k, y - 10 * k, 7 * k, 7 * k, 2 * k); g.fill();
      g.fillStyle = `rgba(255,220,120,${0.5 + 0.3 * Math.sin(t / 5)})`; g.fillRect(x - 12 * k, y - 8 * k, 5 * k, 4 * k);
      kotak(g, x + 5 * k, y - 6 * k, 3 * k, 3 * k, 22 * k, '#777', '#666', '#555', 20 * k);
      asap(g, x + 5 * k, y - 50 * k, k, t);
    },
    genset(g, x, y, k, P, t) {
      kotak(g, x, y, 15 * k, 8 * k, 16 * k, P.a, P.b, P.c);
      g.strokeStyle = 'rgba(0,0,0,.35)'; g.lineWidth = 1;
      for (let i = 0; i < 4; i++) { g.beginPath(); g.moveTo(x + 3 * k + i * 3 * k, y + 5 * k - i * 1.5 * k); g.lineTo(x + 3 * k + i * 3 * k, y - 7 * k - i * 1.5 * k); g.stroke(); }
      kotak(g, x - 9 * k, y - 4 * k, 1.5 * k, 1.5 * k, 10 * k, '#555', '#444', '#333', 16 * k);
      asap(g, x - 9 * k, y - 32 * k, k * 0.8, t);
      g.fillStyle = '#ffe14d'; g.font = `bold ${9 * k}px system-ui`; g.textAlign = 'center'; g.fillText('⚡', x - 7 * k, y - 4 * k);
    },
    tangki(g, x, y, k, P) {
      silinder(g, x, y, 16 * k, 20 * k, P.a, P.c, P.b);
      g.fillStyle = P.x; g.beginPath(); g.ellipse(x, y - 20 * k, 16 * k, 8 * k, 0, Math.PI, 0); g.lineTo(x + 16 * k, y - 20 * k);
      g.ellipse(x, y - 20 * k, 16 * k, 13 * k, 0, 0, Math.PI, true); g.fill();
      g.fillStyle = P.x; g.beginPath(); g.ellipse(x, y - 20 * k, 16 * k, 12 * k, 0, Math.PI, 0); g.fill();
      g.strokeStyle = 'rgba(0,0,0,.25)'; g.stroke();
      g.strokeStyle = '#777'; g.lineWidth = 2 * k; g.beginPath(); g.moveTo(x + 15 * k, y - 8 * k); g.lineTo(x + 22 * k, y - 4 * k); g.lineTo(x + 22 * k, y + 2 * k); g.stroke();
    },
    press(g, x, y, k, P) {
      kotak(g, x, y, 13 * k, 9 * k, 4 * k, '#666', '#555', '#444');
      kotak(g, x, y, 8 * k, 6 * k, 9 * k, '#c49a5a', '#9a7340', '#7a5a30', 4 * k);
      [[-12, 0], [12, 0]].forEach(([a]) => kotak(g, x + a * k, y + a * 0.25 * k, 1.8 * k, 1.8 * k, 34 * k, P.a, P.b, P.c));
      kotak(g, x, y, 13 * k, 4 * k, 4 * k, P.x, P.a, P.b, 30 * k);
      g.fillStyle = '#d0d6da'; g.fillRect(x - 1.5 * k, y - 30 * k, 3 * k, 14 * k);
    },
    conveyor(g, x, y, k, P, t) {
      [[-20], [0], [20]].forEach(([a]) => kotak(g, x + a * k, y + a * 0.5 * k, 1.5 * k, 1.5 * k, 10 * k, '#555', '#444', '#333'));
      const P2 = kotak(g, x, y, 26 * k, 6 * k, 3 * k, '#2e2e2e', P.b, P.c, 10 * k);
      g.fillStyle = '#5a5a5a';
      for (let i = 0; i < 6; i++) { const f = ((t / 3 + i * 9) % 52) - 26; const [a, b] = P2(f * k, 0, 3 * k); g.fillRect(a - 1, b - 1, 2.5 * k, 1.5); }
      [[-12, '#c8452f'], [2, '#d9b425'], [16, P.x]].forEach(([u, c]) => { const f = ((t / 3 + u + 26) % 52) - 26; const [a, b] = P2(f * k, 0, 3 * k); kotak(g, a, b + 13 * k, 2.6 * k, 2.6 * k, 3 * k, c, c, 'rgba(0,0,0,.3)', 13 * k); });
      kotak(g, x - 22 * k, y - 11 * k, 6 * k, 8 * k, 12 * k, P.a, P.b, P.c, 13 * k);
    },
    cacah(g, x, y, k, P, t) {
      kotak(g, x, y, 12 * k, 10 * k, 18 * k, P.a, P.b, P.c);
      const P2 = (a, b, z) => [x + a - b, y + (a + b) / 2 - z];
      const z0 = 18 * k, z1 = 30 * k;
      poly(g, [P2(-5 * k, 5 * k, z0), P2(5 * k, 5 * k, z0), P2(10 * k, 10 * k, z1), P2(-10 * k, 10 * k, z1)], '#9aa3ab', 'rgba(0,0,0,.3)');
      poly(g, [P2(5 * k, 5 * k, z0), P2(5 * k, -5 * k, z0), P2(10 * k, -10 * k, z1), P2(10 * k, 10 * k, z1)], '#7a838b', 'rgba(0,0,0,.3)');
      poly(g, [P2(-10 * k, -10 * k, z1), P2(10 * k, -10 * k, z1), P2(10 * k, 10 * k, z1), P2(-10 * k, 10 * k, z1)], '#2a2a2a');
      g.save(); g.translate(x - 9 * k, y - 6 * k); g.rotate(t / 8); g.strokeStyle = '#ddd'; g.lineWidth = 1.5;
      for (let i = 0; i < 4; i++) { g.rotate(Math.PI / 2); g.beginPath(); g.moveTo(0, 0); g.lineTo(0, 4 * k); g.stroke(); } g.restore();
    },
    lab(g, x, y, k, P, t) {
      kotak(g, x, y, 14 * k, 10 * k, 18 * k, '#e8eef0', '#c8d2d6', '#a9b5ba');
      kotak(g, x, y, 15 * k, 11 * k, 3 * k, P.a, P.b, P.c, 18 * k);
      g.fillStyle = '#5ab7e0'; poly(g, [[x - 12 * k, y - 6 * k], [x - 4 * k, y - 2 * k], [x - 4 * k, y - 10 * k], [x - 12 * k, y - 14 * k]], '#5ab7e0');
      g.strokeStyle = '#888'; g.lineWidth = 1.5; g.beginPath(); g.moveTo(x + 6 * k, y - 26 * k); g.lineTo(x + 6 * k, y - 38 * k); g.stroke();
      g.fillStyle = Math.floor(t / 25) % 2 ? '#ff5a4a' : '#7a2a22'; g.beginPath(); g.arc(x + 6 * k, y - 39 * k, 2 * k, 0, 7); g.fill();
    },
    gerobak(g, x, y, k, P) {
      kotak(g, x, y - 6 * k, 14 * k, 8 * k, 10 * k, '#3d7a3a', '#2f6a2c', '#245622', 4 * k);
      g.fillStyle = '#222'; g.beginPath(); g.ellipse(x - 8 * k, y + 1 * k, 4 * k, 5 * k, 0, 0, 7); g.fill();
    },
    mesin(g, x, y, k, P, t) {
      kotak(g, x, y, 13 * k, 10 * k, 20 * k, P.a, P.b, P.c);
      g.save(); g.translate(x - 8 * k, y - 8 * k); g.rotate(t / 30); g.fillStyle = '#e4e4e4'; g.font = `${12 * k}px system-ui`; g.textAlign = 'center'; g.textBaseline = 'middle'; g.fillText('⚙', 0, 0); g.restore();
    },
  };

  function gambar(g, J, x, y, r, t, nama) {
    const k = r / 16;   // r = footprint radius from the catalogue area; a 1 m2 bin is about half the player height
    g.save();
    if (J.key !== 'biopori') bayang(g, x, y, r * (J.key === 'angin' ? 0.6 : 1));
    (GAMBAR[J.key] || GAMBAR.mesin)(g, x, y, k, J.pal, t || 0, String(nama || '').toLowerCase());
    g.restore();
  }

  const ikonCache = {};
  function ikon(nama, kategori) {
    const J = jenis(nama, kategori), id = J.key + '|' + J.pal.a + '|' + (J.key === 'angin' ? nama : '');
    if (ikonCache[id]) return ikonCache[id];
    const c = document.createElement('canvas'); c.width = 96; c.height = 96;
    const g = c.getContext('2d');
    const r = { angin: 14, kincir: 18, surya: 19, conveyor: 15, rak: 16, tong3: 20, meja: 17 }[J.key] || 19;
    gambar(g, J, 48, 82, r, 12, nama);
    return (ikonCache[id] = c.toDataURL('image/png'));
  }

  window.TN_MESIN = { jenis, gambar, ikon };
})();
