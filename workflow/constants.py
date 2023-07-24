import re
def get_trailing_number(s):
    m = re.search(r'\d+$', s)
    return int(m.group()) if m else None

GTIFF_creation_options = {
    'TILES': 'YES',
    'COMPRESS': 'ZSTD',
    'PREDICTOR': '2',
    'BIGTIFF': 'IF_SAFER',
    'NUM_THREADS': 'ALL_CPUS'
}

GTIFF_write_options = {
    'NUM_THREADS': 'ALL_CPUS'
    #USE_OPENCL: 'TRUE'
}

GTIFF_creation_options_str = ' '.join([f'-co "{key}={value}"' for key, value in GTIFF_creation_options.items()])
GTIFF_write_options_str = ' '.join([f'-wo "{key}={value}"' for key, value in GTIFF_creation_options.items()])
