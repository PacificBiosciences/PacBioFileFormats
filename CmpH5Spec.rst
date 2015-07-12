===================================================
PacBio Alignment File Format (cmp.h5) Specification
===================================================


.. moduleauthor:: Jason Chin, Dale Webster, Susan Tang, Jim Bullard,
                  Mark Chaisson, David Alexander, Dimitris Iliopoulos


Revision History
================

.. tabularcolumns:: |r|r|L|J|
 
+---------+------------+--------------------+-------------------------------+
| Version |    Date    |      Authors       |Comments                       |
+=========+============+====================+===============================+
| 0.1     | 07/24/2009 | Jason Chin         |First draft                    |
+---------+------------+--------------------+-------------------------------+
| 0.2     | 11/04/2009 | Jason Chin         |2nd draft, incorporated changes|
|         |            |                    |from prototype                 |
+---------+------------+--------------------+-------------------------------+
| 0.3     | 11/17/2009 | Susan Tang         |Added consensus record         |
+---------+------------+--------------------+-------------------------------+
| 0.4     | 03/11/2009 | Jason Chin,        |Added SF related spec and      |
|         |            | James Bullard      |indexing proposal              |
+---------+------------+--------------------+-------------------------------+
| 0.5     | 07/06/2010 | Dale Webster       |Added PB Internal Format Spec  |
+---------+------------+--------------------+-------------------------------+
|         |            |                    |Major Revision before v.       |
|         |            |                    |1.2. Remove all reference to   |
|         |            |                    |earlier Astro type cmp.h5.     |
|         |            | Jason Chin,        |Meta-data group hierarchy      |
|         |            | James Bullard,     |changed. New attributes        |
|         |            | Dale Webster,      |added. Define a few file       |
| 1.2rc   | 10/25/2010 | Dimitris           |operation behaviors.           |
|         |            | Iliopoulos, Ali    |                               |
|         |            | Bashir             |We call this document version  |
|         |            |                    |1.2rc to match the software    |
|         |            |                    |release version for FCR.       |
|         |            |                    |Preliminary support for strobe |
|         |            |                    |read timing information.       |
+---------+------------+--------------------+-------------------------------+
|         |            |                    |Finalize 1.2 spec , updated    |
| 1.2     | 12/22/2010 | Jason Chin         |examples, revise the FileLog   |
|         |            |                    |info group, remove TODO, remove|
|         |            |                    |"rc" in the version string.    |
+---------+------------+--------------------+-------------------------------+
|1.3.1    | 03/6/2012  | David Alexander,   |QV record types                |
|         |            | Mark Chaisson      |changed. lastRow datasets      |
|         |            |                    |removed.  Converted to         |
|         |            |                    |reStructuredText. Some material|
|         |            |                    |moved to Appendices            |
+---------+------------+--------------------+-------------------------------+
|2.0.0    |02/12/2013  | David Alexander,   |Addition of chemistry tag      |
|         |            | James Bullard      |information per-movie.  Removal|
|         |            |                    |of master dataset constructs.  |
|         |            |                    |Sortedness of a file now       |
|         |            |                    |indicated by presence of       |
|         |            |                    |OffsetTable.                   |
+---------+------------+--------------------+-------------------------------+
|2.1.0    |08/01/2013  | James Bullard      |Addition of Barcode data       |
+---------+------------+--------------------+-------------------------------+
|2.3.0    |5/21/2014   | David Alexander    |Document revised chemistry     |
|         |            |                    |encoding                       |
+---------+------------+--------------------+-------------------------------+



File Format Versioning
======================

The ``cmp.h5`` file format version is stored in the root group attribute
``Version``.  The version may take one of the following values:

- "1.2.0"
- "1.2.0.SF"
- "1.2.0.PB"
- "1.3.1.SF"
- "1.3.1.PB"
- "2.0.0"
- "2.1.0"
- "2.3.0"

File formats with versions ending in ".SF" (for Springfield) represent
the production file formats that are produced by instruments at
customer sites.  File formats with versions ending in ".PB" (for
PacBio) may contain additional information.  *Version "X.PB" files are
always usable wherever an "X.SF" file is usable; i.e. PacBio internal
files contain a superset of the features required in a Springfield
file, and the same formatting conventions are observed.*


Hierarchy Layout
================

In this section, we specify the general layout. At the top-level, or
root group of the ``cmp.h5`` HDF5 file, there exist six HDF5 groups which
must exist: ``AlnInfo``, ``RefInfo``, ``MovieInfo``, ``AlnGroup``,
``RefGroup``, ``FileLog``.

There are basically three different categories of data groups:

1. The *Info* groups contain information about particular aspects of
   the data contained in the file to some external references, e.g.,
   reference sequences used for alignments, movies information for
   the reads, and ZMW hole numbers, etc. These groups will be
   referred to as info groups. (The only exception of such
   convention is the ``FileLog`` group. It should be considered as an
   Info group even though the group does have a "Info" suffix. )

2. The *Group* HDF5 groups contain information about how the data is
   stored in the file and function as key-value-pair mappings from
   integer IDs to character paths. Each "Group" HDF5 group will
   contain at least two datasets one of which will be called ID and
   the other will be called Path. The ID is the key used to refer to
   the HDF5 path stored in parallel in the Path dataset. To avoid
   ambiguity these groups will be referred to as mapping groups.

3. Additionally, at the top-level of the file, zero or more
   alignment data groups will exist---these groups contain the
   actual alignment data for each reference sequence and alignment
   group. These groups will be called data groups.

All datasets stored under the same HDF5 group irrespective of type
shall always have the same number of rows or, in the case of
dimensionless vectors, length.

Here we specify the minimal set of datasets in each of aforementioned
groups:

