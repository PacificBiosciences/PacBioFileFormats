FASTA file format
=================

Best practices
--------------

The ubiquitous FASTA_ format is flexible, to a fault. The following
best practices will guarantee success in using FASTA files with PacBio
software (for example as genome references).

    1.  Sequences in FASTA files should be wrapped at a uniform line
        length, to enable indexing. (A common convention is to wrap
        lines at 60 characters.)  Windows and UNIX line endings are
        both acceptable.

    2.  FASTA files should contain no empty lines (or lines containing
        only whitespace [#whitespace]_). FASTA files should contain
        no unnecessary whitespace (for example, no trailing whitespace
        on sequence lines).

    3.  Sequence contigs in a FASTA file are preceded by identifying
        header lines. The *header*, which is the text between the '>'
        character and the newline, is comprised of:

            - an *identifier*, which is the first whitespace-delimited
              token of the header

            - an (optional) *comment*, which consists of the suffix
              of the header following the first whitespace. Some APIs
              may call this string the *description* or the
              *metadata*, but the usage of the comment is completely
              application-defined.

        Sequence contigs will be identified in the PacBio system and
        in downstream analysis files using the *identifier*, so the
        *identifiers* contained in a FASTA file must be unique.

    4. Sequences should only contain characters from the following
       string (IUPAC_ nucleotide characters, minus '-' and '.')::

         "gatcuryswkmbdhvnGATCURYSWKMBDHVN"

    5. Headers should not contain any instances of the '>' character,
       and *identifiers* should not begin with an asterisk ('*') or
       contain any of the following characters::

         ',' ':'  '"' (double quote)

    6. PacBio software that imports reference genomes is allowed to
       outright reject FASTA files that do not meet our requirements;
       it will never attempt to rewrite/translate a file to fit the
       requirements.


Examples
--------

The following FASTA file would be accepted by the PacBio reference
uploader. Downstream files (reports, variant call files) would report
the chromosomes as 'chr1', 'chr2'::

  >chr1 Jackalope chromosome 1;length=7
  GATTACA
  >chr2 Jackalope chromosome 2;length=7
  TTACAGA

The following file would be *rejected* by the PacBio reference
uploader, for violating the identifier uniqueness requirement (in 3,
above)::

  >Jackalope chromosome 1;length=7
  GATTACA
  >Jackalope chromosome 2;length=7
  TTACAGA



Implications for bioinformatics tool writers
--------------------------------------------

Since a FASTA presented to a bioinformatics tool may contain
characters beyond "GATCN", tools should use a FASTA reader API capable
of normalizing sequence characters. For example, SeqAn_ uses a
`Dna5String` abstraction to project input sequence characters into
"GATCN"; FASTA readers in pbcore will soon offer normalization.


.. _FASTA: http://en.wikipedia.org/wiki/FASTA_format
.. _IUPAC: http://en.wikipedia.org/wiki/Nucleic_acid_notation
.. _SeqAn: http://www.seqan.de/
.. [#whitespace] We define a whitespace character as one for which the
                 standard C `isspace` function returns `true` (nonzero).
