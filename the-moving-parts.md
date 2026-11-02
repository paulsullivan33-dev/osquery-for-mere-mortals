# The Moving Parts

osquery presents as two programs and a
pile of tables. Underneath, six parts do
six different jobs, and nearly every
surprise in this guide — including most
of the troubleshooting chapter — is one
of these parts behaving exactly as
designed while the reader expected
another part's behaviour. This chapter
names them.

## The tables

The heart of the thing. A **table** is a
named view of one kind of system fact:
`processes`, `users`, `listening_ports`,
`deb_packages`, `os_version`. On the
lab's Linux build there were **164** of
them; the shelf differs by platform —
a Windows machine offers registry and
scheduled-task tables a Linux machine
has never heard of, and this build's
`deb_packages` is `rpm_packages` on a
Fedora box. Each table is a piece of
code that knows how to *gather* its
fact: read `/proc`, ask the kernel,
parse the package database. Gathering
happens **when the query runs**, not on
a schedule in the background — which is
why two identical questions a second
apart can disagree (chapter 13 met a
process count of 32 becoming 33 between
two queries, because the machine was
alive in between).

Two families of tables exist. **State
tables** — nearly everything in this
guide — answer "what is true now".
**Event tables** (names like
`process_events`, `file_events`) answer
"what happened", are fed by publishers
inside the daemon, and only fill up
while osqueryd runs with them enabled.
The lab's daemon ran with its event
publishers switched off by the default
configuration — its startup log says so
in so many words — so the event tables
are documented-only in this guide.

## The shell: osqueryi

`osqueryi` is the interactive face: a
SQLite-flavoured prompt with dot
commands of its own — `.tables` to list
the shelf, `.schema NAME` to print a
table's definition, `.mode` to change
how answers are drawn. Given a query as
a command-line argument it runs it and
exits, which is how scripts use it
(chapter 8). The shell asks as **whoever
runs it**: started by an ordinary user
it sees what that user may see, and
some tables answer empty rather than
complain (chapter 14's shadow trick).
Started as root, it sees everything.

## The daemon: osqueryd

`osqueryd` is the same engine with a
timetable. It reads a **configuration**
— which questions, how often — and asks
them on schedule, keeping its working
memory in an embedded database
(RocksDB; the file `osquery.db`) and
writing answers to the **logger**, by
default a file: `osqueryd.results.log`.
A **watchdog** normally supervises it,
restarting the worker process if it
misbehaves; the lab switched the
watchdog off (`--disable_watchdog`)
because one visible process is easier to
watch by hand, and chapter 10 notes the
difference. On a normally installed
machine a service unit (systemd, on
Linux) starts the daemon; the package
installs that unit **disabled**, so the
daemon runs when you say so, not merely
because you installed it — the lab
verified the status reports
`inactive (dead)` and deliberately left
it that way.

## The configuration and the packs

The daemon's configuration is one JSON
file — conventionally
`/etc/osquery/osquery.conf` — holding
options, a **schedule** of named
questions with intervals, and a list of
**packs**. A pack is a second JSON file
full of related questions with a theme:
the package ships packs for incident
response, IT compliance, hardware
monitoring and known-bad patterns, and
chapter 9 writes a small one. Questions
from a pack join the schedule under
names like `pack_lab_os_version` — pack
first, so the log says where each
question came from. A helper,
**osqueryctl**, starts and stops the
service and can check the configuration
without running anything:
`osqueryctl config-check`.

## The results log

The daemon's diary, one JSON object per
line. A line names the question, the
machine, the time, the columns of the
answer, and an **action**: `added` for
rows that appeared (or changed —
chapter 10 takes this apart: a changed
row is written as its old self removed
and its new self added). Because the
logging is **differential**, the log is
a record of *changes to answers*, not a
tape of every answer — the single most
misunderstood fact in this guide, and
the reason chapter 10 reads the
`osquery_schedule` table's execution
counts before believing a quiet log.

## Which part holds what

| Question | The part that answers it |
| --- | --- |
| Why did this query return different rows twice? | The tables — they gather live, between your two questions |
| Why is this table empty for me but not for root? | The shell's identity — tables respect the asker's permissions |
| Why is the results log quiet though the daemon runs? | The differential logger — unchanged answers are not written |
| Where did the question `pack_lab_os_version` come from? | The pack named in the configuration |
| Why won't the daemon start on my config? | The configuration — check it before it runs (chapter 9) |
| Who restarts the daemon when it crashes? | The service unit outside, and the watchdog inside |

Keep this table in mind. When osquery
surprises you, the surprise has an
address, and the address is one of
these six.
