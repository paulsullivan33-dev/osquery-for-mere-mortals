# osquery for Mere Mortals

Questions about a computer — what is
running, what is listening, who is logged
in, which packages are installed — are
usually answered by a different tool for
every question, each with its own output
format. **osquery** answers all of them
the same way: it presents the operating
system as a set of **SQL tables**, and
you ask with `SELECT`. Processes are a
table. Listening ports are a table.
Users, packages, logged-in sessions —
tables. If you can write a `WHERE`
clause, you can interrogate a machine.

This guide explains how osquery carves a
living system into tables, how to install
it from the project's official package,
and how to ask your first questions in
its interactive shell, **osqueryi**. Then
it goes where one-off questions stop:
**query packs** — bundles of questions
other people wrote — and **osqueryd**,
the daemon that asks your questions on a
schedule and writes down how the answers
change.

The lab that wrote this guide ran the
real thing: **osquery 5.24.0**, the
official `.deb` package, on a small
Ubuntu 24.04 machine. In the shell it
explored the 164 tables this build
offers, read their schemas, and ran real
queries against the machine itself — its
OS version, uptime, users, processes,
listening ports and installed packages.
It hashed a file by asking a table. It
took osquery's answers as JSON and fed
them to a script. It wrote a small query
pack and a daemon configuration, proved
both with osquery's own config check,
and then ran the daemon by hand for
about ninety seconds and read its
results log line by line: five scheduled
questions, dozens of answers, and one
question whose answer never changed —
and which therefore appears in the log
exactly once.

One honesty note belongs here, before
any procedure. osquery sees *deeply*:
run with enough privilege it can report
every process's command line, every
logged-in user, the contents of the
password-shadow table's metadata, the
hash of any file. That is the point of
the tool, and it is also a responsibility.
**Only run osquery on machines you own
or are authorised to inventory**, and
treat its results logs as sensitive —
they are a map of the machine. The lab
ran it on its own sandbox, and the guide
says so wherever the depth of what it
can see matters.

What the lab could not do, it did not
fake. The sandbox has no service manager
doing the honours, so the daemon was run
in the open, by hand, and stopped the
same way; starting it as a managed
service the usual way is described, and
labelled, as the reader's step rather
than the lab's result. Fleets of machines
reporting to a central server, osquery
on Windows and macOS, and the event
tables that watch history instead of
state are taught from the documentation
and labelled as such. `criteria.md`
keeps the full ledger of what was run
and what was only read.

## What this guide covers

- [**What osquery is**](what-osquery-is.md) —
  the mental model: an operating system
  presented as SQL tables, asked questions
  now by a shell and forever by a daemon,
  and why the depth it sees with carries
  a rule about permission
- [**The moving parts**](the-moving-parts.md) —
  the tables, the interactive shell, the
  daemon, the configuration, the packs,
  and the results log — and which part
  holds what
- [**Installing osquery**](installing-osquery.md) —
  the official package, what it puts
  where, and the version check that
  proves it runs
- [**Your first queries**](your-first-queries.md) —
  the table list, the schema of a table,
  and first answers: what OS this is and
  how long it has been up
- [**Accounts and processes**](accounts-and-processes.md) —
  the users table, who is logged in, the
  process list, and the fifteen-character
  catch in process names
- [**Ports, packages and files**](ports-packages-and-files.md) —
  listening ports and the programs behind
  them, the package database as a table,
  and hashing a file with a query
- [**Shaping queries**](shaping-queries.md) —
  reading a schema before you query,
  joins between tables, the clock as a
  table, and the errors that teach the
  shape of the thing
- [**Output and scripting**](output-and-scripting.md) —
  pretty tables for humans, JSON for
  programs, the vertical line mode, and
  a script that counts what a query found
- [**Query packs**](query-packs.md) —
  questions bundled by other people: what
  a pack is, the ones the package ships,
  and a small pack of this guide's own,
  registered and proven
- [**Scheduling with osqueryd**](scheduling-with-osqueryd.md) —
  the daemon's config, its schedule, the
  results log and its differential habit
  of only writing down changes
- [**Recipes**](recipes.md) — what is
  listening in one question, the morning
  inventory as JSON, memory hogs, whether
  a package is installed, and the
  before-and-after hash
- [**The neighbours**](the-neighbours.md) —
  the classic tools it stands beside,
  auditd the historian, Lynis the judge,
  and the fleet managers that give
  osquery a headquarters
- [**Limits**](limits.md) — snapshots
  that race, tables that answer empty
  instead of refusing, names cut at
  fifteen characters, a reader that
  never writes, and a log that stays
  silent when nothing changed
- [**Troubleshooting**](troubleshooting.md) —
  the missing table, the silent schema,
  the empty answer that means "not as
  root", the config the daemon refuses,
  and the package lock that means wait
- [**Glossary**](glossary.md) — the
  terms, collected in one place

## What it doesn't cover

Managing a fleet: enrolling many
machines to a central osquery server
over TLS, pushing configuration to them,
and streaming their results into a
pipeline is a real and documented part
of osquery's world — and a second
machine's worth of setup this guide
points at (chapter 12 names the tools)
rather than performs. Writing osquery
extensions in C++ or Go, and the event
tables that record history (process
starts, file changes) rather than state,
are likewise described from the
documentation; the lab's daemon ran with
the event publishers switched off, and
chapter 10 says exactly what that means.
osquery on Windows and macOS uses the
same shell and the same SQL with a
different shelf of tables; this guide's
hands were on the Linux shelf.

## How to use this guide

Read chapter 1 for the model and
chapter 2 before installing anything —
knowing which part holds what turns
later confusion into a named problem.
Chapters 3 and 4 get you a program and
your first answers in one sitting.
Chapters 5 to 7 are the core skill: the
questions people actually ask a machine.
Chapter 8 is the bridge to scripts,
chapters 9 and 10 to the daemon, and
chapter 14 is the one to keep open the
first time an answer comes back empty —
in osquery, empty is a message, and it
is rarely the one you first think. The
lab's transcripts live in
`osquery-lab/transcripts/`; its query
pack is `osquery-lab/lab-pack.json`, its
daemon configuration is
`osquery-lab/osquery.conf`, its sample
results log is
`osquery-lab/sample-results.log`, and
its counting script is
`osquery-lab/count-ports.py`.

---

## Part of the series

This guide is one of the [For Mere Mortals](https://paulsullivan33-dev.github.io/mere-mortals/) guides: plain-language guides to the tools programmers and makers use.

Related guides:

- [SQL for Mere Mortals](https://paulsullivan33-dev.github.io/sql-for-mere-mortals/)
- [SQLite for Mere Mortals](https://paulsullivan33-dev.github.io/sqlite-for-mere-mortals/)
- [Watching Your System for Mere Mortals](https://paulsullivan33-dev.github.io/watching-your-system-for-mere-mortals/)
- [Lynis for Mere Mortals](https://paulsullivan33-dev.github.io/lynis-for-mere-mortals/)

## License

The writing in this guide is licensed under [CC BY 4.0](https://github.com/paulsullivan33-dev/osquery-for-mere-mortals/blob/main/LICENSE). Code examples and lab scripts are licensed under the [MIT License](https://github.com/paulsullivan33-dev/osquery-for-mere-mortals/blob/main/LICENSE-CODE).