1. An info group named ``AlnInfo`` containing information about each
   alignment stored in the file. The ``AlnInfo`` group should
   contain the following datasets:

    a. ``AlnIndex``: Dataset whose rows represent unique alignments
       and whose columns store relevant information about each
       alignment.  The ``AlnIndex`` dataset has a string list
       attribute, ``ColumnNames``, containing the names of the columns
       of this dataset.

    b. (CCS only): A vector dataset ``NumPasses``, of the same length
       as ``AlnIndex``, indicating the number of CCS subreads that
       were used to generate the consensus read in the corresponding
       row of ``AlnIndex``.

    b. (Optional) Vector datasets, of the same length as ``AlnIndex``,
       the same storing information about each alignment (e.g.,
       ``ZScore``, ``SNR``, and ``Edna``).

2. An info group named ``RefInfo`` containing information about the
   reference sequences used during alignment. The ``RefInfo`` group
   should contain the following datasets:

    a. ``ID``: Identifier of the record.

    b. ``FullName``: Name of the sequence as given by the FASTA file
       used during alignment.

    c. ``MD5``: md5 hashes of the DNA sequence used during alignment.

    .. note::

        The MD5 convention used in cmp.h5 files differs from the standard
        convention in SAM files.  SAM files store the "MD5 checksum of the
        sequence in the uppercase, with gaps and spaces removed."  *cmp.h5
        files contain the MD5 checksums of the reference contig sequences
        as present in the refernece FASTA file---case preserved, spaces
        and gaps intact (but newlines removed).*


    d. ``Length``: The length of the DNA sequence used during
       alignment.

3. An info group named ``MovieInfo`` containing information about
   the movies which produced the alignments. This ``MovieInfo``
   group should contain the following datasets:

    a. ``ID``: Identifier of the record.

    b. ``Name``: Movie name.

    c. ``FrameRate``: The camera speed in frames per second used
        to record the movie.

    d. Datasets encoding information about the sequencing chemistry
       that was used.  This is encoded in one of two manners:

      1.  Datasets ``SequencingKit``, ``BindingKit``, and
         ``SoftwareVersion`` represent the partnumbers read by the
         instrument barcode reader for each movie run, as well as the
         basecaller version.  Decoding of this identifying "triple"
         for each movie is deferred to the tools that actually need to
         know the chemistry details---specifically, the Quiver
         variant/consensus calling tool and the base-modification
         identification tools.

      2. *(Versions 2.2.0 and earlier, and manual override in 2.3.0
         and after)* Dataset ``SequencingChemistry``, representing a
         canonical string representation (for example, "P4-C2") of the
         chemistry.  Note that this places the burden for decoding of
         the barcode information on the software that constructs the
         ``cmp.h5`` rather than client software.

      Software that parses the ``cmp.h5`` format shall rely on the
      datasets in (1) as the canonical chemistry information, only
      falling back to the information in (2) if the datasets in (1)
      are absent.

4. An info group named ``FileLog`` containing information about the
   history of the file itself.

    a. ``ID``: Identifier of the record

    b. ``Program``: The name of the program that touches the file

    c. ``Version``: The version of the program that touches the file

    d. ``Timestamp``: A `W3C compatible timestamp`_ string of the
       date-time when the file is touched.


    e. ``CommandLine``: Detail command line string that details
       how the program is used

    f. ``Log``: The field to store any extra details

5. A mapping group named ``RefGroup`` that records the reference
   sequence information used in the alignments: The ``RefGroup``
   group should contain the following datasets:

    a. ``ID``

    b. ``Path``

    c. ``RefInfoID``: ``RefInfoID`` refers to elements of the
       ``/RefInfo/ID`` dataset.

6. A mapping group named ``AlnGroup`` that records the different
   partitions of alignments. This data group should contains:

    a. ``ID``
    b. ``Path``

7. Zero or more data groups containing the actual alignments. The
   names of the groups are defined by the dataset ``/RefGroup/Path``.
   Each reference group contains one or more alignment groups
   (representing alignments from some predefined grouping, such as:
   SMRTcell, acquisition, or movie, etc). The full HDF5 paths to the
   alignment groups including the group names are defined in the
   dataset ``/AlnGroup/Path``. An alignment group should contain:

    a. A single alignment array dataset named ``AlnArray``

    b. (Optional) Datasets for quality values and pulse features that can be
       aligned to the read bases. Detailed information about
       necessary datasets is defined in sections 10 and 11.

8. (Optional) User-defined datasets conforming to the conventions
   of simple HDF5 types and having the same length as each sibling
   in its containing group.

It may be helpful to inspect the output of *h5ls* applied to a
1.3.1.SF cmp.h5 file::

    mp-f052:~ $ h5ls -r  ~/Data/new_cmph5/alignments.cmp.h5
    /                        Group
    /AlnGroup                Group
    /AlnGroup/ID             Dataset {1/Inf}
    /AlnGroup/Path           Dataset {1/Inf}
    /AlnInfo                 Group
    /AlnInfo/AlnIndex        Dataset {16866/Inf, 22/Inf}
    /FileLog                 Group
    /FileLog/CommandLine     Dataset {3/Inf}
    /FileLog/ID              Dataset {3/Inf}
    /FileLog/Log             Dataset {3/Inf}
    /FileLog/Program         Dataset {3/Inf}
    /FileLog/Timestamp       Dataset {3/Inf}
    /FileLog/Version         Dataset {3/Inf}
    /MovieInfo               Group
    /MovieInfo/FrameRate     Dataset {1/Inf}
    /MovieInfo/SequencingChemistry     Dataset {1/Inf}
    /MovieInfo/ID            Dataset {1/Inf}
    /MovieInfo/Name          Dataset {1/Inf}
    /RefGroup                Group
    /RefGroup/ID             Dataset {1/Inf}
    /RefGroup/OffsetTable    Dataset {1/Inf, 3/Inf}
    /RefGroup/Path           Dataset {1/Inf}
    /RefGroup/RefInfoID      Dataset {1/Inf}
    /RefInfo                 Group
    /RefInfo/FullName        Dataset {1/Inf}
    /RefInfo/ID              Dataset {1/Inf}
    /RefInfo/Length          Dataset {1/Inf}
    /RefInfo/MD5             Dataset {1/Inf}
    /ref000001               Group
    /ref000001/m120225_045819_richard_c100304312550000001523012308061200_s1_p0 Group
    /ref000001/m120225_045819_richard_c100304312550000001523012308061200_s1_p0/AlnArray Dataset {39434696/Inf}
    /ref000001/m120225_045819_richard_c100304312550000001523012308061200_s1_p0/DeletionQV Dataset {39434696/Inf}
    /ref000001/m120225_045819_richard_c100304312550000001523012308061200_s1_p0/DeletionTag Dataset {39434696/Inf}
    /ref000001/m120225_045819_richard_c100304312550000001523012308061200_s1_p0/IPD Dataset {39434696/Inf}
    /ref000001/m120225_045819_richard_c100304312550000001523012308061200_s1_p0/InsertionQV Dataset {39434696/Inf}
    /ref000001/m120225_045819_richard_c100304312550000001523012308061200_s1_p0/MergeQV Dataset {39434696/Inf}
    /ref000001/m120225_045819_richard_c100304312550000001523012308061200_s1_p0/PulseWidth Dataset {39434696/Inf}
    /ref000001/m120225_045819_richard_c100304312550000001523012308061200_s1_p0/QualityValue Dataset {39434696/Inf}
    /ref000001/m120225_045819_richard_c100304312550000001523012308061200_s1_p0/SubstitutionQV Dataset {39434696/Inf}
    /ref000001/m120225_045819_richard_c100304312550000001523012308061200_s1_p0/SubstitutionTag Dataset {39434696/Inf}





