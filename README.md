# CI Security Demo (mini-project)

This mini-project is prepared to demonstrate a CI pipeline that performs:
- SAST with Semgrep (detects `subprocess.run(..., shell=True)` in `app.py`)
- SCA with Snyk (you can add a SNYK_TOKEN secret in GitHub to enable full features; `requirements.txt` pins Flask==2.0.0)
- DAST proof-of-concept: a lightweight `curl` check that fetches `/echo?msg=<script>alert(1)</script>` and saves the response.
- A small report generator that aggregates outputs into `report.html` and the workflow uploads artifacts.

## What I included
- `app.py` : vulnerable Flask app (command injection pattern + reflected XSS)
- `requirements.txt` : Flask==2.0.0
- `.semgrep.yml` : rule that flags use of `subprocess.*(..., shell=True)`
- `.github/workflows/ci.yml` : GitHub Actions workflow that runs Semgrep, Snyk, starts the app and performs a simple DAST fetch, then generates a report
- `report_generator.py` : simple script to combine outputs into an HTML file
- `README.md` : this file

## How to use
1. Unzip and push this repo to GitHub.
2. (Optional) Add your `SNYK_TOKEN` to the repository secrets for Snyk to run with full functionality.
3. The workflow will run on `push` and produce artifacts named `security-reports` containing `semgrep.json`, `snyk.json`, `dast_response.html` and `report.html`.

## Notes and tips
- The GitHub Actions workflow uses a lightweight `curl`-based DAST fallback so it will reliably show the reflected XSS in `dast_response.html` without requiring complex Docker/ZAP setup. If you want to integrate OWASP ZAP inside the workflow, you can replace the `curl` step with a ZAP docker invocation or the official ZAP GitHub Action.
- Semgrep may be strict about rule matching contexts; the included `.semgrep.yml` is tuned to flag `subprocess.run(..., shell=True)` patterns.
- Snyk requires a token for full SCA scanning on private repos; for public quick tests it may still report issues.
