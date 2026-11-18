import webbrowser
from pathlib import Path

from ..service import data_manager as dm
from .utils.list_menu import list_menu, ask_text

# section di JSON -> (label tampilan, nama field isinya)
SECTIONS = {
    "tutorials": ("Tutorial", "url"),
    "docs": ("Dokumentasi", "url"),
    "projects": ("Project", "path"),
}


def main_menu():
    """Menu paling awal: pilih topik belajar."""
    while True:
        topics = dm.list_topics()
        if not topics:
            print("Belum ada materi. Taruh file .json di folder app/materials/.")
            return

        print("\n===== Learning Environment =====")
        choice = list_menu(topics, back_label="Keluar")
        if choice is None:
            print("Sampai jumpa, semangat belajarnya!")
            return
        topic_menu(topics[choice])


def topic_menu(topic):
    """Menu di dalam satu topik (misal: Python)."""
    actions = {
        "Lihat tutorial": lambda: show_resources(topic, "tutorials"),
        "Lihat dokumentasi": lambda: show_resources(topic, "docs"),
        "Lihat project": lambda: show_resources(topic, "projects"),
        "Update progress belajar": lambda: update_progress(topic),
        "Tambah resource baru": lambda: add_resource(topic),
    }

    while True:
        data = dm.load_topic(topic)  # dibaca ulang tiap loop biar selalu terbaru
        name = dm.get_name(data, topic.title())
        progress = dm.get_progress(data) or "(belum diisi)"

        print(f"\n===== {name} =====")
        print(f"Terakhir sampai: {progress}")
        choice = list_menu(list(actions), back_label="Kembali")
        if choice is None:
            return
        list(actions.values())[choice]()


def _label(item, field):
    """Teks satu baris untuk ditampilkan di daftar."""
    value = item.get(field, "-")
    if field == "path":
        status = "ada" if Path(value).expanduser().exists() else "folder tidak ditemukan"
        return f"{item.get('name', '?')} -> {value} [{status}]"
    return f"{item.get('name', '?')} -> {value}"


def show_resources(topic, section):
    """Tampilkan daftar tutorial/docs/project. Link bisa langsung dibuka."""
    label, field = SECTIONS[section]
    data = dm.load_topic(topic)
    items = data.get(section, [])
    if not items:
        print(f"\nBelum ada {label.lower()}. Tambah lewat menu 'Tambah resource baru'.")
        return

    title = f"\n--- {label} ---"
    if field == "url":
        title += " (pilih nomor untuk buka di browser)"

    while True:
        choice = list_menu([_label(it, field) for it in items], title=title)
        if choice is None:
            return
        if field == "url":
            url = items[choice]["url"]
            print(f"Membuka: {url}")
            webbrowser.open(url)  # kalau tidak ada browser, link di atas bisa di-copy manual


def update_progress(topic):
    data = dm.load_topic(topic)
    current = dm.get_progress(data) or "(belum diisi)"
    print(f"\nProgress sekarang: {current}")
    text = ask_text("Sekarang sampai mana? (Enter = batal)", allow_empty=True)
    if not text:
        print("Dibatalkan.")
        return
    dm.set_progress(data, text)
    dm.save_topic(topic, data)
    print("Progress disimpan.")


def add_resource(topic):
    sections = list(SECTIONS)
    labels = [SECTIONS[s][0] for s in sections]
    choice = list_menu(labels, title="\nMau tambah apa?", back_label="Batal")
    if choice is None:
        return

    section = sections[choice]
    label, field = SECTIONS[section]
    name = ask_text(f"Nama {label.lower()}")
    value = ask_text("URL" if field == "url" else "Path folder")

    data = dm.load_topic(topic)
    dm.add_item(data, section, {"name": name, field: value})
    dm.save_topic(topic, data)
    print(f"{label} '{name}' ditambahkan.")
