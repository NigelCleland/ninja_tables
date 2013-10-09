#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Use CSVReader rather than a full pandas implementation for simplicity
import jinja2
import csv
import os
import sys
import optparse

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

    dict_headers, data = flush_keys(dict_headers, data)

    with open(new_filename, 'w') as f:
        f.write(template.render(headers=dict_headers, data=data))

    os.remove(intermediate)

def flush_keys(headers, data):
    """ This function "fixes" the issue when numbers are passed as headers
    which Jinja was failing to recognise, e.g type issues.
    Fixed this by converting them all to floats

    Need to figure out a smarter way as to whether to use floats or ints here
    It seems...

    """
    headers2 = {}
    for key, value in headers.iteritems():
        try:
            key = int_check(key)
            value = int_check(value)
        except:
            pass
        headers2[key] = value

    data2 = []
    for line in data:
        new_dict = {}
        for key, value in line.iteritems():
            try:
                key = int_check(key)
            except:
                pass
            new_dict[key] = value
        data2.append(new_dict)

    return headers2, data2



def int_check(x):
    try:
        int_x = int(x)
        fl_x = float(x)
        x = int_x if int_x == fl_x else fl_x
    except:
        pass
    return x

def main():
    p = optparse.OptionParser(description="Convert a CSV file into a"\
        "functional, simple LaTeX table",
        prog="ninja_tables",
        version="ninja_tables 0.1",
        usage="%prog filename.csv")
    p.add_option('--template', '-t', default='standard_booktab.tex',
                 help="The template to be applied to the table, must be located in the _static directory")
    options, arguments = p.parse_args()

    if len(arguments) == 1:
        template = os.path.join('_template', options.template)
        render_table(arguments[0], template)
    else:
        p.print_help()

if __name__ == '__main__':
    main()
