===================================
BAM format specification for PacBio
===================================

.. moduleauthor:: David Alexander, Marcus Kinsella, Derek Barnett,
                  Armin Toepfer, Brett Bowman


.. warning::
   This specification, while close to being final, is still subject to
   change.  We will provide no support for BAM files until the 3.0
   spec is finalized.


The BAM format is a binary, compressed, record-oriented container
format for raw or aligned sequence reads.  The associated SAM format
is a text representation of the same data.  The `specifications for
BAM/SAM`_ are maintained by the SAM/BAM Format Specification Working
Group.

PacBio-produced BAM files are fully compatible with the BAM
specification.  In this document we describe the way we make use of
the extensibility mechanisms of the BAM specification to encode
PacBio-specific information, as well as conventions we adhere to.

An example file adhering to this specification will be maintained in
the *pbcore* Python library.


Version
=======

The PacBio BAM specification version described here is 3.0b7. PacBio
BAM files adhering to this spec contain the tag ``pb:3.0b7`` in the
``@HD`` header.


Coordinate conventions
======================

The BAM format uses a 0-based coordinate system to refer to positions
and intervals on the reference.

PacBio also uses a 0-based coordinate system to refer to positions and
intervals within sequence reads.  Positions in PacBio reads are
reckoned from the first polymerase read base (as base 0), *not* the
first base in the HQ region.

Perhaps confusingly, the text SAM format uses 1-based coordinate
system.

Note that following the SAM/BAM specification, 0-based coordinate
intervals are defined as half-open (end exclusive) while 1-based
intervals are closed.

.. raw:: latex

         \newpage

*Query* versus *aligned query* terminology
==========================================

A sequence read presented to an aligner is termed a *query*; typically
this query will be a subsequence of an entire PacBio polymerase
read---most commonly, it will be a *subread*, which is basecalls from
a single pass of the insert DNA molecule.

Upon alignment, generally only a subsequence of the query will align
to the reference genome, and that subsequence is referred to as the
*aligned query*.  Under *soft-clipping*, the entirety of the query is
stored in the aligned BAM, but the CIGAR field indicates that some
bases at either end are excluded from the alignment.

Abstractly, we denote the extent of the *query* in polymerase read as
`[qStart, qEnd)` and the extent of the aligned subinterval as `[aStart, aEnd)`
The following graphic illustrates these intervals::

              qStart                         qEnd
    0         |  aStart                aEnd  |
    [--...----*--*---------------------*-----*-----...------)  < "polymerase read" coord. system
              ~~~----------------------~~~~~~                  <  query; "-" = aligning subseq.
    [--...-------*---------...---------*-----------...------)  < "ref." / "target" coord. system
    0            tStart                tEnd


In our BAM files, the qStart, qEnd are contained in the ``qs`` and
``qe`` tags, (and reflected in the ``QNAME``); the bounds of the
*aligned query* in the polymerase read can be determined by adjusting
``qs`` and ``qe`` by the number of soft-clipped bases at the ends of
the alignment (as found in the CIGAR).

.. note::
   In the legacy cmp.h5 file format, soft-clipping was not possible,
   and the bounds of the original query were not stored.  Only
   `aStart, aEnd` were stored, although in that file format they were
   referred to as `rStart, rEnd`.


QNAME convention
================

By convention the ``QNAME`` ("query template name") for unrolled reads
and subreads is in the following format::

   {movieName}/{holeNumber}/{qStart}_{qEnd}

where ``[qStart, qEnd)`` is the 0-based coordinate interval
representing the span of the *query* in the polymerase read, as above.

For CCS reads, the ``QNAME`` convention is::

  {movieName}/{holeNumber}/ccs


CIGAR conventions
=================

The "M" CIGAR op (``BAM_CMATCH``) is *forbidden* in PacBio BAM files.
PacBio BAM files use the more explicit ops "X" (``BAM_CDIFF``) and "="
(``BAM_CEQUAL``).  PacBio software will abort if ``BAM_CMATCH`` is
found in a CIGAR field.


BAM filename conventions
========================

