"""Contoh numerik terisolasi untuk usulan aturan. Jalankan setelah simulasi.py."""
from simulasi import HASIL, K, tulis
from statistics import median, quantiles
import csv


def segmen(lalu, kini, batas):
    awal = max(lalu, kini-K["cap_jam"])
    titik = sorted({awal, kini, *(b for b in batas if awal<b<kini)})
    return list(zip(titik,titik[1:]))


def uji_musim_dan_pemulihan():
    # Dua musim, 90 hari per musim. Hak kredit tiap hari terbatas pada gram
    # kontrak asal; sisa yang belum tertangani tetap menjadi kewajiban musim.
    tabel = []
    poin = kas = 0
    for musim in (1, 2):
        target = sah = landfill = 0
        for hari in range(1, 91):
            terbit = 1000 if musim==1 or hari<=45 else 500
            target += terbit
            material = terbit*9//10
            residu = terbit-material
            landfill += residu
            bagian_terkendali = residu if musim==1 else residu//2
            sah += material+bagian_terkendali
            poin += material
            kas += 2*material
            assert sah<=target and landfill<=target//10
        tabel.append(dict(musim=musim,target_g=target,layak_g=sah,
            landfill_g=landfill,zwm=100*sah/target,upacara=sah==target,
            poin_lintas_musim=poin,kas_lintas_musim=kas))
    assert tabel[0]["upacara"] and not tabel[1]["upacara"]
    assert tabel[1]["poin_lintas_musim"]>tabel[0]["poin_lintas_musim"]
    tulis("rollover.csv",tabel)
    # Jasa pilah memberi pembiayaan terikat pada batch, tanpa hibah cair.
    # Sekali per hari; hanya ketika dana bebas tak cukup untuk batch minimum.
    for kas_awal in (0,319,399,400,10000):
        kekurangan = max(0,400-kas_awal)
        voucher = kekurangan
        saldo = kas_awal
        if saldo+voucher>=400:
            saldo -= 400-voucher
            voucher = 0
        assert saldo==max(0,kas_awal-400) and voucher==0
    # Bila pasar belum buka, voucher tidak menjamin penjualan. Kontrak jasa
    # pemulihan wajib menyediakan pembeli terikat atau ongkos atas kerja sah.


def cek():
    uji_musim_dan_pemulihan()
    assert segmen(0,26,[24])==[(18,24),(24,26)]
    assert segmen(26,26,[24])==[]
    assert segmen(0,100,[24])==[(92,100)]
    # Paket massa abstrak dalam gram, mencakup massa pembantu eksternal.
    resep = [
        ("pilah",[10000],[5000,1800,1000,700,1400,100]),
        ("kompos",[1000,100],[450,50,600]), # produk, residu, air/gas
        ("plastik",[1000,200],[765,135,300]), # produk bersih, reject, efluen
        ("kertas_logam",[1000],[830,100,70]),
        ("termal",[1000,1800],[180,2620]), # abu, gas bruto
        ("scrubber",[2620,200],[2700,120]), # gas lewat, lumpur
        ("alga",[120,100,10],[55,50,125]), # biomassa, gas, cairan
        ("stabilisasi",[180,120,60],[330,30]), # abu dan lumpur + aditif
        ("B3_serah",[100],[100])]
    for _,masuk,keluar in resep:
        assert sum(masuk)==sum(keluar)
    # Fiksasi sebagian gas saja. Sisa 2580 g keluar melewati kendali.
    assert 1000+1800+200+100+10+60==2580+55+50+125+330+30
    # God pada laju 5800 poin/hari. Uji pemain sengaja reset sebelum berpindah jalur.
    hasil=[]
    for reset in range(4):
        for hari_reset in (1,4,10):
            for bonus in (0,.1):
                import math
                durasi=reset*hari_reset+math.ceil(400000/min(6100,5800*(1+bonus*reset)))
                hasil.append(dict(reset=reset,hari_per_reset=hari_reset,bonus=bonus,hari_god=durasi))
    tulis("insentif_reset.csv",hasil)
    with (HASIL/"pemain.csv").open() as f:
        rows=list(csv.DictReader(f))
    tabel=[]
    for sk in ("bersama","kalibrasi","baru"):
        for t in range(1,10):
            grup=[r for r in rows if r["skenario"]==sk]
            xs=[int(r[f"tier_{t}"]) for r in grup if r[f"tier_{t}"]]
            q=quantiles(xs,n=10) if len(xs)>1 else None
            tabel.append(dict(skenario=sk,tier=t,n=len(grup),mencapai=len(xs),p10=round(q[0],1) if q else "",p50=median(xs) if xs else "",p90=round(q[-1],1) if q else ""))
    tulis("waktu_tier.csv",tabel)
    print("Cap, retry waktu, batas musim/aturan, 9 resep dan neraca gabungan lulus.")


if __name__=="__main__":
    cek()
