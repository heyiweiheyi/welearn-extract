"""Package a prepared directory of course audio and video files."""

import argparse
import os
from pathlib import Path
from tempfile import NamedTemporaryFile
from zipfile import ZipFile


MEDIA_SUFFIXES = {'.m4a', '.mp3', '.wav', '.ogg', '.opus', '.aac', '.flac',
                  '.mp4', '.webm', '.mov', '.mkv', '.m4v'}


def package_media(source: Path, output: Path) -> int:
    source = source.resolve(strict=True)
    output = output.resolve()
    if not source.is_dir() or output.suffix.lower() != '.zip':
        raise ValueError('Provide a media directory and an output path ending in .zip.')

    entries = []
    seen = set()
    for path in sorted(source.rglob('*')):
        if path.suffix.lower() not in MEDIA_SUFFIXES or not path.is_file():
            continue
        if path.is_symlink() or not path.resolve().is_relative_to(source):
            raise ValueError(f'Media entry is a link or points outside the source: {path.name}')
        name = path.relative_to(source).as_posix()
        if name.casefold() in seen or path.stat().st_size == 0:
            raise ValueError(f'Duplicate archive name or empty file: {name}')
        seen.add(name.casefold())
        entries.append((path, name))
    if not entries:
        raise ValueError('No supported audio or video files found.')

    output.parent.mkdir(parents=True, exist_ok=True)
    with NamedTemporaryFile(dir=output.parent, suffix='.zip.part', delete=False) as handle:
        temporary = Path(handle.name)
    try:
        with ZipFile(temporary, 'w') as archive:
            for path, name in entries:
                archive.write(path, name)
        with ZipFile(temporary) as archive:
            if archive.namelist() != [name for _, name in entries] or archive.testzip() is not None:
                raise ValueError('ZIP integrity check failed.')
        os.replace(temporary, output)
    finally:
        temporary.unlink(missing_ok=True)
    return len(entries)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('source', type=Path, help='Directory containing the selected local media')
    parser.add_argument('output', type=Path, help='ZIP path. An existing ZIP is replaced after validation.')
    args = parser.parse_args()
    try:
        count = package_media(args.source, args.output)
    except (OSError, ValueError) as error:
        parser.exit(1, f'{error}\n')
    print(f'Packaged {count} media file(s).')


if __name__ == '__main__':
    main()
