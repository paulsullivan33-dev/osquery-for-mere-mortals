# Limits

What osquery cannot do, stated plainly.
Most of these the lab met directly; the
rest are labelled as documentation.

**Answers are snapshots, and snapshots
race.** A table is gathered at the
moment the query runs. The lab counted
32 processes and, a minute later, 33 —
both answers true, neither wrong. A
process that lives for a millisecond
between two daemon runs is invisible to
both. osquery tells you what is true
*when you ask*, and any conclusion of
the form "this never happens" needs
more than snapshots to stand on.

**It reads; it never writes.** osquery's
SQL has no verbs for changing the
system. It cannot kill the process,
close the port, or remove the package
it just showed you. That is a design
virtue — a question tool that cannot
break anything — and a hard boundary:
remediation is always another tool's
job, taken by a human who read the
answer.

**Empty is an answer with several
meanings.** A table can come back empty
because the fact is absent — or because
you lack the privilege to see it. The
lab ran the same count on `shadow` as
root (41 rows) and as the user `nobody`
(**0 rows, exit 0, no complaint**).
Tables also answer empty when their
data source is off: the event tables
stay empty while their publishers are
disabled. Chapter 14 is the field guide
to telling the meanings apart; the
limit itself stands — osquery will not
always tell you *why* it showed you
nothing.

**Some rows are partially blind.**
`listening_ports` on the lab's shared
sandbox returned 294 rows it could see
but not attribute — `pid = -1`, port 0,
sockets belonging to neighbouring
namespaces. Visibility into other
tenants' sockets is a property of the
environment, and osquery reports the
fact of a socket without inventing an
owner. On an ordinary machine the crowd
thins to nearly nothing, but −1 is a
standing possibility wherever
containers and namespaces share a
kernel.

**Names are cut at fifteen
characters.** Process `name` is the
kernel's `comm` field, fifteen
characters long, and a longer program
name is truncated without ceremony
(`Plex Script Hos`). The full story is
in `path` and `cmdline` — but a query
that matches or groups on `name` alone
is reasoning about abbreviations.

**The log stays silent when nothing
changed.** Differential logging
(chapter 10) means the results log is a
record of changes, not of checks. A
question can run a thousand times and
log once. Any consumer of the log —
human or SIEM — that reads silence as
absence will misunderstand a healthy
daemon; the `osquery_schedule`
executions counter is the ground truth,
and checking it is a habit, not an
option.

**State, not history — unless you build
the history.** The tables this guide
teaches describe now. The event tables
that describe *then* need the daemon,
an enabled publisher (audit, inotify),
and storage for the stream — the lab's
daemon ran with publishers disabled and
this guide does not present event data
it did not gather. Turning osquery into
a historian is documented, supported,
and a project of its own.

**The shelf is platform-shaped.** 164
tables on this Linux build; a different
count, with different names, on macOS
and Windows, and `deb_packages` simply
does not exist where `rpm_packages`
lives. Queries are portable in grammar,
not in vocabulary — a pack written for
one platform is a draft on another,
which is why packs declare their
platform and why chapter 9's does.

**It is a tenant, not a ghost.** The
daemon holds a database, uses memory
like a modest service, and its worker
is deliberately supervised by a
watchdog because table code touches
half the system. On a tiny machine the
footprint is noticeable; the classic
tools of chapter 12 ask nothing of the
machine between questions.

**Depth is not judgement.** osquery
will faithfully report the open port,
the odd process, the unsigned package —
and has no opinion about any of them.
The gap between "facts, promptly" and
"someone should look at this" is
filled by packs written by people, by
Lynis-style auditors, or by you,
reading. The tool's honesty about that
gap is a feature this guide has tried
to copy.
