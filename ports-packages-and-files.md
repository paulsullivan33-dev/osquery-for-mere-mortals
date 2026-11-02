# Ports, Packages and Files

**Outcome: you can name every program
that is listening on your machine, ask
the package database questions it
usually only answers one package at a
time, and take a file's fingerprint
without leaving SQL.**

## What is listening: `listening_ports`

The raw table, on the lab machine,
taught a lesson before it taught any
ports:

```bash
osqueryi "SELECT COUNT(*) AS all_rows FROM listening_ports;"
# 354
osqueryi "SELECT COUNT(*) AS owner_unknown FROM listening_ports WHERE pid = -1;"
# 294
osqueryi "SELECT COUNT(*) AS real_listeners FROM listening_ports WHERE port > 0;"
# 32
```

354 rows, of which 294 had `pid = -1`
and port 0: sockets the sandbox's
network plumbing let osquery *see* in
the kernel's tables but not *attribute*
— they belong to neighbouring
namespaces on a shared machine, and the
columns osquery could not fill come
back as −1 and empty. On an ordinary
single machine this crowd mostly
vanishes, but the shape is worth
learning once: **`pid = -1` means "a
socket exists and I cannot name its
owner"**, and the working filter is
`WHERE port > 0`. The 32 remaining rows
collapsed, under `DISTINCT`, to 16
listeners — the sandbox reported each
real listener twice, once per gathering
path, which is why `DISTINCT` appears
in this guide's port questions as a
matter of habit.

The `protocol` column speaks in
numbers: **6 is TCP, 17 is UDP** — the
IANA protocol numbers every networking
tool secretly uses. So "what TCP is
listening" is `WHERE protocol = 6`.

## Naming the listener: a first join

A port number alone is half an answer.
The other half lives in `processes`,
and SQL already knows how to fetch it:

```bash
osqueryi "SELECT DISTINCT lp.port, lp.protocol, p.name, lp.pid FROM listening_ports lp JOIN processes p ON lp.pid = p.pid WHERE lp.port > 0 ORDER BY lp.port;"
```

Every one of the lab's sixteen
listeners belonged to a single
co-tenant program — a media server
holding its customary row of ports,
including 32400 on `0.0.0.0` (all
interfaces) and its helpers on
`127.0.0.1` (this machine only). That
address column is the risk column:
`127.0.0.1` is a conversation with
oneself, `0.0.0.0` is an open door to
the network, and the join is what turns
"some port is open" into a sentence
with a subject. Full output in
transcript
`osquery-lab/transcripts/t05-listening-ports.txt`.

## The package database: `deb_packages`

On Debian and Ubuntu systems the whole
dpkg database is a table (on RPM
systems its twin is `rpm_packages`):

```bash
osqueryi "SELECT COUNT(*) AS deb_rows FROM deb_packages;"
# 2078
osqueryi "SELECT name, version, arch, source FROM deb_packages WHERE name = 'osquery';"
# osquery | 5.24.0-1.linux | amd64 | (empty)
```

`source` names the *source package* a
binary was built from — and it is empty
for **331** of the lab's packages,
which a `GROUP BY source` exposes at
once. An empty source is the mark of a
package installed from a loose `.deb`
rather than built from the
distribution's source tree — osquery
itself, installed in chapter 3, is one
of them. "Which packages did not come
from the distribution?" is a real audit
question, and it is one `WHERE` clause:

```sql
SELECT name, version FROM deb_packages WHERE source = '';
```

## Fingerprinting a file: `hash`

One more table before the chapter ends,
because it changes what a query can
mean. `hash` computes a file's digests
when you name the file in a `WHERE`
clause — the constraint is required;
the table has no rows until you point
it at a path:

```bash
osqueryi "SELECT md5, sha1, sha256 FROM hash WHERE path = '/usr/bin/osqueryi';"
```

```text
md5     837810e2b05b2c69fb739742c21c8cfc
sha1    22aea3a1d64661ac9629a19ae6f176347b6df4cf
sha256  a3392d689294f879a500dc78ecb404afb74bfbe553701fa49509181f28e9df89
```

(Yours will match if your osquery is
the same build — that is rather the
point of a fingerprint.) Asking "did
this file change?" becomes asking the
same question twice, days apart, and
comparing strings — chapter 11 turns it
into a recipe, and chapter 10's daemon
can be set to ask it for you.

**The check for this chapter:** the
join names a program you recognise for
every listener on your machine, and
any listener it cannot name gets a
second look from you — that second look
is the entire security habit this
chapter exists to build.
