#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Use CSVReader rather than a full pandas implementation for simplicity
import jinja2
import csv
import os
import sys

# Get the environment

def render_template(template_name, size):
    """ Render a Template which will then be used to render the table

    """

    header = " & ".join(["%{{ header.%s }}%" % x for x in range(size)])
    data = " & ".join(["%{{ item.%s }}%" % x for x in range(size)])
    tab_columns = "l"*(size + 1)
    begin_block = "%{ for item in data }%"
    end_block = "%{ endfor }%"

    renderer = define_renderer()
    template = renderer.get_template(template_name)
    intermediate_file = 'intermediate.tex'

    with open(intermediate_file, 'w') as f:
        f.write(template.render((header, data, tab_columns)))

    return intermediate_file

def define_renderer():
    renderer = jinja2.Environment(
        block_start_string='%{',
        block_end_string='}%'
        variable_start_string='%{{',
        variable_end_string='}}%',
        loader=jinja2.FileSystemLoad(os.path.abspath('.'))
        )

    return renderer

def render_table(file_name, template_name="template_name.tex"):

    renderer = define_renderer()
    intermediate = render_template(template_name, len(headers))
    template = renderer.get_template(intermediate)
    new_filename = file_name.replace('.csv', '.tex')

    with open(new_filename, 'w') as f:
        f.write(template.render((headers, data)))




if __name__ == '__main__':
    # If a tempalte is passed
    if len(sys.argv) == 2:
        # If a tempalte is passed use it
        render_table(sys.argv[1], sys.argv[2])
    else:
        # Default Template
        render_table(sys.argv[1])
