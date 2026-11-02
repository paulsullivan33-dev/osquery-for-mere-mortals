# Writing criteria for this guide

Every "for Mere Mortals" guide is written to the same nine-point
standard, so a reader who trusts one can trust the rest. Here it
is, with the verification notes for this particular guide below.

1. **Fix it first.** Reader outcomes lead, not action items: each
   chapter opens by naming the outcome it delivers, shows a check
   the reader can run to confirm they got it, and a reasonable
   reader finishes able to state what was done, what it means,
   and what to try next.
2. **Plain language.** Short sentences, everyday vocabulary,
   technical terms defined on first use. No slang, and no
   idioms that only make sense in one country — the reader may
   be translating as they go.
3. **No dead ends.** A guide never tells the reader to do
   something it cannot show them how to verify. Every claim a
   reader relies on — an install, a command, an output — is
   something this guide demonstrates or clearly labels
   documented-only below.
4. **Live-verified where it matters.** Procedures are run for
   real in the guide's lab wherever the build machine allows it,
   and the transcripts kept in the repository are the evidence.
   What could not be run is listed honestly below, never
   presented as if it had been.
5. **General audiences.** Nothing in this guide — examples,
   fixtures, names, addresses — is modelled on any particular
   reader or author's real life, network, or organisations.
   The lab's queries ran against its own sandbox machine and
   report that machine's generic system facts.
6. **Standalone.** A reader needs this guide, its lab, and
   nothing else. Where another guide would genuinely help, it
   is pointed to once, by name, and the chapter still completes
   without it.
7. **Honest about limits.** Chapter 13 names what the tool
   cannot do: answers are point-in-time snapshots that race
   (the lab counted 32 processes, then 33), osquery reads and
   never writes, protected tables answer empty instead of
   refusing (the shadow count is 41 as root, 0 as nobody, both
   exit 0), sockets can be visible but unattributable
   (pid −1), process names truncate at fifteen characters,
   the results log stays silent when nothing changed, state
   tables are not history, and the table shelf is
   platform-shaped — 164 tables here, a different shelf
   elsewhere.
8. **The ethics rule is in the text, early.** osquery sees
   deeply — every process's command line, every logged-in
   user, file hashes, protected tables when run as root — so
   chapter 1 and the README state the line before any
   procedure depends on it: run osquery only on machines you
   own or are authorised to inventory, treat results logs as
   sensitive maps of a machine, and recognise that a question
   scheduled about other people's activity is surveillance,
   to be disclosed and governed as such.
9. **Builds clean.** The site builds with MkDocs in strict mode
   with no warnings, and a fresh reader following the chapters
   in order reaches the stated outcome of each.

## Verification notes for this guide

