===================================================
PacBio DataSet File Format Specification
===================================================

1. Introduction
===============

This document defines the 4.0.0 Secondary DataSet abstraction and its
XML file representation. A DataSet is a set of a particular
sequence data type, such as subreads, references or aligned subreads.
The actual data is stored in files external to the XML, usually in FASTA
or BAM files.

1.1 Motivating Use Cases
--------------------------

The concept of a homogenous set of elements of a particular data type is
used throughout Pacific Biosciences Secondary Analysis.
These "sets of data" have historically been represented in
different ways, sometimes explicitly by creating large files
that contain all the data in the set (e.g. a FASTA file of subreads),
and sometimes implicitly by using pointers to the data, such as with a FOFN
(file of file names).

In many cases these solutions are serviceable, but they have
disadvantages. The reliance on explicit file creation imposes a heavy
burden that will exacerbated by future instrument throughput increases. The
FOFN partially breaks the tight coupling between explicit files and
sets of data, but it fails to allow facile subsetting of files. Tools
are forced to reimplement filtering or subsetting logic in their own
idiosyncratic ways.

The DataSet XML abstraction (or DataSet for short) satisfies these use cases in a unified way
using a canonical representation used throughout SMRT Link 4.0
and the associated. Here is a sampling of the uses of cases for DataSets:

- Refer to a **set of subreads** in multiple BAM files
- Refer to a **subset of subreads** by id from one or more BAM files
- Refer to a **set of alignments** from multiple different references or movies
- Run algorithms such as Arrow on a **subset of alignments** (e.g. on a
  particular chromosome, or a particular chromosome region, or from reads
  labeled with a particular barcode)
- Refer to a **subset of alignments** that obey certain criteria (such as a length minimum).
- Perform any analysis that can be performed on an entire file of a particular
  data type (reads, read regions, alignments) on a **subset of that data type**  without creating a new file.


2. Data Format Definition
=========================

2.1 XML Representation
----------------------

The canonical representation of a DataSet is an XML file that
contains a single DataSet element with four major sections, one mandatory
and three optional:

    1.  A mandatory ``<pbbase:ExternalResources>`` section with references to external
        data sources, typically in BAM or FASTA format. The records in these
        files are the elements of the set of data represented by the DataSet.

    2.  An optional ``<pbds:Filters>`` section that filters or subsets the elements
        of the set in the above files, for example by length.

    3.  An optional ``<pbds:DataSetMetadata>`` section that contains metadata about
        the DataSet, usually at minimum the number of records and their total
        length, but possibly much more. For example, subread and CCS
        read DataSets have metadata regarding instrument collection or
        biological samples. The Metadata section should be considered
        to refer to the DataSet elements prior to applying Filters.

    4.  An optional ``<pbds:DataSets>`` section that labels subdatasets of the
        DataSet, for example labelling reads from a particular file as
        "High SNR."

