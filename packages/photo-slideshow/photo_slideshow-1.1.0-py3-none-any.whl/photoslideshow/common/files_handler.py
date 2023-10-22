from pathlib import Path, PureWindowsPath


def scan_folder(path, patterns):
    """
    Scan given folder for photos
    :param path:
    :param patterns:
    :return:
    """
    folder = Path(path)
    files = []
    for f in folder.iterdir():
        # PureWindowsPath matches with case insensitivity
        if any(PureWindowsPath(f).match(p) for p in patterns):
            files.append(f.absolute())
        if f.is_dir() and not f.name.startswith('.'):  # ignore folders starting with ".*"
            files.extend(scan_folder(f.absolute(), patterns))
    return files


def save_config(config):
    config_file = config.get('path', 'userconfig')
    with open(config_file, 'w') as conf:
        config.write(conf)
