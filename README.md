<sub><code>THE BIT TRADING COMPANY</code>&nbsp;&nbsp;HOUSE PAPERS</sub>

# .github

The papers every repository in the organisation inherits, and the page the organisation shows the public.

A repository that keeps its own copy of any file below uses its own. A repository that keeps none gets these.

## Contents

| Folio | Paper | What it is for |
|:--|:--|:--|
| I | [profile/README.md](profile/README.md) | The organisation's public page |
| II | [CONTRIBUTING.md](CONTRIBUTING.md) | How to offer a change |
| III | [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md) | How people are treated here |
| IV | [SECURITY.md](SECURITY.md) | How to report a weakness, privately |
| V | [SUPPORT.md](SUPPORT.md) | Where a question should go |
| — | [.github/ISSUE_TEMPLATE/](.github/ISSUE_TEMPLATE/) | The forms for a fault and for a proposal |
| — | [.github/PULL_REQUEST_TEMPLATE.md](.github/PULL_REQUEST_TEMPLATE.md) | The cover sheet for a change |

There is no licence here, on purpose. GitHub does not pass a licence down from this repository, so each repository states its own.

## The look

Three colours and one square.

| | Value | Used for |
|:--|:--|:--|
| Paper | `#f7f4ec` | Ground in light, figure in dark |
| Ink | `#161512` | Figure in light, ground in dark |
| Gold | `#cfab0a` | One mark at a time, never two |

The artwork in [profile/assets/](profile/assets/) is generated, not drawn:

```bash
python3 tools/render_assets.py
```

The script needs nothing beyond Python's standard library. It writes a light and a dark version of each piece, and the profile page chooses between them from the reader's colour scheme. The typefaces are system stacks: the site's heading face is commercial and is not embedded here.

## Changing these papers

1. The profile page refers to its images by their full address on `main`, because relative paths do not resolve on an organisation's page. A banner changed on a branch will not show until it is merged.
2. Words on the profile page are public words. They state nothing that cannot be traced to a source, and a person approves them before they are merged.
3. Keep the voice: plain, short, and no louder than the facts.
