# A Sony Global Website Media Scraper
This python scripts download the photographs in the highest resolution and the sound scape and background music of all the locations in [Sony Global - alpha CLOCK: WORLD TIME, CAPTURED BY alpha](www.sony.net/united/clock/). 

## Usage
1. The script needs `PyV8` to evaluate the javascript code. Please download it from [Google Code Archive](https://code.google.com/archive/p/pyv8/downloads)  
2. Change the `pwd` in the script to the path where you want to put the media and run the script:  
```
python Heritage.py  
```

## What happened?
All the media will be downloaded into different folders with their own location name (actually their id).  
Each location includes 12 photographs took in the same place in various time, 10 other extra photographs in different aspects, and also a .json file for a brief introduction of the location.  
Some locations also provide soundscapes.  
All the theme songs were put in the `Theme Song of World Heritage` folder.

