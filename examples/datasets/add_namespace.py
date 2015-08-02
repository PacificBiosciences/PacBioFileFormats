#!/usr/bin/python 
import os
import sys


tags = [
    "pbbase:AutomationParameter",
    "pbbase:AutomationParameters",
    "pbbase:BinCount",
    "pbbase:BinCounts",
    "pbbase:BinLabel",
    "pbbase:BinLabels",
    "pbbase:BinWidth",
    "pbbase:ExternalResource",
    "pbbase:ExternalResources",
    "pbbase:FileIndex",
    "pbbase:FileIndices",
    "pbbase:MaxBinValue",
    "pbbase:MaxOutlierValue",
    "pbbase:MetricDescription",
    "pbbase:MinBinValue",
    "pbbase:MinOutlierValue",
    "pbbase:NumBins",
    "pbbase:Properties",
    "pbbase:Property",
    "pbbase:Sample95thPct",
    "pbbase:SampleMean",
    "pbbase:SampleMed",
    "pbbase:SampleSize",
    "pbbase:SampleStd",
    "pbds:AdapterDimerFraction",
    "pbsec:BarcodeConstruction",
    "pbds:ControlReadLenDist",
    "pbds:ControlReadQualDist",
    "pbsec:DataSetMetadata",
    "pbds:DataSet",
    "pbds:DataSets",
    "pbds:Filter",
    "pbds:Filters",
    "pbds:Provenance",
    "pbds:ParentTool",
    "pbds:InsertReadLenDist",
    "pbds:InsertReadQualDist",
    "pbds:MedianInsertDist",
    "pbds:NumRecords",
    "pbds:NumSequencingZmws",
    "pbds:ProdDist",
    "pbds:ReadLenDist",
    "pbds:ReadQualDist",
    "pbds:ReadTypeDist",
    "pbds:ShortInsertFraction",
    "pbds:SubreadSet",
    "pbds:SummaryStats",
    "pbds:TotalLength",
    "pbmeta:Automation",
    "pbmeta:AutomationName",
    "pbmeta:CellIndex",
    "pbmeta:CellPac",
    "pbmeta:CollectionFileCopy",
    "pbmeta:CollectionMetadata",
    "pbmeta:CollectionNumber",
    "pbmeta:CollectionPathUri",
    "pbmeta:Collections",
    "pbmeta:Concentration",
    "pbmeta:ConfigFileName",
    "pbmeta:CopyFiles",
    "pbmeta:InstCtrlVer",
    "pbmeta:MetricsVerbosity",
    "pbmeta:Name",
    "pbmeta:OutputOptions",
    "pbmeta:PlateId",
    "pbmeta:Primary",
    "pbmeta:Readout",
    "pbmeta:ResultsFolder",
    "pbmeta:RunDetails",
    "pbmeta:RunId",
    "pbmeta:SampleReuseEnabled",
    "pbmeta:SequencingCondition",
    "pbmeta:SigProcVer",
    "pbmeta:SizeSelectionEnabled",
    "pbmeta:StageHotstartEnabled",
    "pbmeta:UseCount",
    "pbmeta:WellName",
    "pbmeta:WellSample",
    "pbsample:BioSample",
    "pbsample:BioSamplePointer",
    "pbsample:BioSamplePointers",
    "pbsample:BioSamples",
    "pbsec:AlignmentSet",
    "pbsec:BarcodeSet",
    "pbsec:ConsensusReadSet",
    "pbsec:ContigSet",
    "pbsec:ReferenceSet",
    "pbsec:Ploidy",
    "pbsec:Organism",
    "pbsec:Contig",
    "pbsec:Contigs"
]



namespaces = ( ' xmlns:pbbase="http://pacificbiosciences.com/PacBioBaseDataModel.xsd"  xmlns:pbsample="http://pacificbiosciences.com/PacBioSampleInfo.xsd" xmlns:pbmeta="http://pacificbiosciences.com/PacBioCollectionMetadata.xsd" xmlns:pbds="http://pacificbiosciences.com/PacBioDatasets.xsd" xmlns:pbsec="http://pacificbiosciences.com/PacBioSecondaryDataModel.xsd" '
)

def update_xml(file):
    with open(file) as infile:
        with sys.stdout as out:
            lines = infile.readlines()
            lines[1] = lines[1].replace(" ", namespaces, 1)
            for idx in range(len(lines)):
                for tag in tags:
                    suffix = tag.split(":")[1],
                    lines[idx] = lines[idx].replace("<%s " % suffix, "<%s " % tag, 1)
                    lines[idx] = lines[idx].replace("<%s>" % suffix, "<%s>" % tag, 1)
                    lines[idx] = lines[idx].replace("</%s" % suffix, "</%s" % tag, 1)
                out.write(lines[idx])
          

for file in sys.argv[1:]:
    update_xml(file)

    

