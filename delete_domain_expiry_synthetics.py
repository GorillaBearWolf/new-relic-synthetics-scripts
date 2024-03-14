#!/usr/bin/env python
# -*- coding: utf-8 -*-


"""_summary_
"""


import os
from dotenv import load_dotenv
import synthetics_functions


def main():
    load_dotenv()

    graph_url = "https://api.newrelic.com/graphql"
    api_key = os.environ.get("NEW_RELIC_API_KEY")
    headers = {"X-Api-Key": api_key, "Content-Type": "application/json"}
    url_file = "test_urls.txt"
    query = "name LIKE 'Domain Expiry'"
    c = 0


    urls = synthetics_functions.get_urls(url_file)
    monitors = synthetics_functions.get_entities(graph_url, query, headers)

    for url in urls:
        clean_url = url.strip()

        for i in range(len(monitors)):
            if clean_url:
                ids = synthetics_functions.get_ids(i, clean_url, monitors)
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
                mutation = synthetics_functions.get_delete_monitor_mutation(guid)
                break

        response = synthetics_functions.make_graph_post_request(
            graph_url, headers, mutation
        )

        if "deletedGuid" in response.text and response.status_code == 200:
            c += 1
            print(f"{c}/{len(urls)} : {response.status_code}/Ok : `{clean_url}` monitor deleted")
        else:
            print(
                f"{response.status_code} : `{clean_url}` monitor not deleted : {response.text}"
            )

    print("All found URLs have been processed.")


if __name__ == "__main__":
    main()