Since we will be using BAM format for different kinds of data, we will
use a ``suffix.bam`` filename convention:

  +------------------------------------+------------------------------+
  | Data type                          | Filename template            |
  +====================================+==============================+
  | Polymerase reads from movie        | *movieName*.polymerase.bam   |
  +------------------------------------+------------------------------+
  | Subreads from movie                | *movieName*.subreads.bam     |
  +------------------------------------+------------------------------+
  | Excised adapters and barcodes      | *movieName*.scraps.bam       |
  +------------------------------------+------------------------------+
  | CCS reads computed from movie      | *movieName*.ccs.bam          |
  +------------------------------------+------------------------------+
  | Aligned subreads in a job          | *jobID*.aligned_subreads.bam |
  +------------------------------------+------------------------------+
  | Aligned CCS in a job               | *jobID*.aligned_ccs.bam      |
  +------------------------------------+------------------------------+


BAM sorting conventions
=======================

*Aligned* PacBio BAM files shall be sorted by position in the standard
fashion as done by ``samtools sort``.  The BAM ``@HD::SO`` tag shall
be set to ``coordinate``.

*Unaligned* PacBio BAM files shall be sorted by ``QNAME``, so that all
subreads from a ZMW hole are stored contiguously in a file, with
groups by ZMW hole number in numerical order, and within a ZMW,
numerically by ``qStart``.  In case subreads and CCS reads are
combined in a BAM, the CCS reads will sort after the subreads (``ccs``
follows ``{qStart}_{qEnd}``). Note that this sorting is not strictly
alphabetical, so we shall set the BAM ``@HD::SO`` tag to ``unknown``.


Use of headers for file-level information
=========================================

Beyond the usual information encoded in headers that is called for
SAM/BAM spec, we encode special information as follows.


``@RG`` (read group) header entries:

  ``ID`` tag (identifier)
      contains an 8-character string interpretable as the hexadecimal
      representation of an integer.  Read groups should have distinct
      ``ID`` values.

      .. note::
         Read group identifiers for PacBio data are calculated as follows::

           RGID_STRING := md5(movieName + "//" + readType))[:8]
           RGID_INT     := int32.Parse(RGID_STRING)

         where `movieName` is the moviename (@RG::PU) and `readType`
         is the read type (found in @RG::DS).  Note that `movieName`
         is lowercase while `readType` is uppercase.  `md5` is
         understood to be the (lowercase) hex md5 digest of the input
         string.

         RGID_STRING is used in the @RG header, while RGID_INT is used
         in the RG tag of BAM records.

         Note that RGID_INT may be negative.

         Example: CCS reads for a movie named "movie32" would have
             - RGID_STRING = "f5b4ffb6"
             - RGID_ID     = -172687434

  ``PL`` tag ("platform"):
      contains ``"PACBIO"``

  ``PU`` tag ("platform unit"):
      contains the PacBio movie name.

  ``DS`` tag ("description"):
      contains some semantic information about the reads in the group,
      encoded as a semicolon-delimited list of "Key=Value" strings, as
      follows:

      **Mandatory items:**

      .. tabularcolumns:: |l|p{5cm}|l|

      +-------------------+----------------------------------------+----------------+
      | Key               | Value spec                             | Value example  |
      +===================+========================================+================+
      | READTYPE          | One of POLYMERASE, HQREGION,           | SUBREAD        |
      |                   | SUBREAD, CCS, SCRAP, or UNKNOWN        |                |
      +-------------------+----------------------------------------+----------------+
      | BINDINGKIT        | Binding kit part number                | 100236500      |
      +-------------------+----------------------------------------+----------------+
      | SEQUENCINGKIT     | Sequencing kit part number             | 001558034      |
      +-------------------+----------------------------------------+----------------+
      | BASECALLERVERSION | Basecaller version number              | 2.1            |
      +-------------------+----------------------------------------+----------------+
      | FRAMERATEHZ       | Frame rate in Hz                       | 100            |
      +-------------------+----------------------------------------+----------------+
      | CONTROL           | TRUE if reads are classified as        | TRUE           |
      |                   | spike-in controls, otherwise CONTROL   |                |
      |                   | key is absent                          |                |
      +-------------------+----------------------------------------+----------------+
      
      .. note::

         The READTYPE values encountered in secondary analysis will be
         limited to SUBREAD and CCS.  The remaining READTYPE values
         will only be encountered in intermediate steps before
         secondary analysis.

      |
      **Base feature manifest---absent item  means feature absent from reads:**


      +---------------------+-----------------------------------------+----------------+
      | Key                 | Value spec                              | Value example  |
      +=====================+=========================================+================+
      | DeletionQV          | Name of tag used for DeletionQV         | dq             |
      +---------------------+-----------------------------------------+----------------+
      | DeletionTag         | Name of tag used for DeletionTag        | dt             |
      +---------------------+-----------------------------------------+----------------+
      | InsertionQV         | Name of tag used for InsertionQV        | iq             |
      +---------------------+-----------------------------------------+----------------+
      | MergeQV             | Name of tag used for MergeQV            | mq             |
      +---------------------+-----------------------------------------+----------------+
      | SubstitutionQV      | Name of tag used for SubstitutionQV     | sq             |
      +---------------------+-----------------------------------------+----------------+
      | SubstitutionTag     | Name of tag used for SubstitutionTag    | st             |
      +---------------------+-----------------------------------------+----------------+
      | Ipd:Frames          | Name of tag used for IPD, in raw frame  | ip             |
      |                     | count.                                  |                |
      +---------------------+-----------------------------------------+----------------+
      | Ipd:CodecV1         | Name of tag used for IPD, compressed    | ip             |
      |                     | according to Codec V1.                  |                |
      +---------------------+-----------------------------------------+----------------+
      | PulseWidth:Frames   | Name of tag used for PulseWidth, in raw | pw             |
      |                     | frame count.                            |                |
      +---------------------+-----------------------------------------+----------------+
      | PulseWidth:CodecV1  | Name of tag used for PulseWidth,        | pw             |
      |                     | compressed according to Codec V1.       |                |
      +---------------------+-----------------------------------------+----------------+




