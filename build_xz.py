"""Build the xz-utils backdoor graph (CVE-2024-3094) for knowledge-graph-editor.

All data is embedded below, hand-curated from git clones of the involved
repositories, the GitHub API, distro bug trackers, and the xz-devel mailing
list archive — following Russ Cox's timeline (https://research.swtch.com/xz-timeline)
as the curation checklist. Routine commits are folded into counts on the
rails; only story-bearing items become nodes.

Privacy: email addresses are omitted throughout. The personas ("Jia Tan",
"Jigar Kumar", "Dennis Ens", "Hans Jansen") are recorded as personas, with
no speculation about who operated them. Mailing-list/bug text is linked and
summarized, never copied.
"""

import json
from pathlib import Path

OUT = Path(__file__).parent / "graphs" / "xz-backdoor"

XZ = "https://git.tukaani.org/?p=xz.git;a=commitdiff;h="
MAIL = "https://www.mail-archive.com/xz-devel@tukaani.org/"

# (id-suffix, repo, hash, author, author_date, committer, commit_date, subject, caption-or-None)
COMMITS = [
    ("xz:6468f7e", "xz", "6468f7e41a8e9c611e4ba8d34e2175c5dacdbeb4", "jiat75", "2022-01-28",
     "Lasse Collin", "2022-02-07", "liblzma: Add NULL checks to LZMA and LZMA2 properties encoders.",
     "First xz commit by the Jia Tan persona — authored under the alias 'jiat75', ten days before Collin merged it."),
    ("xz:0c210ca", "xz", "0c210ca7f489e971e94e1ddc72b0b0806e3c7935", "Lasse Collin", "2023-01-06",
     "Jia Tan", "2023-01-09", "Tests: test_filter_flags: Clean up minor issues.",
     "Jia Tan's first act as committer: Collin's own patch now passes through the attacker's hands. Commit access achieved."),
    ("xz:18b845e", "xz", "18b845e69752c975dfeda418ec00eda22605c2ee", "Lasse Collin", "2023-01-11",
     "Lasse Collin", "2023-01-11", "Bump version and soname for 5.4.1.",
     "Collin's last release before the handoff."),
    ("xz:23b5c36", "xz", "23b5c36fb71904bfbe16bb20f976da38dadf6c3b", "Hans Jansen", "2023-06-22",
     "Lasse Collin", "2023-06-27", "Add ifunc check to configure.ac",
     "The 'Hans Jansen' persona contributes ifunc support — the exact mechanism the backdoor later hooks."),
    ("xz:b72d212", "xz", "b72d21202402a603db6d512fb9271cfa83249639", "Hans Jansen", "2023-06-22",
     "Lasse Collin", "2023-06-27", "Add ifunc check to CMakeLists.txt", None),
    ("xz:233885a", "xz", "233885a437f8b55a5c8442984ebc0aaa579e92de", "Hans Jansen", "2023-10-12",
     "Jia Tan", "2023-10-13", "liblzma: Rename crc_macros.h to crc_common.h.", None),
    ("xz:93e6fb0", "xz", "93e6fb08b22c7c13be2dd1e7274fe78413436254", "Hans Jansen", "2023-10-12",
     "Jia Tan", "2023-10-13", "liblzma: Moved CLMUL CRC logic to crc_common.h.", None),
    ("xz:f1cd9d7", "xz", "f1cd9d7194f005cd66ec03c6635ceae75f90ef17", "Hans Jansen", "2023-10-12",
     "Jia Tan", "2023-10-13", "liblzma: Added crc32_clmul to crc32_fast.c.",
     "One persona authors, the other commits: the CRC changes that stage the backdoor's landing zone."),
    ("xz:cf44e4b", "xz", "cf44e4b7f5dfdbf8c78aef377c10f71e274f63c0", "Jia Tan", "2024-02-23",
     "Jia Tan", "2024-02-23", "Tests: Add a few test files.",
     "The backdoor binary arrives, hidden inside 'test files'."),
    ("xz:a100f91", "xz", "a100f9111c8cc7f5b5f0e4a5e8af3de7161c7975", "Jia Tan", "2024-02-26",
     "Lasse Collin", "2024-02-28", "Build: Fix Linux Landlock feature test in Autotools and CMake builds.",
     "A one-character typo quietly disables the Landlock sandbox check — authored by Jia Tan, unknowingly committed by Collin."),
    ("xz:74b138d", "xz", "74b138d2a6529f2c07729d7c77b1725a8e8b16f1", "Jia Tan", "2024-03-09",
     "Jia Tan", "2024-03-09", "Tests: Update two test files.",
     "The backdoor payload is updated for v5.6.1 — after the Valgrind reports nearly exposed it."),
    ("xz:1107712", "xz", "1107712e372f7593ad729764c0c2644d0e4aa675", "Lasse Collin", "2024-04-08",
     "Lasse Collin", "2024-04-09", "Remove the backdoor found in 5.6.0 and 5.6.1 (CVE-2024-3094).",
     "Collin removes the backdoor and begins reclaiming the project."),
    ("xz-java:52fcb4a", "xz-java", "52fcb4a1b81a6ea0a719414ce93bcdf6fd3e3a43", "Jia Tan", "2022-12-09",
     "Jia Tan", "2022-12-09", "Removes unused imports flagged by text editor.",
     "Jia Tan also commits to XZ for Java — the repo Dennis Ens's pressure was about."),
    ("xz-java:8e46fdf", "xz-java", "8e46fdf903563b75849a37150be1cbf51ba12c53", "Jia Tan", "2022-12-17",
     "Jia Tan", "2022-12-17", "Implements ARM64 filter described in xz spec version 1.1.0.", None),
    ("xz-java:67d9763", "xz-java", "67d976302ace949e2e07ae3077d35cbd4ae3e375", "Jia Tan", "2024-01-19",
     "Jia Tan", "2024-01-19", "Update docs and metadata for new project website.", None),
    ("oss-fuzz:6403e93", "oss-fuzz", "6403e93344476972e908ce17e8244f5c2b957dfd", "Jia Tan", "2023-03-20",
     "Jia Tan", "2023-03-20", "XZ updates (#9960)",
     "Redirects oss-fuzz's xz bug reports to the attacker's own address."),
    ("oss-fuzz:d2e42b2", "oss-fuzz", "d2e42b2e489eac6fe6268e381b7db151f4c892c5", "Jia Tan", "2023-07-07",
     "Jia Tan", "2023-07-07", "xz: Disable ifunc to fix Issue 60259. (#10667)",
     "Disables ifunc in fuzzing builds — keeping the fuzzers away from the hook the backdoor uses."),
    ("systemd:3fc72d5", "systemd", "3fc72d54132151c131301fc7954e0b44cdd3c860", "Matteo Croce", "2024-02-15",
     "GitHub merge", "2024-03-05", "Dynamically load compression libraries",
     "systemd drops its hard liblzma dependency — likely the change that forced the attacker's rushed timetable."),
]