The build machine is a 2-CPU, 7.7 GB Ubuntu 24.04 sandbox,
shared with other work while the lab ran (process and port
listings therefore include other tenants' ordinary programs —
generic names and numbers only, no personal data; counts in
the text are the counts the lab saw and are labelled as the
lab's). osquery **5.24.0** was installed from the project's
official package `osquery_5.24.0-1.linux_amd64.deb`
(11,200,014 bytes, SHA-256
`8ae0416d85336a1aea6883920ae9c2751a98538fe0bb624822e92934d3be5592`)
downloaded from the project's own package host,
pkg.osquery.io, and installed unmodified with `dpkg -i`. All
transcripts live in `osquery-lab/transcripts/`; the guide's
pack is `osquery-lab/lab-pack.json`, its daemon configuration
is `osquery-lab/osquery.conf`, a captured results log is
`osquery-lab/sample-results.log`, and its counting script is
`osquery-lab/count-ports.py`.

Run for real, with transcripts as evidence:

- Install and identity: the `.deb` install (after one refusal
  while another package operation held the dpkg lock —
  recorded in chapter 3), `osqueryi --version` and
  `osqueryd --version` both reporting 5.24.0, the shipped
  packs listed (t00).
- The shell's shelf: `.tables` in full — 164 tables counted —
  and the prefix filter's behaviour, including `.tables port`
  matching the portage tables instead of `listening_ports`,
  and `.tables listening` and `.tables osquery` (t01).
- Identity questions: `os_version`, `uptime`, a chosen-column
  `system_info`, and the `osquery_info` error → `.schema` →
  corrected-query sequence, kept whole (t02).
- Accounts: 41 rows in `users`; the uid-filtered list (root
  and nobody, the sandbox having no human accounts);
  `logged_in_users` showing only the boot record (t03).
- Processes: a live count (32, then 33 in a `GROUP BY uid` a
  minute later — the race is reported, not smoothed), the
  top-ten by resident memory with fifteen-character name
  truncation visible, and `path`/`cmdline` for pid 1 (t04).
- Listening ports: 354 rows in total, 294 with `pid = -1`,
  32 with real ports collapsing under `DISTINCT` to 16
  listeners, and the join to `processes` naming the owner of
  every one (t05).
- Packages and files: 2,078 rows in `deb_packages`, osquery's
  own row, 331 packages with empty `source`, and the
  `md5`/`sha1`/`sha256` of `/usr/bin/osqueryi` from the
  `hash` table (t06, t07).
- Shaping: the full `.schema` of `processes` and of `time`,
  a processes⋈users join, the `local_time` error and its
  correction (t07).
- Output: `--json`, `--csv` (pipe-separated, as osquery
  emits it), `.mode line`, JSON piped into the lab's own
  counting script (17 distinct ports across 34 rows), and
  the JSON morning-inventory recipe producing its file
  (t08).
- Packs and config: the lab pack and configuration written,
  installed to `/etc/osquery/`, and validated both by
  `osqueryd --config_check` (exit 0) and
  `osqueryctl config-check`; the merged schedule read back
  through `osquery_schedule` — two config questions plus the
  pack's three under `pack_lab_` names — and `osquery_packs`
  listing `main` and `lab` (t09).
- The daemon: osqueryd 5.24.0 run by hand (detached with
  `setsid`, watchdog disabled, database and logs in the
  lab's scratch space) for about ninety seconds against that
  configuration. The results log gathered 57 lines; the
  daemon's own database afterwards reported executions of
  6, 6, 4, 4, 4 across the five questions — matching the
  15/20-second intervals — and the line counts per question
  (11, 1, 1, 9, 35) demonstrate the differential arithmetic
  chapter 10 teaches. The daemon was stopped with `kill` and
  removed its own pidfile (t10, `sample-results.log`).
- Failures: `no such table` and a syntax error (both
  one-line `Error:`s, exit 1); `.schema` of a nonexistent
  table printing nothing and exiting 0; a JSON-broken config
  refused by `--config_check` with the parse error and exit
  1; `osqueryctl status` reporting the unit
  `inactive (dead)`; and the `shadow` count as root (41)
  versus as the user `nobody` (0, exit 0) (t11).

Documented only — described from the project's documentation,
not run, and the text does not claim otherwise:

- Running osqueryd as a managed service: the package's unit
  is present and verified *disabled*; starting it
  (`osqueryctl start`, systemd) was deliberately not done in
  this sandbox, which has no service manager doing the
  honours for the lab. The daemon chapter runs osqueryd
  directly instead, and says so.
- Fleets: TLS enrolment to a central server, remote
  configuration, log streaming, and the Fleet/Kolide
  managers of chapter 11 — characterised, not run.
- The event tables and their publishers: the lab daemon's
  startup log records the audit, inotify and syslog
  publishers as "disabled via configuration", and no event
  data was gathered or is presented.
- Extensions: the `osquery_extensions` table was listed; no
  extension was written, loaded or run.
- Other platforms: the macOS and Windows table shelves and
  the shipped `osx-attacks` / `windows-*` packs were read as
  files, never executed; queries here are the Linux build's.
- The neighbour tools of chapter 11 (the classic Unix tools,
  auditd, Lynis, Wazuh, Fleet, Kolide) — characterised from
  their documentation, not benchmarked.

Fixtures are this guide's own and deliberately generic: a
three-question pack about OS identity, TCP listeners and
large processes; a two-question schedule about uptime and
user count; and queries pointed at the lab machine itself.
No names, organisations or real events appear; the sandbox's
listings show the ordinary programs any shared machine runs.
