#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""_summary_

Returns:
    _type_: _description_
"""

import requests
import base64
import json


def get_urls(url_file):
    with open(url_file, 'r') as f:
        urls = f.readlines()
    return urls


def create_domain_check_payload(js_file, url):
    with open(js_file, 'r') as f:
        script = f.readlines()
    script[0] = "var request = require('request');\n"
    script[2] = f"var domain = '{url}';\n"
    joined_script = ''.join(script)
    return base64.b64encode(joined_script.encode('utf-8')).decode('utf-8')


def get_entities(url, query, headers):
    entities = []
    next_cursor = 'null'

    while True:
        mutation = {
                    "query": f"{{ actor {{ entitySearch( query: \"{query}\") {{ results (cursor: {next_cursor or ''}) {{ nextCursor entities {{ ... on SyntheticMonitorEntityOutline {{ name guid monitorId tags {{key values}}}}}}}}}}}}}}"
                    }

        response = requests.request("POST", url, headers=headers, json=mutation)

        if response.status_code != 200:
                raise Exception(f"Query failed: {response.text}")

        data = response.json()

        entities += data['data']['actor']['entitySearch']['results']['entities']
        next_cursor = f'"{data['data']['actor']['entitySearch']['results']['nextCursor']}"'

        if next_cursor == '"None"':
            break

    return entities


def get_create_script_monitor_mutation(url, account_id):
    return "{\"query\":\"mutation SyntheticsCreateScriptApiMonitor {\\n    syntheticsCreateScriptApiMonitor(\\n        accountId: " + account_id + "\\n        monitor: {\\n            name: \\\"Domain Expiry - " + url + "\\\"\\n            period: EVERY_DAY\\n            runtime: {\\n                runtimeType: \\\"NODE_API\\\"\\n                runtimeTypeVersion: \\\"16.10\\\"\\n                scriptLanguage: \\\"JAVASCRIPT\\\"\\n            }\\n            script: \\\"\\\"\\n            status: ENABLED\\n            locations: { public: \\\"AWS_US_EAST_1\\\" }\\n        }\\n    ) {\\n        errors {\\n            description\\n            type\\n        }\\n    }\\n}\\n\",\"variables\":{}}"


def get_delete_monitor_mutation(guid):
    return "{\"query\":\"mutation SyntheticsDeleteMonitor {\\n    syntheticsDeleteMonitor(guid: \\\"" + guid + "\\\") {\\n        deletedGuid\\n    }\\n}\\n\",\"variables\":{}}"


def get_ids(i, url, monitors):
    if url in monitors[i]["name"]:
        monitors.append(monitors.pop(monitors.index(monitors[i])))
        return monitors[-1]["monitorId"], monitors[-1]["guid"]
    if IndexError:
        return IndexError
    else:
        return False


def make_graph_post_request(url, headers, mutation):
    response = requests.request("POST", url, headers=headers, data=mutation)
    return response


def make_rest_put_request(endpoint, headers, data):
    response = requests.request("PUT", endpoint, headers=headers, data=json.dumps(data))
    return response
