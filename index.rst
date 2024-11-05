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


Internal file formats
=====================

.. toctree::
   :maxdepth: 1

   SubreadsBAM
   SubreadsInternalBAM


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
