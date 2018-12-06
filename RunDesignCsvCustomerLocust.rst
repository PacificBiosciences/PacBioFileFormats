=======================================
Run Design CSV specification for PacBio
=======================================

The Run Design CSV is a comma-separated file which can be imported into SMRT Link to create a run design. Each line in the CSV represents a sample.

+----------------------------------------+----------------------------------------------------------------------------+-------------------------------------------------------------------+
| Key                                    | Value Example                                                              | Value Spec                                                        |
+========================================+============================================================================+===================================================================+
| Experiment Name                        | NoRS_Standard_Edna.1                                                       | Can be any ASCII string. Defaults to Run Name.                    |
+----------------------------------------+----------------------------------------------------------------------------+-------------------------------------------------------------------+
| Experiment Id                          | 325/3250057                                                                | Must be a valid experiment ID. Details below.                     |
+----------------------------------------+----------------------------------------------------------------------------+-------------------------------------------------------------------+
| Experiment Description                 | 20170530_A6_Iguana_VVnC_SampleSheet_TEMPLATE                               | Can be any ASCII string. Defaults to Run Description.             |
+----------------------------------------+----------------------------------------------------------------------------+-------------------------------------------------------------------+
| Run Name                               | 20170530_A6_Iguana_VVnC_SampleSheet_TEMPLATE                               | Can be any ASCII string.                                          |
+----------------------------------------+----------------------------------------------------------------------------+-------------------------------------------------------------------+
| System Name                            | Sequel                                                                     | Must be either Sequel or Sequel II                                |
+----------------------------------------+----------------------------------------------------------------------------+-------------------------------------------------------------------+
| Run Description                        | ecoliK12_pbi_March2013                                                     | Can be any ASCII string.                                          |
+----------------------------------------+----------------------------------------------------------------------------+-------------------------------------------------------------------+
| Is Collection                          | TRUE                                                                       | Must be a Boolean value. Boolean details below.                   |
+----------------------------------------+----------------------------------------------------------------------------+-------------------------------------------------------------------+
| Well No.                               | A01                                                                        | Must be a valid well number. Details below.                       |
+----------------------------------------+----------------------------------------------------------------------------+-------------------------------------------------------------------+
| Sample Name                            | SMS_Iguana_A6_3230046_A01_TestCase_SB_BindKit_ChemKitv2_8rxnKit            | Can be any ASCII string.                                          |
+----------------------------------------+----------------------------------------------------------------------------+-------------------------------------------------------------------+
| Collection Time                        | 120                                                                        | Must be a float >= 1 and <= 1200. Time is in minutes.             |
+----------------------------------------+----------------------------------------------------------------------------+-------------------------------------------------------------------+
| Sample Description                     | SMS_Iguana_A6_3230046_A01_TestCase_SB_BindKit_ChemKit                      | Can be any ASCII string.                                          |
+----------------------------------------+----------------------------------------------------------------------------+-------------------------------------------------------------------+
| Insert Size                            | 2000                                                                       | Must be an integer >= 10. Units are in bp.                        |
+----------------------------------------+----------------------------------------------------------------------------+-------------------------------------------------------------------+
| On Plate Loading Concentration         | 5                                                                          | Must be a float. Units are in pM.                                 |
+----------------------------------------+----------------------------------------------------------------------------+-------------------------------------------------------------------+
| Size Selection                         | FALSE                                                                      | Must be a Boolean value. Boolean details below. Default is False. |
+----------------------------------------+----------------------------------------------------------------------------+-------------------------------------------------------------------+
| DNA Template Prep Kit Box Barcode      | DM1117100259100111716                                                      | Must be valid kit barcode. Details below.                         |
+----------------------------------------+----------------------------------------------------------------------------+-------------------------------------------------------------------+
| DNA Control Complex Box Barcode        | DM1234101084300123120                                                      | Must be valid kit barcode. Details below.                         |
+----------------------------------------+----------------------------------------------------------------------------+-------------------------------------------------------------------+
| Binding Kit Box Barcode                | DM1117100862200111716                                                      | Must be valid kit barcode. Details below.                         |
+----------------------------------------+----------------------------------------------------------------------------+-------------------------------------------------------------------+
| Sequencing Kit Box Barcode             | DM0001100861800123120                                                      | Must be valid kit barcode. Details below.                         |
+----------------------------------------+----------------------------------------------------------------------------+-------------------------------------------------------------------+
| Automation Name                        | Diffusion                                                                  | Can be "diffusion", "magbead", or a custom script. Details below. |
+----------------------------------------+----------------------------------------------------------------------------+-------------------------------------------------------------------+
| Automation Parameters                  | ExtensionTime=double:60|ExtendFirst=boolean:True                           | Must follow format demonstrated in Value Example. Details below.  |
+----------------------------------------+----------------------------------------------------------------------------+-------------------------------------------------------------------+
| Enable CCS Analysis                    | TRUE                                                                       | Must be a Boolean value. Boolean details below.                   |
+----------------------------------------+----------------------------------------------------------------------------+-------------------------------------------------------------------+
| Sample is Barcoded                     | TRUE                                                                       | Must be a Boolean value. Details on booleans below.               |
+----------------------------------------+----------------------------------------------------------------------------+-------------------------------------------------------------------+
| Barcode Set                            | dad4949d-f637-0979-b5d1-9777eff62008                                       | Must be a uuid for a barcodeset present in the database.          |
+----------------------------------------+----------------------------------------------------------------------------+-------------------------------------------------------------------+
| Same Barcodes on Both Ends of Sequence | TRUE                                                                       | Must be a Boolean value. Details on booleans below.               |
+----------------------------------------+----------------------------------------------------------------------------+-------------------------------------------------------------------+
| Barcode Name                           | lbc1--lbc1                                                                 | Must be a valid barcode pair.                                     |
+----------------------------------------+----------------------------------------------------------------------------+-------------------------------------------------------------------+
| Bio Sample Name                        | sample1                                                                    | Can be any ASCII string.                                          |
+----------------------------------------+----------------------------------------------------------------------------+-------------------------------------------------------------------+
| Pipeline Id                            | pbsmrtpipe.pipelines.sa3_ds_isoseq3_with_genome                            | Must be a valid pbsmrtpipe pileine Id                             |
+----------------------------------------+----------------------------------------------------------------------------+-------------------------------------------------------------------+
| Analysis Name                          | sample1 analysis                                                           | Can be any ASCII string.                                          |
+----------------------------------------+----------------------------------------------------------------------------+-------------------------------------------------------------------+
| Entry Points                           | PacBio.DataSet.BarcodeSet;eid_barcode;afe89e3f-17ca-e9b8-eae9-b701dbb1f02d | A "|" separated list with entries: file_type;entry_id;uuid        |
+----------------------------------------+----------------------------------------------------------------------------+-------------------------------------------------------------------+
| Task Options                           | isocollapse.task_options.allow_extra_5exon;boolean;false                   | A "|" separated list with entries: task_id;value_type;value       |
+----------------------------------------+----------------------------------------------------------------------------+-------------------------------------------------------------------+


