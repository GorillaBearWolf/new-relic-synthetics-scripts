#!/usr/bin/env python
# -*- coding: utf-8 -*-


import requests


def get_urls(txt_file):
    with open(txt_file, 'r') as f:
        urls = f.readlines()
    return urls


def get_monitors(headers, url):
    mutation = "{\"query\":\"{\\n    actor {\\n        entitySearch(query: \\\"name LIKE 'Domain Expiry'\\\") {\\n            results {\\n                entities {\\n                    ... on SyntheticMonitorEntityOutline {\\n                        guid\\n                        name\\n                    }\\n                }\\n            }\\n        }\\n    }\\n}\\n\",\"variables\":{}}"
    response = requests.request("POST", url, headers=headers, data=mutation)
    data = response.json()
    filtered_monitors = data["data"]["actor"]["entitySearch"]["results"]["entities"]
    return filtered_monitors


def get_guid(i, url, monitors):
    if url in monitors[i]["name"]:
        monitors.append(monitors.pop(monitors.index(monitors[i])))
        return monitors[-1]["guid"]
    if IndexError:
        return IndexError
    else:
        return False


def get_update_script_monitor_mutation(guid, url):
    return "{\"query\":\"mutation SyntheticsUpdateScriptApiMonitor {\\n    syntheticsUpdateScriptApiMonitor(\\n        guid: \\\"" + guid + "\\\"\\n        monitor: {\\n            script: \\\"var request = require('request');\
        var domain = \\\\\\\"" + url + "\\\\\\\"; var options = {     'method': 'GET',     'url': 'https://www.rdap.net/domain/' + domain, };\
        request(options, function(error, response) {     if (error) throw new Error(error);\
        var newBody = JSON.parse(response.body);\
        var expDate = newBody.events[1].eventDate;\
        var newExp = Date.parse(expDate);\
        var now = Date.now();\
        var daysToExp = (newExp - now) / 86400000;\
        $util.insights.set(\\\\\\\"checkedDomain\\\\\\\", domain);\
        $util.insights.set(\\\\\\\"domainExpirationDate\\\\\\\", newExp);\
        $util.insights.set(\\\\\\\"daysToExpiration\\\\\\\", daysToExp);\
        console.log(expDate + '\\\\\\\\n' + newExp + '\\\\\\\\n' + now + '\\\\\\\\n' + daysToExp); });\\\"\\n            status: ENABLED\\n            locations: { public: \\\"AWS_US_EAST_1\\\" }\\n        }\\n    ) {\\n        errors {\\n            description\\n            type\\n        }\\n    }\\n}\\n\",\"variables\":{}}"


def get_delete_monitor_mutation(guid):
    return "{\"query\":\"mutation SyntheticsDeleteMonitor {\\n    syntheticsDeleteMonitor(guid: \\\"" + guid + "\\\") {\\n    deletedGuid\\n    }\\n}\\n\",\"variables\":{}}"


def get_create_script_monitor_mutation(url, account_id):
    return "{\"query\":\"mutation SyntheticsCreateScriptApiMonitor {\\n    syntheticsCreateScriptApiMonitor(\\n        accountId: " + account_id + "\\n        monitor: {\\n            name: \\\"Domain Expiry - " + url + "\\\"\\n            period: EVERY_DAY\\n            runtime: {\\n                runtimeType: \\\"NODE_API\\\"\\n                runtimeTypeVersion: \\\"16.10\\\"\\n                scriptLanguage: \\\"JAVASCRIPT\\\"\\n            }\\n            script: \\\"var request = require('request');\
        var domain = \\\\\\\"" + url + "\\\\\\\"; var options = {     'method': 'GET',     'url': 'https://www.rdap.net/domain/' + domain, };\
        request(options, function(error, response) {     if (error) throw new Error(error);\
        var newBody = JSON.parse(response.body);\
        var expDate = newBody.events[1].eventDate;\
        var newExp = Date.parse(expDate);\
        var now = Date.now();\
        var daysToExp = (newExp - now) / 86400000;\
        $util.insights.set(\\\\\\\"checkedDomain\\\\\\\", domain);\
        $util.insights.set(\\\\\\\"domainExpirationDate\\\\\\\", newExp);\
        $util.insights.set(\\\\\\\"daysToExpiration\\\\\\\", daysToExp);\
        console.log(expDate + '\\\\\\\\n' + newExp + '\\\\\\\\n' + now + '\\\\\\\\n' + daysToExp); });\\\"\\n            status: ENABLED\\n            locations: { public: \\\"AWS_US_EAST_1\\\" }\\n        }\\n    ) {\\n        errors {\\n            description\\n            type\\n        }\\n    }\\n}\\n\",\"variables\":{}}"


def make_graph_request(url, headers, mutation):
    response = requests.request("POST", url, headers=headers, data=mutation)
    return response
