#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Use CSVReader rather than a full pandas implementation for simplicity
import jinja2
import csv
import os
import sys

# Get the environment

def render_table(file_name, template_name="template_name.tex"):
    renderer = jinja2.Environment(
        block_start_string='%{',
        block_end_string='}%'
        variable_start_string='%{{',
        variable_end_string='}}%',
        loader=jinja2.FileSystemLoad(os.path.abspath('.'))
        )

    template=renderer.get_template(template_name)

    # Get the data here
    headers = None
    data = None

    entries = len(headers) * 'l'


if __name__ == '__main__':
    # If a tempalte is passed
    if len(sys.argv) == 2:
        # If a tempalte is passed use it
        render_table(sys.argv[1], sys.argv[2])
    else:
        # Default Template
        render_table(sys.argv[1])