General Requirements
--------------------
The csv may only contain ASCII characters.
Specifically, it must satisfy the regular expression:

  - ``/^[\x00-\x7F]*$/g``

Required Fields
---------------
  - Run Name
  - System Name
  - Well No.
  - Sample Name
  - Collection Time
  - Insert Size
  - DNA Template Prep Kit Box Barcode
  - Binding Kit Box Barcode
  - Sequencing Kit Box Barcode

Is Collection
-------------
This field indicates whether the line is specifying a collection (TRUE), or a barcoded sample (FALSE).
Collection lines should leave Barcode Names and Bio Sample Names blank.
Barcoded sample lines only need to contain the Is Collection, Sample Name, the Barcode Name, and Bio Sample Name fields.

Experiment ID
-------------
Experiment IDs cannot contain the following characters: ``<, >, :, ", \, |, ?, *, or )``.
Experiment IDs cannot start or end with a "/" and cannot have two adjacent "/", i.e. "//".
Experiment IDs also cannot contain spaces.
Specifically, Experiment IDs cannot satisfy the regular expressions:

  - ``/[<>:"\\|?\*]/g``
  - ``/(?:^\/)|\/\/|(?:\/$)/``
  - ``/ /g``

Well No.
--------
The well number must start with a letter "A" through "H", and end in a number "01" through "12",
i.e. "A01" through "H12". In other words, it must satisfy the regular expression:

  - ``/^[A-H](?:0[1-9]|1[0-2])$/``

Automation Name
---------------
The automation name can be either "diffusion" or "magbead" and is not case-sensitive.
A path can also be used, such as "/path/to/my/script/my_script.py".
The path will not be processed further, so if the full URI is required,
it must be provided in the CSV, e.g. "chemistry://path/to/my/script/my_script.py".

Boolean Values
--------------
Acceptable boolean values for true are:

  - "true"
  - "t"
  - "yes"
  - "y"
Acceptable boolean values for false are:

  - "false"
  - "f"
  - "no"
  - "n"

Boolean values are not case-sensitive.

Kit Barcodes
------------
The kit barcodes are composed of three parts:

  - Lot Number (ex: "DM1234")
  - Part Number (ex: "100-619-300")
  - Expiration Date (ex: "2020-12-31")

which is used to make a single string. Using the above example, the barcode would be:

  - DM1234100619300123120

Each kit must have a valid Part Number and cannot be obsolete. The list of kits can be
found through a services endpoint such as:

  - [server name]:[services port number]/smrt-link/bundles/chemistry-pb/active/files/definitions%2FPacBioAutomationConstraints.xml

This services endpoint will list, for each kit, the part numbers ("PartNumber")
and whether it is obsolete ("IsObsolete").
Dates must also be valid, meaning they must exist on the Gregorian calendar.

Parameters
----------
The parameters are a "|" separated list.
Each item follows the format: [parameter name]=[parameter type]:[parameter value].
Primary analysis parameters are:

  - Readout
  - MetricsVerbosity
  - CopyFileTrace
  - CopyFileBaz
  - CopyFileDarkFrame
  - CopyStatsH5

Acceptable parameter types are:

  - String
  - Int32
  - UInt32
  - Double
  - Single
  - Boolean
  - DateTime

The parameter names and types are not case-sensitive.

Barcoded Sample Names
---------------------
The barcoded sample names are a "|" separated list.
Each item in the list follows the format: [barcode name];[biosample name]
The barcode names must be contained within the specified barcodeset.
A given barcode name cannont appear more than once in the list.
The biosample names can be any ASCII string but cannot contain the field separators "|" and ";".
The biosample names cannot be longer than 40 characters.
A maximum of 384 barcodes is permitted per sample.

Auto Analysis fields
--------------------
These fields include: Pipeline Id, Analysis Name, Entry Points, Task Options.
You may define one analysis for each collection and bio sample.
Pipeline Id, Analysis Name and Entry Points fields are required.
The Task Options fields may be left empty, any task options not specified will use pipeline defaults.
