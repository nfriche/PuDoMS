# Thesis
**Please note that all provided commands are suitable for a Windows system and may need modification if ran on a Linux or Mac OS system.

## Downloading Data
In order to get the data, the combined use of the following three repositories are required: 
- https://github.com/jblsmith/matching-salami/tree/master
- https://github.com/DDMAL/SALAMI/tree/main
- https://github.com/DDMAL/SALAMI/tree/main

First, you can download the publicly available mp3 files found in the Internet Archive. This is done using the [SALAMI_download.py](https://github.com/DDMAL/SALAMI/blob/main/SALAMI_download.py) and [id_index_internetarchive.csv](https://github.com/DDMAL/salami-data-public/blob/master/metadata/id_index_internetarchive.csv) files. An updated version of the SALAMI_download.py file (compatible with Python3) can be found in the [data](https://github.com/nfriche/thesis/tree/main/data) folder of this branch. There are 476 matches but 8 URLs are now forbidden or not found so we get 468 mp3 files. 

## Matching Data to Annotations
Download the [annotations](https://github.com/DDMAL/salami-data-public/tree/master/annotations) folder. 

