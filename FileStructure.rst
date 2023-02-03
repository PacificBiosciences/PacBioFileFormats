Revio file structure
====================

The Revio platform has a different output file structure than Sequel II and
Sequel IIe.

Directory structure
-------------------

   Transfer_Scheme_Path/
   └─ rNNNNN_YYYYMMDD_HHMMSS/
      └─ P_WNN/
         ├─ fail_reads/
         ├─ hifi_reads/
         ├─ metadata/
         ├─ pb_formats/
         └─ statistics/

Movie Context ID is defined as

   mNNNNN_YYMMDD_HHMMSS_sN

in particular::

   mNNNNN - instrument identifier
   YYMMDD - date stamp
   HHMMSS - time stamp
   sN     - stage number (Revio has four)

File structure
--------------

In the following example, one barcode ('bc2001') has been used. If
you see the 'default' file infix, this is the standard, unbarcoded TC6 SMRTbell
adapter.

   Transfer_Scheme_Path/
   └─ r84001_20220722_134701
      └─ 1_A01
         ├─ fail_reads
         │  ├─ m84001_220722_134701_s1.fail_reads.bc2001.bam
         │  ├─ m84001_220722_134701_s1.fail_reads.bc2001.bam.pbi
         │  ├─ m84001_220722_134701_s1.fail_reads.unassigned.bam
         │  └─ m84001_220722_134701_s1.fail_reads.unassigned.bam.pbi
         ├─ hifi_reads
         │  ├─ m84001_220722_134701_s1.hifi_reads.bc2001.bam
         │  ├─ m84001_220722_134701_s1.hifi_reads.bc2001.bam.pbi
         │  ├─ m84001_220722_134701_s1.hifi_reads.unassigned.bam
         │  └─ m84001_220722_134701_s1.hifi_reads.unassigned.bam.pbi
         ├─ metadata
         │  ├─ m84001_220722_134701_s1.barcodes.fasta
         │  ├─ m84001_220722_134701_s1.basecaller.log
         │  ├─ m84001_220722_134701_s1.ccs.log
         │  ├─ m84001_220722_134701_s1.darkcal.log
         │  ├─ m84001_220722_134701_s1.fail_reads.alarms.json
         │  ├─ m84001_220722_134701_s1.fail_reads.lima.log
         │  ├─ m84001_220722_134701_s1.fail_reads.primrose.log
         │  ├─ m84001_220722_134701_s1.hifi_reads.alarms.json
         │  ├─ m84001_220722_134701_s1.hifi_reads.lima.log
         │  ├─ m84001_220722_134701_s1.hifi_reads.primrose.log
         │  ├─ m84001_220722_134701_s1.metadata.xml
         │  ├─ m84001_220722_134701_s1.ppa.log
         │  ├─ m84001_220722_134701_s1.run.metadata.xml
         │  ├─ m84001_220722_134701_s1.sts.xml
         │  └─ m84001_220722_134701_s1.transferdone
         ├─ pb_formats
         │  ├─ m84001_220722_134701_s1.consensusreadset.xml
         │  ├─ m84001_220722_134701_s1.fail_reads.bc2001.consensusreadset.xml
         │  ├─ m84001_220722_134701_s1.fail_reads.consensusreadset.xml
         │  ├─ m84001_220722_134701_s1.fail_reads.unassigned.consensusreadset.xml
         │  ├─ m84001_220722_134701_s1.hifi_reads.bc2001.consensusreadset.xml
         │  ├─ m84001_220722_134701_s1.hifi_reads.consensusreadset.xml
         │  └─ m84001_220722_134701_s1.hifi_reads.unassigned.consensusreadset.xml
         └─ statistics
            ├─ m84001_220722_134701_s1.ccs_reports.json
            ├─ m84001_220722_134701_s1.fail_reads.5mc_report.json
            ├─ m84001_220722_134701_s1.fail_reads.lima_counts.txt
            ├─ m84001_220722_134701_s1.fail_reads.lima_guess.json
            ├─ m84001_220722_134701_s1.fail_reads.lima_report.txt
            ├─ m84001_220722_134701_s1.fail_reads.lima_summary.txt
            ├─ m84001_220722_134701_s1.hifi_reads.5mc_report.json
            ├─ m84001_220722_134701_s1.hifi_reads.lima_counts.txt
            ├─ m84001_220722_134701_s1.hifi_reads.lima_guess.json
            ├─ m84001_220722_134701_s1.hifi_reads.lima_report.txt
            ├─ m84001_220722_134701_s1.hifi_reads.lima_summary.txt
            └─ m84001_220722_134701_s1.zmw_metrics.json.gz
