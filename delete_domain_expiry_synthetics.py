#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""_summary_"""

import os
from dotenv import load_dotenv
from synthetics_functions import (
    get_urls,
    get_entities,
    get_ids,
    get_delete_monitor_mutation,
    make_graph_post_request,
)


def main():
    load_dotenv()

    graph_url = "https://api.newrelic.com/graphql"
    api_key = os.environ.get("NEW_RELIC_API_KEY")
    headers = {"X-Api-Key": api_key, "Content-Type": "application/json"}
    url_file = "test_urls.txt"
    query = "name LIKE 'Domain Expiry'"
    c = 0

    urls = get_urls(url_file)
    monitors = get_entities(graph_url, query, headers)

    for url in urls:
        clean_url = url.strip()

        for i in range(len(monitors)):
            if clean_url:
                ids = get_ids(i, clean_url, monitors)
            else:
                print(f"{clean_url} not clean, trying next URL")
                break

            if ids is IndexError:
                i += 1
            elif ids is False:
                print(f"{clean_url} monitor not found")
                break
            else:
                guid = ids[1]
                mutation = get_delete_monitor_mutation(guid)
                break

        response = make_graph_post_request(graph_url, headers, mutation)

        if "deletedGuid" in response.text and response.status_code == 200:
            c += 1
            print(
                f"{c}/{len(urls)} : {response.status_code}/Ok : `{clean_url}` monitor deleted"
            )
        else:
            raise Exception(f"Query failed: {response.text}")

    print("All found URLs have been processed.")


if __name__ == "__main__":
    main()
