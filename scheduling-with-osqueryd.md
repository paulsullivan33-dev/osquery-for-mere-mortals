# Scheduling with osqueryd

**Outcome: the daemon runs the
configuration from chapter 9, its
results log fills with answers, and you
can explain — from the daemon's own
counters — why some questions fill the
log and one barely appears.**

## The daemon, by hand

On a settled machine, the service unit
starts osqueryd and this chapter's work
is already done for you. The lab's
sandbox has no service manager doing
favours, and the package leaves the
unit disabled anyway, so the lab ran
the daemon **in the open**, flags and
all — which has the side benefit of
showing every moving part a service
file would hide:

```bash
setsid osqueryd \
  --config_path=/etc/osquery/osquery.conf \
  --database_path=osquery-labwork/daemon/osquery.db \
  --logger_path=osquery-labwork/daemon/logs \
  --pidfile=osquery-labwork/daemon/osqueryd.pid \
  --disable_watchdog=true &
```

Each flag is a moving part from
chapter 2 with its sleeve rolled up:
the config to obey, the RocksDB
database where the daemon keeps its
memory of previous answers (the memory
*differential* logging is made of), the
directory the results log goes to, a
pidfile so the experiment can be
stopped politely, and the watchdog
dismissed — normally a second process
supervises the worker and restarts it
if it hangs; for a ninety-second
experiment, one honest process is
easier to watch. `setsid` detaches it
into its own session so it belongs to
the experiment rather than to the
terminal. On your own machine, prefer
the service: `osqueryctl start` (or
your service manager's equivalent) gets
the watchdog and the restarts.

## Ninety seconds of answers

The daemon ran for about ninety
seconds. Its results log —
`osquery-lab/sample-results.log` keeps
the full file — gathered **57 lines**.
Counting them by question, with a
three-line Python summary the lab ran
against the live log (transcript
`osquery-lab/transcripts/t10-osqueryd-schedule.txt`):

```text
lab_uptime: 11
lab_user_count: 1
pack_lab_os_version: 1
pack_lab_tcp_listeners: 9
pack_lab_top_processes: 35
```

And here is one line, whole:

```json
{"name":"lab_uptime","hostIdentifier":"htch-runtime","calendarTime":"Mon Nov  2 15:24:48 2026 UTC","unixTime":1793633088,"epoch":0,"counter":0,"numerics":false,"columns":{"days":"0","hours":"0","minutes":"54","total_seconds":"3275"},"action":"added"}
```

Name, machine, two kinds of time, the
answer as `columns`, and the `action`.
Everything a downstream tool needs to
file the fact — and nothing else; the
log is JSON lines precisely so that
chapter 8's scripting habits apply to
it unchanged.

## Why the counts differ: differential logging

After stopping the daemon
(`kill $(cat osqueryd.pid)` — it removed
its own pidfile on the way out), the
lab asked the daemon's database how
many times each question had actually
*run*:

```text
| lab_uptime             | 6 |
| lab_user_count         | 6 |
| pack_lab_os_version    | 4 |
| pack_lab_tcp_listeners | 4 |
| pack_lab_top_processes | 4 |
```

Six executions at a 15-second interval,
four at 20 — the arithmetic of ninety
seconds, and the proof that the quiet
questions were running all along. The
log counts unpack like this:

- **`lab_user_count` ran 6 times and
  logged once.** The answer (41) never
  changed. The first run writes the
  rows as `added`; identical answers
  after that write nothing. Silence in
  the log means *no change*, not *not
  running* — and the executions counter
  is how you tell the difference.
- **`lab_uptime` ran 6 times and logged
  11 lines.** Its one row changes every
  run, and a changed row is logged as
  the old row `removed` plus the new
  row `added` — one line for the first
  run, two for each change: 1 + 5 × 2.
- **`pack_lab_top_processes` ran 4
  times and logged 35 lines.** Five
  rows, and on a busy machine the top
  five reshuffles constantly — each
  execution writes a handful of removals
  and additions. Chatty questions are
  the ones whose answers churn, not the
  ones asked most often.
- The two snapshot questions
  (`os_version`, and the pack's by
  default) log their whole answer as a
  single `snapshot` or `added` record
  per the pack's settings; here
  `os_version` logged once, its answer
  being the least changeable fact on
  the machine.

The daemon's startup log holds one more
honest line, visible in the same
transcript's artefacts: the **event
publishers were disabled** by this
configuration (`inotify`, `syslog`, the
audit publisher — "Publisher disabled
via configuration"). The state tables
this guide teaches need no publishers.
The event tables do, and enabling them
is configuration this guide describes
but did not perform — see chapter 13.

**The check for this chapter:** your
daemon's results log grows, and for
one deliberately unchanging question
you can prove from `osquery_schedule`
that it ran more times than it logged.
Until you can explain a quiet log, do
not trust one.
