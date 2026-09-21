# knowledge-graph-editor demo

Two graphs for
[knowledge-graph-editor](https://github.com/MatrixManAtYrService/knowledge-graph-editor),
picked from the toolbar's graph picker (each graph keeps its own views):

- **xz-backdoor** — the [xz-utils backdoor](https://en.wikipedia.org/wiki/XZ_Utils_backdoor)
  (CVE-2024-3094): "Jia Tan" earned maintainer trust on xz over about two
  years, apparent sockpuppets pressured Lasse Collin on the mailing list, the
  backdoor shipped in 5.6.0 and 5.6.1, and Andres Freund noticed sshd taking
  500ms too long.
- **first-ascents** — the fourteen 8000-meter peaks, 1950–1964: two
  interleaving date timelines (Himalaya vs Karakoram) and a by-elevation
  skewer cutting across both.

This repo holds only the *data* (`graphs/<id>/` — JSON files, committed like
code); the editor itself is pulled straight from GitHub as a Python
dependency.

## Run it

```bash
uv run kge serve
# open http://localhost:8151
```

That's the whole setup: [uv](https://docs.astral.sh/uv/) resolves the `kge`
dependency from GitHub (Python 3.12+ required), and the browser UI ships
inside the package. `kge serve` finds every graph under `graphs/`. Don't have
uv? `nix develop` provides it. Agents read and edit the same graphs via the
CLI (`--graph xz-backdoor` / `--graph first-ascents`); run
`uv run kge onboarding` for the collaboration model.

## Graph 1: the xz backdoor

### Why this story?

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

### Data provenance

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
rails, so only story-bearing items are nodes. `build_xz.py` regenerates
`graphs/xz-backdoor/` from the curated tables embedded in it — no network
needed.

#### Licensing and privacy

Commit hashes, dates, names, subjects, and links are facts about public
repositories; no xz source code or message text is redistributed. Email
addresses are omitted throughout. "Jia Tan", "Jigar Kumar", "Dennis Ens",
and "Hans Jansen" are recorded as the personas they are, with no speculation
about who operated them.

## Graph 2: first ascents of the 8000ers

The fourteen peaks above 8000 meters were all first climbed in one
fifteen-year window — by people who were born, who tried and failed, who
tried and died, and who occasionally collected two. The graph splits that
into **what happened** (dated events) and **who and where** (free-floating
climbers, skewered peaks):

- **mountains** — one rail per nation credited with a first ascent (the
  summit party's flag; captions carry the nuance), ordered by
  `orderKey: elevation`. Austria's four-peak run sits beside single-peak
  rails like Italy's K2, and each *skewer node* carries `data.nation`
  itself, so the rail — bulb, arrowhead, and all — wears its country's
  legend color. **Apply proportional order** and the bundle's axis becomes
  an altimeter: a cluster at 8000–8200 m, then daylight up to Everest.
- **timeline** — a single rail of *event* nodes ordered by
  `orderKey: date`, from Mummery's birth in 1855 to Chogolisa's belated
  first ascent in 1975. Climbers float free, tied to their dates by typed
  edges — `born`, `attempt`, `ascent`, `first-ascent`, and the grim
  `died-ascending` — and each event, where relevant, points `on` its
  mountain. Ordinary deaths stay off the timeline (the date sits in the
  climber's data); dying on one of these mountains earns a `†` node. One
  date can carry several stories: 1957-06-27 on Chogolisa is Buhl's
  `died-ascending` and Diemberger's `attempt` in a single node.

Every peak has its first ascenders in the graph, and several of them
attempted each other's mountains first: Tenzing high on Everest a year
before his summit, Hillary failing on Cho Oyu, the French giving up on
Dhaulagiri before walking over to Annapurna, Schoening surviving the K2
retreat that killed Gilkey and then bagging Gasherbrum I. Node color binds
to `data.nation` on climbers, peaks, and events alike, so the timeline
reads as a national relay — and proportional order stretches it into a
century-and-a-quarter with the 1950s crammed in the middle.

`build_ascents.py` regenerates `graphs/first-ascents/` from tables embedded
in it; every node links its Wikipedia article.

## Make it yours

`uv run kge add-graph my-graph` (or the UI's **New graph** button) seeds an
empty graph next to these two — or delete `graphs/` entirely and run
`kge serve` again for a blank slate. Add your own types and nodes; commit
`graphs/` like any other source.
