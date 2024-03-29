============================
DataSet format specification
============================

A PacBio DataSet is an XML file representing a set of a particular sequence data type
such as subreads, references or aligned subreads. The actual data elements
contained in a DataSet are stored in files referred to by the XML, usually in FASTA or BAM files.
The DataSet can optionally filter these files or store metadata about their contents.


Version
=======

This document defines the 4.0.1 SMRT Link DataSet abstraction and its
XML file representation. The 4.0.1 format is produced by the 10.0.0 release of PacBio
Primary Analysis and SMRT Link software.


Motivating Use Cases
====================

The concept of a homogenous set of elements of a particular data type is
used throughout Pacific Biosciences software.
These "sets of data" have historically been represented in
different ways, sometimes explicitly by creating large files
that contain all the data in the set (e.g. a FASTA file of subreads),
and sometimes implicitly by using pointers to the data, such as with a FOFN
(file of file names).

In many cases these solutions are serviceable, but they have
disadvantages. The reliance on explicit file creation imposes a heavy
burden that will be exacerbated by future instrument throughput increases. The
FOFN partially breaks the tight coupling between explicit files and
sets of data, but it fails to allow facile subsetting of files. With previous methods,
consuming tools were forced to reimplement filtering or subsetting logic in their own
idiosyncratic ways.

The DataSet XML abstraction (or DataSet for short) addresses these problems
by providing a standard way to perform the following activities\:

- Refer to a **set of subreads** in multiple BAM files
- Refer to a **subset of subreads** by id from one or more BAM files
- Refer to a **subset of alignments** for input to algorithms such as Arrow (e.g. on a
  particular chromosome, or a particular chromosome region)
- Perform any analysis that can be performed on an entire file of a particular
  data type (subreads, alignments) on a **subset of that data type**  without creating a new file.


Format Definition
=================


XML Representation
----------------------

The canonical representation of a DataSet is an XML file that
contains a single DataSet element with four major sections, one mandatory
and three optional\:

1.  A mandatory ``<pbbase:ExternalResources>`` section with references to external
    data sources in BAM or FASTA format and their associated indices or metadata files.
    The records in these files are the elements of the set of data represented by the DataSet.

2.  An optional ``<pbds:Filters>`` section that filters or subsets the elements
    of the set in the above files, for example by length.

3.  An optional ``<pbds:DataSetMetadata>`` section that contains metadata about
    the DataSet, usually at minimum the number of records and their total
    length, but possibly much more. For example, subread and CCS
    read DataSets have metadata regarding instrument collection or
    biological samples. The Metadata section should be considered
    to refer to the DataSet elements prior to applying Filters.

4.  An optional ``<pbds:DataSets>`` section that can be used to annotate subsets of the
    top-level DataSet. For example, a DataSet that resulted from merging multiple DataSets
    can store a record of the original DataSets in this section, along with their original metadata.

5.  An optional ``<pbbase:SupplementalResources>`` section with references to
    external data or metadata sources in any format, separate from the main
    data files in ExternalResources, but represented using the same
    ``<pbbase:ExternalResource>`` model. This may include files such as
    reports or unbarcoded reads BAM.


Types of DataSets
---------------------

The DataSet XSD_ defines DataSet subclasses for the most common entities consumed and produced by SMRT Analysis pipelines\:

- ConsensusReadSet - CCS (usually HiFi) sequence data in BAM format. This is
  the type of dataset delivered by our current generation of instruments.
- BarcodeSet - The FASTA file and metadata used by barcode detection.
- ReferenceSet - The FASTA reference and associated indices used by pbmm2
  and related tools.
- SubreadSet - This type of DataSet was produced by the Sequel I and II
  instruments. Note that the prefix "Sub" in this case is part of "Subread",
  and does not in any way denote a "subset".
- ConsensusAlignmentSet - Aligned CCS data in BAM format.
- AlignmentSet - Aligned subreads in BAM format.
- TranscriptSet - Processed RNA transcripts in BAM format.
- TranscriptAlignmentSet - Processed and aligned RNA transcripts in BAM format.
- ContigSet - Any FASTA containing contigs.  No longer in production use.

