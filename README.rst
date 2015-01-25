This is a `Python <http://python.org>`_ based utility for geocoding csv files
using various online geocoding service.

*************
Installation
*************

Download the source code

::

    git clone https://github.com/WorldBank-Transport/giokoda.git

Install the module and its dependancies

::

    cd giokoda
    python setup.py install


******
Usage
******

This utility can be used as a Python module or as a python script.

Using the python module
=======================

Basic example::

    from giokoda.utils import geocode_csv
    geocode_csv('input.csv')

The above code will try to goecode the provided `'input.csv'` file and write
its output to `'input.csv-geocoded.csv'`

A `geocode_csv` function can geocode entities from a provided input csv file
and write results to a csv file.

It also returns a dictionary containing error, success and total count of
geocoded rows.

General syntax::

    geocode_csv('input/file.csv', **kwargs)

Required parameter
------------------

    `infile`, *(filepath/str)*
        path to a csv file to geocode.

Optional keyword arguments (`**kwargs`)
---------------------------------------
    `outfile`, (filepath/str)
        path to file to write output csv
    
    `service`, *(str)*, default: `'nominatim'`.
        Name of a geocoding service to use. This can be a name of any geocoding
        service that is supported by
        `geopy <http://geopy.readthedocs.org/en/latest/>`_.

    `query_column`, *(str)*, default: `'name'`
        Name of a column containg text to geocode.

    `service_kwargs`, *(dict)*
        Optional keyword arguments for initialization of geocoding service.

Return
------

`geocode_csv()` returns a dictionary of success, error and total count::
  
    {
        'total': 0,
        'success': 0,
        'error': 0
    }

Using the script
================

* Go to the directory containing the `geocode_csv.py` script.

* Run the script using command line interface.

Example::

    python geocode_csv.py /input/file.csv

or including a api key::

    python geocode_csv.py --service <SERVICE-NAME> --params '{"api_key": "<YOUR-API-KEY>"}' /input/file.csv

General usage::

    geocode_csv.py [-h] [-o OUTPUT] [-s SERVICE] [-c COLUMN] [-p PARAMS] input

Required argument
------------------
    `input`
        Full path to csv file to geocode

`Optional arguments`
---------------------

    `-h, --help`
        show this help message and exit

    `-o OUTPUT, --output OUTPUT`
        Full path to output file

    `-s SERVICE, --service SERVICE`
        Geocoding service name, example arcgis, baidu, google, googlev3, geocoderdotus,
        geonames, yahoo, placefinder, opencage, openmapquest, mapquest, liveaddress,
        navidata, nominatim, geocodefarm, what3words, yandex and ignfrance

    `-c COLUMN, --column COLUMN`
        Name of a column containing strings to geocode

    `-p PARAMS, --params PARAMS`
        Keyword arguments for geocoding service initialization presented as
        json object
