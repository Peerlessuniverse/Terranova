/* TERRA NOVA — Feature Freeze v1.0 Modular UI Extensions (Catalog, 15 Crops, Vitality, Energy, Radio, Celebrations, Sandbox, Leaderboard, Card Export, Admin, Feedback) */
(function () {
  const esc = s => String(s == null ? '' : s).replace(/[&<>"']/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]));
  const fmtGC = n => Number(n || 0).toLocaleString('id-ID') + ' GC';
  const fmtKg = g => (Number(g || 0) / 1000).toLocaleString('id-ID', { maximumFractionDigits: 2 }) + ' kg';

  // ---- Gaia Radio: ONE <audio> element for the whole game (owner's songs in /assets/musik, list in daftar.json).
  // Sources: 'latar' = instrumental background, 'radio' = songs with vocals, 'tema' = the Terra Nova theme.
  // Mode 'auto' follows the scene (Lahan → instrumental, Pasar → radio songs) with a soft crossfade; 'latar' / 'radio'
  // keep one source everywhere. Ducks to 35% during celebrations, pauses while the tab is hidden, and if the browser
  // blocks autoplay it starts on the player's first tap (autoplay fallback).
  const ls = (k, d) => { try { return localStorage.getItem(k) ?? d; } catch (e) { return d; } };
  const lsSet = (k, v) => { try { localStorage.setItem(k, v); } catch (e) { } };
  const MUSIK = { tema: [], latar: [], radio: [] };
  const SUMBER_LABEL = { latar: '🎻 Musik Latar', radio: '📻 Lagu Radio', tema: '⭐ Lagu Tema' };
  const fmtDur = d => `${Math.floor(d / 60)}:${String(Math.round(d % 60)).padStart(2, '0')}`;
  const radio = {
    mode: ['auto', 'latar', 'radio'].includes(ls('tn_musik_mode', 'auto')) ? ls('tn_musik_mode', 'auto') : 'auto',
    acak: ls('tn_musik_acak', '1') === '1',
    vol: Math.min(1, Math.max(0, Number(ls('tn_musik_vol', '0.6')) || 0.6)),
    ingin: ls('tn_musik_on', '1') === '1',   // the player's preference; actual playback waits for a user gesture
    playing: false,
    sumber: null, idx: -1, cur: null,
    el: null, fade: 0, fadeTo: 1, nanti: null, siap: null, terblokir: false,
    muat() {
      return this.siap || (this.siap = fetch('/assets/musik/daftar.json').then(r => r.json()).then(d => { Object.assign(MUSIK, d); }).catch(() => { }));
    },
    sumberUntuk(scene) {
      if (this.mode !== 'auto') return this.mode;
      return scene === 'pasar' ? 'radio' : 'latar';
    },
    pilihIdx(src, kecuali) {
      const n = MUSIK[src].length;
      if (n <= 1) return 0;
      if (!this.acak) return ((kecuali ?? -1) + 1) % n;
      let i; do { i = Math.floor(Math.random() * n); } while (i === kecuali);
      return i;
    },
    audio() {
      if (this.el) return this.el;
      const a = this.el = new Audio();
      a.preload = 'auto';
      a.addEventListener('ended', () => this.berikut());
      a.addEventListener('error', () => { if (this.playing) setTimeout(() => this.berikut(), 1500); });
      setInterval(() => this.tick(), 80);
      document.addEventListener('visibilitychange', () => {
        if (!this.playing) return;
        if (document.hidden) a.pause(); else a.play().catch(() => { });
      });
      return a;
    },
    tick() {   // smooth fades + celebration ducking
      const a = this.el;
      if (!a) return;
      this.fade += Math.sign(this.fadeTo - this.fade) * Math.min(Math.abs(this.fadeTo - this.fade), 0.08);
      if (this.fade <= 0 && this.nanti) { const f = this.nanti; this.nanti = null; f(); }
      const target = this.vol * this.fade * (window.TN_DUCK ? 0.35 : 1);
      a.volume = Math.max(0, Math.min(1, a.volume + (target - a.volume) * 0.35));
    },
    async putar(src, idx, crossfade = true) {
      await this.muat();
      if (!MUSIK[src] || !MUSIK[src].length) return;
      const a = this.audio();
      const mulai = () => {
        this.sumber = src; this.idx = idx; this.cur = MUSIK[src][idx];
        a.src = this.cur.src;
        this.fade = 0; this.fadeTo = 1;
        if (!this.playing) return;
        a.play().then(() => { this.terblokir = false; }).catch(() => { this.terblokir = true; });
        this.umumkan();
      };
      if (crossfade && this.playing && !a.paused && this.fade > 0) { this.fadeTo = 0; this.nanti = mulai; } else mulai();
    },
    berikut() { const src = this.sumber || this.sumberUntuk(window.TN_SCENE); this.putar(src, this.pilihIdx(src, this.idx), false); },
    sebelum() { const src = this.sumber || 'latar', n = MUSIK[src].length; if (n) this.putar(src, (this.idx - 1 + n) % n); },
    gantiScene(scene) {   // called by the game when the scene changes
      if (!this.playing) return;
      const src = this.sumberUntuk(scene);
      if (src !== this.sumber) this.putar(src, this.pilihIdx(src));
    },
    async mulai(scene) {
      this.playing = true;
      await this.muat();
      const a = this.audio();
      const src = this.sumberUntuk(scene || window.TN_SCENE);
      if (this.cur && this.sumber === src) { this.fadeTo = 1; a.play().then(() => { this.terblokir = false; }).catch(() => { this.terblokir = true; }); this.umumkan(); }
      else this.putar(src, this.pilihIdx(src), false);
    },
    henti() { this.playing = false; if (this.el) { this.el.pause(); } },
    toggle(scene) {
      if (this.playing) this.henti(); else this.mulai(scene);
      this.ingin = this.playing; lsSet('tn_musik_on', this.playing ? '1' : '0');
      return this.playing;
    },
    setMode(m) {
      this.mode = m; lsSet('tn_musik_mode', m);
      if (this.playing) this.gantiScene(window.TN_SCENE);
    },
    setAcak(v) { this.acak = v; lsSet('tn_musik_acak', v ? '1' : '0'); },
    setVol(v) { this.vol = v; lsSet('tn_musik_vol', String(v)); },
    pilihLagu(src, id) {   // manual pick: lock to that source so the next song continues from the same list
      const i = MUSIK[src].findIndex(t => t.id === id);
      if (i < 0) return;
      if (src !== 'tema') this.setMode(src);
      this.playing = true; this.ingin = true; lsSet('tn_musik_on', '1');
      this.putar(src, i);
    },
    umumkan() {
      if (!this.cur) return;
      window.dispatchEvent(new CustomEvent('tn-musik', { detail: { judul: this.cur.judul, sumber: this.sumber } }));
      if ('mediaSession' in navigator && window.MediaMetadata) {
        navigator.mediaSession.metadata = new MediaMetadata({ title: this.cur.judul, artist: this.cur.artis || 'Ukolabs', album: 'Terra Nova · ' + SUMBER_LABEL[this.sumber] });
        try { navigator.mediaSession.setActionHandler('nexttrack', () => this.berikut()); navigator.mediaSession.setActionHandler('previoustrack', () => this.sebelum()); } catch (e) { }
      }
    },
    getTrack() { return this.cur ? { title: this.cur.judul } : { title: '—' }; },
  };
  // autoplay fallback: browsers only allow sound after a user gesture, so honour the saved preference on the first tap
  const pertamaKali = () => {
    window.removeEventListener('pointerdown', pertamaKali, true); window.removeEventListener('keydown', pertamaKali, true);
    if (radio.ingin && !radio.playing) { radio.mulai(window.TN_SCENE); window.dispatchEvent(new CustomEvent('tn-musik-status')); }
    else if (radio.playing && radio.terblokir && radio.el) radio.el.play().catch(() => { });
  };
  window.addEventListener('pointerdown', pertamaKali, true);
  window.addEventListener('keydown', pertamaKali, true);
  radio.muat();

  // ---- Async data caches (on-demand, never preloaded at boot!)
  const catState = { kind: 'machine', cat: '', q: '', page: 1, active: false, data: null, loading: false };
  const lbState = { board: 'sustainability', data: null };
  const adminState = { data: null };
  const fbState = { data: null };

  let catReq = 0;
  async function loadCatalog() {
    const my = ++catReq;   // a newer request (e.g. switching kiosks quickly) wins; stale responses are ignored
    catState.loading = true;
    const qs = new URLSearchParams({
      kind: catState.kind, cat: catState.cat, q: catState.q,
      page: String(catState.page), per_page: '24', active: catState.active ? '1' : '0'
    });
    const r = await fetch('/catalog?' + qs.toString(), { credentials: 'same-origin' });
    const data = await r.json();
    if (my !== catReq) return;
    catState.data = data;
    catState.loading = false;
    window.renderSheet && window.renderSheet();
  }

  async function loadLeaderboard(board) {
    if (board) lbState.board = board;
    const r = await fetch('/leaderboard?board=' + encodeURIComponent(lbState.board), { credentials: 'same-origin' });
    lbState.data = await r.json();
    window.renderSheet && window.renderSheet();
  }

  async function loadAdmin() {
    const r = await fetch('/admin/config', { credentials: 'same-origin' });
    adminState.data = await r.json();
    window.renderSheet && window.renderSheet();
  }

  async function loadFeedback() {
    const r = await fetch('/feedback', { credentials: 'same-origin' });
    fbState.data = await r.json();
    window.renderSheet && window.renderSheet();
  }

  // ---- On-demand PNG Achievement Card Export (3 sizes, Prototype Label, zero PII)
  function exportCardPNG(state, sizeKey) {
    const sizes = { square: [1080, 1080], story: [1080, 1920], landscape: [1200, 628] };
    const [W, H] = sizes[sizeKey] || sizes.square;
    const c = document.createElement('canvas');
    c.width = W; c.height = H;
    const ctx = c.getContext('2d');
    const gr = ctx.createLinearGradient(0, 0, W, H);
    gr.addColorStop(0, '#0b241a'); gr.addColorStop(0.5, '#164532'); gr.addColorStop(1, '#091b14');
    ctx.fillStyle = gr; ctx.fillRect(0, 0, W, H);
    ctx.strokeStyle = '#e8c56e'; ctx.lineWidth = 10;
    ctx.strokeRect(36, 36, W - 72, H - 72);
    ctx.fillStyle = '#e8c56e'; ctx.font = 'bold 42px Georgia, serif'; ctx.textAlign = 'center';
    ctx.fillText('TERRA NOVA · PERADABAN BUMI BARU', W / 2, 120);
    ctx.fillStyle = '#9be37f'; ctx.font = 'bold 26px system-ui';
    ctx.fillText('PROTOTYPE ACHIEVEMENT · LOCAL BUILD (UNVERIFIED)', W / 2, 168);
    ctx.fillStyle = '#ffffff'; ctx.font = 'bold 64px Georgia, serif';
    ctx.fillText(state.nama || 'Penjaga Bumi', W / 2, H * 0.42);
    ctx.fillStyle = '#f3d98b'; ctx.font = 'bold 44px system-ui';
    ctx.fillText(`Tier: ${state.tier} · ${state.kota}`, W / 2, H * 0.50);
    const st = state.stat || {};
    ctx.fillStyle = '#e7f3df'; ctx.font = '28px system-ui';
    ctx.fillText(`Sampah Dipulihkan: ${(st.pulih_unik_g / 1000).toFixed(1)} kg · Tier: ${(state.gt_claimed || []).length}/9 · Misi Tambahan: ${(state.pr_claimed || []).length}/10`, W / 2, H * 0.60);
    ctx.fillText(`Listrik dari Sampah: ${((state.energy || {}).waste_origin_used_wh / 1000 || 0).toFixed(2)} kWh · Self-Made: ${(state.wallet || {}).self_made_provisional ? 'Ya (Provisional)' : 'Sandbox Top-Up'}`, W / 2, H * 0.66);
    ctx.fillStyle = '#9fb6a6'; ctx.font = '22px system-ui';
    ctx.fillText(`Tanggal: ${new Date().toISOString().slice(0, 10)} · Chapter I: The Calling of Gaia · teranova.id`, W / 2, H - 80);
    const a = document.createElement('a');
    a.download = `terranova-card-${sizeKey}-${Date.now()}.png`;
    a.href = c.toDataURL('image/png');
    a.click();
  }

  // ---- Sheet Renderer for all Feature Freeze modes
  function renderFFSheet(mode, s, meta, closeBtn, back) {
    const st = s.stat || {};
    if (mode === 'energi') {
      const en = s.energy || {};
      const ev = meta.event_aktif || {};
      const gsg = meta.gsg || {};
      return `<div class="sh-head">${back}<h3>⚡ Pusat Energi</h3>${closeBtn}</div>
        <p class="sh-note">Cuaca hari ini: <b>${esc(ev.nama)}</b> — ${esc(ev.efek)} · Batas uji DRES rumah tangga: 100 kW / 200 kWh.</p>
        <div class="grid">
          <div class="card-box"><b>🔥 Biogas dari Sampah Organik</b>
            <small>Stok organik: ${fmtKg(s.organik_g)} · Biogas: ${(en.biogas_m3_x100 / 100).toFixed(2)} m³</small>
            <button class="act" data-a="olah_biogas">Olah 5 kg Organik → Biogas<small>Digester sendiri gratis / mitra 2.500 GC</small></button>
            <button class="act" data-a="jalankan_energi" data-sumber="biogas">Jalankan Genset Biogas (1,2 kWh)<small>Listrik dari sampah (sewa genset mitra 2.000 GC)</small></button>
          </div>
          <div class="card-box"><b>Energi Terbarukan (DRES)</b>
            <small>Baterai: ${en.battery_wh} / ${en.battery_cap_wh} Wh (Terbarukan: ${en.battery_renew_wh} Wh)</small>
            ${(() => {
              const wi = meta.waktu_info || {};
              const malam = !(wi.faktor_surya > 0);
              if (!wi.surya_terpasang_w && !wi.hidro_terpasang_w) return '<small>Belum ada panel surya/mikrohidro. Beli Solar Kit di Pasar → Katalog, lalu baterai terisi sendiri di siang hari.</small>';
              return `<small>${malam ? '🌙 Malam (WIB): panel surya istirahat' : '☀️ Siang (WIB): panel surya mengisi'} · daya kini ±${(wi.daya_kini_w || 0).toLocaleString('id-ID')} W dari ${((wi.surya_terpasang_w || 0) + (wi.hidro_terpasang_w || 0)).toLocaleString('id-ID')} W terpasang</small>
                <small>Waktu nyata: matahari terbit 06.00, terbenam 18.00 WIB; ±5 jam puncak per hari${wi.hidro_terpasang_w ? '; mikrohidro mengalir 24 jam' : ''}.</small>`;
            })()}
            <small>Rugi baterai tercatat: ${en.battery_loss_wh} Wh (10% round-trip)</small>
            <button class="act" data-a="jalankan_energi" data-sumber="renewable">Salurkan Listrik Terbarukan<small>Hitung provenance tanpa kredit ganda</small></button>
          </div>
          <div class="card-box"><b>📒 Catatan Listrik</b>
            <small>Listrik dari sampah terpakai: <b>${(en.waste_origin_used_wh / 1000).toFixed(2)} kWh</b></small>
            <small>Terbarukan terpakai: <b>${(en.renewable_used_wh / 1000).toFixed(2)} kWh</b></small>
            <small>Target: 1 kWh untuk tier Ascendant · 10 kWh untuk Archon &amp; God</small>
            <button class="act hint" data-a="audit_energi"><b>✓ Cek Catatan Listrik</b><small>Syarat tier Ascendant &amp; God · sudah dicek ${st.audit_energi || 0}×</small></button>
          </div>
        </div>`;
    }

    if (mode === 'katalog') {
      // Pasar map (Evaluasi 4): each kiosk shows the catalogue locked to its own kind/categories
      const kios = window.TN_KIOS || null;
      if (kios && catState.kios !== kios.id) Object.assign(catState, { kios: kios.id, kind: kios.kind, cat: kios.cat, page: 1, q: '', active: kios.active !== false, data: null, loading: false });
      if (!kios && catState.kios) Object.assign(catState, { kios: null, cat: '', page: 1, data: null, loading: false });
      if (!catState.data && !catState.loading) loadCatalog();
      const d = catState.data;
      const stats = (d && d.stats) || meta.catalog_stats || {};
      const listHtml = !d ? '<p class="sh-note">Memuat katalog canonical…</p>' : d.items.map(it => {
        if (it.catalog_kind === 'machine') {
          const isAct = it.status === 'active';
          const img = window.TN_MESIN ? window.TN_MESIN.ikon(it.nama, it.category) : '';
          return `<div class="card-box alat-card ${isAct ? '' : 'locked-box'}">
            <div class="alat-top"><img src="${img}" alt=""><div><b>${esc(it.nama)}</b>
            <small>${esc(it.category)} · ${['', 'skala rumah', 'skala usaha kecil', 'skala industri', 'skala industri besar'][it.f_stage] || 'tahap ' + it.f_stage}</small>
            <small>💰 ${fmtGC(it.harga_gc)} · 📦 ${esc(it.kapasitas)}</small></div></div>
            <div class="alat-fungsi">⚙️ Proses: <b>${esc(it.fungsi)}</b></div>
            ${isAct && it.efek ? `<ul class="efek">${it.efek.map(t => `<li>${esc(t)}</li>`).join('')}</ul>` : ''}
            ${isAct && it.harga_gc > 0 ? `<div class="menu-row" style="margin-top:4px">
              <button class="act" data-a="beli_mesin" data-mid="${esc(it.id)}" data-harga="${it.harga_gc}" data-nama="${esc(it.nama)}">🛒 Beli<small>${/angkut/i.test((it.efek || [])[0] || '') ? 'Dipakai di menu Angkut' : 'Langsung tampil di lahan'}</small></button>
              <button class="act" data-a="sewa_mesin" data-mid="${esc(it.id)}" data-nama="${esc(it.nama)}">⏱️ Sewa 24 jam</button>
            </div>` : `<small>🔒 ${it.status === 'active' ? 'Tidak dijual' : 'Belum dibuka (menunggu validasi resep)'} · hanya untuk dipelajari</small>`}
          </div>`;
        }
        if (it.catalog_kind === 'material') {
          return `<div class="card-box ${it.hazardous ? 'locked-box' : ''}">
            <b>${esc(it.nama)}</b>
            <small>${esc(it.category)} (${esc(it.unit)}) · Output: ${esc(it.output_id)} (${it.yield_pct}%)</small>
            <small>Bank: ${fmtGC(it.bank_gc)} · Pengepul: ${fmtGC(it.pengepul_gc)} · Bandar: ${fmtGC(it.bandar_gc)}</small>
            ${it.hazardous ? `<small>⚠️ B3/Khusus · Biaya disposal ${fmtGC(it.disposal_fee)}</small>` : ''}
          </div>`;
        }
        if (it.catalog_kind === 'crop') {
          return `<div class="card-box"><b>${it.rare ? '✨ ' : '🌱 '}${esc(it.nama)}${it.rare ? ' (langka)' : ''}</b>
            <small>Tumbuh ${it.detik} dtk · Hasil ${it.hasil_g} g · ${fmtGC(it.gc_per_kg)}/kg · +${it.vitality} Vit</small>
            <button class="act" data-a="beli_benih" data-crop="${esc(it.id)}">Beli Benih (${fmtGC(it.benih_gc)})</button>
          </div>`;
        }
        return `<div class="card-box"><b>${esc(it.nama)}</b>
          <small>${fmtGC(it.harga_gc)}/${esc(it.unit)} · +${it.vitality} Vitalitas (${esc(it.group)})</small>
          <button class="act" data-a="beli_pangan" data-food="${esc(it.id)}">Beli 1 ${esc(it.unit)}</button>
        </div>`;
      }).join('');
      if (kios) return `<div class="sh-head">${back}<h3>${kios.judul}</h3>${closeBtn}</div>${kios.atas || ''}
        <div class="menu-row" style="margin:0 0 8px">
          <input id="catSearch" placeholder="Cari di kios ini…" value="${esc(catState.q)}" style="flex:2;min-width:140px;background:#0b1d14;border:1px solid #4d7a5c;border-radius:8px;padding:6px 10px">
          ${kios.kind === 'machine' ? `<button type="button" id="catActiveOnly">${catState.active ? '✓ Yang bisa dibeli' : 'Semua (termasuk terkunci)'}</button>` : ''}
        </div>
        <div class="grid">${listHtml}</div>
        ${d && d.pages > 1 ? `<div class="menu-row"><button type="button" id="catPrev" ${d.page <= 1 ? 'disabled' : ''}>‹ Sebelumnya</button><button type="button" disabled>Hal ${d.page} / ${d.pages}</button><button type="button" id="catNext" ${d.page >= d.pages ? 'disabled' : ''}>Berikutnya ›</button></div>` : ''}`;
      return `<div class="sh-head">${back}<h3>📚 Ensiklopedia &amp; Pasar Katalog</h3>${closeBtn}</div>
        <p class="sh-note">Total canonical: <b>${stats.materials_total || 282}</b> material, <b>${stats.machines_rows || 307}</b> mesin (${stats.machines_canonical || 288} canonical + ${stats.machines_aliases || 19} alias), <b>15</b> tanaman, <b>4</b> pangan pokok. Mesin tanpa resep tervalidasi terkunci aman.</p>
        <div class="menu-row" style="margin:0 0 8px">
          <select id="catKind"><option value="machine" ${catState.kind === 'machine' ? 'selected' : ''}>Mesin &amp; Energi (307)</option><option value="material" ${catState.kind === 'material' ? 'selected' : ''}>Material &amp; Produk (282)</option><option value="crop" ${catState.kind === 'crop' ? 'selected' : ''}>Benih 15 Tanaman</option><option value="food" ${catState.kind === 'food' ? 'selected' : ''}>Pangan Pokok NPC</option></select>
          <input id="catSearch" placeholder="Cari nama / ID…" value="${esc(catState.q)}" style="flex:2;min-width:140px;background:#0b1d14;border:1px solid #4d7a5c;border-radius:8px;padding:6px 10px">
          ${d && (d.categories || []).length ? `<select id="catCat"><option value="">Semua kategori</option>${d.categories.map(c => `<option value="${esc(c)}" ${catState.cat === c ? 'selected' : ''}>${esc(c)}</option>`).join('')}</select>` : ''}
          <button type="button" id="catActiveOnly">${catState.active ? '✓ Aktif saja' : 'Semua (termasuk terkunci)'}</button>
        </div>
        <div class="grid">${listHtml}</div>
        ${d ? `<div class="menu-row"><button type="button" id="catPrev" ${d.page <= 1 ? 'disabled' : ''}>‹ Sebelumnya</button><button type="button" disabled>Hal ${d.page} / ${d.pages} (${d.total} item)</button><button type="button" id="catNext" ${d.page >= d.pages ? 'disabled' : ''}>Berikutnya ›</button></div>` : ''}`;
    }

    if (mode === 'radio') {
      radio.muat().then(() => { if (!MUSIK.radio.length) return; const sh = document.querySelector('[data-radio-list]'); if (sh && sh.dataset.radioList === '0') window.renderSheet && window.renderSheet(); });
      const c = radio.cur, on = radio.playing;
      const daftar = src => MUSIK[src].map(t => {
        const aktif = c && radio.sumber === src && c.id === t.id;
        return `<button type="button" class="act ${aktif ? 'hint' : ''}" data-radio="lagu" data-src="${src}" data-val="${esc(t.id)}"><b>${aktif && on ? '🔊' : src === 'radio' ? '🎤' : src === 'tema' ? '⭐' : '🎻'} ${esc(t.judul)}</b><small>${esc(t.artis || 'Ukolabs')} · ${fmtDur(t.durasi || 0)}</small></button>`;
      }).join('');
      const modeBtn = (m, lbl, ket) => `<button type="button" class="${radio.mode === m ? 'hint' : ''}" data-radio="mode" data-val="${m}" title="${ket}">${radio.mode === m ? '✓ ' : ''}${lbl}</button>`;
      return `<div class="sh-head">${back}<h3>📻 Gaia Radio</h3>${closeBtn}</div>
        <div class="card-box" data-radio-list="${MUSIK.radio.length ? 1 : 0}" style="display:flex;align-items:center;gap:12px;flex-wrap:wrap">
          <div style="font-size:34px">${on ? '🎶' : '📻'}</div>
          <div style="flex:1;min-width:160px"><small>${on && c ? SUMBER_LABEL[radio.sumber] : 'Radio mati'}</small><br><b>${on && c ? esc(c.judul) : 'Tekan ▶ untuk memutar'}</b>${on && radio.terblokir ? '<br><small>Ketuk layar sekali agar suara diizinkan browser.</small>' : ''}</div>
          <div style="display:grid;grid-template-columns:1fr 2fr 1fr;gap:6px;width:100%">
            <button type="button" data-radio="prev" aria-label="Lagu sebelumnya" ${c ? '' : 'disabled'}>⏮</button>
            <button type="button" data-radio="toggle" aria-label="${on ? 'Jeda' : 'Putar'}">${on ? '⏸ Jeda' : '▶ Putar'}</button>
            <button type="button" data-radio="next" aria-label="Lagu berikutnya">⏭</button>
          </div>
        </div>
        <div class="menu-row">
          ${modeBtn('auto', '🗺️ Ikuti Tempat', 'Lahan: musik latar · Pasar: lagu radio')}
          ${modeBtn('latar', '🎻 Musik Latar', 'Instrumental tenang di mana saja')}
          ${modeBtn('radio', '📻 Lagu Radio', 'Lagu bervokal di mana saja')}
          <button type="button" data-radio="acak">${radio.acak ? '🔀 Acak' : '🔁 Berurutan'}</button>
        </div>
        <label class="sh-note" style="display:flex;align-items:center;gap:8px">🔉 Volume <input type="range" id="radioVol" min="0" max="1" step="0.05" value="${radio.vol}" style="flex:1"> 🔊</label>
        <h4 class="sh-sub">⭐ Lagu Tema</h4><div class="grid">${daftar('tema')}</div>
        <h4 class="sh-sub">📻 Lagu Radio (${MUSIK.radio.length})</h4><div class="grid">${daftar('radio') || '<p class="sh-note">Memuat daftar lagu…</p>'}</div>
        <h4 class="sh-sub">🎻 Musik Latar (${MUSIK.latar.length})</h4><div class="grid">${daftar('latar')}</div>
        <p class="sh-note">Semua lagu karya Ukolabs untuk Terra Nova. Di mode “Ikuti Tempat”, musik berganti halus saat kamu pindah dari Lahan ke Pasar.</p>`;
    }

    if (mode === 'jurnal') {
      const j = (s.journal || []).slice().reverse();
      return `<div class="sh-head">${back}<h3>📖 Jurnal &amp; Kartu Pencapaian</h3>${closeBtn}</div>
        <p class="sh-note">Unduh kartu pencapaian PNG (tanpa data pribadi/email · label <i>Prototype Achievement Lokal</i>):</p>
        <div class="menu-row" style="margin-top:0;margin-bottom:10px">
          <button type="button" data-card="square">🖼️ Square 1080×1080</button>
          <button type="button" data-card="story">📱 Story 1080×1920</button>
          <button type="button" data-card="landscape">🖥️ Landscape 1200×628</button>
          <button type="button" data-act="replay_opening">🎬 Tonton Ulang Opening</button>
        </div>
        <h4 class="sh-sub">Catatan Perjalanan (${j.length})</h4>
        ${j.length ? j.map(it => `<div class="card-box" style="margin-bottom:6px"><b>${esc(it.title)}</b><small>${esc(it.subtitle)}</small></div>`).join('') : '<p class="sh-note">Belum ada tonggak tercatat. Selesaikan misi GT01 atau PR01!</p>'}`;
    }

    if (mode === 'knowledge') {
      return `<div class="sh-head">${back}<h3>🎓 Knowledge Center</h3>${closeBtn}</div>
        <div class="grid">
          <div class="card-box"><b>Tidak Ada Sampah yang Hilang</b><small>Sumber: Prinsip Pengelolaan Sampah &amp; Simulasi TERRA NOVA (2026). Tidak ada sampah yang hilang; semua menjadi produk olahan, uap/air terkendali, residu, B3 berizin, atau backlog TPA.</small></div>
          <div class="card-box"><b>Jalur Rumah Tangga vs Industri</b><small>Prinsip Constitution v2.0: Tier God dapat dicapai tanpa pabrik besar dan tanpa top-up uang nyata. Kompos, biogas mikro, panel surya, dan akses mitra setara dengan pabrik industri.</small></div>
          <div class="card-box"><b>Keamanan Limbah B3</b><small>Baterai bekas, limbah medis, dan elektronik rusak tidak boleh dicampur ke gerobak atau pengolahan umum — wajib diserahkan melalui jalur pengolah berizin.</small></div>
          <div class="card-box"><b>Ekonomi Realistis (1 GC ≈ Rp1)</b><small>Angka 1 GC ≈ Rp1 adalah skala edukasi simulasi, bukan konversi uang tunai atau penawaran harga pasar nyata.</small></div>
        </div>`;
    }

    if (mode === 'leaderboard') {
      if (!lbState.data) loadLeaderboard();
      const d = lbState.data;
      return `<div class="sh-head">${back}<h3>🏆 Peringkat (Fixture Lokal)</h3>${closeBtn}</div>
        <p class="sh-note"><b>⚠️ FIXTURE LOKAL</b> — bukan ranking publik beta. Tidak memuat email, usia, atau nominal top-up.</p>
        ${d ? `<select id="lbSelect" style="width:100%;min-height:40px;background:#0b1d14;border:1px solid #4d7a5c;border-radius:8px;padding:6px;margin-bottom:10px">${d.boards.map(b => `<option value="${esc(b.id)}" ${b.id === d.board ? 'selected' : ''}>${esc(b.title)} — ${esc(b.metric)}</option>`).join('')}</select>
        <table class="tbl"><tr><th>#</th><th>Pemain</th><th>Kota</th><th>Tier</th><th>${esc(d.metric)}</th><th>Self-Made</th></tr>
        ${d.rows.map((r, i) => `<tr><td>${i + 1}</td><td>${esc(r.nama)}</td><td>${esc(r.kota)}</td><td>${esc(r.tier)}</td><td><b>${Number(r.score).toLocaleString('id-ID')}</b></td><td>${r.self_made ? '🌿 Ya' : '🧪 Sandbox'}</td></tr>`).join('')}</table>` : '<p class="sh-note">Memuat fixture peringkat…</p>'}`;
    }

    if (mode === 'sandbox_store') {
      const pkgs = meta.sandbox_packages || [];
      return `<div class="sh-head">${back}<h3>🧪 Toko GC (SANDBOX LOKAL)</h3>${closeBtn}</div>
        <p class="sh-note"><b>Pay to Build, Play to Achieve:</b> Mode uji lokal tanpa uang nyata. Top-up sandbox hanya menambah GC ekonomi, <b>TIDAK</b> memberi XP, lencana, atau status God, dan menandai akun keluar dari jalur Self-Made provisional.</p>
        <div class="grid">${pkgs.map(p => `<div class="card-box"><b>${esc(p.nama)}</b><small>${fmtGC(p.gc)} · Simulasi Rp ${p.idr.toLocaleString('id-ID')}</small>
          <button class="act warn" data-a="sandbox_topup" data-sku="${esc(p.sku)}">Uji Kredit Sandbox</button></div>`).join('')}</div>`;
    }

    if (mode === 'dukung') {
      const u = meta.support_urls || {};
      return `<div class="sh-head">${back}<h3>💚 Dukung TERRA NOVA</h3>${closeBtn}</div>
        <p class="sh-note">Dukungan bersifat sukarela dan <b>tidak pernah</b> memberi keuntungan gameplay, GC, XP, atau status God/Chosen.</p>
        <div class="grid">
          <div class="card-box"><b>Apresiasi / Donasi</b><small>Tautan resmi pemilik belum diisi (aman, tanpa transaksi di dalam game).</small>
            ${u.support_url ? `<a href="${esc(u.support_url)}" target="_blank" rel="noopener noreferrer"><button class="act">Buka Tautan Resmi</button></a>` : '<button class="act" disabled>Segera Hadir (tautan belum diatur)</button>'}</div>
          <div class="card-box"><b>Kemitraan &amp; Sponsor Edukasi</b><small>Label sponsor wajib jelas; sponsor tidak pernah memengaruhi fakta edukasi atau peringkat.</small>
            ${u.sponsor_contact_url ? `<a href="${esc(u.sponsor_contact_url)}" target="_blank" rel="noopener noreferrer"><button class="act">Hubungi Sponsor</button></a>` : '<button class="act" disabled>Segera Hadir (kontak belum diatur)</button>'}</div>
        </div>`;
    }

    if (mode === 'admin') {
      if (!adminState.data) loadAdmin();
      const d = adminState.data;
      const c = (d && d.config) || {};
      if (d && !d.is_admin) {
        return `<div class="sh-head">${back}<h3>🛠️ Admin Config</h3>${closeBtn}</div>
          <div class="lock-box"><b>🔒 Khusus akun pemilik</b><p>Pengaturan global (modal awal, pengali harga, tautan) hanya bisa diubah oleh akun admin.</p></div>`;
      }
      return `<div class="sh-head">${back}<h3>🛠️ Admin Config Lokal (v${c.version || 1})</h3>${closeBtn}</div>
        <p class="sh-note">Hanya untuk review lokal loopback. Setiap perubahan tercatat di <code>admin_audit</code> dan dapat di-rollback.</p>
        <div class="grid">
          <div class="card-box"><b>Modal Awal (GC)</b><input id="admStarter" type="number" value="${c.starter_gc || 1000000}" style="background:#0b1d14;border:1px solid #4d7a5c;border-radius:8px;padding:6px">
            <small>1.000.000 uji utama · 100.000 stress test</small></div>
          <div class="card-box"><b>Pengali Harga Pasar</b><input id="admMult" type="number" step="0.05" value="${c.price_multiplier || 1}" style="background:#0b1d14;border:1px solid #4d7a5c;border-radius:8px;padding:6px">
            <small>Rentang sah 0.5 – 2.0</small></div>
        </div>
        <div class="menu-row">
          <button type="button" id="admSave">💾 Terbitkan Versi Config</button>
          <button type="button" id="admStress">🧪 Reset Akun ke Stress Test 100k GC</button>
          ${c.version > 1 ? `<button type="button" id="admRollback" data-ver="${c.version - 1}">↩️ Rollback ke v${c.version - 1}</button>` : ''}
        </div>
        ${d && d.audit ? `<h4 class="sh-sub">Audit Log Terbaru</h4>${d.audit.slice(0, 5).map(a => `<small style="display:block;color:var(--muted)">v${a.version} · ${esc(a.actor)} — ${esc(a.reason)}</small>`).join('')}` : ''}`;
    }

    if (mode === 'feedback') {
      if (!fbState.data) loadFeedback();
      const items = (fbState.data && fbState.data.items) || [];
      return `<div class="sh-head">${back}<h3>💬 Masukan &amp; Laporan Bug</h3>${closeBtn}</div>
        <div class="card-box">
          <select id="fbCat" style="background:#0b1d14;border:1px solid #4d7a5c;border-radius:8px;padding:6px"><option value="bug">Laporan Bug</option><option value="saran">Saran Gameplay</option><option value="ekonomi">Kalibrasi Ekonomi</option><option value="edukasi">Koreksi Fakta Edukasi</option></select>
          <textarea id="fbMsg" rows="3" placeholder="Tulis masukan Anda di sini (tersimpan lokal di SQLite)…" style="width:100%;background:#0b1d14;color:#fff;border:1px solid #4d7a5c;border-radius:8px;padding:8px"></textarea>
          <button type="button" id="fbSend" class="act">Kirim Masukan Lokal</button>
        </div>
        ${items.length ? `<h4 class="sh-sub">Riwayat Masukan (${items.length})</h4>${items.slice(0, 5).map(x => `<small style="display:block;margin-bottom:4px">[${esc(x.category)}] ${esc(x.message)}</small>`).join('')}` : ''}`;
    }

    return null;
  }

  // Event wiring for Feature Freeze controls
  document.addEventListener('change', e => {
    if (e.target.id === 'catKind') { catState.kind = e.target.value; catState.cat = ''; catState.page = 1; loadCatalog(); }
    if (e.target.id === 'catCat') { catState.cat = e.target.value; catState.page = 1; loadCatalog(); }
    if (e.target.id === 'lbSelect') { loadLeaderboard(e.target.value); }
  });
  let searchDebounce = null;
  document.addEventListener('input', e => {
    if (e.target.id === 'catSearch') {
      catState.q = e.target.value; catState.page = 1;
      clearTimeout(searchDebounce); searchDebounce = setTimeout(loadCatalog, 220);
    }
  });
  document.addEventListener('input', e => { if (e.target.id === 'radioVol') radio.setVol(Number(e.target.value)); });
  document.addEventListener('click', async e => {
    const b = e.target.closest('button');
    if (!b) return;
    if (b.id === 'catActiveOnly') { catState.active = !catState.active; catState.page = 1; loadCatalog(); return; }
    if (b.id === 'catPrev' && catState.page > 1) { catState.page--; loadCatalog(); return; }
    if (b.id === 'catNext') { catState.page++; loadCatalog(); return; }
    if (b.dataset.radio) {
      const r = b.dataset.radio;
      if (r === 'toggle') radio.toggle(window.TN_SCENE);
      if (r === 'mode') radio.setMode(b.dataset.val);
      if (r === 'acak') radio.setAcak(!radio.acak);
      if (r === 'lagu') radio.pilihLagu(b.dataset.src, b.dataset.val);
      if (r === 'next') { if (radio.playing) radio.berikut(); else radio.mulai(window.TN_SCENE); radio.playing = true; }
      if (r === 'prev') radio.sebelum();
      window.dispatchEvent(new CustomEvent('tn-musik-status'));
      window.renderSheet && window.renderSheet();
      return;
    }
    if (b.dataset.card && window.TN_STATE) { exportCardPNG(window.TN_STATE, b.dataset.card); return; }
    if (b.id === 'admSave') {
      const res = await fetch('/admin/config', {
        method: 'POST', headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ updates: { starter_gc: Number(document.getElementById('admStarter').value), price_multiplier: Number(document.getElementById('admMult').value) }, reason: 'editor lokal' })
      });
      const d = await res.json();
      if (document.getElementById('status')) document.getElementById('status').textContent = d.pesan || 'Tersimpan.';
      loadAdmin(); return;
    }
    if (b.id === 'admRollback') {
      const res = await fetch('/admin/config', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ rollback_to: Number(b.dataset.ver), reason: 'rollback UI' }) });
      const d = await res.json();
      if (document.getElementById('status')) document.getElementById('status').textContent = d.pesan || 'Rollback selesai.';
      loadAdmin(); return;
    }
    if (b.id === 'admStress') {
      if (confirm('Reset akun ini ke skenario Stress Test 100.000 GC?')) {
        await window.TN_SEND({ aksi: 'reset_sim', starter_gc: 100000 });
        location.href = '/';
      }
      return;
    }
    if (b.id === 'fbSend') {
      const msg = (document.getElementById('fbMsg').value || '').trim();
      const cat = document.getElementById('fbCat').value;
      const res = await fetch('/feedback', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ category: cat, message: msg, rating: 5, consent: true }) });
      const d = await res.json();
      if (document.getElementById('status')) document.getElementById('status').textContent = d.pesan || 'Terkirim.';
      if (res.ok) { document.getElementById('fbMsg').value = ''; loadFeedback(); }
      return;
    }
  });

  window.TN_FF = { esc, fmtGC, fmtKg, radio, renderFFSheet, loadCatalog, loadLeaderboard, loadAdmin, loadFeedback, exportCardPNG };
})();
