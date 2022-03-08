===================================
BAM format specification for PacBio
===================================

.. moduleauthor:: Derek Barnett, David Seifert, James Drake, Jessica Mattick,
                  Martin Smith, Armin Toepfer

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

The PacBio BAM specification version described here is 6.0.0. PacBio
BAM files adhering to this spec contain the tag ``pb:6.0.0`` in the
``@HD`` header.


Coordinate conventions
======================

The BAM format uses a 0-based coordinate system to refer to positions
and intervals on the reference.

PacBio also uses a 0-based coordinate system to refer to positions and
intervals within sequence reads.  Positions in PacBio reads are
reckoned from the first ZMW read base (as base 0), *not* the
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
this query will be a subsequence of an entire PacBio ZMW
read---most commonly, it will be a *subread*, which is basecalls from
a single pass of the insert DNA molecule.

Upon alignment, generally only a subsequence of the query will align
to the reference genome, and that subsequence is referred to as the
*aligned query*.  Under *soft-clipping*, the entirety of the query is
stored in the aligned BAM, but the CIGAR field indicates that some
bases at either end are excluded from the alignment.

Abstractly, we denote the extent of the *query* in ZMW read as
`[qStart, qEnd)` and the extent of the aligned subinterval as `[aStart, aEnd)`
The following graphic illustrates these intervals::

              qStart                         qEnd
    0         |  aStart                aEnd  |
    [--...----*--*---------------------*-----*-----...------)  < "ZMW read" coord. system
              ~~~----------------------~~~~~~                  <  query; "-" = aligning subseq.
    [--...-------*---------...---------*-----------...------)  < "ref." / "target" coord. system
    0            tStart                tEnd


In our BAM files, the qStart, qEnd are contained in the ``qs`` and
``qe`` tags, (and reflected in the ``QNAME``); the bounds of the
*aligned query* in the ZMW read can be determined by adjusting
``qs`` and ``qe`` by the number of soft-clipped bases at the ends of
the alignment (as found in the CIGAR).

.. note::
   In the legacy cmp.h5 file format, soft-clipping was not possible,
   and the bounds of the original query were not stored.  Only
   `aStart, aEnd` were stored, although in that file format they were
   referred to as `rStart, rEnd`.

HiFi reads
==========
HiFi reads are defined as consensus reads with a QV >=20. These are treated in 
the same manner as CCS reads in PacBio BAM files, unless noted otherwise.

QNAME convention
================

By convention the ``QNAME`` ("query template name") for unrolled reads
and subreads is in the following format::

   {movieName}/{holeNumber}/{qStart}_{qEnd}

where ``[qStart, qEnd)`` is the 0-based coordinate interval
representing the span of the *query* in the ZMW read, as above.

For CCS reads, the ``QNAME`` convention is::

  {movieName}/{holeNumber}/ccs

The ``QNAME`` for by-strand CCS reads includes a suffix ``fwd`` or ``rev`` to 
indicate strand relative to the other by-strand read for the ZMW. Strand 
assignment by CCS is arbitrary and does not imply the strand that may be 
assigned during mapping.

  {movieName}/{holeNumber}/ccs/fwd
  {movieName}/{holeNumber}/ccs/rev

For segmented CCS reads, the base ``QNAME`` follows the CCS read conventions, 
while also appending the 0-based coordinate interval ``[qStart, qEnd)`` that 
represents a span within the source read:: 

  {movieName}/{holeNumber}/ccs/{qStart}_{qEnd}
  {movieName}/{holeNumber}/ccs/fwd/{qStart}_{qEnd}
  {movieName}/{holeNumber}/ccs/rev/{qStart}_{qEnd}

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
  | ZMW reads from movie               | *movieName*.zmws.bam         |
  +------------------------------------+------------------------------+
  | Analysis-ready subreads :sup:`1`   | *movieName*.subreads.bam     |
  |  from movie                        |                              |
  +------------------------------------+------------------------------+
  | Excised adapters, barcodes, and    | *movieName*.scraps.bam       |
  |  rejected subreads                 |                              |
  +------------------------------------+------------------------------+
  | CCS reads computed from movie      | *movieName*.ccs.bam          |
  +------------------------------------+------------------------------+
  | Aligned subreads in a job          | *jobID*.aligned_subreads.bam |
  +------------------------------------+------------------------------+
  | Aligned CCS in a job               | *jobID*.aligned_ccs.bam      |
  +------------------------------------+------------------------------+

  :sup:`1`
    Data in a ``subreads.bam`` file should be ``analysis ready``, meaning
    that all of the data present is expected to be useful for down-stream
    analyses.  Any subreads for which we have strong evidence will not
    be useful (e.g. double-adapter inserts, single-molecule artifacts)
    should be excluded from this file and placed in ``scraps.bam`` as
    a ``Filtered`` with an SC tag of ``F``.

