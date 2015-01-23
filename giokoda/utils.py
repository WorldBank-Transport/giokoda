import sys
import csv
from pprint import pprint
from geopy import geocoders, get_geocoder_for_service
import settings

GEOCODERS = settings.GEOCODERS
DEFAULT_GEOCODER = settings.DEFAULT_GEOCODER


def geocode_csv(infile, **kwargs):
    """
    Geocode entities from a provided input csv file and write results to an
    output csv file.
    
    Return a dictionary containing error, success and total count of geocoded
    rows.

    **Example:**

    Basic usage::

        >>> from giokoda.utils import geocode_csv
        >>> geocode_csv('input.csv')

    This will will try to goecode the `'input.csv'` file and write output to
    `'input.csv-geocoded.csv'`.

    **Parameters:**

    `infile` *(filepath/str)*: path to a csv file to geocode

    `*kwargs`: Optional and arbitary keyword arguments
      `outfile` (filepath/str): path to file to write output csv

      `service` *(str)*: default: `'nominatim'`. Name of a geocoding service to
      use. This can be a name of any geocoding service accepted by geopy.

      `query_column` *(str)*: default: `'name'`. Name of a column containg text
      to geocode.

      `service_kwargs` *(dict)*: Optional keyword arguments for initialization
      of geocoding service.

    **Returns:**
      A dictionary of total success and error count::
      
        {
            'total': 0,
            'success': 0,
            'error': 0
        }
    """
    # Collect parameters
    outfile = kwargs.get('outfile', '%s-geocoded.csv' %infile)
    service = kwargs.get('service', DEFAULT_GEOCODER)
    query_column = kwargs.get('query_column', 'name')
    service_kwargs = GEOCODERS.get(service, GEOCODERS[DEFAULT_GEOCODER])
    service_kwargs.update(kwargs.get('service_kwargs', {}))
    # Instanciate geocoder service
    api_key = service_kwargs.pop('api_key', None)
    Geocoder = get_geocoder_for_service(service)
    if api_key:
        geocoder = Geocoder(api_key, **service_kwargs)
    else:
        geocoder = Geocoder(**service_kwargs)
    # Read csv 
    incsv = csv.DictReader(open(infile, 'r'))
    # Initialize csv writer
    writer = csv.writer(open(outfile, 'w'))
    # Geocode each row
    first_row = True
    successful = 0
    total = 0
    errors = 0
    for row in incsv:
        sorted_row = {'latitude': '', 'longitude': ''}
        for key,value in sorted(row.items()):
            sorted_row[key] = value
        try:
            query = sorted_row.get(query_column)
            if query:
                location = geocoder.geocode(query)
                if location and location.latitude and location.longitude:
                    sorted_row['latitude'] = location.latitude
                    sorted_row['longitude'] = location.longitude
                    successful += 1
        except Exception as e:
            errors += 1
            sys.stdout.write('\n\033[91m%s\033[0m\n' %e)
            pprint(sorted_row)
        if first_row:
            # write header
            writer.writerow(sorted_row.keys())
            first_row = False
        else:
            total += 1
        # Write row
        writer.writerow(sorted_row.values())
    return {'total': total, 'success': successful, 'error': errors}
