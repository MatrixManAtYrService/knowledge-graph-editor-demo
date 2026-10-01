# knowledge-graph-editor demo

Two example graphs for
[knowledge-graph-editor](https://github.com/MatrixManAtYrService/knowledge-graph-editor)
(kge):

- **xz-backdoor**: how "Jia Tan" spent two years earning maintainer trust on
  xz-utils, shipped a backdoor in 5.6.0, and was caught because sshd got
  500ms slower ([CVE-2024-3094](https://en.wikipedia.org/wiki/XZ_Utils_backdoor)).
- **first-ascents**: the first ascents of all fourteen 8000-meter peaks,
  which happened between 1950 and 1964.

## Run it

```bash
uv run kge serve        # then open http://localhost:8151
```

Use the toolbar to switch between graphs. Each graph has its own saved views.
This repo holds only the data in `graphs/`. kge comes from GitHub as a Python
dependency. If you don't have uv, `nix develop` provides it.

## Published copy

`docs/` holds a read-only export of both graphs. To host it, point GitHub Pages at
the `docs/` folder on `main`.
Visitors can focus, filter, and click around, and the URL follows along, so
they can share a link to exactly what they're looking at. direnv sets
`KGE_SITE_DIR=docs`, so every Save in the editor refreshes `docs/`. Commit it
along with `graphs/`. To rebuild the export by hand, run
`uv run kge export --out docs`.

## The xz backdoor

The xz story is a set of parallel timelines, and kge draws each one as a
**skewer**: a rail whose nodes stay in order along it.

- **xz repo**: the commits that matter to the story.
- **xz releases**: the tagger changes at v5.4.2, and two releases are
  backdoored.
- **xz-devel mailing list**: the pressure campaign, from Jia Tan's first post
  to Lasse Collin agreeing to share maintainership.
- **xz-java, oss-fuzz, libarchive, systemd**: earlier contributions in other
  projects, the fuzzer changes that hid the backdoor from testing, and the
  dependency cleanup that put the attacker on a deadline.
- **the endgame**: February and March 2024, with distro bugs, near-misses,
  and disclosure.

Every rail is ordered by date, so the sidebar's **skewers** section treats
them as one bundle. **Apply shared order** interleaves the events into a
single sequence. **Apply proportional order** places them on a real date
scale, where the attacker's patience shows up as long stretches of empty
rail.

People aren't nodes in this graph. Each item records its `actor` instead, and
node color follows that field. Jia Tan's commits, posts, and bug reports are
red on every rail, the sockpuppets get their own colors, and you can see the
release rail change color when Jia Tan takes over tagging. The color legend
in the sidebar shows who is who. Click any item to read its caption.

### Sources

The curation follows [Russ Cox's timeline](https://research.swtch.com/xz-timeline),
which links nearly every commit, email, and bug:

- **Commits and tags** come from clones of
  [xz](https://github.com/tukaani-project/xz) and
  [xz-java](https://git.tukaani.org/xz-java.git), and from the GitHub API for
  [oss-fuzz](https://github.com/google/oss-fuzz),
  [libarchive](https://github.com/libarchive/libarchive), and
  [systemd](https://github.com/systemd/systemd). Author and committer are
  stored separately because the difference matters to the story.
- **PRs and distro bugs** come from GitHub and from the Debian, Ubuntu,
  Gentoo, and Red Hat trackers. Each node links to its source.
- **Mailing list posts** come from the
  [xz-devel archive](https://www.mail-archive.com/xz-devel@tukaani.org/).
  The graph links and summarizes them and never copies their text.

The window from October 2021 to April 2024 has 1,115 xz commits. Only the
ones that matter to the story are nodes, and the rest are counted on the
rails. `build_xz.py` regenerates the graph from data embedded in the script.

The graph contains no xz source code and no message text, and it leaves out
email addresses. "Jia Tan", "Jigar Kumar", "Dennis Ens", and "Hans Jansen"
appear as personas, with no guess at who was behind them.

## First ascents of the 8000ers

- **mountains**: one rail per nation credited with a first ascent, with its
  peaks ordered by elevation. Each rail takes its nation's color. Apply
  proportional order and the axis becomes an altimeter: most peaks sit
  between 8000 and 8200 m, and Everest stands well above the rest.
- **timeline**: one rail of dated events, from Mummery's birth in 1855 to
  Chogolisa's first ascent in 1975. Climbers sit off the rail and connect to
  events with `born`, `attempt`, `ascent`, `first-ascent`, and
  `died-ascending` edges.

Color follows nationality, so the timeline reads like a relay between
nations. Look for climbers who tried each other's mountains first: Tenzing on
Everest the year before his summit, Hillary turning back on Cho Oyu, and
Schoening surviving the K2 retreat before climbing Gasherbrum I.

`build_ascents.py` regenerates this graph, and every node links to its
Wikipedia article.

## Make your own

`uv run kge add-graph my-graph`, or the **+** next to the graph picker, adds an
empty graph alongside these two. To start from nothing, delete `graphs/` and
run `kge serve` again.
