# Thesis
**Please note that all provided commands are suitable for a Windows system and may need modification if ran on anything else.
## How the Data Was Downloaded
The data has already been downloaded and is available to use in this repository. However, if you would like to mimic the process we used to download the data, we provide corresponding scripts to do so. 

In order to get the data using the given scripts, you must have Chrome and ChromeDriver installed. Make sure the versions match up. 
Download the files into a directory and run the following command from that directory in your command prompt.

```
python link_scraper.py
```

This will generate a csv file of 2000 URLs you can use to download the PDF and MIDI files. Using this csv, you can then run musescore_scraper.py in order to download the metadata, PDF, and MIDI files of all the links you just obtained. The urls.csv file found in the data folder is the result of running link_scraper.py on several different URLs to maximize the scraping of public domain songs on MuseScore. 

*Prequisites: Create a MuseScore account in order to be able to download files and modify the code to include your username and password.
Please note that MuseScore has a download limit of 20 per day so this code is only meant to run in batches of 19 URLs. 
Additionally, the ID for the download button changes on a daily basis so be sure to update the two occurences in the code with the up-to-date ID. 

```
python musescore_scraper.py
```

## Using the Data

The data in this repository is provided in its original, unedited form. In order to preprocess the data, we provide several different scripts in order to assist you, including code to compress the files into singular channels, code to generate audio, and code to for data augmentation. 
