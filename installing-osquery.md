# Installing osquery

**Outcome: `osqueryi` and `osqueryd` on
your machine, both able to state their
version, from the project's own
package.** osquery is distributed by the
osquery project itself — the download
page at osquery.io points at the
project's package hosts, and the same
release is published on the project's
GitHub releases page.

## The package

The lab installed **osquery 5.24.0**,
the `.deb` for 64-bit Ubuntu/Debian
systems:

```bash
curl -LO https://pkg.osquery.io/deb/osquery_5.24.0-1.linux_amd64.deb
sha256sum osquery_5.24.0-1.linux_amd64.deb
sudo dpkg -i osquery_5.24.0-1.linux_amd64.deb
```

The lab's download measured 11,200,014
bytes with SHA-256
`8ae0416d85336a1aea6883920ae9c2751a98538fe0bb624822e92934d3be5592`
(transcript
`osquery-lab/transcripts/t00-install-and-version.txt`).
Yours will differ the day a newer
release ships; the shape of the name —
`osquery_<version>-1.linux_amd64.deb` —
is the constant, and checking the sum
against the release's published sums is
the habit that makes the check worth
doing. There is also an apt repository
on the same host for machines that
should follow osquery updates with
their ordinary package updates; the lab
used the single `.deb`, which is the
form this guide's commands assume.

One install-time trap the lab met for
real: if another package operation is
running — an unattended upgrade, a
colleague's `apt-get` — `dpkg` refuses
with *"dpkg frontend lock was locked
by another process"*. The lock is doing
its job. Wait for the other operation
to finish and run the install again;
the error message itself warns against
the tempting alternative of deleting
lock files.

## What the package puts where

```text
/usr/bin/osqueryi     the interactive shell
/usr/bin/osqueryd     the daemon
/usr/bin/osqueryctl   the service helper
/opt/osquery/         the programs' shared files,
                      including share/osquery/packs/
/etc/osquery/         where your osquery.conf and
                      your own packs will live
```

The daemon is **not** started by the
install. The package registers a service
unit and leaves it disabled; chapter 10
shows the status command reporting
`inactive (dead)`, which is the correct
state for a tool this powerful until
you have decided what it should ask.

## The check

```bash
osqueryi --version
osqueryd --version
```

```text
osqueryi version 5.24.0
osqueryd version 5.24.0
```

That is the whole acceptance test for
this chapter. `dpkg -l osquery` should
agree (`ii  osquery  5.24.0-1.linux`).
Everything after this chapter assumes
the two binaries on the path and an
`/etc/osquery/` directory ready to
receive a configuration; the shell
needs no configuration at all, which is
where the next chapter starts.