BAM sorting conventions
=======================

*Aligned* PacBio reads shall be sorted by position in the standard
fashion as done by ``samtools sort``.  The BAM ``@HD::SO`` tag shall
be set to ``coordinate``.

*Unaligned* PacBio reads are grouped by ZMW hole number, sorted in numerical order.
Reads from a ZMW are stored contiguously in a BAM file. Within a ZMW subreads 
are stored first, sorted numerically by ``{qStart}_{qEnd}``, followed by CCS 
reads, and finally segmented CCS reads, sorted numerically by ``{qStart}_{qEnd}``. 
This is similar to sorting by ``QNAME`` but not strictly alphabetical, so the 
BAM ``@HD:SO`` header tag is set to ``unknown``.


Use of headers for file-level information
=========================================

Beyond the usual information encoded in headers that is called for
SAM/BAM spec, we encode special information as follows.


``@RG`` (read group) header entries:

  ``ID`` tag (identifier):
      contains an 8-character string interpretable as the hexadecimal
      representation of an integer.  Optionally, a read group identifier may
      contain barcode labels to distinguish demultiplexed samples. Read groups
      should have distinct ``ID`` values.

      .. note::
         Standard read group identifiers for PacBio data are calculated as
         follows::

           RGID_STRING := md5(movieName + "//" + readType)[:8]

         where `movieName` is the moviename (@RG::PU) and `readType`
         is the read type (found in @RG::DS).  Note that `movieName`
         is lowercase while `readType` is uppercase.  `md5` is
         understood to be the (lowercase) hex md5 digest of the input
         string.

         Optionally for `readType` CCS, strandness can be encoded in the ``ID``.
         This is to ensure that multiple types of reads, double- and single-
         stranded, can be stored in the same BAM file, without hole number
         collisions in the PacBio BAM index file.
         The RGID_STRING is then defined as::

           RGID_STRING := md5(movieName + "//" + readType + "// + strand)[:8]

         where strand must be lowercase ``fwd`` or ``rev``; it may not be empty.

         The RGID_INT is defined as::

           RGID_INT    := int32.Parse(RGID_STRING)

         RGID_STRING is used in the @RG header and in the `RG` tag of
         BAM records, while RGID_INT is used in the PacBio BAM index
         file.

         Note that RGID_INT may be negative.

         Example: CCS reads for a movie named "movie32" would have
             - RGID_STRING = "f5b4ffb6"
             - RGID_INT    = -172687434

         Optional barcode labels must be appended to the RGID_STRING as
         follows::

           {RGID_STRING}/{bcForward}--{bcReverse}

         where the ``bcForward`` and ``bcReverse`` labels correspond to the
         0-based positions in the FASTA file of barcodes. These are the same
         values used to populate a barcoded record's ``bc`` tag.

  ``PL`` tag ("platform"):
      contains ``"PACBIO"``.

  ``PM`` tag ("platform model"):
      contains ``"ASTRO"``, ``"RS"``, or ``"SEQUEL"``, reflecting the
      PacBio instrument series.

  ``PU`` tag ("platform unit"):
      contains the PacBio movie name.

  ``LB`` tag ("Well Sample Name"):
      contains the user-supplied name of the library.

  ``SM`` tag ("Bio Sample Name"):
      contains the user-supplied name of the biological sample.

  ``BC`` tag ("barcodes"):
      contains the barcode sequences associated with this read group. This tag
      is not required in all PacBio BAM files, but must be provided when the
      read group ID includes barcode labels.

      The value must be represented in the format recommended by the SAM/BAM
      spec. Barcode *sequences* will be concatenated by a single dash. If both
      barcodes are the same, only one needs to be provided.

        {seq}
        {seq1}-{seq2}

      Note that this differs from the format used to label barcode indices on
      a read group's ID.

  ``DS`` tag ("description"):
      contains some semantic information about the reads in the group,
      encoded as a semicolon-delimited list of "Key=Value" strings, as
      follows:

      **Mandatory items:**

      .. tabularcolumns:: |l|p{5cm}|l|

      +-------------------+-------------------------------------------+------------------+
      | Key               | Value spec                                | Value example    |
      +===================+===========================================+==================+
      | READTYPE          | One of SUBREAD, CCS, SEGMENT,             | SUBREAD          |
      |                   | ZMW, HQREGION, SCRAP, or UNKNOWN          |                  |
      +-------------------+-------------------------------------------+------------------+
      | SOURCE            | For segmented reads, the READTYPE of its  | CCS              |
      |                   | source read. Key is present for segmented |                  |
      |                   | reads only.                               |                  |
      +-------------------+-------------------------------------------+------------------+
      | BINDINGKIT        | Binding kit part number                   | 100-236-500      |
      +-------------------+-------------------------------------------+------------------+
      | SEQUENCINGKIT     | Sequencing kit part number                | 001-558-034      |
      +-------------------+-------------------------------------------+------------------+
      | BASECALLERVERSION | Basecaller version number                 | 5.0.0            |
      +-------------------+-------------------------------------------+------------------+
      | FRAMERATEHZ       | Frame rate in Hz                          | 100              |
      +-------------------+-------------------------------------------+------------------+
      | CONTROL           | TRUE if reads are classified as           | TRUE             |
      |                   | spike-in controls, otherwise CONTROL      |                  |
      |                   | key is absent                             |                  |
      +-------------------+-------------------------------------------+------------------+
      | STRAND            | Stores strandness of single-stranded      | FORWARD          |
      |                   | reads as FORWARD or REVERSE.              |                  |
      |                   | Key is absent if reads are                |                  |
      |                   | double-stranded. Only applies to CCS or   |                  |
      |                   | segmented CCS reads.                      |                  |
      +-------------------+-------------------------------------------+------------------+

      .. note::

         The READTYPE values encountered in secondary analysis will be limited to SUBREAD, 
         CCS, and SEGMENT.  The remaining READTYPE values will only be 
         encountered in intermediate steps before secondary analysis.

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


      **Optional items:**

      .. note::

         These items are optional if there are no "bc" tags in the reads
         belonging to this read-group, otherwise they are mandatory.

      +---------------------+-----------------------------------------+----------------------------------+
      | Key                 | Value spec                              | Value example                    |
      +=====================+=========================================+==================================+
      | BarcodeFile         | Name of the Fasta file containing the   | pacbio_384_barcodes.fasta        |
      |                     | sequences of the barcodes used          |                                  |
      +---------------------+-----------------------------------------+----------------------------------+
      | BarcodeHash         | The MD5 hash of the contents of the     | 0a294bb959fc6c766967fc8beeb4d88d |
      |                     | barcoding sequence file, as generated   |                                  |
      |                     | by the *md5sum* commandline tool        |                                  |
      +---------------------+-----------------------------------------+----------------------------------+
      | BarcodeCount        | The number of barcode sequences in the  | 384                              |
      |                     | Barcode File                            |                                  |
      +---------------------+-----------------------------------------+----------------------------------+
      | BarcodeMode         | Experimental design of the barcodes     | Symmetric                        |
      |                     | Must be Symmetric/Asymmetric/Tailed or  |                                  |
      |                     | None                                    |                                  |
      +---------------------+-----------------------------------------+----------------------------------+
      | BarcodeQuality      | The type of value encoded by the bq tag | Probability                      |
      |                     | Must be Score/Probability/None          |                                  |
      +---------------------+-----------------------------------------+----------------------------------+


Use of read tags for per-read information
=========================================

  +-----------+------------+-------------------------------------------------------------------------+
  | **Tag**   | **Type**   | **Description**                                                         |
  +===========+============+=========================================================================+
  | qs        | i          | 0-based start of query in the ZMW read (absent in CCS).                 |
  |           |            | For segmented CCS reads, the 0-based start of the query in its source   |
  |           |            | read.                                                                   | 
  +-----------+------------+-------------------------------------------------------------------------+
  | qe        | i          | 0-based end of query in the ZMW read (absent in CCS).                   |
  |           |            | For segmented CCS reads, the 0-based end of the query in its source     | 
  |           |            | read.                                                                   |
  +-----------+------------+-------------------------------------------------------------------------+
  | ws        | i          | Start of first base of the query ('qs') in approximate raw frame count  |
  |           |            | since start of movie. For CCS and segmented CCS reads, the start of the | 
  |           |            | first base of the first incorporated subread.                           |
  +-----------+------------+-------------------------------------------------------------------------+
  | we        | i          | Start of last base of the query ('qe - 1') in approximate raw frame     |
  |           |            | count since start of movie. For CCS and segmented CCS reads, the start  |
  |           |            | of the last base of the last incorporated subread.                      |
  +-----------+------------+-------------------------------------------------------------------------+
  | zm        | i          | ZMW hole number                                                         |
  +-----------+------------+-------------------------------------------------------------------------+
  | np        | i          | Number of passes. 1 for subreads, variable for CCS and segmented CCS    | 
  |           |            | reads - encodes number of *complete* passes of the insert. Segmented    |
  |           |            | CCS reads inherit this value from the source read.                      |
  +-----------+------------+-------------------------------------------------------------------------+
  | ec        | f          | Effective coverage. The average subread coverage across all windows     |
  |           |            | (only present in CCS and segmented CCS reads). Segmented CCS reads      |
  |           |            | reads inherit this value from the source read.                          |
  +-----------+------------+-------------------------------------------------------------------------+
  | rq        | f          | Float in [0, 1] encoding expected accuracy                              |
  +-----------+------------+-------------------------------------------------------------------------+
  | sn        | B,f        | 4 floats for the average signal-to-noise ratio of A, C, G, and T (in    |
  |           |            | (that order) over the HQRegion                                          |
  +-----------+------------+-------------------------------------------------------------------------+



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
  | pw        | B,C *or* B,S  | PulseWidth (raw frames or codec V1)                |
  +-----------+---------------+----------------------------------------------------+


Notes:

- QV metrics are ASCII+33 encoded as strings
- *DeletionTag* and *SubstitutionTag* represent alternate basecalls,
  or "N" when there is no alternate basecall available.  In other
  words, they are strings over the alphabet "ACGTN".
- The IPD (interpulse duration) value associated with a base is the number of
  frames *preceding* its incorporation, while the PW (pulse width) is the
  number of frames during its incorporation.
- Encoding of kinetics features (``ip``, ``pw``) is described below.


Use of read tags for HiFi per-read-base kinetic information
===========================================================

The following read tags contain averaged kinetic information (IPD/PulseWidth)
from subreads when applying CCS to generate HiFi reads. These are computed
and stored independently for both orientations of the insert. Forward is
defined & stored with respect to the orientation represented in ``SEQ`` and is
considered to be the native orientation. Reverse tags are stored in the opposite
direction, e.g. from the last base to the first. As with other PacBio-specific
tags, aligners will not re-orient these fields.


  +-----------+---------------+----------------------------------------------------+
  | **Tag**   | **Type**      |**Description**                                     |
  +===========+===============+====================================================+
  | fi        | B,C           | Forward IPD (codec V1)                             |
  +-----------+---------------+----------------------------------------------------+
  | ri        | B,C           | Reverse IPD (codec V1)                             |
  +-----------+---------------+----------------------------------------------------+
  | fp        | B,C           | Forward PulseWidth (codec V1)                      |
  +-----------+---------------+----------------------------------------------------+
  | rp        | B,C           | Reverse PulseWidth (codec V1)                      |
  +-----------+---------------+----------------------------------------------------+
  | fn        | i             | Forward number of complete passes (zero or more)   |
  +-----------+---------------+----------------------------------------------------+
  | rn        | i             | Reverse number of complete passes (zero or more)   |
  +-----------+---------------+----------------------------------------------------+

The following clipping example illustrates the coordinate system for these tags,
shown as stored in the BAM file::

  --------
  Original
  --------

      SEQ:  A   A   C   C   G   T   T   A   G   C
    fi/fp: f0, f1, f2, f3, f4, f5, f6, f7, f8, f9
    ri/rp: r9, r8, r7, r6, r5, r4, r3, r2, r1, r0

  -----------------
  Clipped to [1, 4)
  -----------------

      SEQ:  A   C   C
    fi/fp: f1, f2, f3
    ri/rp: r3, r2, r1

Notes:

- When CCS filtering is disabled, no averaging occurs with ZMWs that don't
  have enough passes to generate HiFi reads. Instead, the pw/ip values are
  passed as is from a representative subread.
- Minor cases exist where a certain orientation may get filtered out entirely
  from a ZMW, preventing valid values from being passed for that record. In
  these cases, empty lists will be passed for the respective record/orientation
  and number of passes will be set to zero.
- Flanking zeroes in kinetics arrays should be ignored for the respective strand.
  For instance, when ``SEQ`` is ``AAACGCGTTT`` and ``fp:B:C,0,0,0,3,4,5,6,0,0,0``,
  then any downstream application should only use ``CGCG`` in its analysis, and
  ignore the ``AAA`` and ``TTT`` stretches.


Use of read tags for per-read-base base modifications
=====================================================

The following read tags encode base modification information. Base modifications are
encoded according to the `SAM tags specifications`_ and any conflict is unintentional.


  +-----------+---------------+----------------------------------------------------+
  | **Tag**   | **Type**      |**Description**                                     |
  +===========+===============+====================================================+
  | Mm        | Z             | Base modifications / methylation                   |
  +-----------+---------------+----------------------------------------------------+
  | Ml        | B,C           | Base modification probabilities                    |
  +-----------+---------------+----------------------------------------------------+


Notes:

- For informational purposes only: The continuous probability range of 0.0 to 1.0 is
  remapped to the discrete integers 0 to 255 inclusively in the ``Ml`` tag.
  The probability range corresponding to an integer *N* is *N/256* to *(N + 1)/256*.


How to annotate scrap reads
===========================

Reads that belong to a read group with READTYPE=SCRAP have to be annotated
in a hierarchical fashion:

1) Classification with tag *sz* occurs on a per ZMW level, distinguishing
   between spike-in controls, sentinels of the basecaller, malformed ZMWs,
   and user-defined templates.
2) A region-wise annotation with tag *sc* to label adapters, barcodes,
   low-quality regions, and filtered subreads.

  +-----------+---------------+-----------------------------------------+
  | **Tag**   | **Type**      |**Description**                          |
  +===========+===============+=========================================+
  | sz        | A             | ZMW classification annotation, one of   |
  |           |               | N:=Normal, C:=Control, M:=Malformed,    |
  |           |               | or S:=Sentinel :sup:`1`                 |
  +-----------+---------------+-----------------------------------------+
  | sc        | A             | Scrap region-type annotation, one of    |
  |           |               | A:=Adapter, B:=Barcode, L:=LQRegion,    |
  |           |               | or F:=Filtered :sup:`2`                 |
  +-----------+---------------+-----------------------------------------+

  :sup:`1`
    reads in the subreads/hqregions/zmws.bam file are implicitly
    marked as Normal, as they stem from user-defined templates.

  :sup:`2`
    sc tags 'A', 'B', and 'L' denote specific classes of non-subread data,
    whereas the 'F' tag is reserved for subreads that are undesirable for
    downstream analysis, e.g., being artifactual or too short.

