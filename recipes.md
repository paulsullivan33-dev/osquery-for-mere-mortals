# Recipes

Short jobs, each built only from pieces
the earlier chapters verified. Unless a
recipe says otherwise, the outputs
quoted are the lab's.

## What is listening, in one question

Chapter 6's join, kept whole — the
single most useful osquery question
there is:

```bash
osqueryi "SELECT DISTINCT lp.port, lp.protocol, p.name, lp.pid FROM listening_ports lp JOIN processes p ON lp.pid = p.pid WHERE lp.port > 0 ORDER BY lp.port;"
```

Read it as an audit: every row should
be a program you can account for, on an
address you intended. `protocol` 6 is
TCP, 17 is UDP; add `AND lp.protocol = 6`
for the TCP-only view, or
`AND lp.address = '0.0.0.0'` for just
the doors open to the network.

## The morning inventory, as JSON

Four identity questions, appended to
one file a script (or a diff) can read
later:

```bash
for t in os_version uptime; do
  osqueryi --json "SELECT * FROM $t;"
done > inventory.json
osqueryi --json "SELECT hostname, physical_memory FROM system_info;" >> inventory.json
osqueryi --json "SELECT COUNT(*) AS processes FROM processes;" >> inventory.json
```

Each query writes its own JSON array,
so the file is a small anthology rather
than one document — chapter 8's
contract, applied with open eyes. Run
it daily and the *changes* (a new OS
version string, a memory total that
moved) stand out in a way no dashboard
improves on.

## Find the memory hogs

Chapter 5's top ten, tightened to five
and ready for a terminal:

```bash
osqueryi "SELECT pid, name, ROUND(resident_size/1048576.0, 1) AS rss_mb FROM processes ORDER BY resident_size DESC LIMIT 5;"
```

Remember the fifteen characters
(chapter 5): when a name in the list is
cut off mid-word, follow it up with
`path` and `cmdline` for that pid
before concluding anything.

## Did that package actually install?

```bash
osqueryi "SELECT name, version, arch FROM deb_packages WHERE name = 'osquery';"
```

An empty table is the answer "no" —
(the table, not an error). Chapter 6's
companion question finds what arrived
outside the distribution's own tree:

```bash
osqueryi "SELECT name, version FROM deb_packages WHERE source = '' LIMIT 10;"
```

## Before-and-after: hash a file you care about

```bash
osqueryi --json "SELECT sha256 FROM hash WHERE path = '/usr/bin/osqueryi';" > before.json
# ... time passes, an update happens ...
osqueryi --json "SELECT sha256 FROM hash WHERE path = '/usr/bin/osqueryi';" > after.json
diff before.json after.json
```

Silence from `diff` is the file
unchanged; a one-line difference is a
changed binary with the new fingerprint
already in hand. Point it at a config
file, a script you run as root, or
anything whose surprise modification
would ruin your week — and chapter 10's
daemon can ask it on a schedule if you
add it to a pack.

## Who has been on this machine?

Chapter 5's table, with the boot record
kept — the fastest honest answer to
"did anyone log in?":

```bash
osqueryi "SELECT type, user, tty, host, time FROM logged_in_users ORDER BY time;"
```

On the lab's sandbox the only row was
the boot itself. Interpret yours under
chapter 1's rule: your machine, your
question to ask.

## Count a thing, every day, without the daemon

Chapter 8's bridge in one line — the
poor person's schedule, using the lab's
own script as the shape:

```bash
osqueryi --json "SELECT port FROM listening_ports WHERE port > 0;" \
  | python3 osquery-lab/count-ports.py
```

Stdout is one line of fact; a cron job
appending it to a file builds the same
history chapter 10's log builds, at
human scale. Graduate to osqueryd when
the questions multiply — not before.
