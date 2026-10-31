# Updating the profile

Edit `profile.json` and commit. The workflow rebuilds the README, the info card and the landing page data.

This file is public. Keep private details out of it.

| Change | Edit |
| --- | --- |
| New paper | Add to `publications` |
| Manuscript moves on | Update its `status` (`in_prep`, `under_review`, `accepted`). Once published, move it to `publications` |
| New report | Add to `reports` |
| Project | Add or edit in `projects`: `name`, `url`, `summary`, optional `live` |
| New job, or job still running | Add to `timeline`. Set `"end": null` while it is running |
| Availability, location, links | `identity` and `links` |
| Info card text | `card`. Keep lines under about 60 characters. `{peer_reviewed}`, `{under_review}`, `{in_prep}`, `{reports}`, `{tenure_short}`, `{orcid_id}` and `{location}` fill in automatically |

`manuscripts` and `reports` feed the counts only and are not displayed.

`contributions.json` and `site.json` are generated. README text outside the AUTO markers is hand-written.
