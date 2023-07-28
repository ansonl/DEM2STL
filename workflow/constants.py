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

configuration_keywords = {
    'GDAL_VRT_ENABLE_PYTHON': 'YES'
}

GTIFF_creation_options_str = ' '.join([f'-co "{key}={value}"' for key, value in GTIFF_creation_options.items()])
GTIFF_write_options_str = ' '.join([f'-wo "{key}={value}"' for key, value in GTIFF_creation_options.items()])

# https://gdal.org/programs/raster_common_options.html#cmdoption-config
configuration_keywords_str = ' '.join([f'--config "{key} {value}"' for key, value in configuration_keywords.items()])