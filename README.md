# lightning-alert
## Background
A program that reads lightning events data as a stream from standard input (one lightning strike per line as a JSON object, and matches that data against a source of assets (also in JSON format) to produce an alert.

An example 'strike' from assets looks like this:
```json
{
    "flashType": 1,
    "strikeTime": 1386285909025,
    "latitude": 33.5524951,
    "longitude": -94.5822016,
    "peakAmps": 15815,
    "reserved": "000",
    "icHeight": 8940,
    "receivedTime": 1386285919187,
    "numberOfSensors": 17,
    "multiplicity": 1
}
```
### Where:

- flashType=(0='cloud to ground', 1='cloud to cloud', 9='heartbeat')
- strikeTime=the number of milliseconds since January 1, 1970, 00:00:00 GMT

An example of an 'asset' is as follows:
```json
  {
    "assetName":"Dante Street",
    "quadKey":"023112133033",
    "assetOwner":"6720"
  }
```

Notice that the lightning strikes are in lat/long format, whereas the assets are listed in quadkey format.

For each strike received, the program should simply print to the console the following message:
```log
lightning alert for <assetOwner>:<assetName>
```

```log
lightning alert for 6720:Dante Street
```
### NOTE:
Once we know lightning is in the area, we don't want to be alerted for it over & over again. Therefore, if the program already printed an alert for a lightning strike at a particular location, it should ignore any additional strikes that occur in that quadkey for that asset owner.

## Requirements:
- Written and Tested under Python 3.9.7
- To compute for the Quadkey this program makes use of [pyquadkey2](https://github.com/muety/pyquadkey2)

### Installation
To install [pyquadkey2](https://github.com/muety/pyquadkey2), run:
```log
$ pip install pyquadkey2
```
If you're having issues with the installation, please follow their latest README.md in [pyquadkey2](https://github.com/muety/pyquadkey2)

