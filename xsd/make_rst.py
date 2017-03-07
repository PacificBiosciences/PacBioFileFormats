#!/usr/bin/python

# This script creates rst snippets from example xmls files.

import glob, os

for xml_filename in glob.glob("*.xsd"):

    dataset_type_list = list(xml_filename.split(".")[0])
    dataset_type_list[0] = dataset_type_list[0].upper()

    lines = ["============================\n"] +        \
            ["%s\n" % "".join(dataset_type_list) ] +    \
            ["============================\n"] +        \
            ["\n.. literalinclude:: %s\n    :language: xml\n" %  xml_filename]
    rst_filename = xml_filename.split(".")[0] + ".rst"
    try:
        with open(rst_filename, "w") as rst_fh:
            rst_fh.write("".join(lines))
    except Exception, e:
        print "rst file: %s is not accessible: %s" % (rst_filename, e)

        
