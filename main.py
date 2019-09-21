#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os 

from betamax import Betamax
from betamax_serializers import pretty_json

from manga_reader import MangaReaderWorker


WORKERS_DIR = os.path.dirname(os.path.abspath(__file__))
CASSETTES_DIR = os.path.join(WORKERS_DIR, u'resources', u'cassettes')
MATCH_REQUESTS_ON = [u'method', u'uri', u'path', u'query']

Betamax.register_serializer(pretty_json.PrettyJSONSerializer)
with Betamax.configure() as config:
    config.cassette_library_dir = CASSETTES_DIR
    config.default_cassette_options[u'serialize_with'] = u'prettyjson'
    config.default_cassette_options[u'match_requests_on'] = MATCH_REQUESTS_ON
    config.default_cassette_options[u'preserve_exact_body_bytes'] = True


if __name__ == "__main__":
    worker = MangaReaderWorker()
    with Betamax(worker.session) as vcr:
        vcr.use_cassette(u'manga_list')
        worker.download_mangas()
