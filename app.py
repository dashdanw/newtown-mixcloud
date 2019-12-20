#!/usr/bin/env python

from client import MixcloudAPI
from newtown import process_line
from newtown import get_mp3_url_from_show_archive

import csv
import os
import time

if os.path.isfile('debug.log'):
    os.rename('debug.log', f'debug.log.{int(time.time())}')
from logger import logger

client = MixcloudAPI()
auth = client.authorize()

with open('uploads.csv') as csvfile:
    reader = csv.DictReader(csvfile)
    for line in reader:
        try:
            tags, episodes = process_line(line)
            for e in episodes:
                try:
                    if 'newtownradio.com/show-archive' not in e:
                        logger.warning(f'url {e} not a newtown archive, skipping')
                        continue
                    file_loc, title = get_mp3_url_from_show_archive(e)
                    logger.info(f'url {e} downloaded successfully')
                    upload = client.upload(filename=file_loc, name=title, tags=tags)
                    logger.info(f'url {e} uploaded successfully')
                    os.remove(file_loc)
                except Exception as e:
                    logger.warning(f'Error processing episode {e}, skipping')
        except Exception as e:
            logger.warning(f'Error parsing line {line}, skipping.')