Only the first three types are supported as input to SMRT Link workflows.
Previous versions of SMRT Link also supported HdfSubreadSet and
GmapReferenceSet types, but these have been removed from the system.

SubreadSet example
---------------------

Here is a simple example of a DataSet XML using a SubreadSet containing all four
sections. It creates a set of subreads from two subread BAM files and
associated indices and filters the subreads by quality using the ``rq`` field of the underlying
BAM records::

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
        Version="4.0.1"
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
    </pbds:SubreadSet>



Operations on DataSets
--------------------------

DataSets support operations that would naively be expected of sets, such
as subsetting and union (although notably not intersection) as well as
some additional operations such as consolidation.
The result of performing these operations is itself a new DataSet, with the
operations included as a kind of "recipe" for producing the new DataSet from the original.
Because of this, operations are presented here as part of the DataSet format.


Subsetting (Filtering)
++++++++++++++++++++++

The SubreadSet example given above is the result of applying a length subset or ``Filter`` operation
on a DataSet of two BAM files (e.g. by applying the dataset_ command).

Each ``Filter`` is composed of ``Property`` tags representing logical predicates that elements of the DataSet must
satisfy. ``Property`` tags are defined by three attributes: ``Name``, ``Operator`` and ``Value``, where the ``Name``
refers to a field or derived value from individual DataSet records, and the ``Operator`` is used to compare a particular record's
field with the ``Value`` attribute. Individual ``Filter`` tags can be combined to create more complicated filters; these ``Filter`` tags are
logically "ORed" while individual ``Property`` tags within a ``Filter`` are "ANDed" together.

In summary, the ``Filter`` and ``Property`` tags provide a powerful means of subsetting DataSets without manipulating
the underlying file representations.


*Filter Property Names and Values*
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The following table shows ``Property`` ``Name``'s that are supported by either the pbbam C++ API, the pbcore Python API (*italicized*)
or both (**bold**). Some accepted alternative ways of representing a ``Property`` are given in the Alternative Names column.
Those ``Property``'s that allow list values in both pbbam and pbcore are indicated by brackets.
Finally, the right column shows the allowed type of ``Property`` ``Value`` associated with that particular ``Property`` ``Name``.

+---------------+------------------------------------------------+-------------------------+-----------+
| Property Name | Description                                    | Alternative Names       | Value     |
+===============+================================================+=========================+===========+
| **readstart** | Alignment start                                | astart  as              | uint32_t  |
+---------------+------------------------------------------------+-------------------------+-----------+
| ae            | Alignment end                                  | aend                    | uint32_t  |
+---------------+------------------------------------------------+-------------------------+-----------+
| alignedlength | Alignment length                               |                         | uint32_t  |
+---------------+------------------------------------------------+-------------------------+-----------+
| **accuracy**  | Alignment identity                             | identity                | float     |
+---------------+------------------------------------------------+-------------------------+-----------+
| **qname**     | Query name                                     | *qid*                   | string    |
+---------------+------------------------------------------------+-------------------------+-----------+
| **qstart**    | Query start                                    | **qs**                  | int       |
+---------------+------------------------------------------------+-------------------------+-----------+
| **qend**      | Query end                                      | **qe**                  | int       |
+---------------+------------------------------------------------+-------------------------+-----------+
| **length**    | Query length                                   | querylength             | int       |
+---------------+------------------------------------------------+-------------------------+-----------+
| **rname**     | Reference name                                 |                         | string    |
+---------------+------------------------------------------------+-------------------------+-----------+
| **tstart**    | Reference start                                | ts  **pos**             | uint32_t  |
+---------------+------------------------------------------------+-------------------------+-----------+
| **tend**      | Reference end                                  | te                      | uint32_t  |
+---------------+------------------------------------------------+-------------------------+-----------+
| qname_file    | Query names from a file                        |                         | filename  |
+---------------+------------------------------------------------+-------------------------+-----------+
| **rq**        | Predicted read quality                         |                         | float     |
+---------------+------------------------------------------------+-------------------------+-----------+
| **movie**     | Movie name (e.g. m150404_101626_42267_s1_p0)   |                         | string    |
+---------------+------------------------------------------------+-------------------------+-----------+
| **zm**        | ZMW (e.g. m150404_101626_42267_s1_p0/100)      | zmw                     | string[]  |
+---------------+------------------------------------------------+-------------------------+-----------+
| **bc**        | Barcode name                                   | barcode                 | string[]  |
+---------------+------------------------------------------------+-------------------------+-----------+
| **bcq**       | Barcode quality                                | **bq**                  | uint8_t   |
+---------------+------------------------------------------------+-------------------------+-----------+
| **bcf**       | Barcode forward                                |                         | string[]  |
+---------------+------------------------------------------------+-------------------------+-----------+
| **bcr**       | Barcode reverse                                |                         | string[]  |
+---------------+------------------------------------------------+-------------------------+-----------+
| **cx**        | Local context (see below for special Values)   |                         | see below |
+---------------+------------------------------------------------+-------------------------+-----------+
| *n_subreads*  | Number of subreads                             |                         | int       |
+---------------+------------------------------------------------+-------------------------+-----------+
| *mapqv*       | Mapping quality                                |                         | int       |
+---------------+------------------------------------------------+-------------------------+-----------+