# (version, date, tagged_by, backdoored)
RELEASES = [
    ("5.4.0", "2022-12-13", "Lasse Collin", False),
    ("5.4.1", "2023-01-11", "Lasse Collin", False),
    ("5.4.2", "2023-03-18", "Jia Tan", False),
    ("5.4.3", "2023-05-04", "Jia Tan", False),
    ("5.4.4", "2023-08-02", "Jia Tan", False),
    ("5.4.5", "2023-11-01", "Jia Tan", False),
    ("5.4.6", "2024-01-26", "Jia Tan", False),
    ("5.6.0", "2024-02-24", "Jia Tan", True),
    ("5.6.1", "2024-03-09", "Jia Tan", True),
]

# (id-suffix, repo, number, opened_by(person id-suffix), created, merged, title, caption-or-None)
PRS = [
    ("libarchive:1598", "libarchive", 1598, "jia-tan", "2021-10-19", "2021-11-15",
     "Zip entry size unset now honors user requested compression level",
     "The earliest Jia Tan activity in this dataset — building a contribution history before xz."),
    ("libarchive:1609", "libarchive", 1609, "jia-tan", "2021-11-02", "2021-11-15",
     "Added error text to warning when untaring with bsdtar",
     "Quietly swapped safe_fprintf for fprintf; re-reviewed only after the disclosure."),
    ("libarchive:2101", "libarchive", 2101, "emaste", "2024-03-29", "2024-03-29",
     "tar: make error reporting more robust and use correct errno",
     "Post-disclosure hardening: the community re-audits Jia Tan's old changes within hours."),
    ("systemd:31550", "systemd", 31550, "teknoraver", "2024-02-29", "2024-03-05",
     "Dynamically load compression libraries", None),
]

