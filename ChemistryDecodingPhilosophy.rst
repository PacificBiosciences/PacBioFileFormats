
Location of chemistry information
---------------------------------

Prior to 2.3, the chemistry information associated with a basecall
file was was stored in the metadata.xml file associated with the run.
This metadata.xml file is now only consulted for these legacy files.
For 2.3 basecall files, the canonical chemistry information associated
with a bax.h5 or ccs.h5 file is present in the files as the following
*attributes*:

+----------------------------+-----------------------------------------+----------------+------------------+
|Item                        | Attribute                               | Example        | Comment          |
+----------------------------+-----------------------------------------+----------------+------------------+
| BindingKit                 |``/ScanData/RunInfo/BindingKit``         |                |                  |
+----------------------------+-----------------------------------------+----------------+------------------+
| SequencingKit              |``/ScanData/RunInfo/SequencingKit``      |                |                  |
+----------------------------+-----------------------------------------+----------------+------------------+
| SoftwareVersion            |``/PulseData/BaseCalls/ChangeListID``    | "2.1.1.1.12345"|truncate to first |
|                            |                                         |                |three components, |
|                            |                                         |                |e.g. "2.1.1"      |
+----------------------------+-----------------------------------------+----------------+------------------+
| SequencingChemistry        |``/ScanData/RunInfo/SequencingChemistry``| "P4-C2"        |Normallly absent. |
|                            |                                         |                |Only to be used   |
|                            |                                         |                |when other items  |
|                            |                                         |                |are absent.       |
+----------------------------+-----------------------------------------+----------------+------------------+

The SequencingChemistry attribute will normally be absent; if it is
present *and the other information is absent*, it will be used; this
allows a simple mechanism for "fixing" bax files with broken or
incorrect chemistry information.

Note that in the case of the ccs.h5 file, the presence of the
SoftwareVersion data under the ``/PulseData/BaseCalls`` group required
the reintroduction of that group to ccs.h5 files, so the presence of
that group should not be used to determine whether raw basecalls are
present.  The safe way to check for raw basecalls is to look for the
dataset ``/PulseData/BaseCalls/Basecalls``.

In a cmp.h5 (alignment) file, the canonical chemistry information
associated with *each movie* is present in the *movie info table*, in
the following datasets:


+----------------------------+----------------------------------+-----------------------------+
| Item                       | Dataset                          | Comment                     |
+----------------------------+----------------------------------+-----------------------------+
| BindingKit                 |``/MovieInfo/BindingKit``         |                             |
+----------------------------+----------------------------------+-----------------------------+
| SequencingKit              |``/MovieInfo/SequencingKit``      |                             |
+----------------------------+----------------------------------+-----------------------------+
| SoftwareVersion            |``/MovieInfo/SoftwareVersion``    |                             |
+----------------------------+----------------------------------+-----------------------------+
| SequencingChemistry        |``/MovieInfo/SequencingChemistry``| Normally absent in 2.3      |
|                            |                                  | cmp.h5 files; present in    |
|                            |                                  | earlier versions.  Ignored  |
|                            |                                  | when other datasets present.|
+----------------------------+----------------------------------+-----------------------------+




Practical guidelines for file parsers
-------------------------------------

Parsers for cmp.h5, bas.h5, and ccs.h5 files should

1. be able to open the files even if they lack chemistry information
2. throw an exception on an attempt to access the chemistry
   information if it is absent.
3. only use the "SequencingChemistry" datum if the normal "triple" of
   chemistry information is absent.





The chemistry information problem
---------------------------------

Some pieces of PacBio secondary software (Quiver, base modification
analysis) require information about the sequencing chemistry
configuration in order to function optimally.  When the sample is
input to the instrument, the technician scans the barcodes for the
*binding kit* and the *sequencing kit*; these partnumbers are recorded
and used as the basis for identifying the "sequencing chemistry"
condition.  For example, we can decode these partnumbers to identify
the sequencing chemistry condition as "P4-C2".

The basecaller version is also a determinant of the statistical
structure of the basecall data, so it is considered a part of the
chemistry information.  Together these three pieces of data---the
*binding kit partnumber*, the *sequencing kit partnumber*, and the
*basecaller version* define the characteristics up the input data to
secondary applications.  We will refer to these elements as the
"triple".