Use of read tags for per-read information
=========================================

  +-----------+------------+------------------------------------------------------------------+
  | **Tag**   | **Type**   | **Description**                                                  |
  +===========+============+==================================================================+
  | qs        | i          | 0-based start of query in the polymerase read (absent in CCS)    |
  +-----------+------------+------------------------------------------------------------------+
  | qe        | i          | 0-based end of query in the polymerase read (absent in CCS)      |
  +-----------+------------+------------------------------------------------------------------+
  | zm        | i          | ZMW hole number                                                  |
  +-----------+------------+------------------------------------------------------------------+
  | np        | i          | NumPasses (1 for subreads, variable for CCS---encodes number of  |
  |           |            | *complete* passes of the insert)                                 |
  +-----------+------------+------------------------------------------------------------------+
  | rq        | f          | Float in [0, 1] encoding expected accuracy                       |
  +-----------+------------+------------------------------------------------------------------+
  | sn        | B,f        | 4 floats for the average signal-to-noise ratio of A, C, G, and T |
  |           |            | (in that order) over the HQRegion                                |
  +-----------+------------+------------------------------------------------------------------+



Use of read tags for per-read-base information
==============================================

The following read tags encode features measured/calculated
per-basecall.  Unlike ``SEQ`` and ``QUAL``, aligners will not orient
these tags.  They will be maintained in *native* orientation (in the
same order and sense as collected from the instrument) even if the
read record has been aligned to the reverse strand.


  +-----------+---------------+----------------------------------------------------+
  | **Tag**   | **Type**      |**Description**                                     |
  +===========+===============+====================================================+
  | dq        | Z             | DeletionQV                                         |
  +-----------+---------------+----------------------------------------------------+
  | dt        | Z             | DeletionTag                                        |
  +-----------+---------------+----------------------------------------------------+
  | iq        | Z             | InsertionQV                                        |
  +-----------+---------------+----------------------------------------------------+
  | mq        | Z             | MergeQV                                            |
  +-----------+---------------+----------------------------------------------------+
  | sq        | Z             | SubstitutionQV                                     |
  +-----------+---------------+----------------------------------------------------+
  | st        | Z             | SubstitutionTag                                    |
  +-----------+---------------+----------------------------------------------------+
  | ip        | B,C *or* B,S  | IPD (raw frames or codec V1)                       |
  +-----------+---------------+----------------------------------------------------+
  | pw        | B,C *or* B,S  | PulseWidth (raw frames or codec V1;                |
  |           |               | **PacBio-internal**)                               |
  +-----------+---------------+----------------------------------------------------+