# (id-suffix, date, sender(person id-suffix), url, gist)
POSTS = [
    ("msg00512", "2021-10-29", "jia-tan", f"{MAIL}msg00512.html",
     "Jia Tan's first appearance on xz-devel: a patch adding .editorconfig."),
    ("msg00557", "2022-04-22", "jigar-kumar", f"{MAIL}msg00557.html",
     "First complaint that Jia's patch isn't landing."),
    ("msg00562", "2022-05-19", "dennis-ens", f"{MAIL}msg00562.html",
     "Asks whether XZ for Java is maintained."),
    ("msg00563", "2022-05-19", "lasse-collin", f"{MAIL}msg00563.html",
     "Collin first hints Jia Tan may take a bigger role."),
    ("msg00565", "2022-05-27", "jigar-kumar", f"{MAIL}msg00565.html",
     "Complains a patch is still unmerged."),
    ("msg00566", "2022-06-07", "jigar-kumar", f"{MAIL}msg00566.html",
     "Says nothing will change until there is a new maintainer."),
    ("msg00567", "2022-06-08", "lasse-collin", f"{MAIL}msg00567.html",
     "Collin pushes back, citing limited capacity and mental health."),
    ("msg00568", "2022-06-14", "jigar-kumar", f"{MAIL}msg00568.html",
     "Says the maintainer is choking his own repo."),
    ("msg00569", "2022-06-21", "dennis-ens", f"{MAIL}msg00569.html",
     "Urges Collin to hand off maintainership."),
    ("msg00570", "2022-06-22", "jigar-kumar", f"{MAIL}msg00570.html",
     "Asks why Jia doesn't commit it himself."),
    ("msg00571", "2022-06-29", "lasse-collin", f"{MAIL}msg00571.html",
     "Collin: Jia Tan is now practically a co-maintainer. The campaign worked."),
    ("oss-security-disclosure", "2024-03-29", "andres-freund",
     "https://www.openwall.com/lists/oss-security/2024/03/29/4",
     "Andres Freund's public disclosure: a 500ms sshd slowdown unravels the whole operation. CVE-2024-3094."),
]

# (id-suffix, date, filed_by(person or None), concerns(release version), url, label, gist)
BUGS = [
    ("gentoo-925415", "2024-02-24", None, "5.6.0", "https://bugs.gentoo.org/925415",
     "Gentoo bug 925415", "Real ifunc crashes in 5.6.0 — genuine bugs orbiting the backdoor."),
    ("debian-accept-5.6.0", "2024-02-26", None, "5.6.0",
     "https://tracker.debian.org/news/1506761/accepted-xz-utils-560-01-source-into-unstable/",
     "Debian accepts 5.6.0-0.1", "The backdoored release enters Debian unstable."),
    ("redhat-2267598", "2024-03-04", None, "5.6.0", "https://bugzilla.redhat.com/show_bug.cgi?id=2267598",
     "Red Hat bug 2267598", "Valgrind errors in liblzma's _get_cpuid — the backdoor's entry point, nearly exposed."),
    ("debian-1067708", "2024-03-25", "hans-jansen", "5.6.1",
     "https://bugs.debian.org/cgi-bin/bugreport.cgi?bug=1067708",
     "Debian bug 1067708", "'Hans Jansen' resurfaces to push Debian to update to 5.6.1."),
    ("ubuntu-2059417", "2024-03-28", "jia-tan", "5.6.1",
     "https://bugs.launchpad.net/ubuntu/+source/xz-utils/+bug/2059417",
     "Ubuntu bug 2059417", "Jia Tan asks Ubuntu to pull 5.6.1 from Debian — the day before disclosure."),
    ("debian-rollback", "2024-03-28", None, "5.6.1",
     "https://tracker.debian.org/news/1515519/accepted-xz-utils-561really545-1-source-into-unstable/",
     "Debian rollback (5.6.1+really5.4.5)", "Debian's response after Freund's private report: roll back."),
]

