import concurrent.futures # konkurensi
from os.path import dirname, join, abspath # untuk direktori berkas
import json # membuka, menutup dan menulis berkas json



def jalur_berkas(nomor: int, inisial=True) -> str:
    jlr = dirname(abspath(__file__))
    if inisial:
        return join(jlr, "alquran/{}.json".format(nomor))
    else:
        return join(jlr, "juz_alquran/{}.json".format(nomor))

# klasifikasi berdasarkan surah
def quran(urutan):
    with open(jalur_berkas(urutan)) as berkas:
        return json.load(berkas)

class Surah:
    def __init__(self, urutan):
        muat = quran(urutan)
        self.data: tuple = muat['nomor'], muat['nama'], muat['namaLatin'], muat['jumlahAyat'], muat['tempatTurun'], muat['arti']
        self.ayat: str = muat['ayat']


# klasifikasi berdasarkan juz
def quranJuz(urutan):
    with open(jalur_berkas(urutan, False)) as berkas:
        return json.load(berkas)

def daftar(kunci: str, nomor: int) -> list[str]:
    # simpan data berdasarkan kunci dan nomor
    tampung_data = []
    for k, v in quranJuz(nomor).items():
        for cc in range(v[0], v[1]):
            tampung_data.append(Surah(k).ayat[str(cc)][kunci])
    return tampung_data

class Juz:
    def __init__(self, urutan: int):
        with concurrent.futures.ProcessPoolExecutor() as executor:
            future1 = executor.submit(daftar, "teksArab", urutan)
            future2 = executor.submit(daftar, "teksLatin", urutan)
            future3 = executor.submit(daftar, "teksIndonesia", urutan)

            data_arab = list(future1.result())
            data_latin = list(future2.result())
            data_indo = list(future3.result())

        # # simpan data
        datajuz = {}
        for ui in range(len(data_arab)):
            datajuz[ui] = ui, data_arab[ui], data_latin[ui], data_indo[ui]
        
        self.data: dict[str, tuple] = datajuz

