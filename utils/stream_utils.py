'''
functions for working with the shoutcast radio server
'''

import json

import requests

SERVER_IP = '35.227.60.131'
SERVER_PORT = '8000'
STREAM_ID = '2'
STATS_ENDPOINT = '/statistics?json=1'
ART_ENDPOINT = '/playingart?sid=' + STREAM_ID
STREAM_ENDPOINT = '/listen.pls?sid=' + STREAM_ID


ENDPOINT_TEMPLATE = 'http://{ip}:{port}{endpoint}'
STATS_URL = ENDPOINT_TEMPLATE.format(ip=SERVER_IP,
                                     port=SERVER_PORT,
                                     endpoint=STATS_ENDPOINT)
ART_URL = ENDPOINT_TEMPLATE.format(ip=SERVER_IP,
                                   port=SERVER_PORT,
                                   endpoint=ART_ENDPOINT)
STREAM_URL = ENDPOINT_TEMPLATE.format(ip=SERVER_IP,
                                      port=SERVER_PORT,
                                      endpoint=STREAM_ENDPOINT)


def get_live_info():
    stream_status = False

    try:
        stats = requests.get(STATS_URL)
        stats_dict = json.loads(stats.text)
        
        if stats_dict['streams'][int(STREAM_ID)-1]['streamstatus'] == 1:
            stream_status = stats_dict['streams'][int(STREAM_ID)-1]['songtitle'].split('-')
            live_info = {
                'title': stream_status[0],
                'artist': stream_status[1],
                'album': stream_status[2],
                'art_url': ART_URL,
                'stream_url': STREAM_URL
            }

            return live_info

    except Exception as e:
        print(e)

    return stream_status