Root Group Attributes
=====================

The following mandatory string attributes should be set in the root group:

+-------------+----------------+------------------------------------+
|    Name     | Allowed Values |              Comment               |
+=============+================+====================================+
|             |  "1.2.0"       |                                    |
|             |  "1.2.0.SF"    |The suffix is used to indicate      |
|             |  "1.2.0.PB"    |whether the file includes (".SF") or|
|             |  "1.3.1.SF"    |does not include (".PB") several    |   
|             |  "1.3.1.PB"    |datasets useful for in-house        |
| Version     |  "2.0.0"       |analyses.                           |
+-------------+----------------+------------------------------------+
|             |                |Set to "standard" by default. If the|
|             | "RCCS", "CCS", |cmp.h5 is used for "RCCS" and "CCS",|
| ReadType    | "strobe",      |there will be no pulse              |
|             | "standard", or |features. Each read type will allows|
|             | "cDNA"         |different sets of optional tables.  |
+-------------+----------------+------------------------------------+
|             | The command    |This attribute is reserved for the  |
| CommandLine | line used for  |initial generation.  All            |
|             | generating     |post-initial alignment information  |
|             | this file.     |should be stored in FileLog         |
+-------------+----------------+------------------------------------+



Mapping Groups: ``ID``, and ``Path`` datasets
=============================================

Each mapping group contains at least an ``ID`` and ``Path`` dataset.
The ID dataset contains unique positive integer values. The ``Path``
dataset contains proper HDF5 paths to HDF5 groups within the
file. Elements of the path dataset should conform to the following
regular expression (leading forward slash not included):

"[a-zA-Z\-+_0-9]+" (all lower and upper case ASCII characters,
numbers, "-", and "+").

The ID, Path datasets function as key-value pair mappings. The
individual IDs are used in datasets to reference the relevant
information stored in this particular mapping group.

The following `HDF5 DDL`_ defines the hdf5 data types for these data
sets::

      DATASET "ID" {
         DATATYPE  H5T_STD_U32LE
         DATASPACE  SIMPLE { ( * ) / ( H5S_UNLIMITED ) }
      }
      DATASET "Path" {
         DATATYPE  H5T_STRING {
               STRSIZE H5T_VARIABLE;
               STRPAD H5T_STR_NULLTERM;
               CSET H5T_CSET_ASCII;
               CTYPE H5T_C_S1;
            }
         DATASPACE  SIMPLE { ( * ) / ( H5S_UNLIMITED ) }
      } 


Two datasets are used to avoid compound types in an HDF5 file. This
avoids the complication in reader/writer code implementations. If
there is a mature compound type code base within the PBI development
environment, compound type datasets are recommended for storing such
key-value pairs.


