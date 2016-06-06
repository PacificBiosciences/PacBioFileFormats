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


Pulse features
==============

Background: A spike in the trace can be identified as a pulse and
a pulse can be called as a base. Thus, the number of pulse calls is at 
least equal the number of base calls, as they are also pulses.
As some pulses do not qualify as bases, the number of pulses is
possibly greater than the number of bases.

The pulse BAM extends the vanilla PacBio BAM format with additional
per-read tags. These new pulse tags are of equal length, 
one entry per pulse:

    +---------------------+---------+--------+--------------------+--------------------------------+
    | Feature             | Tag name| Type   |      Example       | Comment                        |
    +=====================+=========+========+====================+================================+
    | Pulse call          | pc      | Z      |        GaAT        | Lowercase used to indicate a   |
    |                     |         |        |                    | pulsecall that was "squashed"  |
    |                     |         |        |                    | by P2B, uppercases are         |
    |                     |         |        |                    | the respective                 |
    |                     |         |        |                    | base calls from the SEQ field  |
    +---------------------+---------+--------+--------------------+--------------------------------+
    | LabelQV             | pq      | Z      |    20,20,12,20     | TODO                           |
    +---------------------+---------+--------+--------------------+--------------------------------+
    | AltLabel            | pt      | Z      |        ---C        | "second best" label; '-' if no |
    |                     |         |        |                    | alternative applicable         |
    +---------------------+---------+--------+--------------------+--------------------------------+
    | MergeQV             | pg      | Z      |                    | TODO                           |
    +---------------------+---------+--------+--------------------+--------------------------------+
    | Pulse mean signal   | pa      | B,S    |      2,3,2,4       | Only includes signal measure   |
    | (pkmean)            |         |        |                    | for the "called" channel       |
    |                     |         |        |                    | *Units:* photoelectron         |
    +---------------------+---------+--------+--------------------+--------------------------------+
    | Pulse mid signal    | pm      | B,S    |      3,3,4,3       | Mean, omitting edge frames     |
    | (pkmid)             |         |        |                    | *Units:* photoelectron         |
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

Additionally we need to encode the *baseline sigma* for each channel
for a read.  The baseline sigma is a piecewise constant function of
time, changing at an interval on the order of 10 to 100 seconds (i.e.,
slowly!).  We tally the number of pulses in each interval ("block")
and the baseline sigma for each channel during that block, as follows:

- "bs" tag = BaselineSigma = `{ A_0, C_0, G_0, T_0, A_1, C_1, G_1, T_1, ... }` (as `float32[]` / `B,f`), where subscript denotes block number.

- "pb" tag = PulseBlockSize
  = number of pulses in each block (`uint32[]`, `B,I`)

Thus, for example, the first `pb[0]` pulses have baseline sigma
`bs[0]` for the A channel.

Note that for RS data, baseline sigma is only calculated once per ZMW;
for Sequel, it is calculated per-time-block per-ZMW, hence the need
for an array.




Unresolved questions
====================

- Where will baseline information be stored?  Current plan is to store
  it in ``sts.h5`` file (which needs a spec of its own).
- The pkmid/pkmean values are stored in photoelections, which means we need 
  the gain in order to compute the values in counts.  This has internal value 
  when back-converting internal BAMs to pls.h5 files, which uses counts to 
  represent pk values.