Notes:

- QV metrics are ASCII+33 encoded as strings
- *DeletionTag* and *SubstitutionTag* represent alternate basecalls,
  or "N" when there is no alternate basecall available.  In other
  words, they are strings over the alphabet "ACGTN".
- Encoding of kinetics features (``ip``, ``pw``) is described below.



Use of sc read tag to annotate scraps
=====================================

Reads that belong to a read group with READTYPE=SCRAP have to be annotated
with the following tag:

  +-----------+---------------+-----------------------------------------+
  | **Tag**   | **Type**      |**Description**                          |
  +===========+===============+=========================================+
  | sc        | A             | Scrap type annotation, one of           |
  |           |               | A:=Adapter, B:=Barcode, or L:=LQRegion  |
  +-----------+---------------+-----------------------------------------+


QUAL
====

The ``QUAL`` field in BAM alignments is intended to reflect the
probability of a basecall being an error.  For PacBio, the utility of
the overall QV is limited; PacBio applications make use of the more
specific QV tracks reflecting probabilities of specific error types.

Thus we populate the ``QUAL`` field of each record with a string of
"0xFF" bytes in the BAM (corresponding to "*" in the SAM record).
APIs may provide an overall QV metric by averaging probabilities
implied by individual QV metrics, then converting back to QV scale.

The ``QUAL`` field will be populated with real values for READTYPE=CCS.


Barcodes and adapters
=====================

In the ``subreads.bam``, we will record per-subread
tags representing the barcode call and a score representing the
confidence of that call.  The exact tags remain to be designated.  The
actual data used to inform the barcode calls---the barcode sequences
and associated pulse features---will be retained in the associated
``scraps.bam`` file, so that ``bam2bam`` can be used at a later time
to reconstitute the full-length polymerase reads in order, for
example, to repeat barcode calling with different options.

Each subread (or CCS read, as the case may be) contains three
additional tags reflecting information about the barcodes and
adapters: ``bc``, ``bq``, and ``cx``.

- The ``bc`` tag contains the *barcode call*, a ``uint16[2]``
  representing the inferred barcodes sequences :math:`B_L, B_R`.
  Integer codes represent position in a FASTA file of barcodes. The
  integer (``uint8``) ``bq`` tag contains the barcode call confidence,
  a Phred-scaled posterior probability that the barcode call in ``bc``
  is correct.  Note that these tags will be computed per-ZMW, not per
  subread, since we can combine information across the multiple
  instances of the barcode sequences in the polymerase read.  In the
  absence of barcodes, ``bc`` and ``bq`` tags will be absent.

- The ``cx`` tag contains a ``uint8`` value encoding the *local
  context* of the subread, indicating information about the
  orientation of the subread and its location with respect to flanking
  landmarks.

  The ``cx`` value is calculated by binary OR-ing together values from
  this flags enum::

    enum LocalContextFlags
    {
        ADAPTER_BEFORE = 1,
        ADAPTER_AFTER  = 2,
        BARCODE_BEFORE = 4,
        BARCODE_AFTER  = 8,
        FORWARD_PASS   = 16,
        REVERSE_PASS   = 32
    };

  Orientation of a subread (designated by one of the mutually
  exclusive ``FORWARD_PASS`` or ``REVERSE_PASS`` bits) can be reckoned
  only if either the adapters or barcode design is asymmetric,
  otherwise these flags must be left unset.  The convention for what
  is considered a "forward" or "reverse" pass is determined by a
  per-ZMW convention, defining one element of the asymmetric
  barcode/adapter pair as the "front" and the other as the "back".  It
  is up to tools producing the BAM to determine whether to use
  adapters or barcodes to reckon the orientation, but if pass
  directions cannot be confidently and consistently assessed for the
  subreads from a ZMW, neither orientation flag should be set. Tools
  consuming the BAM should be aware that orientation information may
  be unavailable for subreads in a ZMW, but if is available for any
  subread in the ZMW, it will be available for all subreads in the
  ZMW.

  The ``ADAPTER_*`` and ``BARCODE_*`` flags reflect whether the
  subread is flanked by adapters or barcodes at the ends.

  The main production use case for this tag is CCS, where it is
  important to know whether the subread is "end-to-end", i.e. whether
  it is immediately flanked by barcode/adapter sequences, and where
  foreknowledge of the orientation can save some work.

