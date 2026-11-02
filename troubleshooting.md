# Troubleshooting

The failures the lab met for real, in
roughly the order a new user meets
them. Transcripts:
`osquery-lab/transcripts/t11-failures.txt`
unless another is named.

## "Error: no such table"

```bash
osqueryi "SELECT * FROM no_such_table;"
# Error: no such table: no_such_table   (exit 1)
```

Either the name is misspelled, or the
table belongs to another platform
(`rpm_packages` on this Debian machine
is exactly this error). `.tables` with
a prefix finds the real name — and
remember chapter 4's catch: the filter
is a **prefix**, so `.tables port`
finds the portage tables and not
`listening_ports`. `.tables listening`
is the ask that works.

## "Error: no such column"

Chapter 4's lesson, repeated because it
is the most common error in the tool:
the column name is wrong, and guessing
a second name wastes the minute that
`.schema <table>` would have spent
once. The schema is the contract; read
it, then write the query (transcript
`t02-system-identity.txt` keeps the
lab's own miss and repair).

## `.schema` prints nothing — and exits 0

The mirror-image trap. Ask `.schema`
about a table that does not exist and
the shell prints **nothing at all** and
reports success. A missing table looks
exactly like a table with no
definition. If a schema comes back
empty, do not debug the table — check
the name against `.tables`.

## The query works as root and returns nothing as me

Privilege, wearing its quiet disguise:

```bash
osqueryi "SELECT COUNT(*) AS shadow_rows FROM shadow;"            # as root: 41
su -s /bin/sh nobody -c 'osqueryi "SELECT COUNT(*) FROM shadow;"' # as nobody: 0
```

Both exit 0. osquery answers many
protected tables with an *empty result*
rather than a refusal, because the
table code simply cannot read what the
user cannot read. Before concluding a
fact is absent, ask who is asking —
and remember the daemon normally runs
as root, which is why its answers and
your shell's answers can honestly
differ.

## The daemon refuses the configuration

```text
E... config.cpp:989] updateSource failed to parse config, of source: .../broken.conf
Error reading config: Error parsing the config JSON
```

A single truncated brace did that — a
pack or schedule file that is not valid
JSON stops the daemon before it starts,
and names the file on its way out. The
defence is chapter 9's habit, run
*before* the daemon ever sees it:

```bash
osqueryctl config-check
osqueryd --config_check --config_path=/etc/osquery/osquery.conf
```

Silence and exit 0 from both is the
all-clear. A config that parses can
still schedule a broken *query* — that
failure surfaces in the daemon's own
log (`osqueryd.INFO`, beside the
results log) at the first execution,
which is the other reason to read the
INFO log after any config change.

## The daemon runs, but the results log is silent

Chapter 10's lesson arriving as a
bug report. Check, in order:

1. The executions counter:
   `SELECT name, executions FROM osquery_schedule;`
   against the daemon's database (the
   shell needs `--config_path` and
   `--database_path` pointed at the
   daemon's, and the daemon stopped, or
   its own shell — the database is
   single-writer). Rising counters with
   a quiet log means **nothing changed**,
   and the daemon is healthy.
2. Flat counters mean the question is
   not scheduled: a pack not registered,
   or a platform line that excludes this
   machine.
3. No log file at all means the logger
   path: `--logger_path` (or the
   service's default `/var/log/osquery/`)
   is where the file lives — look where
   the daemon was told to write, not
   where you assumed.

## The service says "inactive (dead)"

That is the package's default, verified
in the lab with `osqueryctl status`:
the unit is installed **disabled**, and
the daemon runs when you enable and
start it (`osqueryctl start`), not
because you installed the package. If
the status instead says *failed*,
`osqueryctl config-check` and the INFO
log are the next two stops, in that
order.

## `dpkg` refuses: "frontend lock was locked"

Met during this guide's own install
(chapter 3). Another package operation
— an unattended upgrade, a second
terminal — holds the lock, and the lock
is right. Wait for it to finish and
retry. Never delete the lock file; the
error message says so itself, and it
is correct.

## Every listener appears twice

On shared or containerised machines the
port table can report each real
listener twice (the lab's 34 rows, 17
ports — chapter 8 counted them). It is
the same socket gathered by two paths,
not two sockets. `SELECT DISTINCT` is
the standing fix in this guide's port
questions; treat a sudden *odd* count
in raw rows as a prompt to recount with
it, not as a crowd of new listeners.
