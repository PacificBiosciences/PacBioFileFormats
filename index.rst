.. FileFormats documentation master file, created by
   sphinx-quickstart on Tue Apr 30 08:43:59 2013.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.


PacBio bioinformatics file formats
==================================

As of the 3.0 release of SMRTanalysis, PacBio is embracing the
industry standard BAM format for (both aligned and unaligned) basecall
data files.  We have also formulated a BAM companion file format
(`bam.pbi`) enabling fast access to a richer set of per-read
information as well as compatibility for software built around the
legacy `cmp.h5` format.


.. toctree::
   :maxdepth: 1

   Primer
   BAM
   PacBioBamIndex
   FASTA
   DataSet


Legacy formats
==============


.. toctree::
   :maxdepth: 1

   legacy/BasH5Spec
   legacy/CmpH5Spec



APIs available
==============

We occasionally make changes to these file format specifications so we
recommend using PacBio-authored APIs to access these file types.

- C++: pbbam_
- Python: pbcore_

.. _pbbam: https://github.com/PacificBiosciences/pbbam
.. _pbcore: https://github.com/PacificBiosciences/pbcore
