# What osquery Is

You want to know something about a
computer. What is listening on the
network? Which processes are eating the
memory? Is the package you installed
actually there, and which version? Each
question has a classic tool, and each
tool has its own flags and its own
dialect of output, which your script
then has to parse with hope and string
splitting.

**osquery removes the dialects.** It is
a program, first released by Facebook's
security team in 2014 and now an
independent open-source project, that
presents the operating system as a
**relational database**. Not a copy of
the system in a database — the system
itself, read live, through tables:

- `processes` — every running process,
  one row each.
- `listening_ports` — every open
  listening socket.
- `users`, `logged_in_users` —
  accounts, and who is on the machine
  right now.
- `deb_packages` (or `rpm_packages`
  elsewhere) — the package database.
- `os_version`, `system_info`,
  `uptime` — the machine's identity
  papers.

You ask in **SQL** — the same `SELECT`,
`WHERE`, `JOIN` and `GROUP BY` as any
database:

```sql
SELECT port, address
FROM listening_ports
WHERE protocol = 6;
```

and osquery goes and looks, at the
moment you ask, and hands back rows. The
database underneath the answers is
SQLite's engine wearing a costume: the
tables are **virtual tables** whose rows
are gathered from the kernel, from
`/proc`, from the package database,
from wherever the fact actually lives,
each time the query runs.

## Two ways to ask

The same engine wears two faces, and
this guide teaches both.

**osqueryi** is the interactive shell:
a prompt, your question, a table of
answers drawn in boxes. It is how you
explore — what tables exist, what
columns they have, what the machine says
today. Chapters 4 to 8 live here.

**osqueryd** is the daemon: the same
questions, written into a configuration
file with an interval beside each, asked
forever. Its answers go to a **results
log**, and it has a thrifty habit — it
logs *changes*. Ask it every fifteen
seconds how many user accounts exist
and, while the answer stays 41, the log
records the fact once and then keeps
quiet. Chapters 9 and 10 build this up:
a **query pack** of this guide's own,
and a daemon run the lab timed and read
back.

Around the two faces sits an ecosystem
this guide touches honestly but does not
pretend to run: machines can enrol to a
central server and stream their answers
home (fleet management), and extra
tables can be bolted on as **extensions**
written by other people. Those are
chapter 12's neighbours and the fleet
paragraph of chapter 13's limits —
described, not performed.

## A first taste

After installing (chapter 3), the shell
needs one line:

```bash
osqueryi "SELECT * FROM uptime;"
```

```text
+------+-------+---------+---------+---------------+
| days | hours | minutes | seconds | total_seconds |
+------+-------+---------+---------+---------------+
| 0    | 0     | 51      | 13      | 3073          |
+------+-------+---------+---------+---------------+
```

The lab's machine had been up fifty-one
minutes. Nothing was installed into a
database, nothing was imported: the
question was asked and the machine
answered. (Transcript
`osquery-lab/transcripts/t02-system-identity.txt`.)

## What it is not

osquery is not a **writer**: its SQL
asks questions and changes nothing. It
cannot kill a process, close a port, or
remove a package — deliberately. It is
not a **historian** in its basic form:
a query sees the system *now*, and a
process that started and finished
between two questions leaves no trace in
the state tables (history lives in the
separate event tables, which need the
daemon and are documented-only here —
chapter 13 is plain about this). It is
not a **judge**: it reports that a port
is open, not whether the port *should*
be; verdicts are Lynis's trade
(chapter 12). And it is not a monitoring
product with dashboards and alerts —
its outputs are tables, JSON and log
lines, and graphs are somebody else's
job.

## The rule that comes with the eyes

osquery's usefulness is its depth, and
the depth cuts both ways. As the
chapters will show, a single query can
list every command every user is
running, every file a process has open,
the fingerprints of every SSH key on the
box. Run as root — the way the daemon
usually runs — it can read tables like
`shadow` that ordinary users get an
empty answer from (the lab demonstrates
exactly that gap in chapter 14). So the
rule, stated here where the README also
states it and meant the whole way
through: **inventory machines you own,
or machines whose owner has asked you
to inventory them**, keep results logs
somewhere you would keep a password
file, and think before you schedule a
question — a question asked every
fifteen seconds about other people's
activity is surveillance, and should be
treated, and disclosed, as such. On
your own machines, for your own
questions, it is simply the best torch
in the building.

## Who it is for

The administrator of more machines than
they can hold in their head, who wants
one language for "what is true here?"
The security-minded home-lab keeper who
wants to know what is listening and why.
The curious: anyone who has ever run
four commands to answer one question
and suspected there was a tidier way.
The common thread is a machine you are
responsible for, and questions about it
that deserve better than screen-scraping.
