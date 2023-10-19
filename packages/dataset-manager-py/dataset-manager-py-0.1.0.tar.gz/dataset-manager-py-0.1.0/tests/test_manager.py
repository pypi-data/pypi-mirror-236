# Import standard libraries
import os
import tempfile
import unittest

# Import project code
from dataset.manager import DatasetManager


class TestDatasetManager(unittest.TestCase):
    def setUp(self):
        self.loader = DatasetManager()
        self.temp_dir = tempfile.TemporaryDirectory()


    def tearDown(self):
        self.temp_dir.cleanup()


    def test_load_from_hub(self):
        dataset = self.loader.load_from_hub("imdb")
        self.assertIsNotNone(dataset)
        self.assertIsNotNone(self.loader.dataset)


    def test_load_from_disk(self):
        self.loader.load_from_hub("imdb")
        path = os.path.join(self.temp_dir.name, "imdb")
        self.loader.save_to_disk(path)
        self.loader.dataset = None
        loaded_dataset = self.loader.load_from_disk(path)
        self.assertIsNotNone(loaded_dataset)
        self.assertIsNotNone(self.loader.dataset)


    def test_save_to_disk(self):
        self.loader.load_from_hub("imdb")
        path = os.path.join(self.temp_dir.name, "imdb")
        self.loader.save_to_disk(path)
        self.assertTrue(os.path.exists(path))


    def test_archive_dataset(self):
        self.loader.load_from_hub("imdb")
        path = os.path.join(self.temp_dir.name, "imdb")
        self.loader.save_to_disk(path)
        archive_path = os.path.join(self.temp_dir.name, "imdb_archive")
        self.loader.archive_dataset(path, archive_path)
        self.assertTrue(os.path.exists(f"{archive_path}.zip"))


    def test_invalid_archive_format(self):
        with self.assertRaises(ValueError):
            self.loader.archive_dataset("", "", "invalid_format")


    def test_save_without_dataset(self):
        with self.assertRaises(ValueError):
            self.loader.save_to_disk("path")

if __name__ == "__main__":
    unittest.main()
