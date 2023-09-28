# Thesis
**Please note that all provided commands are suitable for a Windows system and may need modification if ran on anything else.
## Downloading the Data
In order to get the data using the given scripts, you must have Chrome and ChromeDriver installed. Make sure the versions match up. 
Download the files into a directory and run the following command from that directory in your command prompt.

```
python link_scraper.py
```

This will generate a csv file of 2000 URLs you can use to download the PDF and MIDI files. This csv is also available in the data folder if you run into any issues with the link scraping script. Using this csv, you can then run musescore_scraper.py in order to download the metadata, PDF, and MIDI files of all the links you just obtained. 

*Prequisites: Create a MuseScore account in order to be able to download files and modify the code to include your username and password.
Please note that MuseScore has a download limit of 20 per day so you will only be able to run this code in batches of 20 URLs. Make sure to respect their download limitations.
Additionally, the ID for the download button changes on a daily basis so be sure to update the two occurences in the code with the up-to-date ID. 

```
python musescore_scraper.py
```

## Preprocessing the Data
