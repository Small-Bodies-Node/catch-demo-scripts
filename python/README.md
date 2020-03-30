# Demo Python Scripts for CATCH API

## Introduction
Demonstration scripts for interacting with the CATCH APIs using Python.

## catch-minimal.py

Near-minimal script to search for comet 65P and display the results.

### Requires
  * Python 3.5+
  * requests
  * sseclient

Requirements may be installed, e.g.,
```
pip install requests sseclient
```

### Usage
```
python3 catch-minimal.py
```

The result is JSON-formatted data.  Example output:
```
{'count': 14, 'data': [{'airmass': 1.038482, 'archive_url': 'https://musforti.astro.umd.edu/catch-images/xxx/neat/tricam/data/p20020222/obsdata/20020222120052c.fits', 'cutout_url': 'https://musforti.astro.umd.edu/catch-images/yyy/65P_P20020222_OBSDATA_20020222120052C_ra174.62244_dec+17.97594_5arcmin.fits', 'ddec': 13.76413, 'dec': 17.97594, 'delta': 2.49069893970196, 'designation': '65P', 'dra': -23.1946, 'exposure': 60.0, 'filter': 'NONE', 'instrument': 'NEAT PALOMAR TRI-CAMERA', 'jd': 2452328.00094907, 'phase': 5.6655, 'productid': 'P20020222_OBSDATA_20020222120052C', 'ra': 174.62244, 'rdot': -5.1794841, 'rh': 3.436865451122, 'sangle': 69.623, 'selong': 159.9563, 'thumbnail_url': 'https://musforti.astro.umd.edu/catch-images/zzz/65P_P20020222_OBSDATA_20020222120052C_ra174.62244_dec+17.97594_5arcmin_thumb.jpg', 'tmtp': -443.404247950763, 'trueanomaly': 258.84013063711, 'unc_a': 5.65, 'unc_b': 0.393, 'unc_theta': -24.108, 'vangle': 114.761, 'vmag': 17.0},
...
}], 'job_id': '53bb8e290e814bccbc242cd5f8a33b9d'}
```

## catch-demo.py

A fully-featured script for interacting with the CATCH APIs.  This script can execute new searches, retrieve results from a prior search, retrieve column metadata for the results, and inspect the CATCH event stream (for debugging purposes).

### Requires
  * Python 3.5+
  * requests
  * sseclient
  * astropy

Requirements may be installed, e.g.,
```
pip install astropy requests sseclient
```

### Usage
See the script help and available commands:
```
$ python3 catch-demo.py --help
usage: catch-demo.py [-h] [--base BASE]
                     {caught,caught/labels,query/moving,stream} ...

optional arguments:
  -h, --help            show this help message and exit
  --base BASE           base URL for query, e.g., https://host/location

API routes:
  {caught,caught/labels,query/moving,stream}
    caught              retrieve caught object data
    caught/labels       retrieve descriptions for caught field/columns
    query/moving        search for a target
    stream              inspect CATCH event stream
```

Execute a new query for comet 65P, do not return cached results:
```
python3 catch-demo.py query/moving 65P --force
```

Repeat the last search, but allow cached data, if available.  Print the data using the JSON format:
```
python3 catch-demo.py query/moving 65P --format=json
```

Get descriptions of the columns/fields (including units):
```
python3 catch-demo.py caught/labels
```
