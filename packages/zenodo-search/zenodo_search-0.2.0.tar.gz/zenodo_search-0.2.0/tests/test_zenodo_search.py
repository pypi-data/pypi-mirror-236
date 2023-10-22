"""Unit tests for h5rdmtoolbox.config"""
import pathlib
import shutil
import unittest

import zenodo_search
import zenodo_search as zsearch

__this_dir__ = pathlib.Path(__file__).parent


class TestZenodoSearch(unittest.TestCase):

    # def test_search_doi_sandbox(self):

    def test_search_doi_sandbox(self):
        r = zsearch.search_doi('8281285', sandbox=True)
        self.assertIsInstance(r, zsearch.ZenodoRecord)
        self.assertEqual('10.5281/zenodo.8281285', r.doi)

        r = zsearch.search('doi:8281285', sandbox=True)
        self.assertIsInstance(r, zsearch.ZenodoRecords)
        self.assertEqual('10.5281/zenodo.8281285', r[0].doi)

    def test_search_doi(self):
        r = zsearch.search_doi('8357399', sandbox=False)
        self.assertIsInstance(r, zsearch.ZenodoRecord)
        self.assertEqual('10.5281/zenodo.8357399', r.doi)

        r = zsearch.search('doi:8357399')
        self.assertIsInstance(r, zsearch.ZenodoRecords)
        self.assertEqual('10.5281/zenodo.8357399', r[0].doi)

    def test_explain_response(self):
        r = zsearch.search('10.5281/zenodo.8220739')
        self.assertEqual('200: OK: Request succeeded. Response included. Usually sent for GET/PUT/PATCH requests.',
                         zenodo_search.explain_response(r.response))
        self.assertEqual('200: OK: Request succeeded. Response included. Usually sent for GET/PUT/PATCH requests.',
                         zenodo_search.explain_response(200))
        with self.assertRaises(TypeError):
            zenodo_search.explain_response('200')
        with self.assertRaises(TypeError):
            zenodo_search.explain_response(200.0)

    def test_download_bucket(self):
        with self.assertRaises(TypeError):
            zenodo_search.download_file(4.5)
        with self.assertRaises(KeyError):
            zenodo_search.download_file({})
        with self.assertRaises(KeyError):
            zenodo_search.download_file({'bucket': 'mybucket'})

        zrecs = zsearch.search('doi:8220739')
        zfile = zrecs[0].files[0]
        self.assertIsInstance(zfile, dict)
        self.assertIsInstance(zrecs[0], zsearch.ZenodoRecord)
        self.assertIsInstance(zfile, zsearch.ZenodoFile)

        filenames = zrecs[0].files.download(destination_dir=None, timeout=10)
        self.assertIsInstance(filenames, list)
        self.assertEqual(len(filenames), 1)
        self.assertIsInstance(filenames[0], pathlib.Path)
        self.assertTrue(filenames[0].exists())
        self.assertTrue(filenames[0].is_file())
        self.assertTrue(filenames[0].name, 'planar_piv.yaml')
        filenames[0].unlink(missing_ok=True)

        filename = zfile.download(destination_dir=None, timeout=10)
        self.assertTrue(filename.exists())
        filename = zfile.download(destination_dir=None, timeout=10)
        self.assertTrue(filename.exists())
        filename.unlink(missing_ok=True)
        self.assertFalse(filename.exists())

        dest_dir = pathlib.Path('mydir')
        file = zfile.download(destination_dir=dest_dir, timeout=10)
        dest_dir.exists()

        self.assertIsInstance(file, pathlib.Path)
        self.assertTrue(file.exists())
        self.assertTrue((dest_dir / 'planar_piv.yaml').exists())

        shutil.rmtree(dest_dir)
        self.assertFalse(dest_dir.exists())

        file = zfile.download(destination_dir=dest_dir, timeout=10)
        self.assertTrue(file.exists())
        self.assertTrue((dest_dir / 'planar_piv.yaml').exists())

        shutil.rmtree(dest_dir)
        self.assertFalse((dest_dir / 'planar_piv.yaml').exists())

    def test_parse_doi(self):
        from zenodo_search import utils
        self.assertEqual('10.5281/zenodo.8220739', utils.parse_doi(8220739))
        self.assertEqual('10.5281/zenodo.8220739', utils.parse_doi('https://zenodo.org/record/8220739'))
        self.assertEqual('10.5281/zenodo.8220739', utils.parse_doi('https://doi.org/10.5281/zenodo.8220739'))

    def test_version(self):
        this_version = 'x.x.x'
        setupcfg_filename = __this_dir__ / '../setup.cfg'
        with open(setupcfg_filename, 'r') as f:
            lines = f.readlines()
            for line in lines:
                if 'version' in line:
                    this_version = line.split(' = ')[-1].strip()
        self.assertEqual(zsearch.__version__, this_version)