# People are not nodes: each item carries data.actor and the default view
# binds node color to it, so one person's commits, PRs, posts, and bugs share
# a color across every rail. Edges stay reserved for structural relations
# (MERGED_AS, TAGGED_AT, CONCERNS, SHIPPED).
ACTOR = {  # id-suffix / alias -> canonical display name
    "lasse-collin": "Lasse Collin",
    "jia-tan": "Jia Tan",
    "jiat75": "Jia Tan",  # the alias slip-up; data.author keeps the raw name
    "hans-jansen": "Hans Jansen",
    "jigar-kumar": "Jigar Kumar",
    "dennis-ens": "Dennis Ens",
    "andres-freund": "Andres Freund",
    "emaste": "Ed Maste",
    "teknoraver": "Matteo Croce",
    "Lasse Collin": "Lasse Collin",
    "Jia Tan": "Jia Tan",
    "Hans Jansen": "Hans Jansen",
    "Matteo Croce": "Matteo Croce",
}

# Pinned actor colors for the default view's colorBind: the attacker red, the
# maintainer blue, the discoverer green, the pressure personas warm shades.
ACTOR_COLORS = {
    "Jia Tan": "#e15759",
    "Lasse Collin": "#4e79a7",
    "Hans Jansen": "#f28e2c",
    "Jigar Kumar": "#edc949",
    "Dennis Ens": "#af7aa1",
    "Andres Freund": "#59a14f",
    "Ed Maste": "#76b7b2",
    "Matteo Croce": "#9c755f",
}

DISTROS = [
    ("debian", "Debian", ["5.6.0", "5.6.1"]),
    ("fedora", "Fedora / Red Hat", ["5.6.0"]),
    ("gentoo", "Gentoo", ["5.6.0"]),
]

# Skewers: (id-suffix, label, description, ordered member node ids)
def c(s: str) -> str:
    return f"commit:{s}"

# One rail per venue — repo, mailing list, tracker timeline. People are NOT
# rails: a person's trail is already their edges (select Jia Tan and walk).
SKEWERS = [
    ("xz-repo", "xz repo (curated)",
     "Story-bearing commits from tukaani-project/xz, by commit date. The window 2021-10..2024-04 has 1115 first-parent commits (445 authored by Jia Tan); routine ones are folded away.",
     [c("xz:6468f7e"), c("xz:0c210ca"), c("xz:18b845e"), c("xz:23b5c36"), c("xz:b72d212"),
      c("xz:233885a"), c("xz:93e6fb0"), c("xz:f1cd9d7"), c("xz:cf44e4b"), c("xz:a100f91"),
      c("xz:74b138d"), c("xz:1107712")]),
    ("releases", "xz releases",
     "The release line. Watch the tagger change hands at 5.4.2 — and which two are backdoored.",
     [f"release:{v}" for v, *_ in RELEASES]),
    ("xz-devel", "xz-devel mailing list",
     "From Jia Tan's first hello to Collin conceding co-maintainership: the social-engineering campaign, in order.",
     [f"post:{p[0]}" for p in POSTS[:11]]),
    ("xz-java", "xz-java repo",
     "Jia Tan's commits to XZ for Java — the repo Dennis Ens's pressure was ostensibly about.",
     [c("xz-java:52fcb4a"), c("xz-java:8e46fdf"), c("xz-java:67d9763")]),
    ("oss-fuzz", "google/oss-fuzz repo",
     "Two commits that kept the fuzzers from noticing anything.",
     [c("oss-fuzz:6403e93"), c("oss-fuzz:d2e42b2")]),
    ("libarchive", "libarchive repo",
     "Jia Tan's pre-xz contribution history — and the post-disclosure re-audit of it.",
     ["pr:libarchive:1598", "pr:libarchive:1609", "pr:libarchive:2101"]),
    ("systemd", "systemd repo",
     "The dependency cleanup that likely forced the attacker's timetable.",
     ["pr:systemd:31550", c("systemd:3fc72d5")]),
    ("endgame", "the endgame",
     "Feb-Mar 2024: push the backdoored releases into distros — then a 500ms delay ends everything.",
     ["bug:gentoo-925415", "bug:debian-accept-5.6.0", "bug:redhat-2267598",
      "bug:debian-1067708", "bug:ubuntu-2059417", "bug:debian-rollback",
      "post:oss-security-disclosure"]),
]

