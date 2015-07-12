===================================================
BAM format additions for *PacBio-internal* analysis
===================================================

.. moduleauthor:: David Alexander, John Nguyen



PacBio-internal BAM flavors
===========================

Several PacBio-internal use cases require extra information to be
carried in our BAM files---beyond

There will be two (3?) flavors of BAM for internal analysis.

The internal analysis files will be fully compliant with the PacBio
BAM spec (with spec version noted in the ``@HD::pb`` tag) but will
include additional per-read tags containing additional information.


.. note:: Do we want to add some tag to each read group to indicate
          the flavor of analysis file?


    +-----------------------+-------------------------------------+
    | Name                  | Use cases                           |
    +=======================+=====================================+
    | Pulse BAM             | Pulse-to-base training and          |
    |                       | refarming; trace viewing            |
    |                       | (PulseRegognizer)                   |
    +-----------------------+-------------------------------------+
    | Internal metrics BAM  | Milhouse analyses                   |
    +-----------------------+-------------------------------------+



Internal metrics BAM
====================

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
partition the frames in the entire polymerase read.



[JVN: what else do you need?]




Pulse BAM
=========

.. note::
   I think it would be reasonable to assume that the Pulse BAM here is
   a valid internal metrics BAM, i.e. we have a subclassing relationship.


The current incarnation of pulse-to-base is a classifier that
determines which pulses will not make it into the base stream (are
"squashed").  This means that we could use a fairly compact encoding
that just represents the diff between the basecalls and their metrics,
and the pulsecalls and their metrics.  However, in the interest of
flexibility and debuggability, we opt for the more obvious (if
verbose) encoding.

The pulse BAM extends the vanilla PacBio BAM format with the following
per-read tags:


    +---------------------+---------+--------+--------------------+--------------------------------+
    | Feature             | Tag name| Type   |     Example        | Comment                        |
    +=====================+=========+========+====================+================================+
    | Pulse call          | pc      |   Z    |     GATTaACA       | Lowercase used to indicate a   |
    |                     |         |        |                    | pulsecall that was "squashed"  |
    |                     |         |        |                    | by P2B                         |
    +---------------------+---------+--------+--------------------+--------------------------------+
    | Pulse mean signal   | pa      | B,S    |  2,3,2,4,4,2,3,3   | Will hopefully be eliminated   |
    | (pkmean)            |         |        |                    | once Dave investigates P2B     |
    +---------------------+---------+--------+--------------------+--------------------------------+
    | Pulse median signal | pm      | B,S    |  3,3,4,3,2,2,2,3   |                                |
    | (pkmid)             |         |        |                    |                                |
    +---------------------+---------+--------+--------------------+--------------------------------+
    | Pre-pulse frames    | pd      | B,S    |  8,5,5,8,7,2,3,4   |                                |
    +---------------------+---------+--------+--------------------+--------------------------------+
    | Pulse width (frames)| px      | B,S    |  2,2,4,5,2,3,2,2   |                                |
    +---------------------+---------+--------+--------------------+--------------------------------+


Note that we encode the entire pulse stream and its attendant
features, even though some of these are at least partially redundant
with base-level features.



Unresolved questions
====================

- Where will baseline information be stored?  Current plan is to store
  it in ``sts.h5`` file (which needs a spec of its own).
