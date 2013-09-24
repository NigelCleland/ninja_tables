#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Use CSVReader rather than a full pandas implementation for simplicity
import jinja2
import csv
import os
import sys

def render_template(template_name, headers):
    """ Render a Template which will then be used to render the table

    """

    header = " & ".join(["{{< headers.%s >}}" % x for x in headers]) + r'\tabularnewline'
    data = " & ".join(["{{< item.%s >}}" % x for x in headers]) + r'\tabularnewline'
    tab_columns = "l"*(len(headers) + 1)
    begin_block = "{< for item in data: >}"
    end_block = "{< endfor >}"

    renderer = define_renderer()
    template = renderer.get_template(template_name)
    intermediate_file = 'intermediate.tex'

    with open(intermediate_file, 'w') as f:
        f.write(template.render({'header':header, 'data':data, 'tab_columns':tab_columns, 'begin_block':begin_block, 'end_block':end_block}))

    return intermediate_file

def define_renderer():
    renderer = jinja2.Environment(
        block_start_string='{<',
        block_end_string='>}',
        variable_start_string='{{<',
        variable_end_string='>}}',
        loader=jinja2.FileSystemLoader('.')
        )

    return renderer

def render_table(file_name, template_name="template_name.tex"):

    with open(file_name) as f:
        first_line = f.readline()

    headers = first_line.strip().split(',')
    data = [line for line in csv.DictReader(open(file_name, 'rb'))]

    renderer = define_renderer()
    intermediate = render_template(template_name, headers)
    template = renderer.get_template(intermediate)
    new_filename = file_name.replace('.csv', '.tex')

    dict_headers = {h:h for h in headers}

    with open(new_filename, 'w') as f:
        f.write(template.render(headers=dict_headers, data=data))

    os.remove(intermediate)

if __name__ == '__main__':
    pass
    # # If a tempalte is passed
    # if len(sys.argv) == 2:
    #     # If a tempalte is passed use it
    #     render_table(sys.argv[1], sys.argv[2])
    # else:
    #     # Default Template
    #     render_table(sys.argv[1])