# ---------------------------------------------------------------------------

nodes: list[dict] = []
edges: list[dict] = []

# Every node carries a uniform data.date (the skewers' ordering key) alongside
# its more specific fields, and a data.actor where a person is responsible.

for suffix, repo, sha, author, adate, committer, cdate, subject, caption in COMMITS:
    data = {"repo": repo, "hash": sha[:12], "subject": subject, "date": cdate,
            "author": author, "author_date": adate, "committer": committer, "commit_date": cdate}
    if author in ACTOR:
        data["actor"] = ACTOR[author]
    if caption:
        data["key_event"] = True
        data["caption"] = caption
    if repo == "xz":
        data["url"] = XZ + sha
    nodes.append({"id": c(suffix), "type": "commit", "label": subject[:44], "data": data})

for version, date, tagger, backdoored in RELEASES:
    nodes.append({
        "id": f"release:{version}", "type": "release", "label": f"v{version}",
        "data": {"version": version, "date": date, "tagged_by": tagger, "actor": ACTOR[tagger],
                 "backdoored": backdoored,
                 **({"caption": "Backdoored release."} if backdoored else {})},
    })

for suffix, repo, number, opener, created, merged, title, caption in PRS:
    data = {"repo": repo, "number": number, "date": created, "created": created, "merged": merged,
            "title": title, "actor": ACTOR[opener],
            "url": f"https://github.com/{'systemd/systemd' if repo == 'systemd' else 'libarchive/libarchive'}/pull/{number}"}
    if caption:
        data["key_event"] = True
        data["caption"] = caption
    nodes.append({"id": f"pr:{suffix}", "type": "pull-request", "label": f"{repo} PR #{number}", "data": data})

edges.append({"type": "MERGED_AS", "from": "pr:systemd:31550", "to": c("systemd:3fc72d5"),
              "data": {"note": "github api"}})

for suffix, date, sender, url, gist in POSTS:
    nodes.append({
        "id": f"post:{suffix}", "type": "post", "label": gist[:44],
        "data": {"date": date, "url": url, "summary": gist, "actor": ACTOR[sender],
                 **({"key_event": True, "caption": gist} if suffix == "oss-security-disclosure" else {})},
    })

for suffix, date, filer, release, url, label, gist in BUGS:
    nodes.append({
        "id": f"bug:{suffix}", "type": "bug-report", "label": label,
        "data": {"date": date, "url": url, "summary": gist,
                 **({"actor": ACTOR[filer]} if filer else {})},
    })
    edges.append({"type": "CONCERNS", "from": f"bug:{suffix}", "to": f"release:{release}", "data": {"note": url}})

for suffix, label, shipped in DISTROS:
    nodes.append({"id": f"distro:{suffix}", "type": "distro", "label": label, "data": {}})
    for v in shipped:
        edges.append({"type": "SHIPPED", "from": f"distro:{suffix}", "to": f"release:{v}",
                      "data": {"note": "distro tracker"}})

