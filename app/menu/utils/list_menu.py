def list_menu(items, title=None, back_label="Kembali"):
    """Tampilkan daftar bernomor, minta user memilih.

    Return:
        index item yang dipilih (mulai dari 0), atau
        None kalau user memilih 0 (kembali/keluar).

    Input yang salah (huruf, nomor di luar range) tidak bikin crash,
    cuma diminta ulang.
    """
    if isinstance(items, dict):
        items = list(items.keys())

    while True:
        if title:
            print(title)
        for i, item in enumerate(items, start=1):
            print(f"{i}. {item}")
        print(f"0. {back_label}")

        raw = input("Pilih nomor: ").strip()
        if raw.isdigit():
            number = int(raw)
            if number == 0:
                return None
            if 1 <= number <= len(items):
                return number - 1
        print("Pilihan tidak valid, coba lagi.\n")


def ask_text(prompt, allow_empty=False):
    """Minta input teks. Kalau allow_empty=False, diulang sampai tidak kosong."""
    while True:
        value = input(f"{prompt}: ").strip()
        if value or allow_empty:
            return value
        print("Tidak boleh kosong.")
