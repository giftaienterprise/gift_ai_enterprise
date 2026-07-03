# GitHub Actions Backend Tests Design

## Goal

Add a small, reliable continuous-integration workflow that validates the
backend before changes are merged. The workflow must mirror the verified
Python 3.11 deployment test path without accessing deployment credentials or
changing production data.

## Triggers

Run the workflow for:

- pull requests targeting `master`;
- pushes to `master`;
- pushes to branches matching `codex/**`.

## Runtime and Steps

Use the current Ubuntu GitHub-hosted runner and Python 3.11. A single backend
test job will:

1. check out the repository;
2. restore and populate the pip dependency cache;
3. install `requirements.txt`;
4. run `python -m pip check`;
5. compile `backend/app` with `python -m compileall`;
6. run `python -m unittest discover -s tests -p 'test_*.py' -v` from the
   `backend` directory.

## Configuration and Security

The job will define test-only `DATABASE_URL` and `SECRET_KEY` environment
variables. It will not read `backend/.env`, use GitHub secrets, contact the ECS
server, deploy code, or modify business data. SQLite files and upload folders
created during the job remain on the disposable runner.

## Failure Behavior

Any failed dependency check, compilation, import, or unit test fails the job.
The workflow performs no cleanup or recovery actions against external systems.
GitHub branch protection may later require this job before merge, but that
policy change is outside this implementation.

## Acceptance Criteria

- The workflow YAML is syntactically valid.
- It uses Python 3.11 and dependency caching.
- Its test command matches the verified server-side test entry point.
- The complete local test suite still passes.
- The first GitHub Actions run completes successfully on the active PR.