QUAL
====

The ``QUAL`` field in BAM alignments is intended to reflect the
reliability of a basecall, using the Phred-encoding convention, as
described in the `SAM spec`__.

Both CCS and raw read BAM files respect this convention; historically,
and for the present moment, the encoded probability reflects the
confidence of a basecall against alternatives including substitution,
deletion, and insertion.

*We expect that more details will follow here in a later spec revision.*

__ `specifications for BAM/SAM`


Subread local context
=====================

Some algorithms can make use of knowledge that a subread was flanked
on both sides by adapter or barcode hits, or that the subread was in
one orientation or the other (as can be deduced when asymmetric
adapters or barcodes are used).

To facilitate such algorithms, we furnish the ``cx`` bitmask tag for
subread records.  The ``cx`` value is calculated by binary OR-ing
together values from this flags enum::

  enum LocalContextFlags
  {
      ADAPTER_BEFORE     = 1,
      ADAPTER_AFTER      = 2,
      BARCODE_BEFORE     = 4,
      BARCODE_AFTER      = 8,
      FORWARD_PASS       = 16,
      REVERSE_PASS       = 32,
      ADAPTER_BEFORE_BAD = 64,
      ADAPTER_AFTER_BAD  = 128
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

The ``ADAPTER_BEFORE_BAD`` and ``ADAPTER_AFTER_BAD`` flags indicate
that one or both adapters flanking this subread do not align to the
adapter reference sequence(s). The adapter on this flank could be missing
from the pbell molecule, or obscured by a local decrease in accuracy.
Likewise, some nearby barcode or insert bases may be missing or
obscured. ``ADAPTER_*_BAD`` flags can not be set unless the
corresponding ``ADAPTER_*`` flag is set.

This tag is mandatory for subread records, but will be absent from
non-subread records (scraps, ZMW read, CCS read, etc.)


  +-----------+---------------+----------------------------------------------------+
  | **Tag**   | **Type**      |**Description**                                     |
  +===========+===============+====================================================+
  | cx        | i             | Subread local context Flags                        |
  +-----------+---------------+----------------------------------------------------+

Missing adapter annotation in CCS reads
=======================================

The ``ma`` and ``ac`` tags indicate whether the molecule that produces a CCS
read is missing a SMRTbell adapter on its left/start or right/end. The tags are
produced by CCS version 6.3.0 and newer based on the ``ADAPTER_BEFORE_BAD`` and
``ADAPTER_AFTER_BAD`` information in the subread ``cx`` tag.

  +-----------+---------------+-------------------------------------------------------------------+
  | **Tag**   | **Type**      |**Description**                                                    |
  +===========+===============+===================================================================+
  | ac        | B,i           | Array containing four counts, in order:                           |
  |           |               | - detected adapters on left/start                                 |
  |           |               | - missing adapters on left/start                                  |
  |           |               | - detected adapters on right/end                                  |
  |           |               | - missing adapter on right/end                                    |
  +-----------+---------------+-------------------------------------------------------------------+
  | ma        | i             | Bitmask storing if an adapter is missing on either side of the    |
  |           |               | molecule. A value of 0 indicates neither end has a confirmed      |
  |           |               | missing adapter.                                                  |
  |           |               | - 0x1 if adapter is missing on left/start                         |
  |           |               | - 0x2 if adapter is missing on right/end                          |
  +-----------+---------------+-------------------------------------------------------------------+

Barcode analysis
================

In multiplexed workflows, we record per-subread tags representing the
barcode call and a score representing the confidence of that call.
The actual data used to inform the barcode calls---the barcode
sequences and associated pulse features---will be retained in the
associated ``scraps.bam`` file.

  +-----------+---------------+----------------------------------------------------+
  | **Tag**   | **Type**      |**Description**                                     |
  +===========+===============+====================================================+
  | bc        | B,S           | Barcode Calls (per-ZMW)                            |
  +-----------+---------------+----------------------------------------------------+
  | bq        | i             | Barcode Quality (per-ZMW)                          |
  +-----------+---------------+----------------------------------------------------+

- Both the ``bc`` and ``bq`` tags are calculated ``per-ZMW``, so every
  subread belonging to a given ZMW should share identical ``bc`` and
  ``bq`` values.  The tags are also inter-depedent, so if a subread
  has the ``bc`` tag, it must also have a ``bq`` tag and vise-versa.
  If the tags are present for any subread in a ZMW, they must be present
  for all of them.  In the absence of barcodes, both the ``bc`` and
  ``bq`` tags will be absent

- The ``bc`` tag contains the *barcode call*, a ``uint16[2]``
  representing the inferred forward and reverse barcodes sequences (as
  determined by their ordering in the Barcode FASTA), or more
  succinctly, it contains the integer pair :math:`B_F, B_R`.  Integer
  codes represent 0-based position in the FASTA file of barcodes.

- The integer (``int``) ``bq`` tag contains the barcode call confidence.
  If the ``BarcodeQuality`` element of the header is set to ``Score``,
  then the tag represents the mean normalized sum of the calculated
  Smith-Waterman scores that support the call in the ``bc`` tag across all
  subreads. For each barcode, the sum of the Smith-Waterman score is normalized
  by the length of the barcode times the match score, then multiplied by 100
  and rounded; this provides an integer value between 0 - 100.
  On the other hand, if the value of the header-tag is ``Probability`` instead,
  then the tag value is a the Phred-scaled posterior probability that the
  barcode call in ``bc`` is correct.
  In both cases, the value will never exceed the ``int8`` range, but for
  backward-compatibility reasons we keep the BAM ``bq`` as ``int``.
  This contract allows the PBI to store ``bq`` as a much smaller ``int8``.

The following (optional) tags describe clipped barcode sequences:

  +-----------+---------------+-------------------------------------------------------+
  | **Tag**   | **Type**      | **Description**                                       |
  +===========+===============+=======================================================+
  | bl        | Z             | Barcode sequence clipped from leading end             |
  +-----------+---------------+-------------------------------------------------------+
  | bt        | Z             | Barcode sequence clipped from trailing end            |
  +-----------+---------------+-------------------------------------------------------+
  | ql        | Z             | Qualities of barcode bases clipped from leading end,  |
  |           |               | stored as a FASTQ string                              |
  +-----------+---------------+-------------------------------------------------------+
  | qt        | Z             | Qualities of barcode bases clipped from trailing end, |
  |           |               | stored as a FASTQ string                              |
  +-----------+---------------+-------------------------------------------------------+
  | bx        | B,i           | Pair of clipped barcode sequence lengths              |
  +-----------+---------------+-------------------------------------------------------+


Barcode information will follow the same convention in CCS output
(``ccs.bam`` files).

Examples (subreads)
-------------------

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



Alignment: the contract for a mapper
====================================

An aligner is expected to accept BAM input and produce aligned BAM
output, where each aligned BAM record in the output preserves intact
all tags present in the original record.  The aligner should not
attempt to orient or complement any of the tags.

(Note that this contrasts with the handling of `SEQ` and `QUAL`, which
are mandated by the BAM/SAM specification to be (respectively)
reverse-complemented, and reversed, for reverse strand alignments.)


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


Segmented reads
===============

Some library preparation approaches produce SMRTbell molecules that are a 
concatenation of smaller DNA fragments separated by known sequences (segment 
adapters). Segmented reads are the result of splitting the read generated from 
those molecules back into the constituent fragments. 

The segment adapter sequences provide markers for splitting the source read 
and their expected sequential order allows the detection of malformed reads. 
These sequences are excised from segmented reads stored in the BAM file.

  +-----------+------------+--------------------------------------------------------------+
  | **Tag**   | **Type**   | **Description**                                              |
  +===========+============+==============================================================+
  | di        | i          | Index of this segment [0, N), denoting its position within   |
  |           |            | the source read                                              |
  +-----------+------------+--------------------------------------------------------------+
  | qs        | i          | 0-based start of segment in its source read                  |
  +-----------+------------+--------------------------------------------------------------+
  | qe        | i          | 0-based end of segment in its source read                    |
  +-----------+------------+--------------------------------------------------------------+
  | dl        | i          | 0-based segment adapter index matching the left flank        |
  |           |            | -1 if not applicable                                         |
  +-----------+------------+--------------------------------------------------------------+
  | dr        | i          | 0-based segment adapter index matching the right flank       |
  |           |            | -1 if not applicable                                         |
  +-----------+------------+--------------------------------------------------------------+
  | ds        | B,C        | Supplemental data enabling reconstitution of the source read |
  |           |            | Binary representation, for internal use only                 |
  +-----------+------------+--------------------------------------------------------------+


Unresolved issues
=================

- Need to move from strings to proper array types for QVs
- '/' preferable to ':' in "IPD:CodecV1"
- Desire for spec for shorter movienames, especially if these are
  ending up in QNAMEs.

.. _specifications for BAM/SAM: http://samtools.github.io/hts-specs/SAMv1.pdf
.. _SAM tags specifications: http://samtools.github.io/hts-specs/SAMtags.pdf
