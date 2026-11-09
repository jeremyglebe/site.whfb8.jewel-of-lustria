# Jewel of Lustria

Web reference for Jeremy Glebe's Warhammer Fantasy Battles expedition campaign.

Site: https://lustria.drowsy.games

## Develop

Requires Python 3 and `lxml`.

- `python build.py` rebuilds the web pages from the preserved campaign source.
- `python check.py` checks local links, anchors and semantic structure.
- `docs/style.css` contains the responsive theme and is retained by the build.
- GitHub Pages serves `main` → `/docs`.

The supplied campaign contains multiple Scenario V drafts. Following the author's direction, the final rules block is used; superseded variants remain in the source for provenance, not in the playable reference. Full Scenario VI is included. No hex-map sequel material is incorporated.

Source attribution and editorial treatment are documented on the website's Source notes page. Build output contains no analytics, external fonts, or runtime dependencies.