``RefGroup`` data group and ``/RefGroup/*`` datasets
====================================================

The ``RefGroup`` mapping group provides a mapping between reference
sequence identifiers (``ID``) to HDF5 paths in the file (``Path``). An
example HDF5 schema can be seen above. A ``RefInfoID`` data set is
used for pointing to the ``ID`` dataset in the RefInfo group and can
be viewed as a foreign key.

The following DDL code block defines the data types for the datasets
and attributes associated with ``/RefGroup``::

   GROUP "RefGroup" {
      DATASET "ID" {
         DATATYPE  H5T_STD_U32LE
         DATASPACE  SIMPLE { ( * ) / ( H5S_UNLIMITED ) }
      }
      DATASET "Path" {
         DATATYPE  H5T_STRING {
               STRSIZE H5T_VARIABLE;
               STRPAD H5T_STR_NULLTERM;
               CSET H5T_CSET_ASCII;
               CTYPE H5T_C_S1;
            }
         DATASPACE  SIMPLE { ( * ) / ( H5S_UNLIMITED ) }
      }
      DATASET "RefInfoID" {
         DATATYPE  H5T_STD_U32LE
         DATASPACE  SIMPLE { ( * ) / ( H5S_UNLIMITED ) }
      }
   }


``AlnGroup`` data group: ``/AlnGroup/*`` datasets
=================================================

The ``AlnGroup`` mapping group provides a mapping between alignment
group identifiers (``ID``) to alignment group paths.

The following DDL code block defines the data types for the datasets
and attributes associated with ``/AlnGroup``::

   GROUP "AlnGroup" {
      DATASET "ID" {
         DATATYPE  H5T_STD_U32LE
         DATASPACE  SIMPLE { ( * ) / ( H5S_UNLIMITED ) }
      }
      DATASET "Path" {
         DATATYPE  H5T_STRING {
               STRSIZE H5T_VARIABLE;
               STRPAD H5T_STR_NULLTERM;
               CSET H5T_CSET_ASCII;
               CTYPE H5T_C_S1;
            }
         DATASPACE  SIMPLE { ( * ) / ( H5S_UNLIMITED ) }
      }
   }



``RefInfo`` info group and ``/RefInfo/*`` datasets
==================================================

The ``RefInfo`` info group provides information about the reference
sequences used during alignment. The ``RefInfo`` group contains at
least 4 datasets including the ``ID`` dataset. The
``RefInfo/FullName`` provides the name of the sequence aligned to and
is the full FASTA name. The ``RefInfo/MD5`` is an ``MD5`` hash of the
reference sequence aligned to. The ``RefInfo/Length`` provides the
length of the sequence aligned to.

Other sequence specific annotations can be stored as parallel datasets
at this level.

The following DDL code block defines the data types for the datasets
and attributes associated ``/RefInfo``::

   GROUP "RefInfo" {
      DATASET "FullName" {
         DATATYPE  H5T_STRING {
               STRSIZE H5T_VARIABLE;
               STRPAD H5T_STR_NULLTERM;
               CSET H5T_CSET_ASCII;
               CTYPE H5T_C_S1;
            }
         DATASPACE  SIMPLE { ( * ) / ( H5S_UNLIMITED ) }
      }
      DATASET "ID" {
         DATATYPE  H5T_STD_U32LE
         DATASPACE  SIMPLE { ( * ) / ( H5S_UNLIMITED ) }
      }
      DATASET "Length" {
         DATATYPE  H5T_STD_U32LE
         DATASPACE  SIMPLE { ( * ) / ( H5S_UNLIMITED ) }
      }
      DATASET "MD5" {
         DATATYPE  H5T_STRING {
               STRSIZE H5T_VARIABLE;
               STRPAD H5T_STR_NULLTERM;
               CSET H5T_CSET_ASCII;
               CTYPE H5T_C_S1;
            }
         DATASPACE  SIMPLE { ( * ) / ( H5S_UNLIMITED ) }
      }
   }


``MovieInfo`` data group: ``MovieInfo/*`` datasets
==================================================

The paired arrays ``MovieInfo/ID`` and ``MovieInfo/Name`` in the
``MovieInfo`` group are defined to indicate the source of the movies
for the reads in the ``AlnInfo/AlnIndex`` dataset. This pair of arrays
functions as a key-value-pair map between IDs and movie names. 

The following DDL code block defines the data types for the datasets
and attributes associated ``/MovieInfo``::

   GROUP "MovieInfo" {
      DATASET "ID" {
         DATATYPE  H5T_STD_U32LE
         DATASPACE  SIMPLE { ( * ) / ( H5S_UNLIMITED ) }
      }
      DATASET "Name" {
         DATATYPE  H5T_STRING {
               STRSIZE H5T_VARIABLE;
               STRPAD H5T_STR_NULLTERM;
               CSET H5T_CSET_ASCII;
               CTYPE H5T_C_S1;
            }
         DATASPACE  SIMPLE { ( * ) / ( H5S_UNLIMITED ) }
      }
   }


``AlnInfo`` data group and the ``AlnArray`` data sets
=====================================================

``AlnInfo`` data group
----------------------
The first column of the AlnIndex can be treated as the equivalent "ID"
dataset in the mapping or the info groups.

The data types of the dataset ``AlnIndex`` are defined as::

    DATASET "AlnIndex" {
     DATATYPE  H5T_STD_U32LE
     DATASPACE  SIMPLE { ( *, 22 ) / ( H5S_UNLIMITED, 22 ) }
    }


``AlnIndex`` dataset
--------------------
The purpose of the ``AlnIndex`` dataset is to:

1. Store the information necessary to retrieve alignments from the
   file. This includes: path, beginning offset, and ending offset
   within the dataset containing the alignment. (This kind of
   reference to alignment is similar to that proposed by HDF5
   group in the bioHDF5 specification.)

2. Store the information, e.g., the orientation (i.e., strand) of
   the alignment, for processing the alignment properly for
   downstream bioinformatics analysis and visualization.

3. Store information that can be used to indentify the original
   reads.

4. Store the unique unsigned 32 bit integer ID as single unique
   key for each individual alignment.

5. Store summary information about the alignment. For example, one
   can store the number of matches, mismatches, insertions,
   deletions, mapping quality, read level quality values, etc.


``AlnIndex`` Dataset Columns
----------------------------

The 22 columns in the `AlnIndex` dataset are described in the table
below.

.. tabularcolumns:: |p{1in}|L|L|

+--------------+--------------------------+-----------------------------+
| Column Name  |Meaning                   | Comment                     |
+==============+==========================+=============================+
|              |                          | Each alignment should       |
|              |                          | have a unique AlnID. No     |
| AlnID        |Non-zero unique 32 bit    | other assumption about      |
|              |integer key for the       | the order of the AlnID      |
|              |alignment record          | should be used for data     |
|              |                          | processing.                 |
+--------------+--------------------------+-----------------------------+
|              |A foreign key referring to|                             |
| AlnGroupID   |AlnGroup/ID               |                             |
+--------------+--------------------------+-----------------------------+
|              |A foreign key referring to|                             |
| MovieID      |MovieInfo/ID              |                             |
+--------------+--------------------------+-----------------------------+
|              |A foreign key referring to|                             |
| RefGroupID   |RefGroup/ID.              |                             |
+--------------+--------------------------+-----------------------------+
|              |The start position        | tStart should always be     |
|              |(0-based, inclusive) of   | less than tEnd, even when   |
| tStart       |the alignment target (the | the hit is against the      |
|              |reference sequence)       | opposite strand.            |
+--------------+--------------------------+-----------------------------+
|              |The end position (0-based,|                             |
|              |not-inclusive) of the     | tEnd should always be       |
|              |alignment target (the     | greater than tStart, even   |
| tEnd         |reference sequence)       | when the hit is against     |
|              |                          | the opposite strand.        |
+--------------+--------------------------+-----------------------------+
|              |                          | The read base should        |
|              |The relative strand in the| never be                    |
|              |alignment. 1 for reversed | reverse-complimented in     |
|              |reference strand; 0 for   | the alignment array, so     |
| RCRefStrand  |forward-forward alignment | we only need to record if   |
|              |                          | the reference bases are     |
|              |                          | presented in reverse        |
|              |                          | complemented strand in      |
|              |                          | the file. "1" means         |
|              |                          | "Yes/True" here.            |
+--------------+--------------------------+-----------------------------+
| HoleNumber   |The HoleNumber from the   |                             |
|              |bas.h5                    |                             |
+--------------+--------------------------+-----------------------------+
| SetNumber    |                          |                             |
+--------------+--------------------------+-----------------------------+
| StrobeNumber | Context dependent value. |                             |
| ExonNumber   | When the read type is    |                             |
|              | Strobe, this field is the|                             |
|              | strobe number.  When the |                             |
|              | read type is cDNA it will|                             |
|              | be the exon number.      |                             |
+--------------+--------------------------+-----------------------------+
|              |                          | If multiple subreads are    |
|              |                          | from the same physical      |
|              |                          | origin, they should have the|
| MoleculeID   |An integer which is unique| same MoleculeID and         |
|              |to all subreads from the  | different physical origins  |
|              |same ZMW.                 | should have different       |
|              |                          | MoleculeID.                 |
+--------------+--------------------------+-----------------------------+
|              |The start position        | Regardless weather the      |
|              |(0-based, inclusive) of   | alignment is a subread or   |
| rStart       |the read in the alignment | not, the position is        |
|              |                          | always relative to the      |
|              |                          | original raw full read      |
|              |                          | sequence.                   |
+--------------+--------------------------+-----------------------------+
|              |The end position (0-based,|                             |
|              |not-inclusive) of the read| rEnd should always be       |
| rEnd         |in the alignment          | greater than rStart.        |
+--------------+--------------------------+-----------------------------+
| MapQV        |TBD                       |                             |
+--------------+--------------------------+-----------------------------+
|              |Number of matched base in |                             |
| nM           |the alignment             |                             |
+--------------+--------------------------+-----------------------------+
|              |Number of mis-matched base|                             |
| nMM          |in the alignment          |                             |
+--------------+--------------------------+-----------------------------+
|              |Number of insertions in   |                             |
|              |the read relative to the  |                             |
| nIns         |reference sequence        |                             |
+--------------+--------------------------+-----------------------------+
|              |Number of deletions       |                             |
|              |(missing bases) in the    |                             |
| nDel         |read relative to the      |                             |
|              |reference sequence        |                             |
+--------------+--------------------------+-----------------------------+
|              |The beginning position    |                             |
|              |(0-based, inclusive) of   |                             |
| Offset_begin |the alignment in the      |                             |
|              |AlignmentArray            |                             |
+--------------+--------------------------+-----------------------------+
|              |The ending position       |                             |
|              |(0-based, exclusive) the  | Not including the padded    |
| Offset_end   |alignment in the          | zero of the alignment       |
|              |AlignmentArray            | array.                      |
+--------------+--------------------------+-----------------------------+
|              |Used for faster access to | See the sorting and         |
| nBackRead    |blocks of sorted reads    | indexing section            |
+--------------+--------------------------+-----------------------------+
|              |Used for faster access to | See the sorting and         |
| nReadOverlap |blocks of sorted reads    | indexing section            |
+--------------+--------------------------+-----------------------------+


The column names should be stored as an attribute ``ColumnNames`` that
contains all names listed in "Column Name" in the table above.




Sequence Alignments
===================

Binary Encoding for Alignment Pair
----------------------------------

The *alignment array* is a one dimensional 8 bit unsigned integer
array where the individual array elements represent a "read base
- reference base" pair packed into one byte. The higher four bits
are set by the read base and the lower four bits are set by the
reference base as the following::

            0 0 0 0 0 0 0 0
            T G C A T G C A


For example, "T" and "T" matched alignment will be presented as
0b10001000=136. "T" vs. "G" mismatch will be represented as
0b10000100=132. Insertion of "T" in read will be 0b10000000=128.
"No-call" ("N") bases are encoded as 0b1111=15 for both read and
reference.


In the ``AlnArray`` dataset, the encoded read base should be always
the same as what has been observed by the sequencing machine
without any complementation. If a read is aligned to the reverse
complement strand of the reference sequence, the lower four bits
represent the complemented base (i.e., the reference has been
complemented).


Alignment Array
---------------

The example below shows the conversion of an alignment pair to
the binary array represented as an integer::

    Alignment:

        Read Bases: ATCTT--ATC-GTTAATTA--A
        Ref. Bases: A-CTCAGA-CAGTCAATTAGCA

    Encoded Alignment Pairs:

        AA -> 17
        T- -> 128
        CC -> 34
        TT -> 136
        TC -> 130
        -A -> 1
        -G -> 4
        ...
        -C -> 2
        AA -> 17

The final encoded array for this alignment is [17, 128, 34, 136, 130,
1, 4, 17, 128, 34, 1, 68, 136, 130, 17, 17, 136, 136, 17, 4, 2, 17, 0].

Note that zero is padded at the end of each alignment as a separator
between different alignments. This will enable some analysis by
simply streaming the alignment array without extra index look-ups
to separate different alignments.

The alignment array is a concatenation of all encoded alignment
arrays of each read and the AlignmentIndex dataset is used to
indentify the origin of each alignment.

Below is an example of the HDF5 type definition for an AlnArray::

    DATASET "AlnArray" {
        DATATYPE H5T_STD_U8LE
        DATASPACE SIMPLE { ( * ) / ( H5S_UNLIMITED ) }
    }



Pulse Metrics and QVs
=====================

In addition to the basic and required ``AlnArray`` dataset present in
each alignment group, pulse metrics and quality values (QVs) may be
optionally provided; however if one of these features is provided for
one alignment group they must be provided for all alignment groups.
These optional datasets are:

    - ``DeletionQV``,
    - ``DeletionTag``,
    - ``InsertionQV``,
    - ``MergeQV``,
    - ``SubstitutionQV``,
    - ``SubstitutionTag``,
    - ``QualityValue``,
    - ``IPD``,
    - ``PulseWidth``,
    - ``StartFrame``,
    - ``pkmid``

Each such dataset is of the same shape as the ``AlnArray`` dataset in
the same alignment group.  Missing values (corresponding to read gaps
in the alignment array) are encoded based on the type of
the dataset:

+------------+---------------+
|Data type   |Missing value  |
|            |encoding       |
+============+===============+
|float32     |NaN            |
+------------+---------------+
|int8 (char) |'-' (ASCII 42) |
+------------+---------------+
|uint8       |255            |
+------------+---------------+
|uint16      |65535          |
+------------+---------------+

A missing value is present at a dataset offset if and only if that
offset corresponds to a read gap in the `AlnArray`.

For the types of the pulse metric and QV datasets, see `Summary of
Attributes and Datasets`_.  Any offset into a pulse metric or QV
dataset corresponds to the same offset in the ``AlnArray``.


Specification for the ``cmp.h5`` used for automatic data analysis from the instrument
=====================================================================================

This section defines the constraints that a cmp.h5 file should satisfy
for automatic data analysis for an SpringField instrument. Such files
are labeled with a root group attribute ``Version`` of "1.2.0.SF" or
"1.3.1.SF".

The ``RefGroup/Path`` for 1.2.0.SF and 1.2.0.PB ``cmp.h5`` files has the form
of "ref%06d" (C string formatting convention). The original FASTA
sequence header should be stored in the ``RefInfo/FullName`` dataset.
Additionally, two other datasets are obligatory: ``RefInfo/Length``
and ``RefInfo/MD5``.

The default of ``AlnGroup`` partition is to group alignments from the
same movie that aligned to the same reference together and we use the
movie filename without suffix as the default alignment group name.



Specification for the ``cmp.h5`` used for PacBio internal data analysis
=======================================================================

In addition to all datasets specified for the standard ``cmp.h5`` the
following additional datasets are required in internal files
("1.2.1.PB"):

1. Within the info group named "MovieInfo" containing information about
   the movies which produced the alignments:

  - ``Exp``: A uint32 dataset specifying the PacBio LIMS Experiment
    code associated with each movie in the corresponding
    ``/MovieInfo/Name`` dataset.

  - ``Run``: A uint32 dataset specifying the PacBio LIMS Run code
    associated with each movie in the corresponding ``/MovieInfo/Name``
    dataset.

  Data type and data space definition::

    DATASET "/MovieInfo/Exp" {
       DATATYPE  H5T_STD_U32LE
       DATASPACE  SIMPLE { ( 1 ) / ( H5S_UNLIMITED ) }
    }
    DATASET "/MovieInfo/Run" {
       DATATYPE  H5T_STD_U32LE
       DATASPACE  SIMPLE { ( 1 ) / ( H5S_UNLIMITED ) }
    }


2. Within the info group named ``AlnInfo`` containing information about
   each alignment stored in the file:

  - ``ZScore``: a float32 dataset containing the alignment
    significance score ("Z Score") computed from the corresponding row
    of the ``/AlnInfo/Index`` table.
  
  Data type and data space definition::

    DATASET "/AlnInfo/ZScore" {
       DATATYPE  H5T_IEEE_F32LE
       DATASPACE  SIMPLE { ( 310 ) / ( H5S_UNLIMITED ) }
    }

3. In addition to all attributes specified for the standard ``cmp.h5`` the
   following additional root level attributes are required:


.. tabularcolumns:: |p{1in}|L|J|p{3in}|

+---------------+-----------------+------------------+-------------------------+
|Attribute name |      Type       |  Sample values   |Comment                  |
+===============+=================+==================+=========================+
|               |                 |                  |Contains the directory   |
|ReportsFolder  |     string      |"Analysis_Reports"|name of the Primary      |
|               |                 |                  |Analysis Reports used for|
|               |                 |                  |this alignment           |
+---------------+-----------------+------------------+-------------------------+
|               |                 |                  |Contains the Perforce    |
|PrimaryPipeline|     string      |     "61453"      |changelist number of the |
|               |                 |                  |Primary Analysis Pipeline|
|               |                 |                  |used for this alignment  |
+---------------+-----------------+------------------+-------------------------+




Sorting, Flattening, Merging, Splitting and Filtering Behaviors
===============================================================

Sorting
-------

In order to provide fast access to cmp.h5 files, we provide sorted
cmp.h5 files. These files have some additional information to quickly
retrieve contiguous regions according to an indexing scheme. The most
typical use case is to obtain a set of reads overlapping a particular
genomic region, where the region can be a single genomic coordinate or
ranges of genomic coordinates.  Note that by default, *sorting* only
entails the sorting of the ``AlnIndex`` dataset, and not the sorting
of the alignment data itself.

A sorted cmp.h5 file has the following additional items as compared to
an unsorted cmp.h5:

1. A dataset ``OffsetTable`` stored within the ``RefGroup``
   mapping group giving the offsets of the reads mapped to a
   reference sequences in the global alignment index.  The dataset
   is a 3 by N unsigned 32 bit unsigned integer array, where N is
   the total number of reference sequences in the ``RegGroup/ID``
   table. The three elements of each row in the array indicate the
   ``RefID``, ``targetStartOffset``, and ``targetEndOffset``. The
   ``targetStartOffest`` and ``targetEndOffset`` give the range of
   the reads in the global ``/AlnInfo/AlnIndex`` that maps to the
   specific reference sequence in the first column of the
   dataset.  /The presence or absence of the ``OffsetTable`` dataset
   should be used to determine whether the file is sorted or unsorted./

2. The alignment index will have two additional columns of
   unsigned 32-bit integers (these could be shorter) ``nBackRead`` and
   ``nReadOverlap`` which gives the maximum number of reads one needs
   to examine to determine overlap and the actual number of reads
   which overlap a position, respectively. A value of -1 indicates
   that the field has not been filled in, whereas a value of 0
   means that no further reads possibly overlap the position of
   interest. Here, nBackRead > nReadOverlap is always true.

3. In addition to sorting the ``AlnIndex``, sorting and indexing can
   perform a "flattening" operation whereby all AlnGroups under each
   RefGroup are merged into a single AlnGroup. The name of the single
   AlnGroup can be anything, however, convention is to use the name:
   "rg-0001" to indicate that the sub-datasets have been merged and
   re-ordered. Additionally, an attribute on this group: repacked will
   be set to 1 to indicate, irrespective of the name, that the
   datasets have been sorted. If the length of any of the child
   datasets of of a "repacked" alignment group would be greater than
   2^32, then additional alignment groups are added serially, e.g.,
   "rg-0002", etc. An alignment will never span more than one
   alignment group.


.. note::

    The time complexity of sorting a cmp.h5 file will be on the order of
    O(n log(n)). Additionally, the columns ``nBackRead`` and
    ``nReadOverlap`` need to be computed. This will be on the order of
    O(max(read length) * n). Access to a given start position in cmp.h5
    will be O(log(n)), however, this will only produce reads having that
    start position. In order to obtain all reads overlapping a position,
    one needs to inspect the ``nBackRead`` to obtain the size of the slice
    that they should grab from the cmp.h5 file. Retrieval, therefore, is
    bound by O(nBackRead log(n)). The additional column, ``nReadOverlap``,
    should allow one to obtain significantly better performance, as the
    search can stop once to obtained number of reads is equal to
    ``nReadOverlap``.


Merging
-------

Merging is performed on a list of cmp.h5 files by selecting the first
file to act as the seed and sequentially merging the rest onto the
seed. If the first file in the list of files to be merged is empty
then the next non-empty file is selected to act as the seed. An exact
copy of the seed is made where all ID-type datasets have their entries
serialized to consecutive 32 bit integers starting from 1. Merging
results modifies a copy of the seed file in place. For each cmp.h5
file in the merging list, the following steps are performed:

1. If the file is empty, its root group Version does not match the
   seed's Version or does not have the same type of loaded
   PulseMetrics as the seed, it is removed from the merging list and
   the next file is considered.

2. Root group attributes are not merged since they are set to the
   seed's Root group attributes.

3. Datasets under the seed's AlnInfo Data group are extended with
   their counterparts from the file to be merged.  The AlnID column of
   the newly added rows in the AlnInfo/Index is updated by resetting
   the old values from the merged file. The new values are set equal
   to a list of integers starting from the maximum AlnID of the seed +
   1, adding 1 for each new AlnID from the merged file.

4. Datasets under the seed's RefInfo, MovieInfo, AlnGroup and RefGroup
   data groups are extended only with new entries from their
   counterparts in the file to be merged. If new RefInfo/ID,
   RefGroup/ID or MovieInfo/ID entries are created, they are mapped
   back to their respective columns in the AlnInfo/Index.

After going through the entire list of files to be merged, the FileLog
attribute from the Root group attributes is modified (TBD).


Splitting
---------
The current splitting behavior is implementation specific and
associated with a single use case, i.e., processing of .cmp.h5 files
involved in Edna analysis- type workflows. It is our aim to generalize
the splitting behavior to accommodate more use cases when those become
available.

A master cmp.h5 file is split into an N number of cmp.h5 files where N
is equal to the number of RefInfo/ID entries in the master
file. Consequently, each new cmp.h5 file contains all data associated
with a single reference sequence. This is done by:

1. Creating N copies of the master cmp.h5 file and sequentially
   selecting a RefInfo/ID entry to become the only entry for each
   copied file, unique amongst the group.

2. Resizing all datasets belonging to AlnInfo, RefInfo, MovieInfo,
   AlnGroup and RefGroup by deleting all entries that are not
   associated with the chosen reference sequence. Splitting maintains
   the values of all ID-type fields and data fields in the
   AlnInfo/Index rows.

3. Maintaining the size and content of the AlnArray and
   PulseMetric-type datasets in the new files as the ones in the
   master.

Barcode Information
===================
In addition to the afforementioned core alignment information, the
cmp.h5 file can be used to store optional datasets containing
``barcode`` annotation on alignments. The pattern leveraged to store
this annotation demonstrates a general mechanism to extend the information
stored in the cmp.h5 file for downstream applications.

In the case of barcoding, we wish to label alignments according to
their barcode so that other applications can leverage this information
when computing statistics over sets of alignments, e.g., consensus
calling within sample. To this end, a parallel dataset to
``/AlnInfo/AlnIndex`` is created. The ``Barcode`` dataset is 32-bit integer
matrix with the same number of rows as the ``AlnIndex`` dataset and 5
columns storing scoring and labeling information.

The ``Barcode`` dataset contains the total number of barcodes scored
for this molecule (``count``), the index of the top-scoring barcode
(``index1``), the score of the top-scoring barcode (``score1``), the
index of the 2nd-highest scoring barcode (``index2``) and its score
(``score2``). These columns are named in the attribute ``ColumnNames``
of the ``Barcode`` dataset.

The ``index1`` and ``index2`` are foreign-keys into the
``BarcodeInfo/ID`` dataset. Analagous to the other *Info datasets, the
``BarcodeInfo/ID`` and ``BarcodeInfo/Name`` are used to retrieve the
human-readable name of the barcode.


Summary of Attributes and Datasets
==================================

Versions prior to 2.0.0 are described in the Appendices.

**File Version 2.0.0 contents:**

+------------+------+--------------------+----------+-------+-----------+
|Parent Group| HDF5 |Resource Name       |Data type |  Shape|           |
|            | data |                    |          |       |           |
+============+======+====================+==========+=======+===========+
|/           |ATTR  |CommandLine         |VLEN_STR  |   None| required  |
+------------+------+--------------------+----------+-------+-----------+
|/           |ATTR  |Index               |VLEN_STR  |   (3,)| optional  |
+------------+------+--------------------+----------+-------+-----------+
|/           |ATTR  |ReadType            |VLEN_STR  |   None| required  |
+------------+------+--------------------+----------+-------+-----------+
|/           |ATTR  |Version             |VLEN_STR  |   None| required  |
+------------+------+--------------------+----------+-------+-----------+
|/AlnGroup   |DS    |ID                  |uint32    |      1| required  |
+------------+------+--------------------+----------+-------+-----------+
|/AlnGroup   |DS    |Path                |VLEN_STR  |      1| required  |
+------------+------+--------------------+----------+-------+-----------+
|/AlnInfo    |DS    |AlnIndex            |uint32    |     22| required  |
+------------+------+--------------------+----------+-------+-----------+
|/AlnInfo    |ATTR  |ColumnNames         |VLEN_STR  |     22| required  |
+------------+------+--------------------+----------+-------+-----------+
|/FileLog    |DS    |CommandLine         |VLEN_STR  |      1| required  |
+------------+------+--------------------+----------+-------+-----------+
|/FileLog    |DS    |ID                  |uint32    |      1| required  |
+------------+------+--------------------+----------+-------+-----------+
|/FileLog    |DS    |Log                 |VLEN_STR  |      1| required  |
+------------+------+--------------------+----------+-------+-----------+
|/FileLog    |DS    |Program             |VLEN_STR  |      1| required  |
+------------+------+--------------------+----------+-------+-----------+
|/FileLog    |DS    |Timestamp           |VLEN_STR  |      1| required  |
+------------+------+--------------------+----------+-------+-----------+
|/FileLog    |DS    |Version             |VLEN_STR  |      1| required  |
+------------+------+--------------------+----------+-------+-----------+
|/MovieInfo  |DS    |ID                  |uint32    |      1| required  |
+------------+------+--------------------+----------+-------+-----------+
|/MovieInfo  |DS    |Name                |VLEN_STR  |      1| required  |
+------------+------+--------------------+----------+-------+-----------+
|/MovieInfo  |DS    |FrameRate           |float32   |      1| required  |
+------------+------+--------------------+----------+-------+-----------+
|/MovieInfo  |DS    |SequencingChemistry |VLEN_STR  |      1| required  |
+------------+------+--------------------+----------+-------+-----------+
|/ref*/*     |DS    |AlnArray            |uint8     |      1| required  |
+------------+------+--------------------+----------+-------+-----------+
|/ref*/*     |DS    |QualityValue        |uint8     |      1| optional  |
+------------+------+--------------------+----------+-------+-----------+
|/ref*/*     |DS    |DeletionQV          |uint8     |      1| optional  |
+------------+------+--------------------+----------+-------+-----------+
|/ref*/*     |DS    |InsertionQV         |uint8     |      1| optional  |
+------------+------+--------------------+----------+-------+-----------+
|/ref*/*     |DS    |MergeQV             |uint8     |      1| optional  |
+------------+------+--------------------+----------+-------+-----------+
|/ref*/*     |DS    |SubstitutionQV      |uint8     |      1| optional  |
+------------+------+--------------------+----------+-------+-----------+
|/ref*/*     |DS    |SubstitutionTag     |char      |      1| optional  |
+------------+------+--------------------+----------+-------+-----------+
|/ref*/*     |DS    |DeletionTag         |char      |      1| optional  |
+------------+------+--------------------+----------+-------+-----------+
|/ref*/*     |DS    |IPD                 |uint16    |      1| optional  |
+------------+------+--------------------+----------+-------+-----------+
|/ref*/*     |DS    |PulseWidth          |uint16    |      1| optional  |
+------------+------+--------------------+----------+-------+-----------+
|/ref*/*     |DS    |PulseIndex          |uint32    |      1| optional  |
+------------+------+--------------------+----------+-------+-----------+
|/RefGroup   |DS    |ID                  |uint32    |      1| required  |
+------------+------+--------------------+----------+-------+-----------+
|/RefGroup   |DS    |OffsetTable         |uint32    |      3| optional  |
+------------+------+--------------------+----------+-------+-----------+
|/RefGroup   |DS    |Path                |VLEN_STR  |      1| required  |
+------------+------+--------------------+----------+-------+-----------+
|/RefGroup   |DS    |RefInfoID           |uint32    |      1| required  |
+------------+------+--------------------+----------+-------+-----------+
|/RefInfo    |DS    |FullName            |VLEN_STR  |      1| required  |
+------------+------+--------------------+----------+-------+-----------+
|/RefInfo    |DS    |ID                  |uint32    |      1| required  |
+------------+------+--------------------+----------+-------+-----------+
|/RefInfo    |DS    |Length              |uint32    |      1| required  |
+------------+------+--------------------+----------+-------+-----------+
|/RefInfo    |DS    |MD5                 |VLEN_STR  |      1| required  |
+------------+------+--------------------+----------+-------+-----------+
|/BarcodeInfo|DS    |ID                  |uint32    |      1| optional  |
+------------+------+--------------------+----------+-------+-----------+
|/BarcodeInfo|DS    |ID                  |uint32    |      1| required  |
+------------+------+--------------------+----------+-------+-----------+
|/BarcodeInfo|DS    |Name                |VLEN_STR  |      1| required  |
+------------+------+--------------------+----------+-------+-----------+


.. _HDF5 DDL: http://www.hdfgroup.org/HDF5/doc/ddl.html
.. _W3C compatible timestamp: http://www.w3.org/TR/NOTE-datetime
