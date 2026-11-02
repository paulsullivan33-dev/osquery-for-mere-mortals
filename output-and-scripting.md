# Output and Scripting

**Outcome: the same question can come
back as a box-drawn table for your eyes,
as JSON for a program, or as one field
per line — and you can hand osqueryi's
answers to a script without scraping a
single box-drawing character.**

## The modes

Everything so far used the default
**pretty** mode: boxes, headers, aligned
columns. It is a reading format, not a
data format. The shell's `.mode` command
and matching command-line flags switch
it:

```bash
printf '.mode line\nSELECT name, version FROM os_version;\n' | osqueryi
```

```text
   name = Ubuntu
version = 24.04.5 LTS (Noble Numbat)
```

**Line mode** prints one field per line
— the readable answer for wide rows like
`system_info`, where pretty mode wraps
itself off the screen.

```bash
osqueryi --csv "SELECT port, protocol FROM listening_ports WHERE port > 0 GROUP BY port, protocol ORDER BY port LIMIT 5;"
```

```text
port|protocol
1901|17
32400|6
```

Note the separator: osquery's "csv" is
separated by **pipes**, not commas —
despite the flag's name. Any parser you
point at it needs the `|` told to it.

## JSON: the scripting contract

```bash
osqueryi --json "SELECT name, version, codename FROM os_version;"
```

```json
[
  {"codename":"noble","name":"Ubuntu","version":"24.04.5 LTS (Noble Numbat)"}
]
```

A JSON array of objects, keys in
alphabetical order, **every value a
string** — port numbers, counts and
byte sizes all arrive as text, and your
script converts the ones it means to do
arithmetic on. Exit codes stay honest in
every mode: a failed question exits 1
with its one-line `Error:` on stderr,
so a script can trust `$?` the way
chapter 4's reader learned to.

## A script on the end of the pipe

The lab's counting script
(`osquery-lab/count-ports.py`, kept in
the repository) reads that JSON on
standard input and counts distinct
ports:

```bash
osqueryi --json "SELECT port FROM listening_ports WHERE port > 0;" \
  | python3 osquery-lab/count-ports.py
```

```text
17 distinct ports across 34 rows
```

Thirty-four rows, seventeen ports: the
doubling chapter 6 met, now measured by
a program instead of eyeballed — and
the count had *grown by one* since the
earlier chapter (a program on the
shared machine opened a new listener
between the two runs), which is the
whole argument for scripting these
questions instead of asking them by
hand once. A hand-asked question is a
photograph; the same question in a
script is a measuring instrument you
can point at the machine every day and
diff. Chapter 10's daemon is that idea
with the scheduling built in — but
plenty of real work stops here, with a
shell script, a cron line, and a JSON
file per day.

**The check for this chapter:** pipe
any question from chapters 5 or 6
through `--json` into a file, load the
file with your language of choice, and
print one row. If the row prints, you
own the bridge between osquery and
every other tool you have.
