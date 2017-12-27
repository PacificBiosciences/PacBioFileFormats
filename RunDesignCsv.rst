=======================================
Run Design CSV specification for PacBio
=======================================

The Run Design CSV is a comma-separated file which can be imported into SMRT Link to create a run design. Each line in the CSV represents a sample.


+-----------------------------------+-----------------------------------------------------------------+----------------------------------------------------------+
| Key                               | Value Example                                                   | Value Spec                                               |
+===================================+=================================================================+==========================================================+
| Experiment Name                   | NoRS_Standard_Edna.1                                            | Can be any string                                        |
+-----------------------------------+-----------------------------------------------------------------+----------------------------------------------------------+
| Experiment Id                     | 325/3250057                                                     | Must be a valid experiment ID. Details below.            |
+-----------------------------------+-----------------------------------------------------------------+----------------------------------------------------------+
| Experiment Description            | 20170530_A6_Iguana_VVnC_SampleSheet_TEMPLATE                    | Can be any string                                        |
+-----------------------------------+-----------------------------------------------------------------+----------------------------------------------------------+
| Run Name                          | 20170530_A6_Iguana_VVnC_SampleSheet_TEMPLATE                    | Can be any string                                        |
+-----------------------------------+-----------------------------------------------------------------+----------------------------------------------------------+
| Run Description                   | ecoliK12_pbi_March2013                                          | Can be any string                                        |
+-----------------------------------+-----------------------------------------------------------------+----------------------------------------------------------+
| Well No.                          | A01                                                             | Must be a valid well number. Details below.              |
+-----------------------------------+-----------------------------------------------------------------+----------------------------------------------------------+
| Sample Name                       | SMS_Iguana_A6_3230046_A01_TestCase_SB_BindKit_ChemKitv2_8rxnKit | Can be any string                                        |
+-----------------------------------+-----------------------------------------------------------------+----------------------------------------------------------+
| Cell No.                          | 1                                                               | Must be a valid cell number                              |
+-----------------------------------+-----------------------------------------------------------------+----------------------------------------------------------+
| Collection Time                   | 120                                                             | Can be any string                                        |
+-----------------------------------+-----------------------------------------------------------------+----------------------------------------------------------+
| Sample Description                | SMS_Iguana_A6_3230046_A01_TestCase_SB_BindKit_ChemKit           | Can be any string                                        |
+-----------------------------------+-----------------------------------------------------------------+----------------------------------------------------------+
| Insert Size                       | 2000                                                            | Can be any string                                        |
+-----------------------------------+-----------------------------------------------------------------+----------------------------------------------------------+
| Size Selection                    | FALSE                                                           | Must be a Boolean value. Details on booleans below.      |
+-----------------------------------+-----------------------------------------------------------------+----------------------------------------------------------+
| Stage Start                       | FALSE                                                           | Must be a Boolean value. Details on booleans below.      |
+-----------------------------------+-----------------------------------------------------------------+----------------------------------------------------------+
| DNA Template Prep Kit Box Barcode | DM1117100259100111716                                           | Must be valid ID                                         |
+-----------------------------------+-----------------------------------------------------------------+----------------------------------------------------------+
| DNA Control Complex Box Barcode   | DM1234101084300123120                                           | Must be valid ID                                         |
+-----------------------------------+-----------------------------------------------------------------+----------------------------------------------------------+
| Binding Kit Box Barcode           | DM1117100862200111716                                           | Must be valid ID                                         |
+-----------------------------------+-----------------------------------------------------------------+----------------------------------------------------------+
| Sequencing Kit Box Barcode        | DM0001100861800123120                                           | Must be valid ID                                         |
+-----------------------------------+-----------------------------------------------------------------+----------------------------------------------------------+
| Wash Kit Box Barcode              | DM2222100866100123120                                           | Must be valid ID                                         |
+-----------------------------------+-----------------------------------------------------------------+----------------------------------------------------------+
| Automation Name                   | Diffusion                                                       | "Can be ""Diffusion""; ""Magbead""; or a path to a file" |
+-----------------------------------+-----------------------------------------------------------------+----------------------------------------------------------+
| Automation Parameters             | ExtensionTime=double:60|ExtendFirst=boolean:True                | Must follow format demonstrated in Value Example         |
+-----------------------------------+-----------------------------------------------------------------+----------------------------------------------------------+
| Primary Analysis                  | Default                                                         | Can be any string                                        |
+-----------------------------------+-----------------------------------------------------------------+----------------------------------------------------------+
| Primary Analysis Parameters       | CopyFileTrace=boolean:true                                      | Must follow format demonstrated in Value Example         |
+-----------------------------------+-----------------------------------------------------------------+----------------------------------------------------------+
| Secondary Analysis                |                                                                 | Can be any string                                        |
+-----------------------------------+-----------------------------------------------------------------+----------------------------------------------------------+
| Secondary Analysis Parameters     |                                                                 | Must follow format demonstrated in Value Example         |
+-----------------------------------+-----------------------------------------------------------------+----------------------------------------------------------+


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

Well No.
--------
The well number must satisfy the regular expression:

  - ``/^[A-H](?:0[1-9]|1[0-2])$/``

Automation Name
---------------
The automation name can be either "Diffusion" or "Magbead" and is not case-sensitive. A path can also be used, such as "/path/to/my/script/my_script.py". The path will not be processed further, so if the full URI is required, it must be provided in the CSV, ex. "chemistry://path/to/my/script/my_script.py".

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
