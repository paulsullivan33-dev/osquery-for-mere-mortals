# The Neighbours

osquery stands in a crowded yard —
tools that watch machines, tools that
judge them, and an ecosystem built on
osquery itself. These are
characterisations from the projects' own
documentation, not benchmarks; the lab
ran osquery only.

## The classic tools: `ps`, `ss`, `dpkg`, and friends

Every table in this guide has an older
answer: `ps` for processes, `ss` or
`netstat` for sockets, `dpkg -l` for
packages, `last` for logins, `cat
/etc/os-release` for the OS. They are
already installed everywhere, they need
no agent and no database, and for a
single question on a single machine
they are often faster to type. What
they do not give you is *one language*:
each speaks its own dialect, joins
between their worlds are shell
gymnastics, and yesterday's output
format is a parser's fond hope.
osquery's bet is that the questions are
worth a uniform tongue — SQL — and a
scheduler. Where the bet loses, it
loses honestly: on a machine you may
not install anything on, the classics
are the whole game, and chapter 13
counts osquery's own footprint among
its limits.

## auditd: the historian

The Linux audit framework watches the
kernel's doorways and writes down
*events* — this process executed, that
file opened — as they happen. osquery's
state tables are a photograph; auditd
is the security camera. The two are
complements, and osquery knows it: its
event tables (documented-only in this
guide, chapter 10) can ride on the
audit pipeline, turning auditd's raw
testimony into rows you can query. If
your question is "what is true now",
osquery alone answers it. If it is
"what happened at 3 a.m.", you want a
historian running *before* 3 a.m., and
auditd is the native one.

## Lynis: the judge

Lynis (which has its own guide in this
series) audits a Unix system against
accumulated best practice and renders
verdicts — this setting is weak, that
service should not run — with a score.
osquery deliberately renders none: it
will tell you a port is open and never
whether it should be. Put them together
and the division of labour is clean:
Lynis decides what to check on a
schedule of audits; osquery is how you
check a hundred little things on a
schedule of seconds. Facts below,
judgement above.

## Wazuh and the SIEM agents

Wazuh (the maintained heir of OSSEC —
the name lives on in osquery's shipped
`ossec-rootkit.conf` pack) is an agent
plus a manager: it collects logs, watches
file integrity, applies rules, and
raises alerts in a console. It is a
*product-shaped* answer to "watch my
machines and wake me when it matters",
where osquery is a *question-shaped*
one. Fleets that outgrow a results log
and a grep usually land here or with
osquery's own managers, next — the
difference is whether alerting or
asking is the centre of your world.

## Fleet and Kolide: osquery with a headquarters

osquery was built to be managed.
**Fleet** (by Fleet Device Management)
and **Kolide** are servers that enrol
osquery agents over TLS, hand them
their schedules and packs, stream the
differential results home, and present
the fleet as — what else — queryable
tables with a web front end. Everything
chapters 9 and 10 did with files, they
do with a control plane: live queries
against a thousand laptops at once,
policies that are just scheduled
questions with pass/fail. This guide
taught the agent alone, deliberately:
until you can read one machine's
results log and explain its silences,
a fleet's worth of them is only a
louder mystery. When the questions
outgrow one machine, these are the
doors the project itself points to.
