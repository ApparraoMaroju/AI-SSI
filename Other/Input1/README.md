# speckit-app

## Application

Run the Next.js application locally:

```bash
npm run dev
```

## Playwright Test Automation Framework

The repository now includes a TypeScript Playwright + Cucumber framework under `tests/e2e/` with:

- smoke, positive, and negative sample features
- parallel execution support
- Extent-style HTML reporting in `reports/extent/`
- Jenkins pipeline support through `Jenkinsfile`

### Install

```bash
npm ci
npx playwright install chromium
```

### Run

```bash
npm run e2e
npm run e2e -- --tags @smoke
npm run e2e -- --tags @positive
npm run e2e -- --tags @negative
npm run e2e -- --workers 4 --tags @regression
```

### Validate

```bash
npm run e2e:validate
```

### Reports

- HTML report: `reports/extent/<run-id>/index.html`
- Summary JSON: `reports/extent/<run-id>/execution-summary.json`
- Diagnostics: `artifacts/<run-id>/`

Additional framework guidance is in `docs/testing/playwright-framework.md` and `docs/testing/jenkins-playwright.md`.
