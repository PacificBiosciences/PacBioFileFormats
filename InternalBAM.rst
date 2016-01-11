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

The internal BAM format **requires** that IPD and Pulsewidth are
stored **losslessy** (for both *base* and *pulse* level tracks).

Additionally, in order to identify the precise start frame
corresponding to a pulse/base event, records in the internal BAM
format includes a vector tag recording the start frame of each pulse.

    +-------------+-----+----------+----------+-----------------------------+
    | Feature     | Tag | Type     | Example  | Comment                     |
    +=============+=====+==========+==========+=============================+
    | Start frame | sf  | B,I      | 10, 15,  | Array containing the first  |
    |             |     |          |  23, 28  | frame number in the pulse,  |
    |             |     |          |          | for every pulse.            |
    +-------------+-----+----------+----------+-----------------------------+

Note that the precise start frame of a pulse or base event must be
identified using this tag; it *cannot* safely be identified by doing a
cumulative sum of (pulse-width-in-frames + pre-pulse-frames), because
occasionally the pre-pulse-frames cannot be represented exactly due to
the truncation to max(uint16) before storage in the BAM.  (The same
held true for RS bas/pls .h5 files).


Signal intensity measures
=========================

Some of the signal intensity measure recorded in the file are in
*dye-weighted-sum* (DWS) space, while others are in *camera* space.

Some of the intensity measures are scalars, reflecting only a single
channel---the "called" channel for a pulse, which is the nominal
channel assigned to the pulse label of the call.  For example: *pkmid*
(``pm``) and *pkmean* (``pa``).  Other intensity measures reflect all
`nCam` channels, for example *pkmid2*.  We refer to these recordings
as **nCam-vectors**.  An nCam-vector metric for a two-camera system
with nominal channel order (green, red) would be stored as follows in
a 1-d BAM array::

   [green_0, red_0, green_1, red_1, ...]

It's important to recall these distinctions when processing the signal
intensity measures.


Nominal channel order
=====================

For four-camera systems, the nominal channel order is (T, G, A, C).

For two-camera systems, the nominal channel order is (green, red).


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
    | MergeQV             | pg      | Z      |                    | TODO                           |
    +---------------------+---------+--------+--------------------+--------------------------------+
    | Pulse mean signal   | pa      | B,S    |      2,3,2,4       | Scalar--only includes signal   |
    | (pkmean)            |         |        |                    | measure for the "called"       |
    |                     |         |        |                    | channel.                       |
    |                     |         |        |                    | **Scalar, DWS space.**         |
    +---------------------+---------+--------+--------------------+--------------------------------+
    | Pulse mid signal    | pm      | B,S    |      3,3,4,3       | Scalar.  Mean, omitting edge   |
    | (pkmid)             |         |        |                    | frames.                        |
    |                     |         |        |                    | **Scalar, DWS space.**         |
    +---------------------+---------+--------+--------------------+--------------------------------+
    | Pulse mean signal 2 | ps      | B,S    |  40,50,41,52,60,44,| Pulse signal measure for all   |
    | (pkmean2)           |         |        |  44,50             | channels.                      |
    |                     |         |        |                    | **nCam-vector, camera space**. |
    +---------------------+---------+--------+--------------------+--------------------------------+
    | Pulse mid signal 2  | pi      | B,S    |  40,50,41,52,60,44,| Like `pkmean2`, but averaging  |
    | (pkmid2)            |         |        |  44,50             | done over pulse interior only. |
    |                     |         |        |                    | **nCam-vector, camera space**  |
    +---------------------+---------+--------+--------------------+--------------------------------+
    | Pre-pulse frames    | pd      | B,S    |      8,5,5,8       | Pre-pulse frames, truncated to |
    |                     |         |        |                    | max(uint16).                   |
    +---------------------+---------+--------+--------------------+--------------------------------+
    | Pulse width (frames)| px      | B,S    |      2,2,4,5       | Pulse width in frames,         |
    |                     |         |        |                    | truncated to max(uint16).      |
    +---------------------+---------+--------+--------------------+--------------------------------+


Note that we encode the entire pulse stream and its attendant
features, even though some of these are at least partially redundant
with base-level features.




Baseline sigma
##############

We encode the *baseline sigma* for each channel for a read, for
compatibility with tools like PulseRecognizer.  The baseline sigma is
a piecewise constant function of time, changing at an interval on the
order of 10 to 100 seconds (i.e., slowly!), **however, in the BAM file
we only record a time average over the trace.**

Baseline measures recorded here are in **DWS space**.  Camera trace
baseline metrics---as well as more a more detailed view of the time
evolution of the baseline---are available in the DME dump.


- "bs" tag = BaselineSigma = `{mean green baseline, mean read baseline}`
  (as `float32[]` / `B,f`)
