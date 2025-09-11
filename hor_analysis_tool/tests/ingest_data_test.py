import unittest
import os
import sys
from pathlib import Path

dirname = os.path.dirname(__file__)
joined_paths = os.path.join(dirname, "..")
sys.path.append(joined_paths)


from src.ingest_data import Ingest_Data

class test_ingest_data(unittest.TestCase):
    def set_ingest_object(self):
        self.ingest_data_obj = Ingest_Data()
    

    def test_clear_downloads(self):
        self.set_ingest_object()
        download_dir = self.ingest_data_obj.downloads_path
        self.ingest_data_obj.clear_downloads()
        self.assertEqual(len(os.listdir(download_dir)), 0)
    
    def test_mov_file(self):
        self.set_ingest_object()
        current_dir = self.ingest_data_obj.current_dir
        source_documents_dir = os.path.abspath(os.path.join(current_dir, "..", "source_documents"))
        source_docs_list = os.listdir(source_documents_dir)
        file_str = self.ingest_data_obj.mov_file()
        self.assertIn("HORs.csv", source_docs_list)
        self.assertIn("HORs.csv", file_str)
        file_path = Path(file_str)
        self.assertTrue(file_path.is_file())
    
    

if __name__ == "__main__":
    unittest.main()
    
        