# sentinel-engine-site

Static project site of [sentinel-engine](https://github.com/rdorta27/sentinel-engine), published to GitHub Pages.

- `site/` is what gets published: HTML, CSS, SVG and `numbers.json`, in English, `es-419` and `pt-br`.
- `scripts/` holds the generators and the tests of the site.
- The numbers come from the frozen runs in `sentinel-engine` (`scripts/site_numbers.py` there writes `numbers.json`).

The site expects `sentinel-engine` as a sibling folder (`../core` by default).

## Work on the site

```
pip install -r requirements.txt
python3 scripts/slots.py --check        # number slots match site/numbers.json
python3 scripts/localize.py --check     # es-419 and pt-br copies match the English pages
python3 -m pytest -q                    # tests; the ones marked core need ../core
```

The tests in the browser use the Chromium or Chrome of the system.

## Publication

- `pages.yml` checks the site on its own and publishes `site/` to GitHub Pages when a push to `main` changes it. In the repository settings, Pages must use the source GitHub Actions.
- `cross-check.yml` clones sentinel-engine and checks that the links and quoted lines of the site still exist there. It runs weekly and on each push, and it never blocks a deploy.
- Public address: https://rdorta27.github.io/sentinel-engine-site/
