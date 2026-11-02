# Query Packs

**Outcome: you understand what a query
pack is, you can read the packs the
package already ships, and this guide's
own small pack is written, validated
and registered with a configuration —
ready for the daemon in the next
chapter.**

## What a pack is

A **pack** is a JSON file containing
named questions that belong together,
each with the SQL, an interval in
seconds, and (when the author was kind)
a description of what the question is
for. Packs are how osquery knowledge
travels: instead of every administrator
inventing "how would I even ask about
that?", the project and its community
publish bundles — ask these, this
often, and you will notice this class
of thing.

The package installs its shelf at
`/opt/osquery/share/osquery/packs/`
(chapter 3's transcript lists it):
`incident-response.conf`,
`it-compliance.conf`,
`hardware-monitoring.conf`,
`vuln-management.conf`,
`osquery-monitoring.conf` (osquery
watching itself), `ossec-rootkit.conf`,
and platform packs like
`windows-attacks.conf` and
`osx-attacks.conf` that a Linux machine
will politely never run. Opening one
and reading the SQL is the best osquery
education there is — every query in
them is a worked example against real
tables, and most of the tables in
chapter 4's list earn their keep in
somebody's pack.

## The lab's pack

Three questions, deliberately small —
the OS identity (does this machine
still think it is what we installed?),
the TCP listeners (chapter 6's
question, on a timer), and the five
largest processes. The full file is
`osquery-lab/lab-pack.json`:

```json
{
  "platform": "linux",
  "version": "1.0.0",
  "queries": {
    "os_version": {
      "query": "SELECT name, version, codename, arch FROM os_version",
      "interval": 20,
      "description": "The operating system's identity, checked by the lab pack."
    },
    "tcp_listeners": {
      "query": "SELECT DISTINCT port, address FROM listening_ports WHERE protocol = 6 AND port > 0 ORDER BY port",
      "interval": 20,
      "description": "TCP listening ports, deduplicated."
    },
    "top_processes": {
      "query": "SELECT pid, name, resident_size FROM processes ORDER BY resident_size DESC LIMIT 5",
      "interval": 20,
      "description": "The five largest processes by resident memory."
    }
  }
}
```

Three conventions to copy. Scheduled
questions are written **without a
trailing semicolon** — the schedule is
not the shell. Each carries an
`interval`, and pack intervals are
floors with manners: osquery spreads
executions out rather than firing every
question on the same second. And
`"platform": "linux"` at the top keeps
the pack off machines it does not
describe.

## Registering it — and proving it

A pack does nothing until a
**configuration** names it. The lab's
configuration (`osquery-lab/osquery.conf`,
installed to `/etc/osquery/osquery.conf`
with the pack beside it in
`/etc/osquery/packs/`) also carries two
questions of its own in a `schedule`
section; its packs entry is one line:

```json
"packs": {
  "lab": "/etc/osquery/packs/lab-pack.json"
}
```

Proof comes before any daemon runs.
osquery checks its own homework two
ways, and the lab ran both (transcript
`osquery-lab/transcripts/t09-query-packs.txt`):

```bash
osqueryd --config_check --config_path=/etc/osquery/osquery.conf
echo $?   # 0
osqueryctl config-check   # also silent, also success
```

Then the shell, told to load the same
configuration, shows the merged result:

```bash
osqueryi --config_path=/etc/osquery/osquery.conf \
  "SELECT name, interval, executions FROM osquery_schedule ORDER BY name;"
```

```text
| lab_uptime             | 15 | 0 |
| lab_user_count         | 15 | 0 |
| pack_lab_os_version    | 20 | 0 |
| pack_lab_tcp_listeners | 20 | 0 |
| pack_lab_top_processes | 20 | 0 |
```

The pack's questions arrived wearing
the prefix `pack_lab_` — pack name
between, so a results log always says
whose question it was. `osquery_packs`
likewise lists two packs: `lab`, and
`main` — the configuration's own
schedule counts as a pack named main.
Executions are 0 across the board: the
schedule exists, nothing has run it
yet. That is the next chapter's job.

**The check for this chapter:** your
own config passes `osqueryctl
config-check`, and `osquery_schedule`
shows your pack's questions with the
prefix you expected. Do not skip the
check to save a minute — chapter 14
shows what the daemon does with a
config it cannot parse, and it is
better met here, on purpose.
