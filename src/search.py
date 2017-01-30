import os

from fnmatch import fnmatchcase


def search(extensions, exclude, base_path):

    fix_extensions(extensions)
    files = {extension: list() for extension in extensions}

    def scan_directory(path):
        for item in os.listdir(path):
            itempath = os.path.join(path, item)

            if os.path.isfile(itempath):
                ext = get_ext_or_none(itempath)
                if ext:
                    files[ext].append(itempath)
            else:
                scan_directory(itempath)

    def get_ext_or_none(filepath):
        _, extension = os.path.splitext(filepath)
        exclude_match = [fnmatchcase(filepath, pattern) for pattern in exclude]
        if extension not in extensions or any(exclude_match):
            return None
        return extension

    scan_directory(base_path)
    return files


def fix_extensions(extensions):
    for i, ext in enumerate(extensions):
        if not ext.startswith('.'):
            extensions[i] = '.' + ext
