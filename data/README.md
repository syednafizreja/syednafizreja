# Updating the profile

Edit `profile.json` on GitHub and commit. The "Update Profile Art & Timeline" workflow then rebuilds the README, the info card and the landing page data, so nothing else needs touching.

| To change | Edit in `profile.json` |
| :--- | :--- |
| New paper | Add to `publications` (the count updates itself) |
| Manuscript moves on | Change its `status`: `in_prep`, `under_review` or `accepted`. Once published, move it to `publications` |
| New report | Add to `reports` |
| Project progress | Update that project's `status` and `as_of` date, and any numbers in `bullets` |
| New job, or job still running | Add to `timeline`. Set `"end": null` for a current role; tenure then counts up on its own |
| Availability, location, links | `identity` and `links` |
| Info card text | `card`. Keep lines under about 60 characters. `{peer_reviewed}`, `{under_review}`, `{in_prep}`, `{reports}`, `{tenure_short}`, `{orcid_id}` and `{location}` fill in automatically |

`contributions.json` and `site.json` are generated. Do not edit them. README text outside the `<!-- AUTO:x -->` markers is hand-written and safe to edit directly.
