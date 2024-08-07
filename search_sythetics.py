#!/usr/bin/env python
# -*- coding: utf-8 -*-


"""_summary_
"""


import os
from pprint import pprint

from dotenv import load_dotenv

from synthetics_functions import get_entities


def main():
    load_dotenv()

    api_key = os.environ.get("NEW_RELIC_API_KEY")
    headers = {"X-Api-Key": api_key, "Content-Type": "application/json"}
    graph_url = "https://api.newrelic.com/graphql"
    query = "name LIKE 'Mobile -'"

    monitors = get_entities(graph_url, query, headers)
    pprint(f'{monitors}\n\nlength={len(monitors)}')


if __name__ == "__main__":
    main()
