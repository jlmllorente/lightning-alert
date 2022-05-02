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
Dependencies:
To install [pyquadkey2](https://github.com/muety/pyquadkey2), run:
```log
$ pip install pyquadkey2
```
If you're having issues with the installation, please follow their latest README.md in [pyquadkey2](https://github.com/muety/pyquadkey2)

## Running the program
```python
python lightning_alert.py --assets=assets.json --requests=lightning.json
```
where:

`lightning_alert.py
` - Main python script

`assets.json` - source of assets in JSON

`lightning.json` - file containing lightning events - one lightning strike per line in JSON 

### Unittest
A unittest script is also included which tests some use-cases that the functions of our main script should handle.
To run the unit tests:
```python
python lightning_alert.py --assets=assets.json --requests=lightning.json
```
The following .json files are used also as input for unit testing:
 - assets_test1.json
 - lightning_test1.json
 - lightning_test2.json

### Answer to the following questions:
 - **What is the time complexity for determining if a strike has occurred for a particular asset?**
   - Once we already have the strike data from input (lightning.json), the time complexity for looking up / matching the data against the source is **O(n)** where **n** is the size of our source (assets.json)
   - For the time complexity of looking up **ALL** lightning JSON object in lightning.json against assets.json, the time complexity is: O(n) + O(m) = **O(n + m)** where **n** is the size of our input (lightning.json) and **m** is the size of our source (assets.json)
- **If we put this code into production, but found it too slow, or it needed to scale to many more users or more frequent strikes, what are the first things you would think of to speed it up?**
  - In terms of purpose, we're using the assets.json like a database. We basically use it for data lookup purposes and we're loading this source /"database" every time we run the program. I don't think this is a good practice specially once the data gets bigger. The first thing I thought of is to use an actual database perhaps a NoSQL db (redis, aws dynamodb, etc.) to store assets data.
  - Also, since we're processing JSON object, fetching data through web API endpoint could also be a good approach.
 

 
