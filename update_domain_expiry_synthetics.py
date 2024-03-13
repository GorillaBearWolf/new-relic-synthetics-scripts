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
    headers = {"X-Api-Key": api_key, "Content-Type": "application/json"}
    graph_url = "https://api.newrelic.com/graphql"
    rest_url = "https://synthetics.newrelic.com/synthetics/api/v3/monitors"
    url_file = "test_urls.txt"
    js_file = 'test.js'
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
                monitor_id = ids[0]
                encoded_script = synthetics_functions.create_domain_check_payload(js_file, clean_url)
                payload = {"scriptText": encoded_script, "monitorId": monitor_id}
                script_endpoint = f'{rest_url}/{monitor_id}/script'
                break

        response = synthetics_functions.make_rest_put_request(script_endpoint, headers, payload)

        if response.status_code == 204:
            c += 1
            print(f"{c}/{len(monitors)} : {response.status_code}/Ok : `{clean_url}` monitor updated")
        else:
            print(
                f"{response.status_code} : `{clean_url}` monitor not updated : {response.text}"
            )

    print("All found URLs have been processed.")


if __name__ == "__main__":
    main()
