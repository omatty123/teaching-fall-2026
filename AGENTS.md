# Teaching webpages

Use this existing GitHub repository (`omatty123/teaching-fall-2026`) and GitHub Pages for Fall teaching webpages. When the user asks to build a class webpage, publish the completed, verified page here and add its direct link to the matching dated prep on the private Teaching HQ: https://teaching-fall-2026-roster.pages.dev/instructor/fall-2026/. The user does not need to repeat this routing. This standing preference was confirmed October 4, 2026.

The public site contains student-facing resources only. Keep instructor prep, student records, credentials, and full copyrighted sources private. Canvas and Google Docs edits require their own task scope.

Preserve other agents' dirty work. Stage exact filenames only; do not use `git add -A` or the broad staging in `deploy.sh --push`. Edit course schedules in `data/<slug>.json`, then run `python3 build.py --strict`. Check local browser behavior and GitHub Pages after pushing. Standalone reading resources may live in `<course>-resources/` with matching assets and source ledgers.