Here is a simple example of a DataSet XML file containing all four
sections. It creates a set of subreads from two subread BAM files and
associated indices, filters the subreads by quality using the ``rq`` field of the underlying
BAM records and labels a subdataset of the subreads as "Long Reads"::

    <?xml version="1.0" encoding="utf-8"?>
    <pbds:SubreadSet
        xmlns="http://pacificbiosciences.com/PacBioDatasets.xsd"
        xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
        xmlns:pbbase="http://pacificbiosciences.com/PacBioBaseDataModel.xsd"
        xmlns:pbsample="http://pacificbiosciences.com/PacBioSampleInfo.xsd"
        xmlns:pbmeta="http://pacificbiosciences.com/PacBioCollectionMetadata.xsd"
        xmlns:pbds="http://pacificbiosciences.com/PacBioDatasets.xsd"
        xsi:schemaLocation="http://pacificbiosciences.com/PacBioDataModel.xsd"
        UniqueId="b095d0a3-94b8-4918-b3af-a3f81bbe519c"
        TimeStampedName="subreadset_150304_231155"
        MetaType="PacBio.DataSet.SubreadSet"
        Name="DataSet_SubreadSet"
        Tags=""
        Version="4.0.0"
        CreatedAt="2015-01-27T09:00:01">
        <pbbase:ExternalResources>
            <pbbase:ExternalResource
                UniqueId="b095d0a3-94b8-4918-b3af-a3f81bbe5193"
                TimeStampedName="subread_bam_150304_231155"
                MetaType="PacBio.SubreadFile.SubreadBamFile"
                ResourceId="m150404_101626_42267_s1_p0.1.subreads.bam">
                <pbbase:FileIndices>
                    <pbbase:FileIndex
                        UniqueId="b095d0a3-94b8-4918-b3af-a3f81bbe5194"
                        TimeStampedName="bam_index_150304_231155"
                        MetaType="PacBio.Index.PacBioIndex"
                        ResourceId="m150404_101626_42267_s1_p0.1.subreads.bam.pbi"/>
                </pbbase:FileIndices>
            </pbbase:ExternalResource>
            <pbbase:ExternalResource
                UniqueId="b095d0a3-94b8-4918-b3af-a3f81bbe5197"
                TimeStampedName="subread_bam_150304_231155"
                MetaType="PacBio.SubreadFile.SubreadBamFile"
                ResourceId="m150404_101626_42267_s1_p0.2.subreads.bam">
                <pbbase:FileIndices>
                    <pbbase:FileIndex
                        UniqueId="b096d0a3-94b8-4918-b3af-a3f81bbe5198"
                        TimeStampedName="bam_index_150304_231155"
                        MetaType="PacBio.Index.PacBioIndex"
                        ResourceId="m150404_101626_42267_s1_p0.2.subreads.bam.pbi"/>
                </pbbase:FileIndices>
            </pbbase:ExternalResource>
        </pbbase:ExternalResources>
        <pbds:Filters>
            <pbds:Filter>
                <pbbase:Properties>
                    <pbbase:Property Name="rq" Operator="gt" Value="0.80"/>
                </pbbase:Properties>
            </pbds:Filter>
        </pbds:Filters>
        <pbds:DataSetMetadata>
            <pbbase:TotalLength>5000</pbbase:TotalLength>
            <pbbase:NumRecords>500</pbbase:NumRecords>
        </pbds:DataSetMetadata>
        <pbds:DataSets>
            <pbds:SubreadSet Name="Long Reads">
                <pbds:Filters>
                    <pbds:Filter>
                        <pbbase:Properties>
                            <pbbase:Property Name="length" Operator="gte" Value="10000"/>
                        </pbbase:Properties>
                    </pbds:Filter>
                </pbds:Filters>
            </pbds:SubreadSet>
        </pbds:DataSets>
    </pbds:SubreadSet>

2.2 Operations on DataSets
--------------------------

DataSets support operations that would naively be expected of sets, such
as subsetting and union (although notably not intersection) as well as
some additional operations such as consolidating and labelling of subsets.
The result of performing these operations is itself a new DataSet.
The subsetting operation is supported efficiently by the PacBio index (\*.pbi files)

Subsetting (Filtering) DataSets
+++++++++++++++++++++++++++++++

The SubreadSet in Section 1 above is conceptually the result of applying a length subset or Filter operation on two
BAM files. Additional filters could be applied, further subsetting the original two BAM files.
Each Filter is composed of Property tags which provide logically predicates which data in the DataSet must
satisfy. Individual Filter tags are logically "ORed" while individual Property tags within a Filter are "ANDed" together.
Property tags are defined by three attributes: Name, Operator and Value, where the Name refers to a field or derived
value from individual BAM records, and the Operator is used to compare that field's value with the Value attribute.

All filters require an associated pbi file, and particular filter support is driven by the presence or absence of the pbi
and the indices within it.  There are three major groups of indices in the pbi: basic data, mapping data, barcode data and associated metadata.
The following Property Names are supported by either the pbbam C++ API or pbcore Python API.
Those that allow list values indicates by brackets, those
supported by both pbbam and pbcore are in **bold**, those only by pbcore are *italicized*.

