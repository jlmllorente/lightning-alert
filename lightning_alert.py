"""
Lightning Alerter
A program that reads lightning events data as a stream from
standard input (one lightning strike per line as a JSON object,
and matches that data against a source of assets (also in JSON format)
to produce an alert.

Usage:
python lightning_alert.py --help

"""
import argparse
import json
import sys
from pyquadkey2 import quadkey

ZOOM_LEVEL = 12
VALID_FLASH_TYPES = (0, 1)


def load_assets(assets_json):
    """
    Load asset JSON file into a list of assets

    Args:
        assets_json (str): JSON file containing the assets
    Returns:
        assets (list): List of assets(dict)
    """
    try:
        with open(assets_json, 'r') as asset_data:
            assets = json.load(asset_data)
            return assets
    except FileNotFoundError:
        print(f"File '{assets_json}' not found")
        sys.exit()


def asset_lookup(assets, quadkeys):
    """
    Look for lightning strike data in asset_data
    based on requested quadkeys.

    Args:
        assets (list): List of Dictionaries containing asset data
        quadkeys (set): Computed Quadkeys based on input
    """
    # Loop in List of Dict - O(m)
    for asset in assets:
        # Check quadkey in map - O(1)
        if asset["quadKey"] in quadkeys:
            print(f"lightning alert for "
                  f"{asset['assetOwner']}:"
                  f"{asset['assetName']}")


def get_quadkeys(input_file):
    """
    Get all the quadkeys from an input file:
    one lightning strike per line as a JSON object

    Args:
        input_file (str): JSON filename
    Returns:
        computed_quadkeys (set): returns a set of quadkeys
    """
    # Initiliaze empty set
    computed_quadkeys = set()
    try:
        with open(input_file, 'r') as sys.stdin:
            # one lightning strike per line - O(n)
            for line in sys.stdin:
                # load json
                request = json.loads(line)

                # Check if valid flashtype
                if request["flashType"] not in VALID_FLASH_TYPES:
                    continue

                # Get quadkey
                request_quadkey = str(quadkey.from_geo(
                    (request['latitude'], request['longitude']), ZOOM_LEVEL))

                # Add new quadkey. Won't add existing values
                computed_quadkeys.add(request_quadkey)
    except FileNotFoundError:
        print(f"File '{input_file}' not found")
        sys.exit()
    return computed_quadkeys


def main(args):
    """
    Lightning Alerter Main Method

    Args:
        args (list): Command line parameters
    """
    parser = argparse.ArgumentParser()
    parser.add_argument('-a',
                        '--assets',
                        help="JSON file containing assets",
                        required=True)
    parser.add_argument('-r',
                        '--requests',
                        help="File containing lightning strike JSON objects",
                        required=True)
    args = parser.parse_args()

    # Load assets data
    asset_data = load_assets(args.assets)

    # Get quadkeys - O(n)
    requested_quadkeys = get_quadkeys(args.requests)

    # Look for requested_quadkeys in asset_data - O(m)
    asset_lookup(asset_data, requested_quadkeys)

if __name__ == "__main__":
    main(sys.argv)
