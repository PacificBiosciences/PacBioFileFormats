#!/usr/bin/python

# This script validates against the PacBio end-to-end 
# data model XSDs checked into perforce. It is a temporary
# to allow validation with python and lxml until the schemas find a more
# permament home on the web.


import glob, os
from lxml import etree

schema_glob = "../../../../../../../../common/datamodel/*/EndToEnd/xsd/*.xsd"

xsds = glob.glob(schema_glob)
if len(xsds) == 0:
    raise SystemExit, "Please put %s in your p4 client spec" % schema_glob

print "Copying xsds from %s to local directory" % schema_glob
for xsd in xsds:
    os.system("cp -f %s ." % xsd)


schema_file = "PacBioDataModel.xsd"

def validate(xmlparser, xmlfilename):
    try:
        with open(xmlfilename, 'r') as f:
            etree.fromstring(f.read(), xmlparser) 
        return True
    except Exception, e:
	print "%s" % e
        return False

print "Opening schema"
with open(schema_file, 'r') as f:
    xsd = etree.parse(schema_file)
xml_validator = etree.XMLSchema(xsd)


filenames = [
  'subread.dataset.xml' ,
  'ccsread.dataset.xml',
  'barcode.dataset.xml',
  'reference.dataset.xml',
  'contig.dataset.xml',
  'alignment.dataset.xml',
  'transformed_rs_subread.dataset.xml'
]

print "Validating files"
for filename in filenames:
    xml = etree.parse(filename)
    if xml_validator.validate(xml):
        print "%s validates" % filename
    else:
        print "%s doesn't validate" % filename
        print "%s" % xml_validator.error_log