*Filter Property Operators*
~~~~~~~~~~~~~~~~~~~~~~~~~~~

The following table shows supported ``Property`` ``Operator``'s\:

+---------------------------------------------------------------+----------------------------------------------------+-------------+
| Property Operator                                             | Description                                        | Other Names |
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


*Possible cx Values*
~~~~~~~~~~~~~~~~~~~~~~~~~~~

The following table shows ``Values``'s that are supported for the ``cx`` local context ``Property`` ``Name``.
The ``Value``'s can be used individually or can be combined to form a compound ``Value`` using a syntax that
looks and behaves similarly to OR-ing bitflags, e.g.\:

    ``Value='ADAPTER_BEFORE | ADAPTER_AFTER'``

+---------------------------------------------------------------+----------------------------------------------------+
| cx Value                                                      | Description                                        |
+===============================================================+====================================================+
| NO_LOCAL_CONTEXT                                              | No local context (e.g. adapters or barcodes)       |
+---------------------------------------------------------------+----------------------------------------------------+
| ADAPTER_BEFORE                                                | An adapter was detected before (5' to) the subread |
+---------------------------------------------------------------+----------------------------------------------------+
| ADAPTER_AFTER                                                 | An adapter was detected after (3' to) this subread |
+---------------------------------------------------------------+----------------------------------------------------+
| BARCODE_BEFORE                                                | A barcode was detected before (5' to) this subread |
+---------------------------------------------------------------+----------------------------------------------------+
| BARCODE_AFTER                                                 | A barcode was detected after (3' to) this subread  |
+---------------------------------------------------------------+----------------------------------------------------+
| FORWARD_PASS                                                  | Subread is forward on the polymerase read          |
+---------------------------------------------------------------+----------------------------------------------------+
| REVERSE_PASS                                                  | Subread is forward on the polymerase read          |
+---------------------------------------------------------------+----------------------------------------------------+


*Filtering and the pbi*
~~~~~~~~~~~~~~~~~~~~~~~
The subsetting/filtering operation is supported efficiently by the
PacBio index (\*.pbi files). The contents of DataSet after applying ``Filter``'s
should in general be decidable using the contents of the pbi file (``rname`` is the one
exception in 4.0 and requires examination of the BAM file header).


Union (Merging)
+++++++++++++++

Unions can be taken of DataSets with the same underlying file type (noted
by the MetaType attribute) and with identical ``Filter``'s. The output of a
union (or merge) operation is a *single* new DataSet XML file containing a *single*
new top-level DataSet element--notably not multiple top-level elements.
For example, the SubreadSet above could be created by taking the union of two SubreadSets each
containing a single BAM file::

    <pbds:SubreadSet xmlns="http://pacificbiosciences.com/PacBioDatasets.xsd">
        <pbbase:ExternalResources>
            <pbbase:ExternalResource MetaType="SubreadFile.SubreadBamFile"
                               ResourceId="file:/mnt/path/to/subreads0.bam"/>
        </pbbase:ExternalResources>
        <pbds:Filters>
            <pbds:Filter>
                <pbbase:Properties>
                    <pbbase:Property Name="rq" Operator="gt" Value="0.75"/>
                </pbbase:Properties>
            </pbds:Filter>
        </pbds:Filters>
        <pbds:DataSetMetadata>
            <pbbase:TotalLength>3000</pbbase:TotalLength>
            <pbbase:NumRecords>300</pbbase:NumRecords>
        </pbds:DataSetMetadata>
    </pbds:SubreadSet>


    <pbds:SubreadSet xmlns="http://pacificbiosciences.com/PacBioDatasets.xsd">
        <pbbase:ExternalResources>
            <pbbase:ExternalResource MetaType="SubreadFile.SubreadBamFile"
                               ResourceId="file:/mnt/path/to/subreads1.bam"/>
        </pbbase:ExternalResources>
        <pbds:Filters>
            <pbds:Filter>
                <pbbase:Properties>
                    <pbbase:Property Name="rq" Operator="gt" Value="0.75"/>
                </pbbase:Properties>
            </pbds:Filter>
        </pbds:Filters>
        <pbds:DataSetMetadata>
            <pbbase:TotalLength>2000</pbbase:TotalLength>
            <pbbase:NumRecords>200</pbbase:NumRecords>
        </pbds:DataSetMetadata>
    </pbds:SubreadSet>


Tools that merge multiple DataSets together can optionally store the original input DataSets
in the DataSets tag of the output DataSet. In this way the original DataSets are maintained
as "subdatasets" of the new DataSet. Merging tools should adhere to the following best practices\:

- Subdatasets should be created for each input DataSet when two or more files with no subdatasets are merged or used to create a new DataSet.
- If in the process of merging a new DataSet is created, for example, wrapping a "naked" BAM file, a subdataset should be created for those inputs.
- In no case should a subdataset be present if it is identical to the containing DataSet.
- Subdatasets should be preserved when two datasets with subdatasets are merged together.
- If both have subdatasets, the lists of subdatasets should be concatenated.
- If one has no subdatasets, a subdataset should be created for that input and added to the list of subdatasets from the other input file.
- Subdatasets should be preserved during minor manipulations: Adding a filter, changing path absoluteness, adding or removing indices, references etc.
- Subdatasets should be removed during substantial transformations: alignment, producing an AlignmentSet from a SubreadSet.
- Subdatasets should be preserved during consolidation or splitting (except when splitting by subdataset).


Consolidating
+++++++++++++

Consolidating (aka Resolving) a DataSet means creating an explicit
representation in the appropriate format with all filters applied. In practice,
this means building a single BAM file containing all the records implied by the DataSet's
``ExternalResource`` and ``Filter`` directives. Here is consolidated version of the
SubreadSet above::

    <?xml version="1.0" encoding="utf-8" ?>
    <pbds:SubreadSet xmlns="http://pacificbiosciences.com/PacBioDatasets.xsd">
        <pbbase:ExternalResources>
            <pbbase:ExternalResource
                MetaType="SubreadFile.SubreadBamFile"
                ResourceId="file:/mnt/path/to/subreads0_plus_subreads1.bam"/>
        </pbbase:ExternalResources>
        <pbds:DataSetMetadata>
            <pbbase:TotalLength>5000</pbbase:TotalLength>
            <pbbase:NumRecords>500</pbbase:NumRecords>
        </pbds:DataSetMetadata>
    </pbds:SubreadSet>

Consolidated DataSets are useful for export of a DataSet that exists
only implicitly, e.g. by filtering multiple files. They allow the user
to incur the IO overhead of seeking over multiple files once at the
cost of increased disk usage.

DataSet MetaTypes and File Extensions
-------------------------------------

The following table lists the DataSet subclasses defined by the XSD and their associated ``MetaType``
values and expected filename suffix strings. While technically the information conveyed by the ``MetaType`` and suffix
is redundant, it is useful for some downstream consuming tools, and to be fully compliant with this specification
all three should be consistent.

+------------------------+------------------------------------------------+-----------------------------+
| DataSet                | DataSet MetaType                               | DataSet XML File Extension  |
+========================+================================================+=============================+
| ConsensusReadSet       | PacBio.DataSet.ConsensusReadSet                | .consensusreadset.xml       |
+------------------------+------------------------------------------------+-----------------------------+
| BarcodeSet             | PacBio.DataSet.BarcodeSet                      | .barcodeset.xml             |
+------------------------+------------------------------------------------+-----------------------------+
| ReferenceSet           | PacBio.DataSet.ReferenceSet                    | .referenceset.xml           |
+------------------------+------------------------------------------------+-----------------------------+
| ConsensusAlignmentSet  | PacBio.DataSet.ConsensusAlignmentSet           | .consensusalignmentset.xml  |
+------------------------+------------------------------------------------+-----------------------------+
| SubreadSet             | PacBio.DataSet.SubreadSet                      | .subreadset.xml             |
+------------------------+------------------------------------------------+-----------------------------+
| AlignmentSet           | PacBio.DataSet.AlignmentSet                    | .alignmentset.xml           |
+------------------------+------------------------------------------------+-----------------------------+
| TranscriptSet          | PacBio.DataSet.TranscriptSet                   | .transcriptset.xml          |
+------------------------+------------------------------------------------+-----------------------------+
| TranscriptAlignmentSet | PacBio.DataSet.TranscriptAlignmentSet          | .transcriptalignmentset.xml |
+------------------------+------------------------------------------------+-----------------------------+
| ContigSet              | PacBio.DataSet.ContigSet                       | .contigset.xml              |
+-----------------------+------------------------------------------------+------------------------------+


DataSet External Resource MetaTypes and File Extensions
+++++++++++++++++++++++++++++++++++++++++++++++++++++++

The following table lists the ``ExternalResource``'s expected by each DataSet subclass and their
associated ``MetaType`` values and expected filename suffix strings.
In some cases the ``ExternalResource`` can occur in multiple DataSet types, but only for particular
parent ``ExternalResource``'s elements. Note that while this specification allows ``ExternalResource``'s
to in some cases refer to other DataSets, they should in no cases refer to a DataSet of the same type as the parent
(e.g. SubreadSet's should not refer to external SubreadSet's).

+------------------------+-------------------------------------------------+---------------------------+
| DataSet or Tag         | ExternalResource MetaType                       | File Extensions           |
+========================+=================================================+===========================+
| SubreadSet             | PacBio.SubreadFile.SubreadBamFile               | .bam                      |
+------------------------+-------------------------------------------------+---------------------------+
|                        | PacBio.SubreadFile.ScrapsBamFile                | .bam                      |
+------------------------+-------------------------------------------------+---------------------------+
|                        | PacBio.SubreadFile.HqRegionBamFile              | .bam                      |
+------------------------+-------------------------------------------------+---------------------------+
|                        | PacBio.SubreadFile.HqScrapsBamFile              | .bam                      |
+------------------------+-------------------------------------------------+---------------------------+
|                        | PacBio.SubreadFile.LqRegionBamFile              | .bam                      |
+------------------------+-------------------------------------------------+---------------------------+
|                        | PacBio.SubreadFile.LqScrapsBamFile              | .bam                      |
+------------------------+-------------------------------------------------+---------------------------+
|                        | PacBio.SubreadFile.PolymeraseBamFile            | .bam                      |
+------------------------+-------------------------------------------------+---------------------------+
|                        | PacBio.SubreadFile.PolymeraseScrapsBamFile      | .bam                      |
+------------------------+-------------------------------------------------+---------------------------+
|                        | PacBio.SubreadFile.ChipStatsFile                | .sts.xml                  |
+------------------------+-------------------------------------------------+---------------------------+
|                        | PacBio.SubreadFile.ChipStatsH5File              | .sts.h5                   |
+------------------------+-------------------------------------------------+---------------------------+
|                        | PacBio.SubreadFile.AdapterFastaFile             | .fasta                    |
+------------------------+-------------------------------------------------+---------------------------+
|                        | PacBio.SubreadFile.ControlFastaFile             | .fasta                    |
+------------------------+-------------------------------------------------+---------------------------+
| AlignmentSet           | PacBio.AlignmentFile.AlignmentBamFile           | .bam                      |
+------------------------+-------------------------------------------------+---------------------------+
| BarcodeSet             | PacBio.BarcodeFile.BarcodeFastaFile             | .fasta                    |
+------------------------+-------------------------------------------------+---------------------------+
| ConsensusReadSet       | PacBio.ConsensusReadFile.ConsensusReadBamFile   | .bam                      |
+------------------------+-------------------------------------------------+---------------------------+
| ConsensusAlignmentSet  | PacBio.AlignmentFile.ConsensusAlignmentBamFile  | .bam                      |
+------------------------+-------------------------------------------------+---------------------------+
| TranscriptSet          | PacBio.TranscriptFile.TranscriptBamFile         | .bam                      |
+------------------------+-------------------------------------------------+---------------------------+
| TranscriptAlignmentSet | PacBio.AlignmentFile.TranscriptAlignmentBamFile | .bam                      |
+------------------------+-------------------------------------------------+---------------------------+
| ContigSet              | PacBio.ContigFile.ContigFastaFile               | .fasta                    |
+------------------------+-------------------------------------------------+---------------------------+
| ReferenceSet           | PacBio.ReferenceFile.ReferenceFastaFile         | .fasta                    |
+------------------------+-------------------------------------------------+---------------------------+
| Bam ExternalResource   | PacBio.Index.BamIndex                           | .bam.bai                  |
+------------------------+-------------------------------------------------+---------------------------+
|                        | PacBio.Index.PacBioIndex                        | .bam.pbi                  |
+------------------------+-------------------------------------------------+---------------------------+
| Fasta ExternalResource | PacBio.Index.SamIndex                           | .fasta.fai                |
+------------------------+-------------------------------------------------+---------------------------+
|                        | PacBio.Index.SaWriterIndex                      | .fasta.sa                 |
+------------------------+-------------------------------------------------+---------------------------+
|                        | PacBio.GmapDB.GmapDBSummary                     | ?                         |
+------------------------+-------------------------------------------------+---------------------------+
|                        | PacBio.Index.NgmlrRefEncoded                    | .ngm                      |
+------------------------+-------------------------------------------------+---------------------------+
|                        | PacBio.Index.NgmlrRefTable                      | .ngm                      |
+------------------------+-------------------------------------------------+---------------------------+
| ReferenceSet           | PacBio.ReferenceFile.ReferenceAnnotationFile    | .gtf                      |
+------------------------+-------------------------------------------------+---------------------------+
| ReferenceSet           | PacBio.ReferenceFile.PolyAMotifFile             | .txt                      |
+------------------------+-------------------------------------------------+---------------------------+
| ReferenceSet           | PacBio.ReferenceFile.CagePeakFile               | .bed                      |
+------------------------+-------------------------------------------------+---------------------------+
| ReferenceSet           | PacBio.ReferenceFile.IntropolisFile             | .tsv                      |
+------------------------+-------------------------------------------------+---------------------------+
| ReferenceSet           | PacBio.Index.PigeonIndex                        | .pgi                      |
+------------------------+-------------------------------------------------+---------------------------+

Some ``ExternalResource``'s themselves contain associated ``ExternalResources``'s, for example the
indices associated with FASTA files. These associated files are nested within the primary ``ExternalResource``
element to denote their subsidiary nature.


Time Stamped Name
+++++++++++++++++

The pattern for ``TimeStampedName`` attribute generated by production PacBio tools should be\:

<metatype>-<yymmdd_HHmmssttt>

Where ``MetaType`` has been transformed into a lowercase, underscore separated
string and the time string format directives map to the following entities\: year, month, day, hour,
minute, second, millisecond.

+------------------------+----------------------------------------------------------+-------------------+
| DataSet                | TimeStampedName                                          |
+========================+==========================================================+
| ConsensusReadSet       | pacbio_dataset_consensusreadset-<yymmdd_HHmmssttt>       |
+------------------------+----------------------------------------------------------+
| BarcodeSet             | pacbio_dataset_barcodeset-<yymmdd_HHmmssttt>             |
+------------------------+----------------------------------------------------------+
| ReferenceSet           | pacbio_dataset_referenceset-<yymmdd_HHmmssttt>           |
+------------------------+----------------------------------------------------------+
| ConsensusAlignmentSet  | pacbio_dataset_consensusalignmentset-<yymmdd_HHmmssttt>  |
+------------------------+----------------------------------------------------------+
| SubreadSet             | pacbio_dataset_subreadset-<yymmdd_HHmmssttt>             |
+------------------------+----------------------------------------------------------+
| AlignmentSet           | pacbio_dataset_alignmentset-<yymmdd_HHmmssttt>           |
+------------------------+----------------------------------------------------------+
| TranscriptSet          | pacbio_dataset_transcriptset-<yymmdd_HHmmssttt>          |
+------------------------+----------------------------------------------------------+
| TranscriptAlignmentSet | pacbio_dataset_transcriptalignmentset-<yymmdd_HHmmssttt> |
+------------------------+----------------------------------------------------------+
| ContigSet              | pacbio_dataset_contigset-<yymmdd_HHmmssttt>              |
+------------------------+----------------------------------------------------------+

Note that all PacBio.Index.\* ``ExternalResource``'s are given a ``TimeStampedName`` attribute
with an ``"index-"`` prefix.


Singleton DataSet element
-------------------------

While technically an XML file with multiple DataSet elements is valid under the XSD and this spec,
in practice PacBio tools follow a one DataSet element per XML file convention.


Support for the DataSet XML
=======================================================

Support exists for using the DataSet XML throughout the SMRT Analysis stack.


The ``dataset`` command-line tool
---------------------------------

The SMRT Link CL tools (in ``$SMRT_ROOT/smrtcmds/bin``) provide command-line
support for creating, filtering, validating,
merging, splitting, consolidating and other common operations via the ``dataset`` command.  Run ``dataset --help`` to see a list of supported sub-commands.


Core API Support
-----------------

An API is provided in pbcore_ (Python) and pbbam_ (C++) that makes consuming DataSet XML files or the
underlying files such as BAM as burden-free as possible.


Other PacBio command-line tools
--------------------------------

All bioinformatics tools that consume DataSet XML files should be
capable of producing identical results using the equivalent BAM or
FASTA file generated after applying all filters. In other words, the
DataSet XML is not required to obtain bioinformatics results. However,
`support` for the DataSet XML is encouraged for SMRT Analysis tools,
and facilitated using the above API.


SMRT Link integration and workflows
-----------------------------------

The DataSet XML is required for display of DataSets (such as HiFi reads or
references) in SMRT Link and for chunking in the distributed pipelines
using pbsmrtpipe. Moreover, for these applications the DataSetMetadata
field is mandatory, not optional.


Other topics
==============


Mutability and equality
-----------------------
To allow user editing of attributes such as Name without affecting the
underlying DataSet we define the Core DataSet as the XML with the user
editable attributes (Name, Description and Tags) removed (not set to "",
but absent). This Core DataSet is immutable and is the entity on which
identity operations are defined. As a consequence, any modifications
to fields other than Name, Description or Tags requires giving the DataSet
a new universal UniqueId (aka UUID). Operations such as md5 checksum should
be performed on the Core DataSet unless otherwise specified.


I/O trade-offs
--------------
The DataSet model defers I/O operations by replacing up-front file merges
with downstream I/O operations that hit many different files. This allows
consumers to avoid explicit creation of files on disk and the resulting
redundant storage and costly write operations. For many uses this many-file
approach is preferred to explicitly creating the file on disk,
but in some cases it may be desirable to incur the cost of accessing
and filtering multiple files once (e.g. to reduce disk seeks for highly
fragmented DataSets). Determining when the costs outweigh the benefits will
need practical investigation, but regardless the Consolidate operation
provides the means for using the form of DataSet that best fits a
particular use case.


Outstanding Issues and Future Directions
---------------------------------------------

- Document FASTA filters for pbcore / pbbam for releases post-4.0.
- The propagation of subdatasets in merging can result in rather large XML
  files with duplicated information. It is possible this duplication could
  be reduced using XML IDREFs from the subdatasets to information in the top
  level DataSet, for ExternalResources or CollectionMetadata. This should be
  considered as a possible future revision.


Appendix 1: Examples satisfying the motivating use cases
==========================================================

- Refer to a **set of subreads** in multiple BAM files::

    <?xml version="1.0" encoding="utf-8" ?>
    <pbds:SubreadSet xmlns="http://pacificbiosciences.com/PacBioDatasets.xsd">
        <pbbase:ExternalResources>
            <pbbase:ExternalResource MetaType="SubreadFile.SubreadBamFile"
                              ResourceId="file:/mnt/path/to/subreads0.bam"/>
            <pbbase:ExternalResource MetaType="SubreadFile.SubreadBamFile"
                              ResourceId="file:/mnt/path/to/subreads1.bam"/>
        </pbbase:ExternalResources>
        <pbds:Filters>
            <pbds:Filter>
                <pbbase:Properties>
                    <pbbase:Property Name="rq" Operator="gt" Value="0.75"/>
                </pbbase:Properties>
            </pbds:Filter>
        </pbds:Filters>
        <pbds:DataSetMetadata>
            <pbbase:TotalLength>5000</pbbase:TotalLength>
            <pbbase:NumRecords>500</pbbase:NumRecords>
        </pbds:DataSetMetadata>
    </pbds:SubreadSet>


- Refer to a **subset of subreads** by id from one or more BAM files::

    <?xml version="1.0" encoding="utf-8" ?>
    <pbds:SubreadSet xmlns="http://pacificbiosciences.com/PacBioDatasets.xsd">
        <pbbase:ExternalResources>
            <pbbase:ExternalResource MetaType="SubreadFile.SubreadBamFile"
                              ResourceId="file:/mnt/path/to/subreads0.bam"/>
        </pbbase:ExternalResources>
        <pbds:Filters>
            <pbds:Filter>
                <pbbase:Properties>
                    <pbbase:Property Name="qname" Operator="==" Value="m100000/0/0_100"/>
                </pbbase:Properties>
            </pbds:Filter>
            <pbds:Filter>
                <pbbase:Properties>
                    <pbbase:Property Name="qname" Operator="==" Value="m100000/1/0_200"/>
                </pbbase:Properties>
            </pbds:Filter>
        </pbds:Filters>
        <pbds:DataSetMetadata>
            <pbbase:TotalLength>5000</pbbase:TotalLength>
            <pbbase:NumRecords>500</pbbase:NumRecords>
        </pbds:DataSetMetadata>
    </pbds:SubreadSet>


- Refer to a **subset of alignments** for input to algorithms such as Arrow (e.g. on a particular chromosome, or a particular chromosome region, or from reads labeled with a particular barcode)
    - *Use an AlignmentSet filtered by rname*

- Perform any analysis that can be performed on an entire file of a particular data type (reads, read regions, alignments) on a **subset of that data type** without creating a new file. - *Relies on tools using common APIs to access DataSets.*


Appendix 2: Example DataSet XML files
=====================================

Here are some example XML files for each of the above DataSets

.. include:: examples/datasets/subread.rst
.. include:: examples/datasets/ccsread.rst
.. include:: examples/datasets/alignment.rst
.. include:: examples/datasets/reference.rst
.. include:: examples/datasets/contig.rst
.. include:: examples/datasets/barcode.rst


.. _W3C compatible timestamp: http://www.w2.org/TR/NOTE-datetime
.. _pbcoretools: http://pacificbiosciences.github.io/pbcoretools/pbcoretools.html
.. _dataset: http://pacificbiosciences.github.io/pbcoretools/pbcoretools.html
.. _pbbam: http://pbbam.readthedocs.io/en/latest/api/DataSet.html
.. _pbcore: http://pacificbiosciences.github.io/pbcore/pbcore.io.dataset.html#api-overview
.. _XSD: xsd/PacBioDatasets.html
