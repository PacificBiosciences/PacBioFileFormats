==========================================
PacBio BAM index file (``bam.pbi``) format
==========================================

.. moduleauthor:: Derek Barnett, James Drake

PacBio's previous alignment file format (``cmp.h5``) contained a data
table called the *alignment index* that recorded auxiliary identifying
information and precomputed summary statistics per aligned read. This
table served several purposes:

  1. it enabled fast random access to aligned reads satisfying fairly
     complex predicates, for example, reads from a specific list of
     ZMWs which had unambiguous mapping (MapQV==254), or a read with a
     given readname.

  2. it allowed summary reports (readlength, mapped identity/accuracy,
     etc.) to be constructed by quick operations over the alignment
     index instead of loading all of the sequence reads for each
     analysis.

In order to provide backwards-compatibility with the APIs enabled for
accessing the ``cmp.h5``, we have devised a new BAM companion file,
the *PacBio BAM index*, which supports the two use cases above.

Version
===========

This is version ``4.0.0`` of the ``bam.pbi`` specification.

Changelog
===========

  [4.0.0] - 2020-10-08
    * Added nInsOps, nDelOps fields to mapped data section.

  [3.0.2] - 2018-09-13
    * qStart,qLen for CCS records now stored as (0,qLen) instead of (-1,-1)

  [3.0.1] - 2015-09-23
    * Local context flags moved into the always-present "basic" data section.

  [3.0.0] - 2015-07-12
    * Initial publishing of specification.

Format
===========

The format mimics the HDF5 column-based approach without requiring the additional
library dependency. Most sections are laid out as a series of 1-dimensional arrays,
a la HDF5 datasets. Calculating an average or maximum mapQV, for example, would
simply involve a block read of the array and the relevant computation.

It enables the 2 major use cases listed above

  1. Random-access queries, including:

     * by reference or genomic region
     * by read group
     * by query name
     * by ZMW
     * by barcode index
     * etc.

  2. Obtain information without processing entire BAM file

     * Calculate summary statistics
     * Reverse-lookup - get information for a record, given its index

Like the associated BAM & BAI formats, PBI is compressed in the BGZF format.
  See `SAM/BAM spec`_ for details.

All multi-byte numbers in PBI are stored little-endian.

All optional columns in PBI are either present for all rows or for none of them,
  and always present in the order described in this document. This is important
  for correctly accessing specific values by column index.

File sections follow each other immediately in the file and are described below.

  * `PBI Header`_
  * `Basic Data`_
  * `Mapped Data`_ (optional)
  * `Coordinate-Sorted Data`_ (optional)
  * `Barcode Data`_ (optional)

.. _PBI Header:

PBI Header
------------

+-----------+----------+-------------------------------------+---------------+
| Field     | Size     | Definition                          | Value         |
+===========+==========+=====================================+===============+
| magic     | char[4]  | PBI magic string                    | ``PBI\1``     |
+-----------+----------+-------------------------------------+---------------+
| version   | uint32_t | PBI format version (xx.yy.zz)       | 0x00xxyyzz    |
+-----------+----------+-------------------------------------+---------------+
| pbi_flags | uint16_t | bitflag describing file contents :sup:`1`           |
+-----------+----------+-------------------------------------+---------------+
| n_reads   | uint32_t | number of reads in the BAM file                     |
+-----------+----------+-------------------------------------+---------------+
| reserved  | char[18] | reserved space for future expansion | fill(0x00)    |
+-----------+----------+-------------------------------------+---------------+

:sup:`1` pbi_flags:

 +-------------------+--------+-----------------------------------------------+
 | Flag              | Value  | Description                                   |
 +===================+========+===============================================+
 | Basic             | 0x0000 | PbiHeader & BasicData only                    |
 +-------------------+--------+-----------------------------------------------+
 | Mapped            | 0x0001 | MappedData section present                    |
 +-------------------+--------+-----------------------------------------------+
 | Coordinate Sorted | 0x0002 | CoordinateSortedData section present          |
 +-------------------+--------+-----------------------------------------------+
 | Barcode           | 0x0004 | BarcodeData section present                   |
 +-------------------+--------+-----------------------------------------------+

 (0x0008 - 0x8000) are available to mark future data modifiers, add'l sections, etc.

.. _Basic Data:

Basic Data
------------

This section contains data that apply to all PacBio BAM reads.

Each index field is laid out as a column (array), consisting of one value per
BAM record. Thus for *N* records, this section will contain *N* rgId values,
followed by *N* qStart values, then *N* qEnd values, and so on.

+----------------+----------+------------------------------------------------------+
| Field          | Size     | Definition                                           |
+================+==========+======================================================+
| rgId           | int32_t  | Integral value of ``@RG::ID`` :sup:`1`               |
+----------------+----------+------------------------------------------------------+
| qStart         | int32_t  | Start of query in polymerase read (0 for CCS reads)  |
+----------------+----------+------------------------------------------------------+
| qEnd           | int32_t  | End of query in polymerase read (qLen for CCS reads) |
+----------------+----------+------------------------------------------------------+
| holeNumber     | int32_t  | The holenumber of the ZMW producing the read         |
+----------------+----------+------------------------------------------------------+
| readQual       | float    | Expected accuracy ('rq' tag) [0-1]                   |
+----------------+----------+------------------------------------------------------+
| ctxt_flag      | uint8_t  | Local context of subread ('cx' tag) :sup:`2`         |
+----------------+----------+------------------------------------------------------+
| fileOffset     | int64_t  | Virtual offset of record (``bgzf_tell``)             |
+----------------+----------+------------------------------------------------------+

  :sup:`1` Read group identifiers for PacBio data are calculated as follows::

     RGID_STRING := md5(movieName + "//" + readType)) [:8]
     RGID_INT    := int32.Parse(RGID_STRING)

     RGID_STRING is used in the @RG header and in the `RG` tag of BAM
     records. RGID_INT is used here in the PBI index.

     Note that RGID_INT may be negative.

  :sup:`2`
    Local context flags are only valid for Subread / Insert records. For all
    other record-types, or if the CX tag is not present in the record, this
    value should be 0

