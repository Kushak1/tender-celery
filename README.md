# Project I made to get a job

With this script you can parse data from https://zakupki.gov.ru/ using celery


# Quick Start

- Setup redis server
- Pass redis ip to 'broker' at tasks.py
- Start celery worker:

    	$ celery -A tasks worker
- Start main.py

    	python main.py
	
## Requirements

	pip install celery
	pip install xmltodict
    pip install beautifulsoup4
    pip install redis

