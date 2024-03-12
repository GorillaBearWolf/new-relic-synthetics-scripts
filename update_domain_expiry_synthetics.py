#!/usr/bin/env python
# -*- coding: utf-8 -*-


"""_summary_
"""


import os
from dotenv import load_dotenv
import synthetics_functions


def main():
    load_dotenv()

    url_file = "test_urls.txt"
    graph_url = "https://api.newrelic.com/graphql"
    api_key = os.environ.get("NEW_RELIC_API_KEY")
    headers = {"X-Api-Key": api_key, "Content-Type": "application/json"}

    urls = synthetics_functions.get_urls(url_file)

    monitors = synthetics_functions.get_monitors(headers, graph_url)

    for url in urls:
        clean_url = url.strip()

        for i in range(len(urls)):
            if clean_url:
                guid = synthetics_functions.get_guid(i, clean_url, monitors)
            else:
                print(f"{clean_url} not clean, trying next URL")
                break

            if guid is IndexError:
                break
            if guid is False:
                i += 1
            else:
                mutation = synthetics_functions.get_update_script_monitor_mutation(
                    guid, clean_url
                )

            response = synthetics_functions.make_graph_request(
                graph_url, headers, mutation
            )

        if '{"errors":[]}' in response.text and response.status_code == 200:
            print(f"{response.status_code} : `{clean_url}` monitor updated")
        else:
            print(
                f"{response.status_code} : `{clean_url}` monitor not updated : {response.text}"
            )

    print("All found URLs have been processed.")


if __name__ == "__main__":
    main()
