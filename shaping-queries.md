# Shaping Queries

**Outcome: you can read a table's full
definition before querying it, combine
tables with joins on purpose rather
than by luck, and use SQLite's own
functions to turn raw columns into
answers.** The previous chapters asked
questions; this one is about asking
them *well*.

## `.schema`, the contract

Chapter 4 met `.schema` as an error
repair. It is better used as a first
step. Here is the contract for the
busiest table in the guide, exactly as
the shell prints it (transcript
`osquery-lab/transcripts/t07-schema-and-joins.txt`):

```text
CREATE TABLE processes(`pid` BIGINT, `name` TEXT, `path` TEXT,
`cmdline` TEXT, `state` TEXT, `cwd` TEXT, `root` TEXT,
`uid` BIGINT, `gid` BIGINT, `euid` BIGINT, `egid` BIGINT, ...
`resident_size` BIGINT, `total_size` BIGINT, `user_time` BIGINT,
`system_time` BIGINT, `disk_bytes_read` BIGINT,
`disk_bytes_written` BIGINT, `start_time` BIGINT, `parent` BIGINT,
... `cgroup_path` TEXT, PRIMARY KEY (`pid`)) WITHOUT ROWID;
```

Three things to notice. The interesting
columns you have not used yet are all
here — `parent` (every process's
parent pid, so the process *tree* is a
self-join away), `start_time`,
`disk_bytes_read`. Some columns are
marked `HIDDEN`: they exist, they can
be selected, they simply do not appear
in `SELECT *` — `elapsed_time` and
`percent_processor_time` are the useful
pair. And the primary key is `pid`,
which is what makes the joins in this
guide one-to-one instead of hopeful.

## Joins with intent

Chapter 6 joined ports to processes to
*give a port a name*. The same move
gives a process an owner:

```bash
osqueryi "SELECT p.pid, p.name, u.username FROM processes p JOIN users u ON p.uid = u.uid ORDER BY p.pid LIMIT 8;"
```

```text
| 1     | systemd         | root |
| 17    | systemd-journal | root |
| 67    | hatch           | root |
| 752   | hatch-execd     | root |
```

On the lab machine every row said
`root` — a sandbox where one identity
does everything. On a desktop the same
question separates your programs from
the system's at a glance, and swapping
the join key to `p.euid` answers the
sharper question: not who *launched*
it, but whose privileges it is *running
with* — the question behind half of all
privilege-escalation audits.

## The clock is a table too

`time` holds one row: the machine's
idea of now, in pieces — weekday, year,
month, day, hour — plus `unix_time` and
`timezone`. The lab first asked for a
column it does not have:

```text
osqueryi "SELECT datetime(local_time, 'unixepoch') AS now_local, timezone FROM time;"
Error: no such column: local_time
```

`.schema time` (same transcript) shows
the real names, and the corrected
question uses `unix_time` with SQLite's
`datetime()` function to render it
human:

```bash
osqueryi "SELECT datetime(unix_time, 'unixepoch') AS utc_now, weekday, timezone FROM time;"
# 2026-11-02 15:22:41 | Monday | UTC
```

That pairing — a table's raw fact, a
SQLite function shaping it — is the
general pattern. `ROUND(... / 1048576.0, 1)`
turned bytes into mebibytes in
chapter 5; `datetime(..., 'unixepoch')`
turns epoch seconds into dates here;
`COUNT`, `GROUP BY` and `ORDER BY`
have been shaping answers since
chapter 5 without ceremony. osquery's
SQL is SQLite's SQL (the SQLite guide
in this series covers the language
itself); what osquery adds is not new
grammar but new *things to talk about*.

**The check for this chapter:** pick a
table you have not used, read its
`.schema` first, and write a question
whose columns you chose from the
contract — including one `HIDDEN`
column, deliberately. If it errors, the
error names a column, and you know the
rhythm by now.
