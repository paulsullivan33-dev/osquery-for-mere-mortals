# Your First Queries

**Outcome: you can list the tables your
osquery offers, read any table's
definition, and pull a machine's
identity papers — OS, version, uptime —
with three questions.** Everything here
is the interactive shell used two ways:
dot commands typed at its prompt, and
whole questions handed to it as
arguments.

## The shelf: `.tables`

Run the shell with no argument and it
waits at a prompt. Its own commands
start with a dot. The first one to know:

```text
osquery> .tables
  => acpi_tables
  => ai_agent_skills
  => apparmor_events
  ...
  => users
  => yum_sources
```

The lab's build offered **164 tables**
(counted in transcript
`osquery-lab/transcripts/t01-tables.txt`,
which keeps the whole list). Give
`.tables` a word and it filters — by
**prefix**, which is worth knowing
before it surprises you:

```text
osquery> .tables listening
  => listening_ports
osquery> .tables port
  => portage_keywords
  => portage_packages
  => portage_use
```

`port` matched the Gentoo portage
tables, not `listening_ports`, because
the match must be at the start of the
name. `.tables osquery` lists osquery's
own housekeeping tables — `osquery_info`,
`osquery_schedule`, `osquery_packs` —
which chapters 9 and 10 put to work.

Piping commands in works too, which is
how this guide's transcripts were made:

```bash
printf '.tables listening\n' | osqueryi
```

## First answers

A question as an argument runs once and
exits — the form every later chapter
uses:

```bash
osqueryi "SELECT * FROM os_version;"
```

```text
+--------+----------------------------+-------+-------+-------+-------+----------+---------------+----------+--------+
| name   | version                    | major | minor | patch | build | platform | platform_like | codename | arch   |
+--------+----------------------------+-------+-------+-------+-------+----------+---------------+----------+--------+
| Ubuntu | 24.04.5 LTS (Noble Numbat) | 24    | 4     | 0     |       | ubuntu   | debian        | noble    | x86_64 |
+--------+----------------------------+-------+-------+-------+-------+----------+---------------+----------+--------+
```

One row: the machine, introducing
itself. `SELECT * FROM uptime;` gives
the five-column answer from chapter 1
(51 minutes when the lab asked). The
machine's hardware papers take one more
question — and a first lesson in asking
for the columns you want instead of
`*`, because `system_info` has more
columns than a screen enjoys:

```bash
osqueryi "SELECT hostname, cpu_brand, physical_memory, hardware_vendor, hardware_model FROM system_info;"
```

Physical memory arrives as raw bytes
(8,319,901,696 on the lab machine —
divide by 1,073,741,824 for gibibytes).
osquery reports facts in the units the
system keeps them; arithmetic is your
SQL's job, and chapter 7 does some.

## Meeting an error properly

Ask for a column that does not exist
and osquery answers like a database:

```bash
osqueryi "SELECT version, build_platform, platform FROM osquery_info;"
```

```text
Error: no such column: platform
```

Exit code 1, one line, no table. The
repair is the shell's second dot
command — `.schema` prints a table's
definition in full:

```text
osquery> .schema osquery_info
CREATE TABLE osquery_info(`pid` INTEGER, `uuid` TEXT ...,
`version` TEXT ..., `build_platform` TEXT, `build_distro` TEXT, ...);
```

With the real column names in hand the
corrected question works:

```bash
osqueryi "SELECT version, build_platform, build_distro FROM osquery_info;"
# 5.24.0 | linux | centos7
```

(The lab's binary was built on a
CentOS 7 lineage — `build_distro` is
about the binary's birthplace, not your
machine.) Both the mistake and the
repair are kept in transcript
`t02-system-identity.txt`: the workflow
*error → schema → corrected query* is
the single most useful rhythm in this
guide, and chapter 7 builds on it.
**The check for this chapter:** the
three identity questions run on your
machine and the rows describe the
machine you are sitting at. If a column
name fails, you already own the fix.
