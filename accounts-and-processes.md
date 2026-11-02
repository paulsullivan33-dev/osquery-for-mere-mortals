# Accounts and Processes

**Outcome: you can answer "who exists
on this machine, who is on it now, and
what is running" — and you know the two
honest wrinkles in those answers: the
accounts list is longer than the human
list, and process names are cut at
fifteen characters.**

## The accounts: `users`

```bash
osqueryi "SELECT COUNT(*) AS user_rows FROM users;"
```

The lab machine answered **41**. Most
of them are not people: a Linux system
carries a small crowd of service
accounts (one per daemon that wants an
identity of its own), plus `root`, plus
`nobody`. Filtering to the accounts a
human would recognise is a `WHERE`
clause:

```bash
osqueryi "SELECT uid, username, description, directory, shell FROM users WHERE uid >= 1000 OR uid = 0;"
```

```text
+-------+----------+-------------+--------------+-------------------+
| uid   | username | description | directory    | shell             |
+-------+----------+-------------+--------------+-------------------+
| 65534 | nobody   | nobody      | /nonexistent | /usr/sbin/nologin |
| 0     | root     | root        | /root        | /bin/bash         |
+-------+----------+-------------+--------------+-------------------+
```

Two lessons ride along. The lab sandbox
has no ordinary user accounts at all —
on your own machine this query shows
your account, with its real home
directory and shell. And `nobody` slips
through the `uid >= 1000` net because
its uid is 65534, the traditional
overflow value: read results before you
trust a filter's shape. The `shell`
column is its own audit — accounts
whose shell is `/usr/sbin/nologin` or
`/bin/false` cannot start an interactive
session, and an account you expected to
find in that class holding `/bin/bash`
instead is a fact worth a second look.
(Transcript
`osquery-lab/transcripts/t03-users.txt`.)

## Who is on now: `logged_in_users`

```bash
osqueryi "SELECT * FROM logged_in_users;"
```

The lab machine's only row was the
**boot record** — `type = boot_time`,
user `reboot`, the kernel version in
the host column. A sandbox nobody logs
into interactively is a quiet place.
On a lived-in machine this table lists
each session with its terminal, its
origin host, and its start time, which
makes it the natural first question of
any "was someone on this box?"
investigation — always read alongside
chapter 1's rule about whose machines
you may ask about.

## What is running: `processes`

```bash
osqueryi "SELECT COUNT(*) AS process_rows FROM processes;"
osqueryi "SELECT pid, name, ROUND(resident_size/1048576.0, 1) AS rss_mb FROM processes ORDER BY resident_size DESC LIMIT 10;"
```

The count first said **32**; a minute
later a `GROUP BY uid` counted **33** —
not an error, but chapter 2's point in
the wild: the table is gathered live
and processes are born between
questions. The top-ten table is the
practical shape of "what is eating the
memory": a name, a pid, and resident
memory converted from bytes to mebibytes
by the query itself (`resident_size`
arrives in bytes; the division and the
`ROUND` are yours to write).

Now the wrinkle, visible in the lab's
own top ten (transcript
`osquery-lab/transcripts/t04-processes.txt`):
names arrive **truncated to fifteen
characters** — a co-tenant media server
appears as `Plex Media Serv`, its helper
as `Plex Script Hos`. That is not
osquery being lazy; the kernel itself
keeps process names in a fifteen-
character field (the `comm` name), and
the table reports it faithfully. When
the name matters, the same table's
`path` and `cmdline` columns carry the
full story — for pid 1 they give the
complete `/usr/lib/systemd/systemd`,
where `name` alone gives just
`systemd` (same transcript).

**The check for this chapter:** your
`users` count, your own account in the
filtered list, and your machine's
current memory hog named in the top
ten. If the top name looks cut off
mid-word, you have met the fifteen
characters, and you know where the
rest of it lives.
