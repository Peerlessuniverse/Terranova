/* TERRA NOVA — Feature Freeze v1.0 Modular UI Extensions (Catalog, 15 Crops, Vitality, Energy, Radio, Celebrations, Sandbox, Leaderboard, Card Export, Admin, Feedback) */
(function () {
  const esc = s => String(s == null ? '' : s).replace(/[&<>"']/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]));
  const fmtGC = n => Number(n || 0).toLocaleString('id-ID') + ' GC';
  const fmtKg = g => (Number(g || 0) / 1000).toLocaleString('id-ID', { maximumFractionDigits: 2 }) + ' kg';

  // ---- Gaia Radio (Single WebAudio Player, Auto/Manual/Shuffle/Mute, ducks on celebration)
  const RADIO_TRACKS = [
    { id: 'pabrik', title: 'Harmoni Daur Ulang', scene: 'pabrik', notes: [261.6, 293.7, 329.6, 392, 440, 392, 329.6, 293.7], tempo: 520 },
    { id: 'kebun', title: 'Embun Kebun Gaia', scene: 'kebun', notes: [293.7, 349.2, 440, 523.3, 440, 392, 349.2, 329.6], tempo: 640 },
    { id: 'pasar', title: 'Semangat Pasar Nusantara', scene: 'pasar', notes: [329.6, 392, 440, 523.3, 587.3, 523.3, 440, 392], tempo: 380 },
    { id: 'angkut', title: 'Langkah Gerobak Pagi', scene: 'angkut', notes: [246.9, 293.7, 370, 440, 370, 293.7, 329.6, 246.9], tempo: 440 },
    { id: 'jurnal', title: 'Refleksi Bumi Baru', scene: 'menu', notes: [220, 261.6, 329.6, 392, 329.6, 261.6, 246.9, 220], tempo: 720 },
  ];
  const radio = {
    mode: localStorage.getItem('tn_radio_mode') || 'auto', // auto | manual | shuffle
    trackId: localStorage.getItem('tn_radio_track') || 'pabrik',
    playing: false,
    step: 0,
    timer: null,
    ac: null,
    getTrack(scene) {
      if (this.mode === 'manual') return RADIO_TRACKS.find(t => t.id === this.trackId) || RADIO_TRACKS[0];
      if (this.mode === 'shuffle') return RADIO_TRACKS[Math.floor(this.step / 16) % RADIO_TRACKS.length];
      return RADIO_TRACKS.find(t => t.scene === scene) || RADIO_TRACKS[0];
    },
    toggle(scene) {
      this.playing = !this.playing;
      clearInterval(this.timer);
      if (this.playing) {
        this.ac = this.ac || new (window.AudioContext || window.webkitAudioContext)();
        this.ac.resume().catch(() => {});
        this.startLoop(scene);
      }
      return this.playing;
    },
    startLoop(scene) {
      clearInterval(this.timer);
      if (!this.playing) return;
      const tr = this.getTrack(scene);
      this.timer = setInterval(() => {
        if (!this.playing || document.hidden) return;
        const cur = this.getTrack(window.TN_SCENE || 'pabrik');
        const c = this.ac, t = c.currentTime;
        const duck = (window.TN_DUCK ? 0.35 : 1.0);
        const o = c.createOscillator(), g = c.createGain();
        o.type = 'triangle';
        o.frequency.setValueAtTime(cur.notes[this.step % cur.notes.length], t);
        g.gain.setValueAtTime(0, t);
        g.gain.linearRampToValueAtTime(0.035 * duck, t + 0.03);
        g.gain.exponentialRampToValueAtTime(0.0001, t + 0.75);
        o.connect(g).connect(c.destination);
        o.start(t); o.stop(t + 0.8);
        this.step++;
      }, tr.tempo);
    },
    setMode(m, tid) {
      this.mode = m;
      if (tid) this.trackId = tid;
      localStorage.setItem('tn_radio_mode', this.mode);
      localStorage.setItem('tn_radio_track', this.trackId);
      if (this.playing) this.startLoop(window.TN_SCENE || 'pabrik');
    }
  };

  // ---- Async data caches (on-demand, never preloaded at boot!)
  const catState = { kind: 'machine', cat: '', q: '', page: 1, active: false, data: null, loading: false };
  const lbState = { board: 'sustainability', data: null };
  const adminState = { data: null };
  const fbState = { data: null };

  async function loadCatalog() {
    catState.loading = true;
    const qs = new URLSearchParams({
      kind: catState.kind, cat: catState.cat, q: catState.q,
      page: String(catState.page), per_page: '24', active: catState.active ? '1' : '0'
    });
    const r = await fetch('/catalog?' + qs.toString(), { credentials: 'same-origin' });
    catState.data = await r.json();
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
    ctx.fillText(`Massa Pulih: ${(st.pulih_unik_g / 1000).toFixed(1)} kg · Lencana GT: ${(state.gt_claimed || []).length}/9 · PR: ${(state.pr_claimed || []).length}/10`, W / 2, H * 0.60);
    ctx.fillText(`Energi Waste-Origin: ${((state.energy || {}).waste_origin_used_wh / 1000 || 0).toFixed(2)} kWh · Self-Made: ${(state.wallet || {}).self_made_provisional ? 'Ya (Provisional)' : 'Sandbox Top-Up'}`, W / 2, H * 0.66);
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
      return `<div class="sh-head">${back}<h3>⚡ Energy Center (WtE &amp; DRES)</h3>${closeBtn}</div>
        <p class="sh-note">Cuaca hari ini: <b>${esc(ev.nama)}</b> — ${esc(ev.efek)} · Batas uji DRES rumah tangga: 100 kW / 200 kWh.</p>
        <div class="grid">
          <div class="card-box"><b>Digester Biogas (WTE-002)</b>
            <small>Stok organik: ${fmtKg(s.organik_g)} · Biogas: ${(en.biogas_m3_x100 / 100).toFixed(2)} m³</small>
            <button class="act" data-a="olah_biogas">Olah 5 kg Organik → Biogas<small>Digester sendiri gratis / mitra 2.500 GC</small></button>
            <button class="act" data-a="jalankan_energi" data-sumber="biogas">Jalankan Genset Biogas (1,2 kWh)<small>Listrik net waste-origin (mitra 2.000 GC)</small></button>
          </div>
          <div class="card-box"><b>Energi Terbarukan (DRES)</b>
            <small>Baterai: ${en.battery_wh} / ${en.battery_cap_wh} Wh (Terbarukan: ${en.battery_renew_wh} Wh)</small>
            <small>Rugi baterai tercatat: ${en.battery_loss_wh} Wh (10% round-trip)</small>
            <button class="act" data-a="jalankan_energi" data-sumber="renewable">Salurkan Listrik Terbarukan<small>Hitung provenance tanpa kredit ganda</small></button>
          </div>
          <div class="card-box"><b>Neraca &amp; Audit Energi</b>
            <small>Waste-Origin terpakai: <b>${(en.waste_origin_used_wh / 1000).toFixed(2)} kWh</b></small>
            <small>Terbarukan terpakai: <b>${(en.renewable_used_wh / 1000).toFixed(2)} kWh</b></small>
            <small>Target GT06: 1 kWh · GT08/GSG: 10 kWh</small>
            <button class="act hint" data-a="audit_energi">Lakukan Audit Energi<small>Syarat GT06 &amp; GSG (${st.audit_energi || 0}× selesai)</small></button>
          </div>
        </div>`;
    }

    if (mode === 'katalog') {
      if (!catState.data && !catState.loading) loadCatalog();
      const d = catState.data;
      const stats = (d && d.stats) || meta.catalog_stats || {};
      const listHtml = !d ? '<p class="sh-note">Memuat katalog canonical…</p>' : d.items.map(it => {
        if (it.catalog_kind === 'machine') {
          const isAct = it.status === 'active';
          return `<div class="card-box ${isAct ? '' : 'locked-box'}">
            <b>${esc(it.id)} · ${esc(it.nama)}</b>
            <small>${esc(it.category)} · F${it.f_stage} · ${it.is_alias ? 'Alias → ' + esc(it.canonical_id) : 'Canonical'}</small>
            <small>Harga: ${fmtGC(it.harga_gc)} · Kap: ${esc(it.kapasitas)}</small>
            <small>${esc(it.fungsi)}</small>
            ${isAct && it.harga_gc > 0 ? `<div class="menu-row" style="margin-top:4px">
              <button class="act" data-a="beli_mesin" data-mid="${esc(it.id)}">Beli</button>
              <button class="act" data-a="sewa_mesin" data-mid="${esc(it.id)}">Sewa 24j</button>
            </div>` : `<small>🔒 ${esc(it.status)} (hanya edukasi)</small>`}
          </div>`;
        }
        if (it.catalog_kind === 'material') {
          return `<div class="card-box ${it.hazardous ? 'locked-box' : ''}">
            <b>${esc(it.id)} · ${esc(it.nama)}</b>
            <small>${esc(it.category)} (${esc(it.unit)}) · Output: ${esc(it.output_id)} (${it.yield_pct}%)</small>
            <small>Bank: ${fmtGC(it.bank_gc)} · Pengepul: ${fmtGC(it.pengepul_gc)} · Bandar: ${fmtGC(it.bandar_gc)}</small>
            ${it.hazardous ? `<small>⚠️ B3/Khusus · Biaya disposal ${fmtGC(it.disposal_fee)}</small>` : ''}
          </div>`;
        }
        if (it.catalog_kind === 'crop') {
          return `<div class="card-box"><b>${esc(it.id)} · ${esc(it.nama)} ${it.rare ? '✨' : ''}</b>
            <small>Tumbuh ${it.detik} dtk · Hasil ${it.hasil_g} g · ${fmtGC(it.gc_per_kg)}/kg · +${it.vitality} Vit</small>
            <button class="act" data-a="beli_benih" data-crop="${esc(it.id)}">Beli Benih (${fmtGC(it.benih_gc)})</button>
          </div>`;
        }
        return `<div class="card-box"><b>${esc(it.id)} · ${esc(it.nama)}</b>
          <small>${fmtGC(it.harga_gc)}/${esc(it.unit)} · +${it.vitality} Vitalitas (${esc(it.group)})</small>
          <button class="act" data-a="beli_pangan" data-food="${esc(it.id)}">Beli 1 ${esc(it.unit)}</button>
        </div>`;
      }).join('');
      return `<div class="sh-head">${back}<h3>📚 Ensiklopedia &amp; Pasar Katalog</h3>${closeBtn}</div>
        <p class="sh-note">Total canonical: <b>${stats.materials_total || 282}</b> material, <b>${stats.machines_rows || 307}</b> mesin (${stats.machines_canonical || 288} canonical + ${stats.machines_aliases || 19} alias), <b>15</b> tanaman, <b>4</b> pangan pokok. Mesin tanpa resep tervalidasi terkunci aman.</p>
        <div class="menu-row" style="margin:0 0 8px">
          <select id="catKind"><option value="machine" ${catState.kind === 'machine' ? 'selected' : ''}>Mesin &amp; Energi (307)</option><option value="material" ${catState.kind === 'material' ? 'selected' : ''}>Material &amp; Produk (282)</option><option value="crop" ${catState.kind === 'crop' ? 'selected' : ''}>Benih 15 Tanaman</option><option value="food" ${catState.kind === 'food' ? 'selected' : ''}>Pangan Pokok NPC</option></select>
          <input id="catSearch" placeholder="Cari nama / ID…" value="${esc(catState.q)}" style="flex:2;min-width:140px;background:#0b1d14;border:1px solid #4d7a5c;border-radius:8px;padding:6px 10px">
          <button type="button" id="catActiveOnly">${catState.active ? '✓ Aktif saja' : 'Semua (termasuk terkunci)'}</button>
        </div>
        <div class="grid">${listHtml}</div>
        ${d ? `<div class="menu-row"><button type="button" id="catPrev" ${d.page <= 1 ? 'disabled' : ''}>‹ Sebelumnya</button><button type="button" disabled>Hal ${d.page} / ${d.pages} (${d.total} item)</button><button type="button" id="catNext" ${d.page >= d.pages ? 'disabled' : ''}>Berikutnya ›</button></div>` : ''}`;
    }

    if (mode === 'radio') {
      const cur = radio.getTrack(window.TN_SCENE || 'pabrik');
      return `<div class="sh-head">${back}<h3>📻 Gaia Radio</h3>${closeBtn}</div>
        <p class="sh-note">Pemutar audio tunggal lintas-scene. Status: <b>${radio.playing ? 'Memutar — ' + esc(cur.title) : 'Mati'}</b> · Mode: <b>${esc(radio.mode)}</b></p>
        <div class="menu-row">
          <button type="button" data-radio="toggle">${radio.playing ? '⏸ Jeda Radio' : '▶ Putar Radio'}</button>
          <button type="button" data-radio="mode" data-val="auto">Auto per Scene</button>
          <button type="button" data-radio="mode" data-val="shuffle">Acak (Shuffle)</button>
        </div>
        <h4 class="sh-sub">Pilih Lagu Manual</h4>
        <div class="grid">${RADIO_TRACKS.map(t => `<button type="button" class="act ${radio.mode === 'manual' && radio.trackId === t.id ? 'hint' : ''}" data-radio="track" data-val="${t.id}"><b>🎵 ${esc(t.title)}</b><small>Scene: ${esc(t.scene)}</small></button>`).join('')}</div>`;
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
          <div class="card-box"><b>Neraca Massa Konservatif</b><small>Sumber: Prinsip Pengelolaan Sampah &amp; Simulasi TERRA NOVA (2026). Tidak ada sampah yang hilang; semua menjadi produk olahan, uap/air terkendali, residu, B3 berizin, atau backlog TPA.</small></div>
          <div class="card-box"><b>Jalur Rumah Tangga vs Industri</b><small>Prinsip Constitution v2.0: Tier God (GSG) dapat dicapai tanpa pabrik besar dan tanpa top-up uang nyata. Kompos, biogas mikro, panel surya, dan akses mitra setara dengan pabrik industri.</small></div>
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
    if (e.target.id === 'catKind') { catState.kind = e.target.value; catState.page = 1; loadCatalog(); }
    if (e.target.id === 'lbSelect') { loadLeaderboard(e.target.value); }
  });
  let searchDebounce = null;
  document.addEventListener('input', e => {
    if (e.target.id === 'catSearch') {
      catState.q = e.target.value; catState.page = 1;
      clearTimeout(searchDebounce); searchDebounce = setTimeout(loadCatalog, 220);
    }
  });
  document.addEventListener('click', async e => {
    const b = e.target.closest('button');
    if (!b) return;
    if (b.id === 'catActiveOnly') { catState.active = !catState.active; catState.page = 1; loadCatalog(); return; }
    if (b.id === 'catPrev' && catState.page > 1) { catState.page--; loadCatalog(); return; }
    if (b.id === 'catNext') { catState.page++; loadCatalog(); return; }
    if (b.dataset.radio) {
      if (b.dataset.radio === 'toggle') radio.toggle(window.TN_SCENE || 'pabrik');
      if (b.dataset.radio === 'mode') radio.setMode(b.dataset.val);
      if (b.dataset.radio === 'track') radio.setMode('manual', b.dataset.val);
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
      if (res.ok) loadFeedback();
      return;
    }
  });

  window.TN_FF = { esc, fmtGC, fmtKg, radio, renderFFSheet, loadCatalog, loadLeaderboard, loadAdmin, loadFeedback, exportCardPNG };
})();
