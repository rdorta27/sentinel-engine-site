# sentinel-engine-site

Static project site of [sentinel-engine](https://github.com/rdorta27/sentinel-engine), published to GitHub Pages.

- `site/` is what gets published: HTML, CSS, SVG and `numbers.json`, in English, `es-419` and `pt-br`.
- `scripts/` holds the generators and the tests of the site.
- The numbers come from the frozen runs in `sentinel-engine` (`scripts/site_numbers.py` there writes `numbers.json`).

The site expects `sentinel-engine` as a sibling folder (`../core` by default).
