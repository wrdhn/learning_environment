import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from app.menu.utils.list_menu import list_menu
from app.service import data_manager as dm


class TestListMenu(unittest.TestCase):
    def test_pilih_valid(self):
        with patch("builtins.input", return_value="2"):
            self.assertEqual(list_menu(["a", "b"]), 1)

    def test_nol_berarti_kembali(self):
        with patch("builtins.input", return_value="0"):
            self.assertIsNone(list_menu(["a", "b"]))

    def test_input_salah_diulang(self):
        with patch("builtins.input", side_effect=["abc", "9", "1"]):
            self.assertEqual(list_menu(["a", "b"]), 0)


class TestDataManager(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        patcher = patch.object(dm, "MATERIALS_DIR", Path(self.tmp.name))
        patcher.start()
        self.addCleanup(patcher.stop)
        self.addCleanup(self.tmp.cleanup)

    def test_simpan_dan_baca(self):
        dm.save_topic("x", {"docs": []})
        self.assertEqual(dm.load_topic("x"), {"docs": []})
        self.assertEqual(dm.list_topics(), ["x"])

    def test_progress_data_kosong(self):
        data = {}
        self.assertEqual(dm.get_progress(data), "")
        dm.set_progress(data, "Bab 3")
        self.assertEqual(dm.get_progress(data), "Bab 3")

    def test_add_item(self):
        data = {}
        dm.add_item(data, "docs", {"name": "A", "url": "u"})
        self.assertEqual(data["docs"][0]["name"], "A")

    def test_save_tidak_menimpa_data_lain(self):
        dm.save_topic("x", {"a": 1})
        data = dm.load_topic("x")
        data["b"] = 2
        dm.save_topic("x", data)
        self.assertEqual(json.loads((Path(self.tmp.name) / "x.json").read_text()), {"a": 1, "b": 2})


if __name__ == "__main__":
    unittest.main()