.. _Mapped Data:

Mapped Data
------------

This section contains data that apply to all mapped PacBio BAM reads.

Each index field is laid out as a column (array), consisting of one value per
BAM record. Thus for *N* records, this section will contain *N* tId values,
followed by *N* tStart values, then *N* tEnd values, and so on.

+----------------+----------+-----------------------------------------------+
| Field          | Size     | Definition                                    |
+================+==========+===============================================+
| tId            | int32_t  | BAM tid indication aligned reference          |
+----------------+----------+-----------------------------------------------+
| tStart         | uint32_t | (0-based) Start of alignment in reference     |
+----------------+----------+-----------------------------------------------+
| tEnd           | uint32_t | End of alignment in reference (endpos)        |
+----------------+----------+-----------------------------------------------+
| aStart         | uint32_t | Start of aligned query in polymerase read     |
+----------------+----------+-----------------------------------------------+
| aEnd           | uint32_t | End of aligned query in polymerase read       |
+----------------+----------+-----------------------------------------------+
| revStrand      | uint8_t  | 1 if reverse strand alignment, else 0         |
+----------------+----------+-----------------------------------------------+
| nM             | uint32_t | Number of base matches in alignment           |
+----------------+----------+-----------------------------------------------+
| nMM            | uint32_t | Number of base mismatches in alignment        |
+----------------+----------+-----------------------------------------------+
| mapQV          | uint8_t  | The mapping quality [valid ranges 0-254]      |
+----------------+----------+-----------------------------------------------+
| nInsOps        | uint32_t | Number of insertion operations (not bases)    |
+----------------+----------+-----------------------------------------------+
| nDelOps        | uint32_t | Number of deletion operations (not bases)     |
+----------------+----------+-----------------------------------------------+

.. note::
  Inserted and deleted base counts are not included in the index.
  These values are readily computed as::

    nInsertedBases = aEnd - aStart - nM - nMM
    nDeletedBases = tEnd - tStart - nM - nMM

  Alignment length can be computed using::

    aEnd - aStart + tEnd - tStart - nM - nMM

.. _Coordinate-Sorted Data:

Coordinate-Sorted Data
------------------------

In a coordinate-sorted BAM file, the records that are mapped to each reference
form contiguous blocks. The data in this section provide a mapping between each
tId and its start/end rows :sup:`2`.

The lookup table is prefixed with the number of reference entries.

+----------------+----------+-----------------------------------------------+
| Field          | Size     | Definition                                    |
+================+==========+===============================================+
| n_tids         | uint32_t | Number of reference sequences                 |
+----------------+----------+-----------------------------------------------+

The lookup table is laid out as a column (array) of tuples, one per reference.

+----------------+----------+-----------------------------------------------+
| Field          | Size     | Definition                                    |
+================+==========+===============================================+
| tId            | uint32_t | reference sequence ID :sup:`1`                |
+----------------+----------+-----------------------------------------------+
| beginRow       | uint32_t | index of first record mapped on tId :sup:`2`  |
+----------------+----------+-----------------------------------------------+
| endRow         | uint32_t | index of last record mapped on tId :sup:`2`   |
+----------------+----------+-----------------------------------------------+

:sup:`1`
  This dataset should be sorted in *ascending order of the uint32 cast of tId*
  (thus a tId of -1 will follow all other tId values)

:sup:`2`
  Data fields ``beginRow`` and ``endRow``. If ``tId[i]==t``, then
  ``[beginRow, endRow)`` represents range of reads (by 0-based
  ordinal position in the BAM file) mapped to the reference contig
  with *tId* of *t*. If no BAM records are aligned to *t*, then we
  should have ``beginRow, endRow = -1``.

.. _`Barcode Data`:

Barcode Data
---------------

This section contains data that apply to all barcoded PacBio BAM reads.

Each index field is laid out as a column (array), consisting of one value per
BAM record. Thus for *N* records, this section will contain *N* bc_forward
values, followed by *N* bc_reverse values, then *N* bc_qual values.

+---------------+----------+----------------------------------------------+
| Field         | Size     | Definition                                   |
+===============+==========+==============================================+
| bc_forward    | int16_t  | B_F from 'bc' tag (index to barcode FASTA),  |
|               |          | or -1 if not present                         |
+---------------+----------+----------------------------------------------+
| bc_reverse    | int16_t  | B_R from 'bc' tag (index to barcode FASTA),  |
|               |          | or -1 if not present                         |
+---------------+----------+----------------------------------------------+
| bc_qual       | int8_t   | barcode call confidence ('bq' tag),          |
|               |          | or -1 if not present                         |
+---------------+----------+----------------------------------------------+

.. note::
  If the Barcode flag is set in the header, these values must be present
  in all rows, otherwise it should be present for none of them.

  If one Barcode field is set to -1 / non-existant, then all barcode-related
  fields should be set as such.

 .. _`SAM/BAM spec`: http://samtools.github.io/hts-specs/SAMv1.pdf
