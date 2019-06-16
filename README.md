# Backend Engineering Challenge

Hi all! Here you can find the solution I implemented for the backend engineering challenge.

### *Prerequisites*
This project was developed for Python 3.7 and uses the packages in the requirements.txt file. Please run

    pip install -r requirements.txt 
    
to install the exact versions used during development.

### *Usage*
This CLI application has six arguments, which the first two are mandatory. Please run

    unbabel_cli --help
    
in order to get more information:

    unbabel_cli.py [-h] --input_file INPUT_FILE --window_size WINDOW_SIZE
                   [--output_file OUTPUT_FILE] [--client_name CLIENT_NAME]
                   [--source_language SOURCE_LANGUAGE]
                   [--target_language TARGET_LANGUAGE]

    optional arguments:
      -h, --help            show this help message and exit
      --input_file INPUT_FILE
                            path to a json file containing the stream of events to be analysed
      --window_size WINDOW_SIZE
                            time window (in minutes) to be considered on the moving average calculation
      --output_file OUTPUT_FILE
                            path to where the aggregated output is going to be export (json file)
      --client_name CLIENT_NAME
                            specify a client name in order to calculated his KPI
      --source_language SOURCE_LANGUAGE
                            specify a source language in order to calculate its KPI
      --target_language TARGET_LANGUAGE
                            specify a target language in order to calculate its KPI

Note that the last three field are accumulative, i.e. if you e.g. specify a client name and a source language you will get the KPI for that client considering the specified source language (disregards all the other entries).


## Challenge Scenario

At Unbabel we deal with a lot of translation data. One of the metrics we use for our clients' SLAs is the delivery time of a translation. 

In the context of this problem, and to keep things simple, our translation flow is going to be modeled as only one event.

### *translation_delivered*

Example:

```json
{
	"timestamp": "2018-12-26 18:12:19.903159",
	"translation_id": "5aa5b2f39f7254a75aa4",
	"source_language": "en",
	"target_language": "fr",
	"client_name": "easyjet",
	"event_name": "translation_delivered",
	"duration": 20,
	"nr_words": 100
}
```

## Challenge Objective

Your mission is to build a simple command line application that parses a stream of events and produces an aggregated output. In this case, we're interested in calculating, for every minute, a moving average of the translation delivery time for the last X minutes.

If we want to count, for each minute, the moving average delivery time of all translations for the past 10 minutes we would call your application like (feel free to name it anything you like!).

	unbabel_cli --input_file events.json --window_size 10
	
The input file format would be something like:

	{"timestamp": "2018-12-26 18:11:08.509654","translation_id": "5aa5b2f39f7254a75aa5","source_language": "en","target_language": "fr","client_name": "easyjet","event_name": "translation_delivered","nr_words": 30, "duration": 20}
	{"timestamp": "2018-12-26 18:15:19.903159","translation_id": "5aa5b2f39f7254a75aa4","source_language": "en","target_language": "fr","client_name": "easyjet","event_name": "translation_delivered","nr_words": 30, "duration": 31}
	{"timestamp": "2018-12-26 18:23:19.903159","translation_id": "5aa5b2f39f7254a75bb33","source_language": "en","target_language": "fr","client_name": "booking","event_name": "translation_delivered","nr_words": 100, "duration": 54}


The output file would be something in the following format.

```
{"date": "2018-12-26 18:11:00", "average_delivery_time": 0}
{"date": "2018-12-26 18:12:00", "average_delivery_time": 20}
{"date": "2018-12-26 18:13:00", "average_delivery_time": 20}
{"date": "2018-12-26 18:14:00", "average_delivery_time": 20}
{"date": "2018-12-26 18:15:00", "average_delivery_time": 20}
{"date": "2018-12-26 18:16:00", "average_delivery_time": 25.5}
{"date": "2018-12-26 18:17:00", "average_delivery_time": 25.5}
{"date": "2018-12-26 18:18:00", "average_delivery_time": 25.5}
{"date": "2018-12-26 18:19:00", "average_delivery_time": 25.5}
{"date": "2018-12-26 18:20:00", "average_delivery_time": 25.5}
{"date": "2018-12-26 18:21:00", "average_delivery_time": 25.5}
{"date": "2018-12-26 18:22:00", "average_delivery_time": 31}
{"date": "2018-12-26 18:23:00", "average_delivery_time": 31}
{"date": "2018-12-26 18:24:00", "average_delivery_time": 42.5}
```