edges.append({"type": "TAGGED_AT", "from": "release:5.4.1", "to": c("xz:18b845e"),
              "data": {"note": "git tag v5.4.1"}})

for suffix, label, description, members in SKEWERS:
    # orderKey declares what the order means (every member carries data.date):
    # the UI bundles same-key skewers and can keep them parallel, space their
    # members on one shared date scale, and draw a date axis.
    nodes.append({"id": f"skewer:{suffix}", "type": "skewer", "label": label,
                  "data": {"description": description, "orderKey": "date"}})
    for i, m in enumerate(members):
        edges.append({"type": "skewer-order", "from": f"skewer:{suffix}", "to": m, "data": {"index": i}})

schema = {
    # One person = one color, across commits, PRs, posts, bugs, and release
    # tags (watch the tagger color change hands at v5.4.2). The binding is
    # dataset knowledge: this script declares the key, every node that has a
    # responsible person carries data.actor.
    "colorKey": "actor",
    "colorValues": ACTOR_COLORS,
    "nodeTypes": {
        "commit": {"color": "#5b7fa6", "description": "A git commit (story-bearing; routine ones are folded)", "family": "code"},
        "release": {"color": "#e8b931", "description": "An xz release tag", "family": "code"},
        "pull-request": {"color": "#b07aa1", "description": "A GitHub pull request", "family": "code"},
        "post": {"color": "#76b7b2", "description": "A mailing-list message (linked and summarized, not copied)", "family": "social"},
        "bug-report": {"color": "#f28e2c", "description": "A distro bug-tracker item", "family": "distro"},
        "distro": {"color": "#59a14f", "description": "A Linux distribution", "family": "distro"},
        "skewer": {"color": "#9aa0a6", "description": "An ordered colinearity group (layout intent, interpreted by the view)", "family": "layout"},
    },
    "edgeTypes": {
        "MERGED_AS": {"color": "#8f6bb8", "description": "Pull request landed as this commit", "family": "code"},
        "TAGGED_AT": {"color": "#e8b931", "description": "Release tag points at this commit", "family": "code"},
        "CONCERNS": {"color": "#c58a3b", "description": "Bug report is about this release", "family": "distro"},
        "SHIPPED": {"color": "#59a14f", "description": "Distro shipped this release", "family": "distro"},
        "skewer-order": {"color": "#c9cdd2", "description": "Skewer membership; data.index gives the order along the skewer", "family": "layout"},
    },
}

# The graph's identity lives in its directory name (the UI's graph picker
# shows it); the view is just this graph's default perspective.
view = {
    "id": "default",
    "name": "Default",
    "visibleNodeTypes": None,
    "visibleEdgeTypes": None,
    "nodeOverrides": [],
    "edgeOverrides": [],
    "focus": None,
    "focusShow": [],
    "focusHide": [],
    "skewerGroups": {},
    "layout": {"engine": "fcose", "seedPositions": {}, "pinned": [], "skewers": {}, "rules": []},
}

OUT.mkdir(parents=True, exist_ok=True)
(OUT / "views").mkdir(exist_ok=True)
(OUT / "schema.json").write_text(json.dumps(schema, indent=2) + "\n")
(OUT / "nodes.json").write_text(json.dumps({"nodes": sorted(nodes, key=lambda n: n["id"])}, indent=2) + "\n")
(OUT / "edges.json").write_text(
    json.dumps({"edges": sorted(edges, key=lambda e: (e["from"], e["type"], e["to"]))}, indent=2) + "\n")
(OUT / "views" / "default.json").write_text(json.dumps(view, indent=2) + "\n")

kinds: dict[str, int] = {}
for n in nodes:
    kinds[n["type"]] = kinds.get(n["type"], 0) + 1
print("nodes:", len(nodes), kinds)
print("edges:", len(edges), f"({sum(1 for e in edges if e['type'] != 'skewer-order')} non-skewer)")
