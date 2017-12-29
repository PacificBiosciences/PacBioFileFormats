=======================================
Run Design CSV specification for PacBio
=======================================

The Run Design CSV is a comma-separated file which can be imported into SMRT Link to create a run design. Each line in the CSV represents a sample.

+-----------------------------------+-----------------------------------------------------------------+-------------------------------------------------------------------+
| Key                               | Value Example                                                   | Value Spec                                                        |
+===================================+=================================================================+===================================================================+
| Experiment Name                   | NoRS_Standard_Edna.1                                            | Can be any ASCII string.                                          |
+-----------------------------------+-----------------------------------------------------------------+-------------------------------------------------------------------+
| Experiment Id                     | 325/3250057                                                     | Must be a valid experiment ID. Details below.                     |
+-----------------------------------+-----------------------------------------------------------------+-------------------------------------------------------------------+
| Experiment Description            | 20170530_A6_Iguana_VVnC_SampleSheet_TEMPLATE                    | Can be any ASCII string.                                          |
+-----------------------------------+-----------------------------------------------------------------+-------------------------------------------------------------------+
| Run Name                          | 20170530_A6_Iguana_VVnC_SampleSheet_TEMPLATE                    | Can be any ASCII string.                                          |
+-----------------------------------+-----------------------------------------------------------------+-------------------------------------------------------------------+
| Run Description                   | ecoliK12_pbi_March2013                                          | Can be any ASCII string.                                          |
+-----------------------------------+-----------------------------------------------------------------+-------------------------------------------------------------------+
| Well No.                          | A01                                                             | Must be a valid well number. Details below.                       |
+-----------------------------------+-----------------------------------------------------------------+-------------------------------------------------------------------+
| Sample Name                       | SMS_Iguana_A6_3230046_A01_TestCase_SB_BindKit_ChemKitv2_8rxnKit | Can be any ASCII string.                                          |
+-----------------------------------+-----------------------------------------------------------------+-------------------------------------------------------------------+
| Cell No.                          | 1                                                               | Must be an integer from 1 to 8. Details below.                    |
+-----------------------------------+-----------------------------------------------------------------+-------------------------------------------------------------------+
| Collection Time                   | 120                                                             | Must be a float >= 1 and < 1200. Time is in minutes.              |
+-----------------------------------+-----------------------------------------------------------------+-------------------------------------------------------------------+
| Sample Description                | SMS_Iguana_A6_3230046_A01_TestCase_SB_BindKit_ChemKit           | Can be any ASCII string.                                          |
+-----------------------------------+-----------------------------------------------------------------+-------------------------------------------------------------------+
| Insert Size                       | 2000                                                            | Must be an integer > 9.                                           |
+-----------------------------------+-----------------------------------------------------------------+-------------------------------------------------------------------+
| Size Selection                    | FALSE                                                           | Must be a Boolean value. Details on booleans below.               |
+-----------------------------------+-----------------------------------------------------------------+-------------------------------------------------------------------+
| Stage Start                       | FALSE                                                           | Must be a Boolean value. Details on booleans below.               |
+-----------------------------------+-----------------------------------------------------------------+-------------------------------------------------------------------+
| DNA Template Prep Kit Box Barcode | DM1117100259100111716                                           | Must be valid kit barcode. Details below.                         |
+-----------------------------------+-----------------------------------------------------------------+-------------------------------------------------------------------+
| DNA Control Complex Box Barcode   | DM1234101084300123120                                           | Must be valid kit barcode. Details below.                         |
+-----------------------------------+-----------------------------------------------------------------+-------------------------------------------------------------------+
| Binding Kit Box Barcode           | DM1117100862200111716                                           | Must be valid kit barcode. Details below.                         |
+-----------------------------------+-----------------------------------------------------------------+-------------------------------------------------------------------+
| Sequencing Kit Box Barcode        | DM0001100861800123120                                           | Must be valid kit barcode. Details below.                         |
+-----------------------------------+-----------------------------------------------------------------+-------------------------------------------------------------------+
| Wash Kit Box Barcode              | DM2222100866100123120                                           | Must be valid kit barcode. Details below.                         |
+-----------------------------------+-----------------------------------------------------------------+-------------------------------------------------------------------+
| Automation Name                   | Diffusion                                                       | Can be "diffusion", "magbead", or a custom script. Details below. |
+-----------------------------------+-----------------------------------------------------------------+-------------------------------------------------------------------+
| Automation Parameters             | ExtensionTime=double:60|ExtendFirst=boolean:True                | Must follow format demonstrated in Value Example. Details below.  |
+-----------------------------------+-----------------------------------------------------------------+-------------------------------------------------------------------+
| Primary Analysis                  | Default                                                         | Can be any ASCII string.                                          |
+-----------------------------------+-----------------------------------------------------------------+-------------------------------------------------------------------+
| Primary Analysis Parameters       | CopyFileTrace=boolean:true                                      | Must follow format demonstrated in Value Example. Details below.  |
+-----------------------------------+-----------------------------------------------------------------+-------------------------------------------------------------------+

General Requirements
--------------------
The csv may only contain ASCII characters.
Specifically, it must satisfy the regular expression:

  - ``/^[\x00-\x7F]*$/g``

Required Fields
---------------
  - Run Name
  - Well No.
  - Sample Name
  - Collection Time
  - Insert Size
  - DNA Template Prep Kit Box Barcode
  - DNA Control Complex Box Barcode
  - Binding Kit Box Barcode
  - Sequencing Kit Box Barcode
  - Automation Name

Experiment ID
-------------
Experiment IDs cannot contain the following characters: ``<, >, :, ", \, |, ?, *, or )``.
Experiment IDs cannot start or end with a "/" and cannot have two adjacent "/", i.e. "//".
Experiment IDs also cannot contain spaces.
Specifically, Experiment IDs cannot satisfy the regular expressions:

  - ``/[<>:"\\|?\*]/g``
  - ``/(?:^\/)|\/\/|(?:\/$)/``
  - ``/ /g``

Cell No.
--------
The cell numbers must satisfy a valid cell re-use scheme.

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
