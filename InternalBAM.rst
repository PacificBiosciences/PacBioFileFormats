===================================================
BAM format additions for *PacBio-internal* analysis
===================================================

.. moduleauthor:: David Alexander, John Nguyen



PacBio-internal BAM flavors
===========================

Several PacBio-internal use cases require extra information to be
carried in our BAM files.  There is currently a single "internal"
flavor of the BAM spec documented here.

The internal analysis files will be fully compliant with the PacBio
BAM spec (with spec version noted in the ``@HD::pb`` tag) but will
include additional per-read tags containing additional information.


Kinetic information
===================

The internal metrics BAM **requires** that IPD and Pulsewidth are stored
**losslessy** (for both *base* and *pulse* level tracks).

There are some common use cases where we will need to identify read
records that satisfy some constraint on the start/end times of the
corresponding events.  For example, we might be interested in only
reads that occurred within the first hour of sequencing.  To make this
efficient (for example, eliminating the need to chase IPD/PW
information in different subread/scrap records in order to sum all the
event durations since the movie start), each BAM record will have
additional tags ``bf`` (begin frame) and ``ef`` (end frame).


    +------------+-----+----------+----------+---------------------------+
    |Feature     | Tag | Type     | Example  | Comment                   |
    +============+=====+==========+==========+===========================+
    |Begin frame | bf  | i        |   351    | First frame number        |
    |            |     |          |          | considered to be "in" the |
    |            |     |          |          | read record, including    |
    |            |     |          |          | pre-pulse interval        |
    |            |     |          |          | preceding the first pulse |
    |            |     |          |          | event "in" the record.    |
    +------------+-----+----------+----------+---------------------------+
    |End frame   | ef  | i        |  20671   | 1+last frame number       |
    |            |     |          |          | considered to be "in" the |
    |            |     |          |          | read record (last frame in|
    |            |     |          |          | last pulse)               |
    +------------+-----+----------+----------+---------------------------+

These ``[bf, ef)`` intervals for the records from a given ZMW
partition the frames in the entire polymerase read





Pulse features
==============


The pulse BAM extends the vanilla PacBio BAM format with the following
per-read tags:


    +---------------------+---------+--------+--------------------+--------------------------------+
    | Feature             | Tag name| Type   |      Example       | Comment                        |
    +=====================+=========+========+====================+================================+
    | Pulse call          | pc      | Z      |        GaAT        | Lowercase used to indicate a   |
    |                     |         |        |                    | pulsecall that was "squashed"  |
    |                     |         |        |                    | by P2B                         |
    +---------------------+---------+--------+--------------------+--------------------------------+
    | LabelQV             | pq      | Z      |    20,20,12,20     | TODO                           |
    +---------------------+---------+--------+--------------------+--------------------------------+
    | AltLabel            | pt      | Z      |        ---C        | "second best" label; '-' if no |
    |                     |         |        |                    | alternative applicable         |
    +---------------------+---------+--------+--------------------+--------------------------------+
    | AltLabelQV          | pv      | Z      |      0,0,0,3       | TODO                           |
    +---------------------+---------+--------+--------------------+--------------------------------+
    | MergeQV             | pg      | Z      |                    | TODO                           |
    +---------------------+---------+--------+--------------------+--------------------------------+
    | Pulse mean signal   | pa      | B,S    |      2,3,2,4       | Only includes signal measure   |
    | (pkmean)            |         |        |                    | for the "called" channel       |
    +---------------------+---------+--------+--------------------+--------------------------------+
    | Pulse mid signal    | pm      | B,S    |      3,3,4,3       | Mean, omitting edge frames     |
    | (pkmid)             |         |        |                    |                                |
    +---------------------+---------+--------+--------------------+--------------------------------+
    | Pre-pulse frames    | pd      | B,S    |      8,5,5,8       | TODO                           |
    +---------------------+---------+--------+--------------------+--------------------------------+
    | Pulse width (frames)| px      | B,S    |      2,2,4,5       | TODO                           |
    +---------------------+---------+--------+--------------------+--------------------------------+

Question: 
    * Tag LabelQV has type B,C (*uint16_t* array) in BAM, and is not defined in PulseAndBaseICD.xls. However, according to an existing pls.h5 file, its type is *uint8_t* array. Is uint8_t array sufficient? Or is it a typical QV such that its type can be Z in BAM?
    * Tag AltLabelQV has type B,C (*uint16_t* array) in BAM, and is not found in any pls.h5 file. What is the expected value range?
    * Tag MergeQV has type B,C (*uint16_t* array) in BAM, and is not defined in PulseAndBaseICD.xls. However, according to an existing pls.h5 file, its type is *uint8_t* array. Is MergeQV a typical QV such that its type can be Z in BAM?
    * Tag Pre-pulse frames has type B,C (*uint16_t* array) in BAM, and has type *uint32_t* array in PulseAndBaseICD.xml.
    * Frame tags are described as TagName:Codeype (such as IPD:Frames or IPD:CodecV1) in BAM header read group. Should we follow this convention and describe Pre-pulse Frames as *PrePulseFrames:Frames* and Pulse width as *PulseWidthFrames:Frames*?
    * Tag pkmean and pkmid are defined by channel per pulse (which means for each pulse, there are four values, each per channel). However, it sounds like there is exactly one pkmean or pkmid value for each pulse in BAM?

Note that we encode the entire pulse stream and its attendant
features, even though some of these are at least partially redundant
with base-level features.




Baseline sigma
##############

Additionally we need to encode the *baseline sigma* for each channel
for a read.  The baseline sigma is a piecewise constant function of
time, changing at an interval on the order of 10 to 100 seconds (i.e.,
slowly!).  We tally the number of pulses in each interval ("block")
and the baseline sigma for each channel during that block, as follows:

- "bs" tag = BaselineSigma = `{ A_0, C_0, G_0, T_0, A_1, C_1, G_1, T_1, ... }` (as `float32[]` / `B,f`), where subscript denotes block number.

- "pb" tag = PulseBlockSize
  = number of pulses in each block (`uint32`, `i`)

Question: should type of "pb" tag be "i" instead of "B,I"?

Thus, for example, the first `pb[0]` pulses have baseline sigma
`bs[0]` for the A channel.

Note that for RS data, baseline sigma is only calculated once per ZMW;
for Sequel, it is calculated per-time-block per-ZMW, hence the need
for an array.




Unresolved questions
====================

- Where will baseline information be stored?  Current plan is to store
  it in ``sts.h5`` file (which needs a spec of its own).
