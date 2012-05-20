import csv
import sys
import os
import argparse

def setup_environment():
    pathname = os.path.dirname(__file__)
    sys.path.append(os.path.normpath(os.path.join(os.path.abspath(pathname), '..')))
    sys.path.append(os.path.normpath(os.path.join(os.path.abspath(pathname), '../..')))
    os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'

setup_environment()

from rewtfimb.stops.models import Stop
from rewtfimb.routes.models import Route, RouteSegment, SegmentStop
from rewtfimb.cities.models import City

def get_stop(name, city):
    return Stop.objects.get_or_create(name=name, city=city)[0]

def save_segment(stops, route, city):
    if not stops:
        return
    segment = RouteSegment(
                start=get_stop(stops[0], city),
                end=get_stop(stops[-1], city),
                route=route
            )
    segment.save()
    seq = 0
    for s in stops:
        ss = SegmentStop(stop=get_stop(s, city), segment=segment, sequence=seq)
        ss.save()
        seq += 1

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Imports CSVs into the rewtfimb database")
    parser.add_argument("city", help="Name of the city to be imported")
    parser.add_argument("csvsource", help="")

    args = parser.parse_args()

    city = City.objects.get_or_create(name=args.city)[0]
    reader = csv.DictReader(open(args.csvsource))

    for route in reader:
        stops = [s.strip().lower() for s in route['stops'].split(',') if s.strip() != ""]
        r = Route(name=route['name'], city=city)
        r.save()

        save_segment(stops, r, city)
        stops.reverse()
        save_segment(stops, r, city)

        print "Done with %s" % route['name']


            


