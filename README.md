# learning_environment

Aplikasi CLI kecil buat ngatur belajar: simpan link tutorial, dokumentasi, folder project,
dan catatan "terakhir belajar sampai mana" per topik.

## Cara jalan

```bash
python run.py          # cara paling gampang
# atau
python -m app.app
```

Jalankan dari **folder root repo** (yang ada `run.py`-nya). Butuh Python 3.8+, tanpa library tambahan.

## Fitur

- Pilih topik belajar (1 file JSON di `app/materials/` = 1 topik)
- Lihat tutorial / dokumentasi (pilih nomor -> kebuka di browser)
- Lihat project (ada pengecekan folder-nya masih ada atau tidak)
- Update progress belajar
- Tambah resource baru langsung dari menu

## Nambah topik baru

Bikin file `app/materials/<nama>.json` dengan format sama seperti `python.json`:

```json
{
    "material": [{"name": "SQL", "start_from": ""}],
    "tutorials": [],
    "docs": [],
    "projects": []
}
```

Otomatis muncul di menu utama.

## Struktur

```
run.py                       entry point
app/app.py                   run(): jalanin menu + tangkap Ctrl+C
app/menu/main.py             semua menu (utama, topik, tutorial, progress, dll)
app/menu/utils/list_menu.py  list_menu() + ask_text() (input aman)
app/service/data_manager.py  baca/tulis JSON
app/materials/*.json         data materi
tests/                       unit test
```

## Tes

```bash
python -m unittest -v
```

## Catatan Python (buat ingetin lagi)

- `import` / `from x import y`: ambil kode dari file lain. Titik di depan (`from ..service import ...`)
  = import relatif, "naik satu folder dari sini". Makanya file ini harus dijalankan dari root
  lewat `run.py`, bukan `python main.py` langsung.
- `if __name__ == "__main__":` = "jalankan bagian ini hanya kalau file ini dieksekusi langsung,
  bukan kalau cuma di-import".
- `with open(...) as f:` = buka file dan otomatis ditutup walau terjadi error.
- `dict` (`{"a": 1}`) = pasangan kunci-nilai, `list` (`[1, 2]`) = urutan item.
  JSON di repo ini isinya dict yang berisi list of dict.
- `f"Halo {nama}"` = f-string, `{...}` diganti nilai variabel.
- `lambda: fungsi(x)` = fungsi mini tanpa nama. Dipakai di `topic_menu` supaya tiap menu
  bisa dipetakan ke aksinya tanpa banyak `if/elif`.
- `try/except` = tangkap error supaya program tidak mati (lihat `app/app.py`).
