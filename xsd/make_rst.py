#!/usr/bin/python

# This script creates rst snippets from example xmls files.

import glob, os

for xml_filename in glob.glob("*.xsd"):
    with open(xml_filename) as xml_fh:
        lines = xml_fh.readlines()

    dataset_type_list = list(xml_filename.split(".")[0])
    dataset_type_list[0] = dataset_type_list[0].upper()

    lines = ["============================\n"] + ["%s\n" % "".join(dataset_type_list) ] + \
            ["============================\n\n"] + ["::\n"] + \
            ["\n"] + [ "\t%s" % line for line in lines ]
    rst_filename = xml_filename.split(".")[0] + ".rst"
    lines = [line.replace("\t", "  ") for line in lines]
    lines = [line.replace("\r", "") for line in lines]
    try:
        with open(rst_filename, "w") as rst_fh:
            rst_fh.write("".join(lines))
    except Exception, e:
        print "rst file: %s is not accessible: %s" % (rst_filename, e)

        
