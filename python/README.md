# Demo Python Scripts for CATCH API v3.0

## Introduction

Demonstration scripts for interacting with the CATCH API using Python.

## catch-moving-minimal.py

Near-minimal script to search for comet 65P and display the results.

### Dependencies

- Python 3.8+
- requests
- sseclient

Requirements may be installed, e.g.,

```bash
pip install requests sseclient
```

### Usage

```bash
python3 catch-moving-minimal.py
```

The result is JSON-formatted data. Example output:

```json
{"count": 5, "data": [{"airmass": 1.055449, "archive_url": "https://sbnsurveys.astro.umd.edu/api/images/urn%3Anasa%3Apds%3Agbo.ast.neat.survey%3Adata_tricam%3Ap20020121_obsdata_20020121132624c", "cutout_url": "https://sbnsurveys.astro.umd.edu/api/images/urn%3Anasa%3Apds%3Agbo.ast.neat.survey%3Adata_tricam%3Ap20020121_obsdata_20020121132624c?format=fits&size=5.00arcmin&ra=177.51011&dec=15.25013", "date": "2002-01-21 13:26:54.000", "ddec": 9.813682, "dec": 15.25013, "delta": 2.83330835056674, "dra": -2.64437, "drh": -5.0789549, "elong": 128.5424, "exposure": 60.0, "filter": "NONE", "maglimit": null, "mjd_start": 52295.56, "mjd_stop": 52295.560694444444, "phase": 12.5942, "preview_url": "https://sbnsurveys.astro.umd.edu/api/images/urn%3Anasa%3Apds%3Agbo.ast.neat.survey%3Adata_tricam%3Ap20020121_obsdata_20020121132624c?format=jpeg&size=5.00arcmin&ra=177.51011&dec=15.25013", "product_id": "P20020121_OBSDATA_20020121132624C", "ra": 177.51011, "rh": 3.531535016403, "sangle": 103.483, "seeing": null, "source": "neat_palomar_tricam", "source_name": "NEAT Palomar Tricam", "true_anomaly": 254.1847, "unc_a": 4.967, "unc_b": 0.359, "unc_theta": -25.651, "vangle": 116.10500000000002, "vmag": 17.356},
...
], "job_id": "f636420f7f6849a2af19343597f8ef0d", "version": "3.0.0"}
```

## catch-fixed-minimal.py

Minimal script to search for M15 and display the results.

### Dependencies

- Python 3.8+
- requests

Requirements may be installed, e.g.,

```bash
pip install requests
```

### Usage

```bash
python3 catch-fixed-minimal.py
```

The result is JSON-formatted data. Example output:

```json
{"count": 15, "data": [{"airmass": 1.145962, "archive_url": "https://sbnsurveys.astro.umd.edu/api/images/urn%3Anasa%3Apds%3Agbo.ast.neat.survey%3Adata_tricam%3Ap20020729_obsdata_20020729061513a", "cutout_url": "https://sbnsurveys.astro.umd.edu/api/images/urn%3Anasa%3Apds%3Agbo.ast.neat.survey%3Adata_tricam%3Ap20020729_obsdata_20020729061513a?format=fits&size=5.00arcmin&ra=322.4916666666667&dec=12.166944444444443", "exposure": 60.0, "filter": "NONE", "maglimit": null, "mjd_start": 52484.260567129626, "mjd_stop": 52484.26126157407, "preview_url": "https://sbnsurveys.astro.umd.edu/api/images/urn%3Anasa%3Apds%3Agbo.ast.neat.survey%3Adata_tricam%3Ap20020729_obsdata_20020729061513a?format=jpeg&size=5.00arcmin&ra=322.4916666666667&dec=12.166944444444443", "product_id": "P20020729_OBSDATA_20020729061513A", "seeing": null, "source": "neat_palomar_tricam", "source_name": "NEAT Palomar Tricam"}, {"airmass": 1.147728, "archive_url": "https://sbnsurveys.astro.umd.edu/api/images/urn%3Anasa%3Apds%3Agbo.ast.neat.survey%3Adata_tricam%3Ap20020729_obsdata_20020729063040a", "cutout_url": "https://sbnsurveys.astro.umd.edu/api/images/urn%3Anasa%3Apds%3Agbo.ast.neat.survey%3Adata_tricam%3Ap20020729_obsdata_20020729063040a?format=fits&size=5.00arcmin&ra=322.4916666666667&dec=12.166944444444443", "exposure": 60.0, "filter": "NONE", "maglimit": null, "mjd_start": 52484.2712962963, "mjd_stop": 52484.27199074074, "preview_url": "https://sbnsurveys.astro.umd.edu/api/images/urn%3Anasa%3Apds%3Agbo.ast.neat.survey%3Adata_tricam%3Ap20020729_obsdata_20020729063040a?format=jpeg&size=5.00arcmin&ra=322.4916666666667&dec=12.166944444444443", "product_id": "P20020729_OBSDATA_20020729063040A", "seeing": null, "source": "neat_palomar_tricam", "source_name": "NEAT Palomar Tricam"},
...
], "message": "", "query": {"dec": 12.166944444444443, "intersection_type": "ImageIntersectsArea", "ra": 322.4916666666667, "radius": 0, "sources": ["neat_palomar_tricam"], "start_date": null, "stop_date": null}, "version": "3.0.0"}
```

## catch.py

A fully-featured script for interacting with the CATCH APIs. This script can execute new searches, retrieve results from a prior search, retrieve column metadata for the results, and inspect the CATCH event stream (for debugging purposes).

### Dependencies

- Python 3.8+
- requests
- sseclient (optional for tabular output)
- astropy (optional for moving target queries)

Dependencies may be installed, e.g.,

```bash
pip install requests
```

Optionally install astropy and/or sseclient:

```bash
pip install astropy
pip install sseclient
```

### Usage

See the script help and available commands:

```bash
$ python3 catch.py --help
usage: catch.py [-h] [--base BASE]
                {sources,catch,caught,fixed,status/job_id,status/sources,stream} ...

options:
  -h, --help            show this help message and exit
  --base BASE           base URL for query, e.g., https://catch-api.astro.umd.edu

API routes:
  {sources,catch,caught,fixed,status/job_id,status/sources,stream}
    sources             show allowed sources
    catch               search for a moving target
    caught              retrieve caught object data
    fixed               retrieve caught object data
    status/job_id       retrieve job status
    status/sources      retrieve source database summary
    stream              inspect CATCH event stream
```

Get help on catch sub-command:

```bash
python3 catch.py catch --help
```

Execute a new query for comet 65P, do not return cached results:

```bash
python3 catch.py catch 65P --force
```

Repeat the last search, but allow cached data, if available:

```bash
python3 catch.py catch 65P
```

Search for a fixed target:

```bash
python3 catch.py fixed 21:29:58 +12:10:01
```
