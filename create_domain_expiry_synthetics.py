#!/usr/bin/env python
# -*- coding: utf-8 -*-


"""_summary_
"""


import os
from dotenv import load_dotenv
import synthetics_functions


def main():
    load_dotenv()

    api_key = os.environ.get("NEW_RELIC_API_KEY")
    account_id = os.environ.get("NEW_RELIC_ACCOUNT_ID")
    headers = {"X-Api-Key": api_key, "Content-Type": "application/json"}
    graph_url = "https://api.newrelic.com/graphql"
    url_file = "test_urls.txt"
    c = 0

    urls = synthetics_functions.get_urls(url_file)

    for url in urls:
        clean_url = url.strip()

        if clean_url:
            create_mutation = synthetics_functions.get_create_script_monitor_mutation(
                clean_url, account_id
            )
            response = synthetics_functions.make_graph_post_request(
                graph_url, headers, create_mutation
            )

        if '{"errors":[]}' in response.text and response.status_code == 200:
            c += 1
            print(f"{c}/{len(urls)} : {response.status_code}/Ok : `{clean_url}` monitor created")
        else:
            print(
                f"{response.status_code} : `{clean_url}` monitor not created : {response.text}"
            )

    print("All URLs have been processed.")


if __name__ == "__main__":
    main()