+---------------+------------------------------------------------+---------------------------+----------+
| Property Name | Description                                    | Other Names               | Type     |
+===============+================================================+===========================+==========+
| **readstart** | Alignment start                                | astart, as                | uint32_t |
+---------------+------------------------------------------------+---------------------------+----------+
| ae            | Alignment end                                  | aend                      | uint32_t |
+---------------+------------------------------------------------+---------------------------+----------+
| alignedlength | Alignment length                               |                           | uint32_t |
+---------------+------------------------------------------------+---------------------------+----------+
| **accuracy**  | Alignment identity                             | identity                  | float    |
+---------------+------------------------------------------------+---------------------------+----------+
| **qname**     | Query name                                     | *qid*                     | string   |
+---------------+------------------------------------------------+---------------------------+----------+
| **qstart**    | Query start                                    | **qs**                    | int      |
+---------------+------------------------------------------------+---------------------------+----------+
| **qend**      | Query end                                      | **qe**                    | int      |
+---------------+------------------------------------------------+---------------------------+----------+
| **length**    | Query length                                   | querylength               | int      |
+---------------+------------------------------------------------+---------------------------+----------+
| **rname**     | Reference name                                 |                           | string   |
+---------------+------------------------------------------------+---------------------------+----------+
| **tstart**    | Reference start                                | ts  **pos**               | uint32_t |
+---------------+------------------------------------------------+---------------------------+----------+
| **tend**      | Reference end                                  | te                        | uint32_t |
+---------------+------------------------------------------------+---------------------------+----------+
| qname_file    | Query names from a file                        |                           | filename |
+---------------+------------------------------------------------+---------------------------+----------+
| **rq**        | Predicted read quality                         |                           | float    |
+---------------+------------------------------------------------+---------------------------+----------+
| **movie**     | Movie name (e.g. m150404_101626_42267_s1_p0)   |                           | string   |
+---------------+------------------------------------------------+---------------------------+----------+
| **zm**        | ZMW (e.g. m150404_101626_42267_s1_p0/100)      | zmw                       | string[] |
+---------------+------------------------------------------------+---------------------------+----------+
| **bc**        | Barcode name                                   | barcode                   | string[] |
+---------------+------------------------------------------------+---------------------------+----------+
| **bcq**       | Barcode quality                                | **bq**                    | uint8_t  |
+---------------+------------------------------------------------+---------------------------+----------+
| **bcf**       | Barcode forward                                |                           | string[] |
+---------------+------------------------------------------------+---------------------------+----------+
| **bcr**       | Barcode reverse                                |                           | string[] |
+---------------+------------------------------------------------+---------------------------+----------+
| **cx**        | Local context (see below for special Values)   |                           | string[] |
+---------------+------------------------------------------------+---------------------------+----------+
| *n_subreads*  | Number of subreads                             |                           | int      |
+---------------+------------------------------------------------+---------------------------+----------+

Supported Operator values include:

+---------------------------------------------------------------+----------------------------------------------------+-------------+
| Operator Name                                                 | Description                                        | Other Names |
+===============================================================+====================================================+=============+
| ==                                                            | Equal to                                           | =  eq       |
+---------------------------------------------------------------+----------------------------------------------------+-------------+
| !=                                                            | Not Equal to                                       | ne          |
+---------------------------------------------------------------+----------------------------------------------------+-------------+
| <                                                             | Less Than                                          | lt  &lt;    |
+---------------------------------------------------------------+----------------------------------------------------+-------------+
| <=                                                            | Less than or equal to                              | lte  &lt;=  |
+---------------------------------------------------------------+----------------------------------------------------+-------------+
| >                                                             | Greater than                                       | gt  &gt;    |
+---------------------------------------------------------------+----------------------------------------------------+-------------+
| >=                                                            | Greater than or equal to                           | gte  &gt;=  |
+---------------------------------------------------------------+----------------------------------------------------+-------------+
| &                                                             | Contains                                           | and         |
+---------------------------------------------------------------+----------------------------------------------------+-------------+
| ~                                                             | Does not contain                                   | not         |
+---------------------------------------------------------------+----------------------------------------------------+-------------+

Some Operators only operate on certain Property names.

For pbbam, the following Values are for the 'cx' local context tag only.
They can be combined using to form a Value that looks and behaves similarly to OR-ing bitflags:

    Value='ADAPTER_BEFORE | ADAPTER_AFTER'

