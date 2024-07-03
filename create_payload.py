#!/usr/bin/env python
# -*- coding: utf-8 -*-


"""Module under construction
"""


# import os
# from dotenv import load_dotenv
import unittest
import synthetics_functions



def main():
    js_file = 'test.js'
    url = 'aka.ms'

    print(synthetics_functions.create_domain_check_payload(js_file, url))


if __name__ == "__main__":
    main()
