# Glossary

**Config check** — osquery's proof-read
of its own configuration:
`osqueryctl config-check` or `osqueryd
--config_check`. Silence and exit 0
mean the configuration parses and its
packs load.

**Configuration** — the daemon's one
JSON file, conventionally
`/etc/osquery/osquery.conf`: options, a
schedule, and the list of packs.

**Differential logging** — the
daemon's habit of writing a scheduled
question's answer to the results log
only when it changes: new rows as
`added`, departed rows as `removed`.
An unchanged answer writes nothing.

**Event table** — a table of things
that *happened* (process starts, file
changes), fed by a publisher inside
the daemon. Empty unless the daemon
runs with that publisher enabled.

**Extension** — extra tables (or config
and logger backends) bolted onto
osquery as separate programs speaking
to it over a socket. How the shelf
grows beyond the 164 tables a build
ships.

**Host identifier** — the name the
daemon stamps on every results-log
line as `hostIdentifier`; configurable,
the lab used the hostname.

**Interval** — the seconds beside a
scheduled question: how often the
daemon asks it. Pack and schedule
questions alike carry one.

**osqueryctl** — the package's service
helper: start, stop, status, and
`config-check` for the daemon.

**osqueryd** — the daemon: osquery's
engine with a timetable, asking the
configuration's questions forever and
logging the answers.

**osqueryi** — the interactive shell:
a prompt, dot commands (`.tables`,
`.schema`, `.mode`), and answers drawn
as tables. Also runs one question from
the command line and exits.

**Pack** — a JSON file of related
scheduled questions with a theme, a
platform, and intervals: incident
response, compliance, this guide's
three-question lab pack. Questions
from a pack join the schedule as
`pack_<pack>_<question>`.

**Publisher** — the daemon component
that feeds event tables (audit,
inotify, syslog). Disabled publishers
mean empty event tables.

**Results log** — the daemon's diary,
`osqueryd.results.log`: one JSON
object per line — question name,
machine, time, columns, action.

**RocksDB** — the embedded database
(`osquery.db`) where the daemon keeps
its working state, including the
previous answers differential logging
compares against.

**Schedule** — the configuration's list
of named questions and their
intervals, inspectable any time as the
`osquery_schedule` table — including
each question's execution count.

**Snapshot question** — a scheduled
question whose whole answer is logged
each time as one record, instead of
row-by-row differences. The pack
default.

**State table** — a table of what is
true now — processes, ports, packages —
gathered live at the moment the query
runs.

**Table** — osquery's unit of sight: a
named view of one kind of system fact,
with named columns, queried in SQL.
164 of them on this guide's Linux
build.

**Virtual table** — how the tables are
built: SQLite tables whose rows are not
stored anywhere but gathered from the
system on demand, each time they are
queried.

**Watchdog** — the daemon's supervisor
process, which watches the worker and
restarts it if it hangs. Dismissed
with `--disable_watchdog` when one
visible process serves better — an
experiment, a container.