Barcode information will follow the same convention in CCS output
(``ccs.bam`` files), except the ``cx`` tag will be absent.

Examples
---------

.. tabularcolumns:: |l|p{1.5cm}|p{1.5cm}|p{4cm}|

+--------------------------+-----------+----------+---------------------+
|Scenario                  | ``bc``    |  ``bq``  | ``cx``              |
+==========================+===========+==========+=====================+
| No barcodes, end-to-end, | *absent*  | *absent* | ``1|2 = 3``         |
| unknown orientation      |           |          |                     |
+--------------------------+-----------+----------+---------------------+
| Asymmetric barcodes,     | { 1, 37 } |   35     | ``1|2|4|8|16 = 31`` |
| end-to-end, forward pass |           |          |                     |
+--------------------------+-----------+----------+---------------------+
| Symmetric barcodes,      | { 8, 8 }  |   33     |  ``1|2|4|8 = 15``   |
| end-to end               |           |          |                     |
+--------------------------+-----------+----------+---------------------+
| Barcoded, HQ region      | { 8, 8 }  |   33     | ``1|4 = 5``         |
| terminates before second |           |          |                     |
| barcode; unknown         |           |          |                     |
| orientation              |           |          |                     |
+--------------------------+-----------+----------+---------------------+



Alignment: soft-clipping
========================

In the standard production configuration, PacBio's aligners will be
used to align either subreads or CCS reads.  In either case, we will
use *soft clipping* to preserve the unaligned bases at either end of
the query in the aligned BAM file.


Encoding of kinetics pulse features
===================================

Interpulse duration (IPD) and pulsewidth are measured in frames;
natively they are recorded as a ``uint16`` per pulse/base event.  They
may be encoded in BAM read tags in one of two fashions:

  - losslessly as an array of ``uint16``; necessary for PacBio-internal
    applications but entails greater disk space usage.

  - lossy 8-bit compression stored as a ``uint8`` array, following the
    codec specified below ("codec V1").  Provides a substantial
    disk-space savings without affecting important production use
    cases (base modification detection).

In the default production instrument configuration, the lossy encoding
will be used.  The instrument can be switched into a mode
(PacBio-internal mode) where it will emit the full lossless kinetic
features.

Similarly, PulseWidth will *not* be included in the BAM file in the
default production instrument configuration, but it will be available
in "PacBio-internal instrument" mode.

The lossy encoding for IPD and pulsewidth values into the available 256
codepoints is as follows (**codec v1**):

  +---------------------+-----------------+
  | Frames              | Encoding        |
  +---------------------+-----------------+
  | 0 .. 63             | 0, 1, .. 63     |
  +---------------------+-----------------+
  | 64, 66, .. 190      | 64, 65, .. 127  |
  +---------------------+-----------------+
  | 192, 196 .. 444     | 128, 129 .. 191 |
  +---------------------+-----------------+
  | 448, 456, .. 952    | 192, 193 .. 255 |
  +---------------------+-----------------+

In other words, we use the first 64 codepoints to encode frame counts
at single frame resolution, the next 64 to encode the frame counts at
two-frame resolution, and so on.  Durations exceeding 952 frames are
capped at 952.  Durations not enumerated in "Frames" above are rounded
to the nearest enumerated duration then encoded.  For example, a
duration of 194 frames would round to 196 and then be encoded as
codepoint 129.

This encoding has the following features, considered essential for
internal analysis use cases:

- *Exact* frame-level resolution for small durations (up to 64 frames)
- Maximal representable duration is 9.52 seconds (at 100fps), which is
  reasonably far into the tail of the distributions of these metrics.
  Analyses of "pausing" phenomena may still need to account for this
  censoring.

A reference implementation of this encoding/decoding scheme can be
found in `pbcore`.


Unresolved issues
=================

- Need to move from strings to proper array types for QVs
- Need better dynamic range in `rq`, esp. for CCS
- '/' preferable to ':' in "IPD:CodecV1"
- Desire for spec for shorter movienames, especially if these are
  ending up in QNAMEs.

.. _specifications for BAM/SAM: http://samtools.github.io/hts-specs/SAMv1.pdf
