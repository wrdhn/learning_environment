"""Urusan baca/tulis data materi (file JSON di folder app/materials/).

Satu file JSON = satu topik belajar (contoh: python.json).
Mau nambah topik baru? Tinggal bikin file JSON baru di folder materials,
nanti otomatis muncul di menu utama.
"""
import json
import os
from pathlib import Path

# Folder materials, dihitung relatif dari lokasi file ini
# supaya jalan di komputer mana pun (tidak hardcode /home/...).
MATERIALS_DIR = Path(__file__).resolve().parent.parent / "materials"


def _topic_path(topic):
    return MATERIALS_DIR / f"{topic}.json"


def list_topics():
    """Daftar nama topik yang tersedia, mis. ['python']."""
    return sorted(p.stem for p in MATERIALS_DIR.glob("*.json"))


def load_topic(topic):
    """Baca satu topik, hasilnya dict."""
    with open(_topic_path(topic), "r", encoding="utf-8") as f:
        return json.load(f)


def save_topic(topic, data):
    """Simpan dict ke file topik.

    Ditulis ke file sementara dulu, baru ditukar. Jadi kalau program
    mati di tengah jalan, file aslinya tidak rusak/kosong.
    """
    path = _topic_path(topic)
    tmp = path.with_suffix(".json.tmp")
    with open(tmp, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)
    os.replace(tmp, path)


# ---------- helper kecil buat isi data ----------

def get_name(data, fallback):
    """Nama materi (dari data['material'][0]['name']), atau fallback."""
    items = data.get("material") or [{}]
    return items[0].get("name") or fallback


def get_progress(data):
    """Terakhir belajar sampai mana (field 'start_from')."""
    items = data.get("material") or [{}]
    return items[0].get("start_from", "")


def set_progress(data, text):
    """Isi progress. Kalau 'material' belum ada, dibuatkan dulu."""
    if not data.get("material"):
        data["material"] = [{"name": "", "start_from": ""}]
    data["material"][0]["start_from"] = text


def add_item(data, section, entry):
    """Tambah satu item (dict) ke section: 'tutorials', 'docs', atau 'projects'."""
    data.setdefault(section, []).append(entry)
