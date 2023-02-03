PacBio bioinformatics file formats
==================================

PacBio uses the industry standard BAM format for (both aligned and unaligned)
read data files. We have also formulated a BAM companion file format (`bam.pbi`)
enabling fast access to a richer set of per-read information.


.. toctree::
   :maxdepth: 1

   Primer
   BAM
   PacBioBamIndex
   FileStructure
   FASTA
   DataSet
   RunDesignCsv


Internal file formats
=====================

.. toctree::
   :maxdepth: 1

   SubreadsBAM
   SubreadsInternalBAM


APIs available
==============

We occasionally make changes to these file format specifications so we
recommend using PacBio-authored APIs to access these file types.

- C++: pbbam_
- Python: pbcore_


Data Model XSD
================

For completeness, here is the PacBio data model XSD.

.. toctree::
   :maxdepth: 1

   xsd/PacBioDataModel
   xsd/PacBioAutomationConstraints
   xsd/PacBioBaseDataModel
   xsd/PacBioCollectionMetadata
   xsd/PacBioDatasets
   xsd/PacBioDeclData
   xsd/PacBioPartNumbers
   xsd/PacBioPrimaryMetrics
   xsd/PacBioReagentKit
   xsd/PacBioRightsAndRoles
   xsd/PacBioSampleInfo
   xsd/PacBioSeedingData

.. _pbbam: https://github.com/PacificBiosciences/pbbam
.. _pbcore: https://github.com/PacificBiosciences/pbcore
