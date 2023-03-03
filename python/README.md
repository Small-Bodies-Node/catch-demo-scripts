# Demo Python Scripts for CATCH API v2.0

## Introduction

Demonstration scripts for interacting with the CATCH API using Python.

## catch-minimal.py

Near-minimal script to search for comet 65P and display the results.

### Requires

* Python 3.5+
* requests
* sseclient

Requirements may be installed, e.g.,

```bash
pip install requests sseclient
```

### Usage

```bash
python3 catch-minimal.py
```

The result is JSON-formatted data.  Example output:

```json
{"count": 15, "data": [{"airmass": 1.055449, "archive_url": "https://catch.astro.umd.edu/catch-images/archive/neat/tricam/data/p20020121/obsdata/20020121132624c.fits", "cutout_url": "https://catch.astro.umd.edu/catch-images/cutouts/65P_P20020121_OBSDATA_20020121132624C_ra177.51011_dec+15.25013_5arcmin.fits", "ddec": 9.813682, "dec": 15.25013, "delta": 2.83330835061683, "designation": "65P", "dra": -2.64437, "exposure": 60.0, "filter": "NONE", "instrument": "NEAT PALOMAR TRI-CAMERA", "jd": 2452296.06034722, "phase": 12.5942, "preview_url": "https://catch.astro.umd.edu/catch-images/thumbnails/65P_P20020121_OBSDATA_20020121132624C_ra177.51011_dec+15.25013_5arcmin.jpg", "productid": "P20020121_OBSDATA_20020121132624C", "ra": 177.51011, "rdot": -5.0789549, "rh": 3.531535016579, "sangle": 103.483, "selong": 128.5424, "source": "neat_palomar", "thumbnail_url": "https://catch.astro.umd.edu/catch-images/thumbnails/65P_P20020121_OBSDATA_20020121132624C_ra177.51011_dec+15.25013_5arcmin_thumb.jpg", "tmtp": -475.346708036959, "trueanomaly": 254.187062889922, "unc_a": 4.967, "unc_b": 0.359, "unc_theta": 115.651, "vangle": 116.105, "vmag": 17.382},
...
], "job_id": "2837a35c11d640e1a81e3381dbecb024"}
```

## catch-demo.py

A fully-featured script for interacting with the CATCH APIs.  This script can execute new searches, retrieve results from a prior search, retrieve column metadata for the results, and inspect the CATCH event stream (for debugging purposes).

### Requires

* Python 3.5+
* requests
* sseclient
* astropy

Requirements may be installed, e.g.,

```bash
pip install requests sseclient
```

Optionally install astropy for creating tables.

```bash
pip install astropy
```

### Usage

See the script help and available commands:

```bash
$ python3 catch-demo.py --help
usage: catch-demo.py [-h] [--base BASE] {sources,catch,caught,status/job_id,status/sources,stream} ...

optional arguments:
  -h, --help            show this help message and exit
  --base BASE           base URL for query, e.g., https://host/location

API routes:
  {sources,catch,caught,status/job_id,status/sources,stream}
    sources             show allowed sources
    catch               search for a moving target
    caught              retrieve caught object data
    status/job_id       retrieve job status
    status/sources      retrieve source database summary
    stream              inspect CATCH event stream
```

Get help on catch sub-command:

```bash
python3 catch-demo.py catch --help
```

Execute a new query for comet 65P, do not return cached results:

```bash
python3 catch-demo.py catch 65P --force
```

Repeat the last search, but allow cached data, if available.  Print the data using the JSON format:

```bash
python3 catch-demo.py catch 65P --format=json
```
