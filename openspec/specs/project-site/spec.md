# project-site Specification

## Purpose
Defines the static project site in `site/`: its English content, its translations, its numbers from the frozen runs of sentinel-engine, and its publication to GitHub Pages.

## Requirements

### Requirement: The project site is static and in English

This repository SHALL contain a static site in `site/`, in English, that describes the product, how it works, the measured results, the demo cases and the links to the live demo and the repository. The workflow `.github/workflows/pages.yml` SHALL publish `site/` to GitHub Pages from `main`. The workflow `.github/workflows/cross-check.yml` SHALL check the links and quoted lines against sentinel-engine, and it SHALL NOT block a deploy. Traces to REQ-0051 (P0, In progress) and REQ-0056 (P0, In progress).

#### Scenario: Publication

- **WHEN** a change to `site/` merges into `main`
- **THEN** `.github/workflows/pages.yml` publishes the site to GitHub Pages

#### Scenario: A link that sentinel-engine moved

- **WHEN** a file that the site links to changes in sentinel-engine
- **THEN** `.github/workflows/cross-check.yml` fails and names the link, and the site stays published

### Requirement: Site numbers come from the evidence

Each number on the site SHALL come from a field of a frozen `summary.json` of sentinel-engine through `site/numbers.json`, and SHALL show its type: simulation, test suite or projection. `scripts/site_numbers.py` in sentinel-engine SHALL generate the file, and a check there SHALL fail if this copy differs from the evidence. Traces to REQ-0022 (P0, Done) and REQ-0031 (P0, Done).

#### Scenario: A stale number

- **WHEN** a frozen run changes and the copy of `site/numbers.json` is not regenerated
- **THEN** the check in sentinel-engine fails and names the number

### Requirement: The site explains the system with interactive diagrams

The site SHALL offer standalone interactive diagrams of the architecture, one chat turn, the three demo cases and the evidence. Each diagram SHALL work without an external library, with the keyboard and at 390 px. Each number in a diagram SHALL come from `site/numbers.json` and SHALL show its denominator and its type. Traces to REQ-0036 (P0, Done) and REQ-0056 (P0, In progress).

#### Scenario: Demo and production view

- **WHEN** a visitor switches the architecture diagram to production
- **THEN** each mock shows the component that replaces it

#### Scenario: A number in a diagram

- **WHEN** a diagram shows a metric
- **THEN** it shows the denominator, the type label and the field of the evidence

### Requirement: The site answers the questions of a bank

The site SHALL offer a page at `for-banks.html` that explains the path to production, what a bank can verify, the safety and control of the system, the results by language and the common questions. Each number on the page SHALL come from `site/numbers.json` and SHALL show its type. The page SHALL link to the repository for the full setup. Traces to REQ-0051 (P0, In progress) and REQ-0056 (P0, In progress).

#### Scenario: A bank reads the page

- **WHEN** a bank reader opens `for-banks.html`
- **THEN** the page shows the production gaps, the checks the reader can run and the limits of the results

### Requirement: The site holds no secret

The site SHALL NOT hold a password, a key, a bucket name, an account id or a dataset row. The "Try it" section SHALL say that the credentials are in the submission email. Traces to REQ-0034 (P0, Done) and REQ-0027 (P0, Done).

#### Scenario: Search

- **WHEN** a search runs on `site/`
- **THEN** it finds none of these values

### Requirement: The site is available in three languages with one navigation

The site SHALL be available in English, Spanish (es-419) and Portuguese (pt-BR). Every page SHALL show the same navigation and a language switch that opens the same page in the other language. Each translated number SHALL equal the number of the English page. Traces to REQ-0051 (P0, In progress) and REQ-0012 (P0, Done).

#### Scenario: Language switch

- **WHEN** a visitor selects another language on a page
- **THEN** the same page opens in that language, with the same navigation

#### Scenario: Browser language

- **WHEN** a visitor with no saved choice opens the English home page and the browser language is Spanish or Portuguese
- **THEN** the page opens in that language, and the switch can change it
- **WHEN** the browser language is not English, Spanish or Portuguese
- **THEN** the page stays in English

#### Scenario: Saved choice

- **WHEN** a visitor chose a language on an earlier visit and opens any page
- **THEN** the same page opens in that language, even if the browser language is different

#### Scenario: Translated landing page

- **WHEN** a visitor with no saved choice opens a translated page
- **THEN** the page stays in that language

#### Scenario: Query and anchor

- **WHEN** the language changes on a page with a query or an anchor
- **THEN** the new page keeps the same query and anchor

#### Scenario: A text with no translation

- **WHEN** an English page holds a text that a dictionary does not translate
- **THEN** the build and the tests fail and name the text