+---------------------------------------------------------------+----------------------------------------------------+-------------+
| Operator Name                                                 | Description                                        | Other Names |
+===============================================================+====================================================+=============+
| NO_LOCAL_CONTEXT                                              | No local context (e.g. adapters or barcodes)       |             |
+---------------------------------------------------------------+----------------------------------------------------+-------------+
| ADAPTER_BEFORE                                                | An adapter was detected before (5' to) the subread |             |
+---------------------------------------------------------------+----------------------------------------------------+-------------+
| ADAPTER_AFTER                                                 | An adapter was detected after (3' to) this subread |             |
+---------------------------------------------------------------+----------------------------------------------------+-------------+
| BARCODE_BEFORE                                                | A barcode was detected before (5' to) this subread |             |
+---------------------------------------------------------------+----------------------------------------------------+-------------+
| BARCODE_AFTER                                                 | A barcode was detected after (3' to) this subread  |             |
+---------------------------------------------------------------+----------------------------------------------------+-------------+
| FORWARD_PASS                                                  | Subread is forward on the polymerase read          |             |
+---------------------------------------------------------------+----------------------------------------------------+-------------+
| REVERSE_PASS                                                  | Subread is forward on the polymerase read          |             |
+---------------------------------------------------------------+----------------------------------------------------+-------------+

For pbcore, all but 'cx' and 'bc' support the 'in' or '==' operator with vector values.
The 'cx' filters support '=', '!=', '&' and '~' operators, all potentially with values separated by '|' compositions
(see https://github.com/PacificBiosciences/pbcore/blob/master/tests/test_pbdataset_filters.py#L81 for examples)
and raw values or context flag strings (see https://github.com/PacificBiosciences/pbcore/blob/master/pbcore/io/dataset/DataSetMembers.py#L173).


Union of DataSets (aka Merging DataSets)
++++++++++++++++++++++++++++++++++++++++

Unions can be taken of DataSets with the same underlying file type (noted
by the MetaType attribute) and with identical Filters. The SubreadSet
above could be created by taking the union of two SubreadSets each
containing a single BAM file::

    <SubreadSet xmlns="http://pacificbiosciences.com/PacBioDataModel.xsd">
        <ExternalResources>
            <ExternalResource MetaType="SubreadFile.SubreadBamFile"
                               ResourceId="file:/mnt/path/to/subreads0.bam"/>
        </ExternalResources>
        <Filters>
            <Filter>
                <Parameter Name="rq" Value=">0.75"/>
            </Filter>
        </Filters>
        <DataSetMetadata>
            <TotalLength>3000</TotalLength>
            <NumRecords>300</NumRecords>
        </DataSetMetadata>
    </SubreadSet>


    <SubreadSet xmlns="http://pacificbiosciences.com/PacBioDataModel.xsd">
        <ExternalResources>
            <ExternalResource MetaType="SubreadFile.SubreadBamFile"
                               ResourceId="file:/mnt/path/to/subreads1.bam"/>
        </ExternalResources>
        <Filters>
            <Filter>
                <Parameter Name="rq" Value=">0.75"/>
            </Filter>
        </Filters>
        <DataSetMetadata>
            <TotalLength>2000</TotalLength>
            <NumRecords>200</NumRecords>
        </DataSetMetadata>
    </SubreadSet>

Union is also referred to as merging in many Secondary Analysis applications.

Tools that merge datasets together should propagate the original DataSet information in the subdatasets within the resulting dataset, following these practices:
 - Subdatasets should be created for each input DataSet when two or more files with no subdatasets are merged or used to create a new DataSet.
 - If in the process of merging a new DataSet is created, for example, wrapping a "naked" BAM file, a subdataset should be created for those inputs.
 - In no case should a subdataset be present if it is identical to the containing DataSet.
 - Subdatasets should be preserved when two datasets with subdatasets are merged together.

   - If both have subdatasets, the lists of subdatasets should be concatenated.
   - If one has no subdatasets, a subdataset should be created for that input and added to the list of subdatasets from the other input file.

- Subdatasets should be preserved during minor manipulations: Adding a filter, changing path absoluteness, adding or removing indices, references etc.
- Subdatasets should be removed during substantial transformations: alignment, producing an AlignmentSet from a SubreadSet.
- Subdatasets should be preserved during consolidation or splitting (except when splitting by subdataset).


Consolidating DataSets
++++++++++++++++++++++

Consolidating (aka Resolving) a DataSet means creating an explicit
representation in the appropriate format with all filters applied. Here
is consolidated version of the SubreadSet above::

    <?xml version="1.0" encoding="utf-8" ?>
    <SubreadSet xmlns="http://pacificbiosciences.com/PacBioDataModel.xsd">
        <ExternalResources>
            <ExternalResource
                MetaType="SubreadFile.SubreadBamFile"
                ResourceId="file:/mnt/path/to/subreads0_plus_subreads1.bam"/>
        </ExternalResources>
        <DataSetMetadata>
            <TotalLength>5000</TotalLength>
            <NumRecords>500</NumRecords>
        </DataSetMetadata>
    </SubreadSet>

Consolidated DataSets are useful for export of a DataSet that exists
only implicitly, e.g. by filtering multiple files. They allow the user
to incur the IO overhead of seeking over multiple files once at the
cost of increased disk usage.


Labelling subsets of DataSets
+++++++++++++++++++++++++++++

DataSets can contain other DataSets. These DataSets are defined relative
to the parent DataSet, and provide the ability to label subsets of the
parent. For example, in the following DataSet, all alignments to the
reference sequence labelled 2kbControl are labelled 'Control' using the
DataSet ``Name`` field::

    <?xml version="1.0" encoding="utf-8" ?>
    <AlignmentSet xmlns="http://pacificbiosciences.com/PacBioDataModel.xsd">
         ...
        <DataSets>
            <AlignmentSet Name="Control">
                <Filters>
                    <Filter>
                        <Parameter Name="RNAME" Value="2kbControl"/>
                    </Filter>
                </Filters>
            </AlignmentSet>
        </DataSets>
         ...
    </AlignmentSet>

2.3 I/O trade-offs using DataSets
---------------------------------
The DataSet model defers I/O operations by replacing up-front file merges
with downstream I/O operations that hit many different files. This allows
consumers to avoid explicit creation of files on disk and the resulting
redundant storage and costly write operations. For many uses this many-file
approach will be better than explicitly creating the file on disk,
but in some cases it may be desirable to incur the cost of accessing
and filtering multiple files once (e.g. to reduce disk seeks for highly
fragmented DataSets). Determining when the costs outweigh the benefits will
need practical investigation, but regardless the Consolidate operation
provides the means for using the form of DataSet that best fits a
particular use case.


2.4 Types of DataSets
---------------------

DataSets subtypes are defined for the most common "bread-and-butter"
entities consumed and produced by Secondary Analysis pipelines

    - SubreadSet - The basic sequence DataSet generated by the instrument.
    - CCSreadSet - CCS sequence data.
    - AlignmentSet - Aligned reads in BAM format.
    - ReferenceSet - The FASTA reference used by Resequencing, Base Mods,
      Minor Variants. Replaces the reference repository entries.
    - GmapReferenceSet - A FASTA ReferenceSet with a GMAP database.
    - ContigSet - Produced by HGAP or AHA.
    - BarcodeSet - The FASTA file used by barcode detection.

.. note:: Why include barcodes, contigs and references in the DataSet
    concept? Operations on these data types do not typically include the
    set operations such as subsetting, union or labelling of subsets, so why
    include them? The main motivation is to provide a standard interface for
    inputs to pbsmrtpipe and to represent these resources in a standard way
    in SMRT Portal. Rather than special casing these kinds of data in the
    GUI and the pipeline controller (as is done for references in SMRT Portal)
    or forcing these data into one-size fits all solutions (as is done for
    barcodes and contigs by treating them as references in SMRT Portal) making
    them DataSets allows us to treat them as just another subtype of the
    general DataSet concept.


2.5 Examples satisfying the motivating use cases
------------------------------------------------

- Refer to a **set of subreads** in multiple bax.h5 files.

The SubreadSet XML above satisfies this use case using BAM files instead of BAX files::

    <?xml version="1.0" encoding="utf-8" ?>
    <SubreadSet xmlns="http://pacificbiosciences.com/PacBioDataModel.xsd">
        <ExternalResources>
            <ExternalResource MetaType="SubreadFile.SubreadBamFile"
                              ResourceId="file:/mnt/path/to/subreads0.bam"/>
            <ExternalResource MetaType="SubreadFile.SubreadBamFile"
                              ResourceId="file:/mnt/path/to/subreads1.bam"/>
        </ExternalResources>
        <Filters>
            <Filter>
                <Parameter Name="rq" Value=">0.75"/>
            </Filter>
        </Filters>
        <DataSetMetadata>
            <TotalLength>5000</TotalLength>
            <NumRecords>500</NumRecords>
        </DataSetMetadata>
    </SubreadSet>


- Refer to a **subset of subreads** by id from one or more bas.h5 files::

    <?xml version="1.0" encoding="utf-8" ?>
    <SubreadSet xmlns="http://pacificbiosciences.com/PacBioDataModel.xsd">
        <ExternalResources>
            <ExternalResource MetaType="SubreadFile.SubreadBamFile"
                              ResourceId="file:/mnt/path/to/subreads0.bam"/>
        </ExternalResources>
        <Filters>
            <Filter>
                <Parameter Name="QNAME" Value="m100000/0/0_100"/>
            </Filter>
            <Filter>
                <Parameter Name="QNAME" Value="m100000/1/0_200"/>
            </Filter>
        </Filters>
        <DataSetMetadata>
            <TotalLength>5000</TotalLength>
            <NumRecords>500</NumRecords>
        </DataSetMetadata>
    </SubreadSet>


- Run algorithms such as HGAP on a **subset of subreads** (e.g. that align to a contaminant such as E. coli)
    - Use a SubreadSet filtered by RNAME.

- Refer to a **set of alignments** from multiple different references or movies - *Use an AlignmentSet with multiple reference files.*

- Run algorithms such as Arrow on a **subset of alignments** (e.g. on a particular chromosome, or a particular chromosome region, or from reads labeled with a particular barcode) - *Use an AlignmentSet filtered by RNAME.*

- Refer to a **subset of alignments** that obey certain criteria (e.g. the merge/extractBy functionality in Milhouse). - *Use an AlignmentSet filtered by e.g. RNAME.*

- Perform any analysis that can be performed on an entire file of a particular data type (reads, read regions, alignments) on a **subset of that data type** without creating a new file. - *Relies on tools using common APIs to access DataSets.*



DataSet MetaTypes and File Extensions
+++++++++++++++++++++++++++++++++++++

+-----------------------+------------------------------------------------+---------------------------+
| DataSet               | DataSet MetaType                               | DataSet XML File Extension|
+=======================+================================================+===========================+
| SubreadSet            | PacBio.DataSet.SubreadSet                      | .subreadset.xml           |
+-----------------------+------------------------------------------------+---------------------------+
| HdfSubreadSet         | PacBio.DataSet.HdfSubreadSet                   | .hdfsubreadset.xml        |
+-----------------------+------------------------------------------------+---------------------------+
| AlignmentSet          | PacBio.DataSet.AlignmentSet                    | .alignmentset.xml         |
+-----------------------+------------------------------------------------+---------------------------+
| BarcodeSet            | PacBio.DataSet.BarcodeSet                      | .barcodeset.xml           |
+-----------------------+------------------------------------------------+---------------------------+
| ConsensusReadSet      | PacBio.DataSet.ConsensusReadSet                | .consensusreadset.xml     |
+-----------------------+------------------------------------------------+---------------------------+
| ConsensusAlignmentSet | PacBio.DataSet.ConsensusAlignmentSet           | .consensusalignmentset.xml|
+-----------------------+------------------------------------------------+---------------------------+
| ContigSet             | PacBio.DataSet.ContigSet                       | .contigset.xml            |
+-----------------------+------------------------------------------------+---------------------------+
| ReferenceSet          | PacBio.DataSet.ReferenceSet                    | .referenceset.xml         |
+-----------------------+------------------------------------------------+---------------------------+
| GmapReferenceSet      | PacBio.DataSet.GmapReferenceSet                | .gmapreferenceset.xml     |
+-----------------------+------------------------------------------------+---------------------------+


DataSet External Resource MetaTypes and File Extensions
+++++++++++++++++++++++++++++++++++++++++++++++++++++++

+-----------------------+------------------------------------------------+---------------------------+
| DataSet               | ExternalResource MetaType                      | File Extensions           |
+=======================+================================================+===========================+
| SubreadSet            | PacBio.SubreadFile.SubreadBamFile              | .bam                      |
+-----------------------+------------------------------------------------+---------------------------+
| HdfSubreadSet         | PacBio.SubreadFile.BaxFile                     | .bax.h5                   |
+-----------------------+------------------------------------------------+---------------------------+
| AlignmentSet          | PacBio.AlignmentFile.AlignmentBamFile          | .bam, .cmp.h5             |
+-----------------------+------------------------------------------------+---------------------------+
| BarcodeSet            | PacBio.BarcodeFile.BarcodeFastaFile            | .fasta                    |
+-----------------------+------------------------------------------------+---------------------------+
| ConsensusReadSet      | PacBio.ConsensusReadFile.ConsensusReadBamFile  | .bam                      |
+-----------------------+------------------------------------------------+---------------------------+
| ConsensusAlignmentSet | PacBio.AlignmentFile.ConsensusAlignmentBamFile | .bam                      |
+-----------------------+------------------------------------------------+---------------------------+
| ContigSet             | PacBio.ContigFile.ContigFastaFile              | .fasta                    |
+-----------------------+------------------------------------------------+---------------------------+
| ReferenceSet          | PacBio.ReferenceFile.ReferenceFastaFile        | .fasta                    |
+-----------------------+------------------------------------------------+---------------------------+

SubreadSet Special Purpose ExternalResources:
    - PacBio.SubreadFile.ScrapsBamFile
    - PacBio.SubreadFile.HqRegionBamFile
    - PacBio.SubreadFile.HqScrapsBamFile
    - PacBio.SubreadFile.LqRegionBamFile
    - PacBio.SubreadFile.LqScrapsBamFile
    - PacBio.SubreadFile.PolymeraseBamFile
    - PacBio.SubreadFile.PolymeraseScrapsBamFile
    - PacBio.SubreadFile.ChipStatsFile (.sts.xml)
    - PacBio.SubreadFile.ChipStatsH5File (.sts.h5)
    - PacBio.SubreadFile.AdapterFastaFile
    - PacBio.SubreadFile.ControlFastaFile

Bam-Related Special Purpose ExternalResources:
    - PacBio.Index.BamIndex (.bam.bai)
    - PacBio.Index.PacBioIndex (.bam.pbi)

Fasta-Related Special Purpose ExternalResources:
    - PacBio.Index.SamIndex (.fasta.fai)
    - PacBio.Index.SaWriterIndex (.fasta.sa)
    - PacBio.Index.Indexer (.fasta.index)
    - PacBio.Index.FastaContigIndex (.fasta.contig.index)
    - PacBio.GmapDB.GmapDBSummary (a file indicating the location of a gmap db)

DataSet UI Name and Time Stamped Name
+++++++++++++++++++++++++++++++++++++

The pattern for time stamped names generated by secondary should be:

<metatype>-<yymmdd_HHmmssttt>

Where metatype has been transformed into a lowercase, underscore separated
string and the time string format directives map to the following entities:
year, month, day, hour, minute, second, millisecond.

+-----------------------+--------------------------------------------------------+-------------------+
| DataSet               | TimeStampedName                                        | DataSet UI Name   |
+=======================+========================================================+===================+
| SubreadSet            | pacbio_dataset_subreadset-<yymmdd_HHmmssttt>           | TBD               |
+-----------------------+--------------------------------------------------------+-------------------+
| HdfSubreadSet         | pacbio_dataset_hdfsubreadset-<yymmdd_HHmmssttt>        | TBD               |
+-----------------------+--------------------------------------------------------+-------------------+
| AlignmentSet          | pacbio_dataset_alignmentset-<yymmdd_HHmmssttt>         | TBD               |
+-----------------------+--------------------------------------------------------+-------------------+
| BarcodeSet            | pacbio_dataset_barcodeset-<yymmdd_HHmmssttt>           | TBD               |
+-----------------------+--------------------------------------------------------+-------------------+
| ConsensusReadSet      | pacbio_dataset_consensusreadset-<yymmdd_HHmmssttt>     | TBD               |
+-----------------------+--------------------------------------------------------+-------------------+
| ConsensusAlignmentSet | pacbio_dataset_consensusalignmentset-<yymmdd_HHmmssttt>| TBD               |
+-----------------------+--------------------------------------------------------+-------------------+
| ContigSet             | pacbio_dataset_contigset-<yymmdd_HHmmssttt>            | TBD               |
+-----------------------+--------------------------------------------------------+-------------------+
| ReferenceSet          | pacbio_dataset_referenceset-<yymmdd_HHmmssttt>         | TBD               |
+-----------------------+--------------------------------------------------------+-------------------+


2.6 Support for the DataSet XML
--------------------------------------------------------

Support for using the DataSet XML throughout the Secondary Analysis stack:

Core API
++++++++

An API will be provided that makes consuming DataSet XML files or the
underlying files such as BAM as burden-free as possible.

Command-line tools for manipulating DataSets
++++++++++++++++++++++++++++++++++++++++++++

At minimum, 2.0.0 will have the following command-line support::

    dataset.py create subreads.fofn > subreads.xml
    dataset.py filter subreads.xml --parameter "name=rq,value=>0.75" > filtered_subreads.xml
    dataset.py union subreads1.xml subreads2.xml > subreads_union.xml
    dataset.py consolidate subreads1.xml > consolidated_subreads.xml

.. note:: TODO This section needs more detail. Add specs for tools needed
          for creating and manipulating DataSets on the command line.

.. note:: While technically an XML file with multiple DataSet elements is
          valid under the XSD, it is expected that the command line use
          cases will follow 1 XML file - 1 DataSet element convention.


Other Bioinformatics Tools
++++++++++++++++++++++++++

All bioinformatics tools that consume DataSet XML files should be
capable of producing identical results using the equivalent BAM or
FASTA file generated after applying all filters. In other words, the
DataSet XML is not required to obtain bioinformatics results. However,
`support` for the DataSet XML is encouraged for Secondary Analysis tools,
and facilitated using the above API.

SMRT Portal and SMRT Pipe
+++++++++++++++++++++++++

The DataSet XML is required for display of DataSets (such as
references) in SMRT Portal and for chunking in the distributed pipelines
using pbsmrtpipe. Moreover, for these applications the DataSetMetadata
field is mandatory, not optional.

2.7 DataSet mutability and equality
-----------------------------------
To allow user editing of attributes such as Name without affecting the
underlying DataSet we define the Core DataSet as the XML with the user
editable attributes (Name, Description and Tags) removed (not set to "",
but absent).  This Core DataSet is immutable and is the entity on which
identity operations will be defined. As a consequence, any modifications
to fields other than Name, Description or Tags requires giving the DataSet
a new UniqueId. Operations such as md5 checksum should be performed on
the Core DataSet unless otherwise specified.


3. Outstanding Issues and Future Directions
===========================================

- Document FASTA filters for pbcore / pbbam for releases post-4.0.
- The propagation of subdatasets in merging can result in rather large XML files with duplicated information. It is possible this duplication could be reduced using XML IDREFs from the subdatasets to information in the top level DataSet, for ExternalResources or CollectionMetadata. This should be considered as a possible future revision.

Appendix 1: Example DataSet XML files
=====================================

Here are some example XML files for each of the above DataSets

.. include:: examples/datasets/subread.rst
.. include:: examples/datasets/ccsread.rst
.. include:: examples/datasets/alignment.rst
.. include:: examples/datasets/reference.rst
.. include:: examples/datasets/contig.rst
.. include:: examples/datasets/barcode.rst

Appendix 2: Use cases from pre-2.0 Secondary Analysis satisfied by the DataSet XML files
========================================================================================

- Refer to a **set of subreads** in multiple bax.h5 files
    - FOFN of bax.h5 files (for blasr)
    - input.xml of bax.h5 files (for SMRT Pipe)

- Refer to a **subset of subreads** by id from one or more bas.h5 files
    - Whitelist option to P_Filter to generate a FOFN of rgn.h5 files + FOFN of
      bas.h5 files

- Refer to a **set of alignments** from multiple different references or movies
    - Explicitly merge the alignments into a larger (cmp.h5) alignment file
    - Create FOFN of cmp.h5 files

- Run algorithms such as HGAP on a **subset of subreads** (e.g. that align to a contaminant such as E. coli)
    - Awkward, but supported indirectly though whitelist option to P_Filter

- Run algorithms such as Quiver on a **subset of alignments** (e.g. on a particular chromosome, or a particular chromosome region, or from reads labeled with a particular barcode)
    - Command line options to Quiver (to e.g. specify a particular reference). Not currently supported on other algorithms.

- Refer to a **subset of alignments** that obey certain criteria. In particular,  the extractBy reference or accuracy functionality used in Milhouse.
    - Explicit creation of cmp.h5 files using cmph5tools.py select.


- Perform any analysis that can be performed on an entire file of a particular data type (reads, read regions, alignments) on a **subset of that data type**   without creating a new file.
    - Not supported pre-2.0.


.. _W3C compatible timestamp: http://www.w2.org/TR/NOTE-datetime
