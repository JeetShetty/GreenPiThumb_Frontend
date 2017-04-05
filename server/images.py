import datetime
import os

import pytz

# Format of GreenPiThumb image files.
_FILENAME_FORMAT = '%Y-%m-%dT%H%MZ.jpg'


def _files_in_directory(directory):
    paths = os.listdir(directory)
    return [f for f in paths if os.path.isfile(os.path.join(directory, f))]


def _timestamp_from_filename(filename):
    return datetime.datetime.strptime(filename, _FILENAME_FORMAT).replace(
        tzinfo=pytz.utc)


def _filename_to_index_entry(filename):
    return {
        'timestamp': _timestamp_from_filename(filename),
        'filename': filename,
    }


class Indexer(object):
    """Creates an index of GreenPiThumb image files."""

    def __init__(self, images_path):
        """Creates a new Indexer instance.

        Args:
            images_path: Path to the GreenPiThumb images directory.
        """
        self._images_path = images_path

    def index(self):
        """Generates an index of the GreenPiThumb image files.

        Creates an index of all the GreenPiThumb image files in the specified
        images path. If there are non-image files in the directory, these are
        ignored. Any GreenPiThumb image files in subdirectories are also
        ignored.

        Returns:
            A list of dictionaries, one for each GreenPiThumb image file, where
            the dictionary has keys 'timestamp' with the datetime when the file
            was created and 'filename' of the image's filename (without path
            prefix).
        """
        file_index = []
        for filename in _files_in_directory(self._images_path):
            try:
                file_index.append(_filename_to_index_entry(filename))
            except ValueError:
                # Ignore filenames that can't be parsed as GreenPiThumb images.
                pass
        return file_index
