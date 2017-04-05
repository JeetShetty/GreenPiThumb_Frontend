import datetime
import os
import shutil
import tempfile
import unittest

import pytz

from server import images


class ImagesTest(unittest.TestCase):

    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()
        self.indexer = images.Indexer(self.temp_dir)

    def tearDown(self):
        shutil.rmtree(self.temp_dir)

    def test_indexes_image_files(self):
        open(os.path.join(self.temp_dir, '2017-04-01T1851Z.jpg'), 'a').close()
        open(os.path.join(self.temp_dir, '2017-04-01T1853Z.jpg'), 'a').close()
        open(os.path.join(self.temp_dir, '2017-04-02T0000Z.jpg'), 'a').close()
        self.assertItemsEqual(
            [
                {
                    'timestamp': datetime.datetime(
                        2017, 4, 1, 18, 51, 0, tzinfo=pytz.utc),
                    'filename': '2017-04-01T1851Z.jpg',
                },
                {
                    'timestamp': datetime.datetime(
                        2017, 4, 1, 18, 53, 0, tzinfo=pytz.utc),
                    'filename': '2017-04-01T1853Z.jpg',
                },
                {
                    'timestamp': datetime.datetime(
                        2017, 4, 2, 0, 0, 0, tzinfo=pytz.utc),
                    'filename': '2017-04-02T0000Z.jpg',
                },
            ],
            self.indexer.index())

    def test_excludes_non_greenpithumb_image_files(self):
        open(os.path.join(self.temp_dir, '2017-04-01T1851Z.jpg'), 'a').close()
        open(os.path.join(self.temp_dir, '2017-04-01T1853Z.txt'), 'a').close()
        open(os.path.join(self.temp_dir, 'dummyfile.jpg'), 'a').close()
        open(
            os.path.join(self.temp_dir, '2017-04-01T1845Z-extrajunk.jpg'),
            'a').close()
        self.assertItemsEqual(
            [{
                'timestamp': datetime.datetime(
                    2017, 4, 1, 18, 51, 0, tzinfo=pytz.utc),
                'filename': '2017-04-01T1851Z.jpg',
            },],
            self.indexer.index())

    def test_excludes_directories(self):
        open(os.path.join(self.temp_dir, '2017-04-01T1851Z.jpg'), 'a').close()
        os.mkdir(os.path.join(self.temp_dir, 'dummydir'))
        # Make a directory named like an image file.
        os.mkdir(os.path.join(self.temp_dir, '2017-04-05T0000Z.jpg'))

        self.assertItemsEqual(
            [{
                'timestamp': datetime.datetime(
                    2017, 4, 1, 18, 51, 0, tzinfo=pytz.utc),
                'filename': '2017-04-01T1851Z.jpg',
            },],
            self.indexer.index())

    def test_excludes_subdirectories(self):
        subdirectory_path = os.path.join(self.temp_dir, 'child_dir')
        os.mkdir(subdirectory_path)
        open(os.path.join(self.temp_dir, '2017-04-01T1851Z.jpg'), 'a').close()
        open(os.path.join(subdirectory_path, '2017-05-08T0000Z.jpg'),
             'a').close()

        self.assertItemsEqual(
            [{
                'timestamp': datetime.datetime(
                    2017, 4, 1, 18, 51, 0, tzinfo=pytz.utc),
                'filename': '2017-04-01T1851Z.jpg',
            },],
            self.indexer.index())
