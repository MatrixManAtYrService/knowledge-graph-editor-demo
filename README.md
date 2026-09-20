# knowledge-graph-editor demo: the xz backdoor

The [xz-utils backdoor](https://en.wikipedia.org/wiki/XZ_Utils_backdoor)
(CVE-2024-3094) as a
[knowledge-graph-editor](https://github.com/MatrixManAtYrService/knowledge-graph-editor)
graph: "Jia Tan" earned maintainer trust on xz over about two years, apparent
sockpuppets pressured Lasse Collin on the mailing list, the backdoor shipped
in 5.6.0 and 5.6.1, and Andres Freund noticed sshd taking 500ms too long.

This repo holds only the *data* (`graph/` — JSON files, committed like code);
the editor itself is pulled straight from GitHub as a Python dependency.

## Run it

```bash
uv run kge serve
# open http://localhost:8151
```

That's the whole setup: [uv](https://docs.astral.sh/uv/) resolves the `kge`
dependency from GitHub (Python 3.12+ required), and the browser UI ships
inside the package. Don't have uv? `nix develop` provides it. Agents read and
edit the same graph via the CLI; run `uv run kge onboarding` for the
collaboration model.

## Why this story?

Because it's made of *timelines* — which is exactly what kge's **skewer**
feature renders. Each venue gets a rail, an ordered sequence its nodes stay
aligned on. Every rail declares `orderKey: date`, so the sidebar's
**skewers** section treats them as one bundle: check **align** to keep the
rails as parallel lanes, **apply shared order** to interleave events across
all rails evenly (who did what in what order, without the dead time), or
**apply proportional order** to place them by date on one shared scale with
a date axis (the attacker's two-year patience shows up as literal empty
rail):

- **xz repo (curated)** — the story-bearing commits, in order.
- **xz releases** — watch the tagger change hands at v5.4.2, and which two
  releases are backdoored.
- **xz-devel mailing list** — from Jia Tan's first hello to Collin conceding
  co-maintainership: the social-engineering campaign, in order.
- **xz-java, oss-fuzz, libarchive, systemd** — the supporting venues: the
  pre-xz contribution history, the fuzzer blindfolds, the dependency cleanup
  that forced the attacker's clock.
- **the endgame** — Feb–Mar 2024: distro bugs, near-misses, disclosure.

People are deliberately *not* nodes: each item carries `data.actor`, and the
schema **binds node color** to it — so Jia Tan's commits, PRs, posts,
and bug reports wear the same red on every rail at once, the sockpuppets
their own warm shades, and the release rail visibly changes color when the
tagger's hand changes at v5.4.2. That color spread *is* the story; edges
stay reserved for structure (which PR landed as which commit, which bug
concerns which release, who shipped what). Things to try: **apply shared
order** on the date bundle and read the interleaved campaign; **apply
proportional order** and watch the gaps appear; select a commit and read
its `caption` in the inspector; the sidebar's color legend names the cast.

## Data provenance

Everything was curated from primary sources following
[Russ Cox's timeline](https://research.swtch.com/xz-timeline), which links
nearly every commit, email, and bug by URL:

- **Commits and tags**: git clones of
  [tukaani-project/xz](https://github.com/tukaani-project/xz),
  [xz-java](https://git.tukaani.org/xz-java.git), plus the GitHub API for
  [google/oss-fuzz](https://github.com/google/oss-fuzz),
  [libarchive](https://github.com/libarchive/libarchive), and
  [systemd](https://github.com/systemd/systemd). Author and committer are
  recorded separately in each commit's data — on the Landlock-typo commit
  Jia Tan is the author and Lasse Collin the committer, and that difference
  is part of the story (`data.actor`, which drives the color, follows the
  author).
- **PRs and distro bugs**: GitHub REST API, Debian/Ubuntu/Gentoo/Red Hat
  trackers (each node carries its URL).
- **Mailing list**: the [xz-devel archive](https://www.mail-archive.com/xz-devel@tukaani.org/).
  Posts are **linked and summarized in our own words, never copied**.

The full window (2021-10 → 2024-04) contains 1,115 first-parent xz commits
(445 authored by Jia Tan); routine commits are folded into counts on the
rails, so only story-bearing items are nodes. `build_graph.py` regenerates
`graph/` from the curated tables embedded in it — no network needed.

### Licensing and privacy

Commit hashes, dates, names, subjects, and links are facts about public
repositories; no xz source code or message text is redistributed. Email
addresses are omitted throughout. "Jia Tan", "Jigar Kumar", "Dennis Ens",
and "Hans Jansen" are recorded as the personas they are, with no speculation
about who operated them.

## Make it yours

Delete `graph/`, run `kge serve` again (it seeds an empty graph), and add
your own types and nodes. Commit `graph/` like any other source.
