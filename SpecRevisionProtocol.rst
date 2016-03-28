===========================================
File format specification revision protocol
===========================================

.. moduleauthor:: David Alexander


Introduction
============

Experience has taught that there is no such thing as a *small*
specification change.  Any specification change can entail a lot of
work for a lot of people.  Even a seemingly minor specification change
could entail the following:

1. Core APIs (`pbbam` and `pbcore`) need to adopt a policy of either
   backwards-compatibility or of rejecting old data.  The issue of
   forwards-compatibility (old code, new data) needs to be considered
   in the specification revision; this is admittedly thornier.
   Telling people to update their software is not as easy as it
   sounds.

2. If core APIs are not or (cannot be) made backwards compatible, then
   *all test data must be regenerated*.  This is a burden on the test
   team.

3. Data-producing code (e.g. `baz2bam`, `bax2bam`, `bam2bam`) may need
   to be updated.

4. Data-consuming code (back-converters like `bam2bax`; all analysis
   applications; internal tools like PulseRecognizer)


Clearly specification revisions should be considered carefully,
especially now that our platform has stabilitized---we need to value
stability over design perfection.  This protocol is designed to
enforce slow and deliberate review of proposed spec changes.


People
======

The following stakeholders are considered the **core team**: Aaron,
Armin, Brett, Dave, Derek, Jim Drake, Nat, Martin, Yuan.  Decisions should be
reached by unanimous consent.

Aaron and Dave are the **sudoer team** and may waive cooling-off
periods by unanimous consent in case an urgent spec change is needed.

Protocol
========

We will adhere to the following protocol to revise a format specification:

1. Specification change proposal submitted as github pull request
   here; core team notified by email and invited to comment.

2. 1-week period for collecting comments (*waivable by sudoers*)

3. Meeting to discuss the proposal, at which we should weigh the
   impact of the proposal.  If the core team agrees on the proposal, a
   *plan of action* should be agreed-upon.

4. 1-week cooling-off period. Sometimes it takes a while to think of a
   design flaw.  (*waivable by sudoers*)

5. If no flaws are uncovered during the cooling-off period, go forward
   with the revision by:
      - merging the spec revision pull request;
      - record the items in the plan of action as bugs in bugzilla and begin implementation work

Suggested order-of-updates
==========================

The "plan of action" has to consider the order of software changes to
be performed.  Here is a typical, suggested order of operations that
has worked well for us in staging changes to the BAM format, at least
for changes that respect software compatibility with older BAM files:

  1. Core library updates: `pbbam`, `pbcore`
  2. Testing: `pbvalidate`
  3. Data producers: `baz2bam`, `bax2bam`
  4. Data consumers: `bam2bax`, `bam2bam`

It's advisable to do development on a branch until ready for
integration.

Specification changes that declare older BAM files to be invalid are
much more difficult because they require regeneration of test
datasets; such changes need to be negotiated more carefully or avoided
entirely.
