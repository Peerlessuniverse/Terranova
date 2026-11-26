"""Eksperimen Fase 0, Python 3. Tidak memakai layanan eksternal."""
import csv
import json
import math
import random
from pathlib import Path
from statistics import median

AKAR = Path(__file__).resolve().parent
K = json.loads((AKAR / "konfigurasi.json").read_text())
HASIL = AKAR / "hasil"
HASIL.mkdir(exist_ok=True)
SKENARIO = ["sendiri", "bersama", "ringan", "berat", "baru", "berhenti",
            "jenuh", "tanpa_permintaan", "tanpa_modal", "tanpa_stok", "retry", "bonus_reset", "kalibrasi", "kosong"]


def tulis(nama, baris):
    with (HASIL / nama).open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=baris[0].keys())
        w.writeheader()
        w.writerows(baris)


def eksperimen(skenario, benih, strategi_tunggal=0):
    rng = random.Random(benih)
    jumlah = 0 if skenario == "kosong" else 1 if skenario == "sendiri" else 20
    pemain = []
    for i in range(jumlah):
        pemain.append(dict(s=strategi_tunggal if jumlah == 1 else i % 5, stok=[0]*6,
            kas=0 if skenario == "tanpa_modal" else K["modal"], poin=0, karma=0,
            level=0, reset=0, awal=[0]+[None]*8, terakhir=None, hari_aktif=-100,
            olah=0, buang=0, kontrib=0, sumber=0, biaya=0, stok_maks=0, hari_god=None,
            hari_main=0, hari_macet=0, kuitansi=set()))
    target = 0
    for hari in range(1, K["hari"]+1):
        sesi = 3 if skenario == "berat" else 1 if skenario == "ringan" else 2
        aktif = [i for i in range(jumlah) if not (skenario=="baru" and hari<46 or
                 skenario=="berhenti" and hari>30 and i%2==0)]
        for i in aktif:
            pemain[i]["hari_aktif"] = hari
            pemain[i]["hari_main"] += 1
        n7 = sum(p["hari_aktif"] >= hari-6 for p in pemain)
        target += n7*K["target_kg_per_aktif"]
        faktor = {"jenuh":0.2,"tanpa_permintaan":0}.get(skenario,1)
        kuota = [int(x*n7*faktor) for x in K["permintaan"]]
        laku = [0]*6
        cuaca = rng.uniform(.92,1.08)
        harian = [0]*jumlah
        for sesi_ke in range(sesi):
            waktu = (hari-1)*24 + (sesi_ke+1)*24//sesi
            urutan = aktif.copy()
            rng.shuffle(urutan)
            for i in urutan:
                p = pemain[i]
                for ulang in range(2 if skenario=="retry" else 1):
                    if waktu in p["kuitansi"]:
                        continue
                    p["kuitansi"].add(waktu)
                    lalu = p["terakhir"] if p["terakhir"] is not None else (hari-1)*24
                    jam = min(K["cap_jam"], waktu-lalu)
                    p["terakhir"] = waktu
                    s = p["s"]
                    tingkat = K["faktor_level"]**p["level"]
                    profil = K["profil"][s]
                    jumlah_kg = int(K["pilah_kg_jam"]*tingkat*jam)
                    # Kapasitas lini kertas/logam dipakai bersama.
                    for kelompok in ([0],[1],[2,3],[4],[5]):
                        share = sum(profil[j] for j in kelompok)
                        jumlah_kg = min(jumlah_kg,int(K["kapasitas"][kelompok[0]]*tingkat*jam*100/share))
                    ruang = K["gudang_kg"] - sum(p["stok"])
                    # Reservasi konservatif seluruh berat input untuk ruang dan biaya.
                    jumlah_kg = min(jumlah_kg,ruang,int(p["kas"]//4))
                    if skenario=="tanpa_stok":
                        jumlah_kg = 0
                    total = jumlah_kg//100*100
                    biaya = 0
                    if total:
                        biaya = K["angkut_per_kg"]*total + K["opex_pilah"]*total/(K["pilah_kg_jam"]*tingkat)
                    mentah = limbah = terkendali = 0
                    for j, persen in enumerate(profil):
                        masuk = total*persen//100
                        ke_tpa = s==4 and j!=5 or j==4 and s!=3
                        produk = 0 if ke_tpa else masuk*K["produk_persen"][j]//100
                        if j==1 and K["kemurnian_persen"]<K["ambang_plastik"]:
                            produk = 0
                        aliran = 0 if ke_tpa else masuk*K["aliran_terkendali_persen"][j]//100
                        sisa = masuk-produk-aliran
                        assert produk+aliran+sisa==masuk and sisa>=0
                        limbah += sisa
                        terkendali += produk+aliran
                        # Fraksi B3 dikreditkan khusus, terpisah dari pengalihan umum.
                        mentah += ((produk if j==4 else produk+aliran)*K["bobot"][j])
                        if not ke_tpa:
                            biaya += masuk*K["opex"][j]/(K["kapasitas"][j]*tingkat)
                        biaya += sisa*K["tipping_per_kg"]
                        if j==4 and s==3:
                            biaya += aliran*(1-K["efisiensi_filter"])*K["pajak_per_kg"]
                        p["stok"][j] += produk
                    if sesi_ke==0 and total:
                        biaya += K["perawatan_harian"]
                    biaya = math.ceil(biaya)
                    assert biaya<=p["kas"]
                    p["kas"] -= biaya
                    p["biaya"] += biaya
                    p["olah"] += total
                    p["buang"] += limbah
                    p["kontrib"] += terkendali
                    p["stok_maks"] = max(p["stok_maks"],sum(p["stok"]))
                    if not total and sesi_ke==0:
                        p["hari_macet"] += 1
                    # Keputusan jual eksplisit agen setelah produksi.
                    for j, batas in enumerate(kuota):
                        beli = min(p["stok"][j], batas-laku[j])
                        if beli:
                            # Harga rata-rata marginal agar pecah penjualan tak mengubah tarif.
                            def integral(x):
                                return x-x*x/(2*batas) if x<=batas/2 else .5*x+batas/8
                            nilai = math.floor(K["harga"][j]*cuaca*(integral(laku[j]+beli)-integral(laku[j])))
                            laku[j] += beli
                            p["stok"][j] -= beli
                            p["kas"] += nilai
                            p["sumber"] += nilai
                    if p["level"]<K["maks_level"] and total:
                        harga = math.ceil(K["harga_upgrade"]*1.6**p["level"])
                        if p["kas"]>=harga+K["modal"]:
                            p["kas"] -= harga
                            p["biaya"] += harga
                            p["level"] += 1
                    p["karma"] = min(100,max(0,p["karma"]+limbah*K["karma_landfill_per_kg"]-terkendali*K["karma_pulih_per_kg"]))
                    bonus = 1+.1*min(p["reset"],3) if skenario=="bonus_reset" else 1
                    kredit = min(K["batas_poin_harian"]-harian[i],int(max(0,mentah-limbah)*bonus))
                    if skenario=="kalibrasi" and sesi_ke==0 and terkendali>=500 and limbah<=.1*total:
                        kredit = min(K["batas_poin_harian"]-harian[i],kredit+K["misi_harian_kandidat"])
                    p["poin"] += kredit
                    harian[i] += kredit
                    if p["karma"]>=100:
                        p["reset"] += 1
                        p["karma"] = p["poin"] = 0
                    for t,ambang in enumerate(K["tier"]):
                        layak = t<8 or (p["karma"]<=25 and p["olah"]-p["buang"]>=.9*p["olah"] and p["kontrib"]>=K["minimum_pribadi_kg"])
                        if layak and p["poin"]>=ambang and p["awal"][t] is None:
                            p["awal"][t]=hari
                    assert p["kas"]>=0 and sum(p["stok"])<=K["gudang_kg"]
    baris=[]
    for i,p in enumerate(pemain):
        awal = 0 if skenario=="tanpa_modal" else K["modal"]
        assert p["kas"]==awal+p["sumber"]-p["biaya"]
        baris.append(dict(skenario=skenario,benih=benih,pemain=i,strategi=K["strategi"][p["s"]],
            hari_aktif=p["hari_main"],saldo=p["kas"],penciptaan_bersih=p["kas"]-awal,
            sumber=p["sumber"],sink=p["biaya"],poin=p["poin"],karma=round(p["karma"],2),
            reinkarnasi=p["reset"],masuk_kg=p["olah"],landfill_kg=p["buang"],kontribusi_kg=p["kontrib"],
            stok_akhir=sum(p["stok"]),hari_macet=p["hari_macet"],**{f"tier_{t+1}":d for t,d in enumerate(p["awal"])}))
    olah=sum(p["olah"] for p in pemain)
    kontrib=sum(p["kontrib"] for p in pemain)
    buang=olah-kontrib
    zwm=min(target,kontrib)/target if target else None
    # KPI kapasitas metode eksperimen. Kredit massa asal harus dibatasi target.
    bhi=max(0,100-40*(1-zwm)-30*buang/max(1,target*K["batas_residu"])) if target else None
    return baris,dict(skenario=skenario,benih=benih,n=jumlah,target_kg=target,zwm_persen=None if zwm is None else round(100*zwm,2),
        bhi=None if bhi is None else round(bhi,2),upacara=bool(target and kontrib>=target and buang<=K["batas_residu"]*olah))


def main():
    semua, dunia = [], []
    for sk in SKENARIO:
        for benih in K["benih"]:
            for strategi in range(5 if sk=="sendiri" else 1):
                rows, bumi=eksperimen(sk,benih,strategi)
                semua.extend(rows)
                dunia.append(dict(bumi,strategi_tunggal=K["strategi"][strategi] if sk=="sendiri" else ""))
    tulis("pemain.csv",semua)
    tulis("musim.csv",dunia)
    acuan={(r["benih"],r["pemain"]):r for r in semua if r["skenario"]=="bersama"}
    for r in semua:
        if r["skenario"]=="retry":
            a=acuan[r["benih"],r["pemain"]]
            assert all(a[k]==v for k,v in r.items() if k!="skenario")
    ringkas=[]
    for sk in SKENARIO:
        for s in K["strategi"]:
            grup=[r for r in semua if r["skenario"]==sk and r["strategi"]==s]
            if grup:
                d=[r["tier_9"] for r in grup if r["tier_9"] is not None]
                ringkas.append(dict(skenario=sk,strategi=s,n=len(grup),god=len(d),hari_god_median=median(d) if d else "",
                    **{k:median(r[k] for r in grup) for k in ("saldo","poin","karma","reinkarnasi","landfill_kg","kontribusi_kg","penciptaan_bersih","hari_macet")}))
    tulis("ringkasan.csv",ringkas)


if __name__=="__main__":
    main()