This document concerns the way that the "triple" is propagated from
the instrument all the way to secondary applications, and how it is
used.


Decoding
--------

The triple is an inconvenient representation for secondary analysis.
In particular, many different triples may represent the same chemistry
configuration (for example, typically multiple partnumbers correspond
to a given binding kit flavor, like "P4").  Thus before secondary
applications view the chemistry information, it should be put in a
normalized form.  For example, the triple should be *decoded* into a
string that is a more meaningful encapsulation of the upstream data
characteristic, e.g. "P4-C2" or "P4-C2.BCRetrain5".


The ideal world paradigm
------------------------

In an ideal world, the "triple" would be decoded as soon as possible,
by primary software, so that secondary software would never be
burdened with deciphering partnumbers.  *However, since we typically
have not required customers to upgrade their primary software in order
to use a new chemistry, we cannot guarantee correct decoding in
primary*.  Thus decoding has to happen in some stage of secondary
analysis.

*Note that if we could make a primary software update a hard
requirement for using a new chemistry---for example by rejecting
unrecognized barcodes and telling the user to upgrade---it could
eliminate a lot of software complexity described in the following.*



The old paradigm
----------------

In the old (pre-2.3) paradigm, chemistry decoding was performed by a
smrtpipe module run for each secondary job.  Decoded chemistry
information was placed in a "chemistry_mapping.xml" file in the job
data directory.  Secondary applications were then pointed at this file
as descriptor of the chemistry condition per movie.  (The decoded
chemistry information was also copied into any alignment files
(cmp.h5) that were produced by the job, because Dave was of the
philosophy that the data files used as input to secondary should be
self-contained, that no external files should be needed for correct
functioning of quiver, for example.)

There were some advantages to this approach:

- Modularity: decoding was done in one place

There were substantial disadvantages, however:

- This approach did nothing to help users outside of the
  smrtpipe/smrtportal environment, for example command-line users
  constructing a simple pipeline using pbalign.

- If the secondary version was out of date, there was no easy recourse
  for users---they would essentially have to update their entire
  smrtanalysis.  Pat and Dave did design an update mechanism that
  required the user simply to "drop in" a new directory of
  configuration files in the smrtanalysis *etc* directory, but this
  approach now seems at odds with the modularity direction that
  secondary software has taken.



The new paradigm
----------------

In the new paradigm, the chemistry "triple" is piped all the way from
primary to the very end of secondary.  The triple is only decoded
on-demand, by the applications that actually need chemistry
information---Quiver and other consensus tools, and basemods, at
present.

Thus all primary and secondary software acts as a "dumb pipe" and
never need upgrading in order to function properly with a new
chemistry.  The only software that needs to be upgraded is the
software that actually requires the chemistry information---for
example, Quiver and its library components (pbcore, ConsensusCore).

A file (bax.h5 [*]_, cmp.h5) without the chemistry triple is considered
"broken" and is flagged as such at the earliest state possible, by the
"dumb pipe" software.

The guiding star in the design of the new paradigm has been the
"end-to-end principle" of network design--that logic should exist only
at the endpoints of a network.


Details
-------

The current version of instrument software in the field (May 2014) is
2.1.  2.1 primary software places the "triple" in the run's
"metadata.xml" file, not in the bax.h5 files.  This has been
problematic in that customers have an expectation that they can safely
move bax.h5 files, that they are *self contained*.  This incorrect
expectation has led to the most common cause of reported Quiver
problems (and doubtless has caused many unreported instances of poor
Quiver performance, when Quiver could not identify the chemistry and
had to resort to a suboptimal generic model).

In the forthcoming 2.3 primary software release, the chemistry information is
copied into the bax.h5 files (of course, it still is present in the
metadata.xml as well).  This makes the bax.h5 files self-contained.

Also, the 2.3 secondary software release will reject data that is
missing chemistry information at the earliest stage possible, giving
an informative message about what is missing.



.. [*] for backwards compatibility, bax.h5 files are not considered
       broken if a corresponding metadata.xml file, containing the
       chemistry information, exists in the expected location (parent
       directory) relative to the bax.h5 file.  This complexity is
       hidden by the chemistry-information-fetching API.  The
       important requirement is that the chemistry information is
       *available*.
