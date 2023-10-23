"""Showcase (Finnish: vitriini) some packaged content - guided by conventions - processor."""
import argparse
import datetime as dti
import logging
import pathlib
import shutil
import zipfile

from vitriini import (
    ENCODING,
    MAX_PACKED_BYTES,
    MAX_UNPACKED_BYTES,
    log,
)

INCOMING = pathlib.Path('incoming')
SAMPLE = 'Example _funnily_nameD - 42'
SAMPLE_PATH = INCOMING / f'{SAMPLE}.zip'
PROCESSING = pathlib.Path('processing')
SLUG = SAMPLE.replace('_', '-').replace(' ', '-').lower()
OUT_ROOT = PROCESSING / SLUG
STAGE = pathlib.Path('staging')


MAGIC_LINE_LIB = '<script src="https://code.createjs.com/1.0.0/createjs.min.js"></script>'
LOCALIZE_LIB_IN = 'https://code.createjs.com/1.0.0/createjs.min.js'
LOCALIZE_LIB_OUT = '/assets/js/createjs.min.js'


def cess(options: argparse.Namespace) -> int:
    """Process the archive and content."""
    verbose = options.verbose
    if verbose:
        logging.getLogger().setLevel(logging.DEBUG)

    archive_path = pathlib.Path(options.archive_path) if options.archive_path else SAMPLE_PATH
    if not archive_path.is_file():
        log.error('No file.')
        return 1

    slug = archive_path.stem.replace('_', '-').replace(' ', '-').lower()
    processing_root = PROCESSING / slug
    today_folder_name = dti.datetime.today().strftime('%Y%m%d')
    log.info(f'Date folder name will be {today_folder_name}')

    size_packed = archive_path.stat().st_size
    if size_packed > MAX_PACKED_BYTES:
        log.error('Archive too large')
        return 1

    log.info(f'{archive_path} -> {processing_root}/ if size[bytes] {size_packed} <= {MAX_PACKED_BYTES}')

    size_unpacked = 0
    try:
        with zipfile.ZipFile(archive_path, mode='r') as archive:
            zip_info = archive.infolist()
    except zipfile.BadZipFile as err:
        log.error(f'Incoming file is corrupt or has wrong type: {err}')
        return 1

    log.info(f'Information on {len(zip_info)} entries in zip archive info list:')
    for slot, info in enumerate(zip_info, start=1):
        log.info(f'- slot {slot}:')
        log.info(f'  + Filename: {info.filename}')
        log.info(f'  + Modified: {dti.datetime(*info.date_time)}')
        log.info(f'  + Normal size: {info.file_size} bytes')
        log.info(f'  + Compressed size: {info.compress_size} bytes')
        size_unpacked += info.file_size

    log.info(f'{archive_path} -> {processing_root}/ if size[bytes] unpacked {size_unpacked} <= {MAX_UNPACKED_BYTES}')

    if size_unpacked > MAX_UNPACKED_BYTES:
        log.error('Zip bomb?')
        return 1

    log.info(f'Compression factor is {round(size_unpacked / size_packed, 3) :5.3f} = {size_unpacked} / {size_packed}')

    shutil.unpack_archive(archive_path, processing_root)

    top_level_folders = [path for path in processing_root.iterdir() if path.is_dir() and path.name == 'images']
    if not top_level_folders or len(top_level_folders) != 1:
        log.error('No top level folder with name images found or too many folders.')
        return 1
    log.info(
        f'Found: top level folder {tuple(e.name for e in top_level_folders)} SHALL contain an images folder (SUCC)'
    )

    images_has_folders = [path for path in top_level_folders[0].iterdir() if path.is_dir()]
    if images_has_folders:
        log.error('Images folder contains folders but shall not.')
        return 1
    log.info('Images folder SHALL NOT contain any folders (SUCC)')

    image_files = [path for path in top_level_folders[0].iterdir() if path.is_file()]
    if not image_files:
        log.error('Images folder contains no files but shall contain.')
        return 1
    log.info('Images folder SHALL contain files (SUCC)')

    for path in image_files:
        if path.suffix.lower() not in ('.gif', '.jpg', '.jpeg', '.png', '.svg', '.webp'):
            log.warning(f'{path.name} has unexpected suffix')

    top_level_files = [path for path in processing_root.iterdir() if path.is_file() and path.suffix in ('.js', '.html')]
    if not top_level_files:
        log.error('No top level files found.')
        return 1

    html_files = [path for path in top_level_files if path.is_file() and path.suffix == '.html']
    js_files = [path for path in top_level_files if path.is_file() and path.suffix == '.js']
    log.info(
        f'Found: top level files {tuple(e.name for e in top_level_files)} SHALL contain a html'
        f' ({"SUCC" if len(html_files) == 1 else "FAIL"})'
        f' and a js ({"SUCC" if len(js_files) == 1 else "FAIL"}) file'
    )
    if any((len(c) != 1 for c in (html_files, js_files))):
        log.error('Too few or too many JS and HTML files on top-level.')
        return 1

    html_lines = [line.strip() for line in html_files[0].open().readlines()]
    log.info(f'Html file has {len(html_lines)} lines - SHALL have 2 special lines in it (pending).')

    if not any(MAGIC_LINE_LIB in line for line in html_lines):
        log.error('Did not find the library import line inside the html file.')
        return 1

    consistent_reference = f'<script src="{js_files[0].name}?'
    if not any(consistent_reference in line.lower() for line in html_lines):
        log.error('Did not find the library import line inside the html file.')
        return 1

    for slot, line in enumerate(html_lines):
        if MAGIC_LINE_LIB in line:
            html_lines[slot] = line.replace(LOCALIZE_LIB_IN, LOCALIZE_LIB_OUT)
            log.info(f'Did replace ({LOCALIZE_LIB_IN}) with ({LOCALIZE_LIB_OUT}) in slot {slot}')
            old = html_lines[slot + 1]
            html_lines[slot + 1] = html_lines[slot + 1].lower()  # She said sorry and my name is Rosi
            log.info(f'Did lowercase ({old}) into ({html_lines[slot + 1]}) in slot {slot + 1}')

    local_out_root = STAGE / today_folder_name / slug
    try:
        local_out_root.mkdir(parents=True, exist_ok=False)
    except FileExistsError:
        log.error('Staging folder is already there')
        return 1
    log.info(f'Created staging folder {local_out_root}')

    local_out_images_root = local_out_root / 'images'
    try:
        local_out_images_root.mkdir(parents=True, exist_ok=False)
    except FileExistsError:
        log.error('Images folder is already there')
        return 1
    log.info(f'Created images folder {local_out_images_root}')

    with open(local_out_root / 'index.html', 'wt', encoding=ENCODING) as handle:
        handle.write('\n'.join(html_lines))
        handle.write('\n')
    log.info('Created index file in the staging folder')

    shutil.copy(js_files[0], local_out_root / js_files[0].name)
    log.info(f'Copied js file {js_files[0].name} to the staging folder')

    for path in image_files:
        shutil.copy(path, local_out_images_root / path.name)
        log.info(f'Copied js file {path.name} to the images folder')

    log.info('OK - Looks good for now (prototype)')

    return 0
