# Adding Unit Tests to a Bento-Style AWS CDK Repository

This guide explains how to add unit tests to a CDK Python repository that follows the same structure as this one. It covers the test architecture, the shared stack-builder pattern used by both deployments and tests, writing resource and security tests, running tests locally, and the GitHub Actions CI workflow.

---

## Table of Contents

1. [Repository Structure](#1-repository-structure)
2. [Prerequisites](#2-prerequisites)
3. [The Shared Stack Builder (`app/__init__.py`)](#3-the-shared-stack-builder-appinit-py)
4. [Test Directory Layout](#4-test-directory-layout)
5. [Writing Resource Tests](#5-writing-resource-tests)
6. [Security Tests (Centrally Managed)](#6-security-tests-centrally-managed)
7. [Running Tests Locally](#7-running-tests-locally)
8. [GitHub Actions CI Workflow](#8-github-actions-ci-workflow)
9. [Adapting Tests for a New Repository](#9-adapting-tests-for-a-new-repository)

---

## 1. Repository Structure

A compatible repository looks like this:

```
awscdk/bento/
├── app.py                      # CDK entry point (deployment only)
├── cdk.json
├── config.ini                  # Runtime config (NOT committed; fetched from S3 in CI)
├── requirements.txt            # Runtime + test dependencies
├── requirements-dev.txt        # pytest pin (optional override)
├── setup.py
├── app/
│   ├── __init__.py             # ← shared build_stack() function
│   ├── aspects.py              # IAM role renaming via CDK Aspects
│   ├── secrets.py              # Secrets Manager construct
│   ├── service.py              # Reusable Fargate service construct
│   └── stack.py                # Main CDK Stack definition
└── tests/
    ├── __init__.py
    └── unit/
        ├── __init__.py
        ├── test_app_resources.py   # Infrastructure resource assertions
        └── test_app_security.py    # Security assertions (fetched from central repo in CI)
```

---

## 2. Prerequisites

### Python dependencies

Add the following to `requirements.txt`:

```
-e .
aws-cdk-lib==2.150.0
constructs>=10.0.0,<11.0.0
configparser
boto3
jsii
pytest
```

`requirements-dev.txt` can pin pytest independently if needed:

```
pytest==6.2.5
```

Install dependencies (from the `awscdk/bento/` directory):

```bash
pip3 install -r requirements.txt
```

### `config.ini`

Tests read `config.ini` at synthesis time using the standard `ConfigParser`. A valid `config.ini` must be present in the working directory before running tests. Locally, copy one of the tier-specific variants:

```bash
cp config.ini.dev config.ini
```

In CI the file is fetched from S3 (see [§8](#8-github-actions-ci-workflow)).

---

## 3. The Shared Stack Builder (`app/__init__.py`)

The central pattern that makes tests simple is extracting stack construction into a shared `build_stack()` function in `app/__init__.py`. Both `app.py` (deployment) and the test suite call this function.

```python
# app/__init__.py
import aws_cdk as cdk
from aws_cdk import aws_iam as iam
from app.stack import Stack
from app.aspects import MyAspect


def build_stack(app, config, synthesizer=None):
    """Build and configure the CDK stack from a ConfigParser config.

    Pass synthesizer=None in tests (default synthesizer is used).
    Pass a custom DefaultStackSynthesizer in app.py for deployment.
    """
    stack_name = f"{config['main']['program']}-{config['main']['project']}-{config['main']['tier']}"
    kwargs = dict(
        env=cdk.Environment(
            account=config['main']['account_id'],
            region=config['main']['region'],
        ),
    )
    if synthesizer is not None:
        kwargs['synthesizer'] = synthesizer

    stack = Stack(app, stack_name, **kwargs)

    cdk.Aspects.of(stack).add(MyAspect())

    if config.has_option('iam', 'permission_boundary'):
        boundary = iam.ManagedPolicy.from_managed_policy_arn(
            stack, "Boundary", config['iam']['permission_boundary']
        )
        iam.PermissionsBoundary.of(stack).apply(boundary)

    config_tags = dict(s.split(':') for s in config['main']['tags'].split(","))
    env_tags = {'Environment': config['main']['tier']}
    for tag, value in (config_tags | env_tags).items():
        cdk.Tags.of(stack).add(tag, value)

    return stack
```

**Why this matters:** Tests do not need to re-implement stack construction logic. Adding a new resource to `stack.py` automatically makes it testable without touching `app/__init__.py` or the test helper.

`app.py` (the deployment entry point) uses `build_stack()` with a custom synthesizer to target specific CDK bootstrap roles:

```python
# app.py
app = cdk.App()
stack = build_stack(app, config, synthesizer=synthesizer)
app.synth()
```

---

## 4. Test Directory Layout

Create the following files and directories (the `__init__.py` files must exist but can be empty):

```bash
mkdir -p tests/unit tests/cdk.out
touch tests/__init__.py tests/unit/__init__.py
```

The `tests/cdk.out/` directory is where pytest writes the JUnit XML report and where CDK writes synthesized assets during tests. Add it to `.gitignore`.

---

## 5. Writing Resource Tests

### The `_create_test_stack()` helper

All test functions share a common helper that synthesizes the stack into a `Template` object for assertion:

```python
# tests/unit/test_app_resources.py
import aws_cdk as cdk
from aws_cdk import aws_iam as iam
from aws_cdk.assertions import Template, Match
from configparser import ConfigParser
from app.stack import Stack
from app.aspects import MyAspect


def _create_test_stack():
    outdir = "tests/cdk.out"
    app = cdk.App(outdir=outdir)

    config = ConfigParser(interpolation=None)
    config.read('config.ini')

    stack_name = f"{config['main']['program']}-{config['main']['project']}-{config['main']['tier']}"
    stack = Stack(
        app,
        stack_name,
        env=cdk.Environment(
            account=config['main']['account_id'],
            region=config['main']['region'],
        ),
    )

    cdk.Aspects.of(stack).add(MyAspect())

    if config.has_option('iam', 'permission_boundary'):
        boundary = iam.ManagedPolicy.from_managed_policy_arn(
            stack, "Boundary", config['iam']['permission_boundary']
        )
        iam.PermissionsBoundary.of(stack).apply(boundary)

    config_tags = dict(s.split(':') for s in config['main']['tags'].split(","))
    for tag, value in (config_tags | {'Environment': config['main']['tier']}).items():
        cdk.Tags.of(stack).add(tag, value)

    return stack, Template.from_stack(stack), config
```

> **Tip:** If you have already refactored `build_stack()` into `app/__init__.py` you can call that instead, passing `synthesizer=None`.

### Assertion patterns

`aws_cdk.assertions.Template` provides three primary assertion methods:

| Method | Purpose |
|---|---|
| `template.resource_count_is(type, n)` | Assert exactly `n` resources of `type` exist |
| `template.has_resource(type, {})` | Assert at least one resource of `type` exists |
| `template.has_resource_properties(type, props)` | Assert a resource with those exact properties exists |
| `template.find_resources(type)` | Return a dict of all matching resources (for iteration) |

Use `Match.any_value()` where the exact value is not important, and `Match.array_with([...])` to assert a subset of an array.

### Example tests

```python
def test_ecs_resources():
    """ECS task definitions and services are created for all three services"""
    stack, template, config = _create_test_stack()
    template.resource_count_is("AWS::ECS::TaskDefinition", 3)
    template.resource_count_is("AWS::ECS::Service", 3)


def test_ecs_task_definition_properties():
    """ECS task definitions use CPU/memory from config.ini"""
    stack, template, config = _create_test_stack()
    template.has_resource_properties("AWS::ECS::TaskDefinition", {
        "Cpu": config["backend"]["cpu"],
        "Memory": config["backend"]["memory"],
        "NetworkMode": "awsvpc",
        "RequiresCompatibilities": ["FARGATE"]
    })


def test_alb_http_redirect():
    """Port-80 listener redirects to HTTPS with a 301"""
    stack, template, config = _create_test_stack()
    template.has_resource_properties("AWS::ElasticLoadBalancingV2::Listener", {
        "Port": 80,
        "Protocol": "HTTP",
        "DefaultActions": [{"Type": "redirect", "RedirectConfig": {
            "Protocol": "HTTPS", "Port": "443", "StatusCode": "HTTP_301"
        }}]
    })


def test_secrets_manager_secret_name():
    """Secret name matches program/project/tier convention"""
    stack, template, config = _create_test_stack()
    expected = f"{config['main']['program']}/{config['main']['project']}/{config['main']['tier']}"
    template.has_resource_properties("AWS::SecretsManager::Secret", {"Name": expected})


def test_removal_policies():
    """OpenSearch and log groups use DESTROY policy so dev stacks can be torn down cleanly"""
    stack, template, config = _create_test_stack()
    for resource_id, resource in template.find_resources("AWS::OpenSearchService::Domain").items():
        assert resource.get("DeletionPolicy") == "Delete", \
            f"OpenSearch {resource_id} should have DeletionPolicy: Delete"
```

### What to test

Cover at least the following categories:

- **Resource counts** — ECS task definitions, services, target groups, listeners, log groups, IAM roles, KMS keys
- **Config-driven properties** — CPU, memory, health check paths and intervals, listener rule priorities and path patterns
- **Tagging** — all tags from `config.ini` applied to resources
- **ALB configuration** — HTTP→HTTPS redirect, HTTPS listener with certificate, default 404 response, TLS policy
- **ECS service properties** — `AssignPublicIp: DISABLED`, `EnableExecuteCommand: True`, circuit breaker enabled
- **CloudWatch logging** — all containers configured with `awslogs` driver pointing to the correct region
- **Removal policies** — appropriate for the tier (e.g., `DESTROY` for dev)
- **IAM role name prefix** — applied by `MyAspect` using `role_prefix` from `config.ini`

---

## 6. Security Tests (Centrally Managed)

Security-focused tests live in the central `datacommons-devops` repository at `awscdk/tests/unit/test_app_security.py`. They are fetched by the CI workflow at runtime and must **not** be copied into the local repository permanently.

The security test file covers:

| Category | Tests |
|---|---|
| OpenSearch | Node-to-node encryption, encryption at rest, HTTPS enforced, VPC placement, audit logging, least-privilege access policy |
| ALB | TLS 1.2+ SSL policy, HTTP→HTTPS 301 redirect, access logging to S3 |
| ECS / Fargate | No public IP on tasks, CloudWatch logging on all containers |
| Secrets Manager / KMS | Customer-managed KMS key for secrets, KMS key policy grants root full access and restricts cross-account roles to `kms:Decrypt`/`kms:DescribeKey` only, resource policy allows only `secretsmanager:GetSecretValue` and no wildcard principals |
| CloudFront | `redirect-to-https` viewer protocol, trusted key group required (signed URLs enforced) |
| IAM | Permission boundary applied to all roles, no wildcard actions (`iam:*`, `s3:*`, `*`) in execution role policies |

When writing local resource tests, avoid duplicating these security assertions — they will be enforced by the central tests during CI.

---

## 7. Running Tests Locally

From the `awscdk/bento/` directory:

```bash
# Run all tests with verbose output
pytest -v

# Run only resource tests
pytest tests/unit/test_app_resources.py -v

# Run a single test function
pytest tests/unit/test_app_resources.py::test_ecs_resources -v

# Generate the JUnit XML report (same path as CI)
pytest --junitxml=tests/cdk.out/unit-test-report.xml
```

Ensure `config.ini` is present and valid before running. The stack is synthesized during each test function call via `_create_test_stack()`, so a VPC lookup is performed against AWS — export valid credentials or use `cdk.App(outdir=..., context={"aws:cdk:disable-asset-staging": "true"})` with a mocked account if credentials are unavailable.

---

## 8. GitHub Actions CI Workflow

The workflow file at `.github/workflows/unit_test.yml` triggers on any push that touches `awscdk/bento/**` and on `workflow_dispatch`.

### Key steps

```
1. Checkout code (with full history for rebase support)
2. Set up Python 3.9
3. pip install -r requirements.txt
4. Authenticate to AWS via OIDC (role-to-assume stored as repo secret)
5. Download config.ini from S3:
     aws s3api get-object \
       --bucket crdc-popsci-cdk-config-bucket \
       --key config/config.ini.dev \
       ./config.ini.dev
     envsubst < config.ini.dev > config.ini
6. Fetch security tests from datacommons-devops (sparse checkout)
7. Copy security tests into tests/unit/test_app_security.py
8. pytest --junitxml=tests/cdk.out/unit-test-report.xml
   (continue-on-error: true so the next steps always run)
9. If tests failed:
   a. Upload the XML report as a secret GitHub Gist
   b. Create a GitHub issue with the gist link and test analysis instructions
   c. Assign the issue to @copilot for automated investigation
   d. Wait for Copilot to open a PR, then retarget it to the triggering branch
```

### Required secrets

| Secret | Purpose |
|---|---|
| `AWS_ROLE_TO_ASSUME` | OIDC role ARN for AWS authentication |
| `AWS_REGION` | Target region |
| `AWS_ACCOUNT` | AWS account ID (passed as `AWS_DEFAULT_ACCOUNT`) |
| `COPILOT_TOKEN` | Classic PAT with `repo` + `gist` scopes (required to create gists and assign @copilot) |

### Adapting the workflow

To use this workflow in another repository:

1. Copy `.github/workflows/unit_test.yml` into the target repo.
2. Update the `paths` trigger: `awscdk/<your-project>/**`
3. Update the S3 bucket and key path in the "Get config files" step.
4. Update the `cd awscdk/bento` path in the install and pytest steps to match your project directory.
5. Verify that the `datacommons-devops` sparse-checkout path for `test_app_security.py` is still valid, or update it if security tests have moved.

---

## 9. Adapting Tests for a New Repository

When adding unit tests to a new repository that has a different set of AWS resources, follow this checklist:

### Step 1 — Refactor `app/__init__.py`

Extract stack construction from `stack.py`/`app.py` into a `build_stack(app, config, synthesizer=None)` function as shown in [§3](#3-the-shared-stack-builder-appinit-py). This is the single most important structural change.

### Step 2 — Create the test scaffold

```bash
mkdir -p tests/unit tests/cdk.out
touch tests/__init__.py tests/unit/__init__.py
echo "tests/cdk.out/" >> .gitignore
```

### Step 3 — Write a `_create_test_stack()` helper

Copy the helper from [§5](#5-writing-resource-tests) and update the imports to match your `app/` module structure.

### Step 4 — Write resource count tests first

Start with `template.resource_count_is(...)` assertions for every AWS resource type your stack creates. These tests are fast to write and immediately catch regressions when resources are accidentally removed or duplicated.

### Step 5 — Add config-driven property tests

For each configurable value (CPU, memory, paths, ports, health check settings, certificate ARNs), write a `has_resource_properties` test that reads the expected value from `config.ini` via the `config` object returned by `_create_test_stack()`. This ensures tests stay in sync with configuration changes automatically.

### Step 6 — Adjust security test expectations

Review `test_app_security.py` from `datacommons-devops`. If your stack does not include a resource type that a security test targets (e.g., no OpenSearch, no CloudFront), those tests use `pytest.skip()` automatically and will not fail. No changes to the security test file are needed for resources you have not deployed.

### Step 7 — Verify the workflow config

Update the S3 bucket path and CDK project directory in the workflow YAML so that CI fetches the correct `config.ini` for your environment.

---

## Common Pitfalls

| Issue | Fix |
|---|---|
| `Unable to resolve resource with logical ID` | Stack synthesis requires a valid VPC lookup; ensure AWS credentials are set or add VPC context to `cdk.context.json` |
| `config.ini` not found | Run tests from the `awscdk/bento/` directory, not the repo root |
| IAM role name assertion fails | Verify `config.ini` has `[iam] role_prefix` set; `MyAspect` only renames roles when this option is present |
| Security test fails with `KeyError: 'db'` | Your `config.ini` is missing the `[db]` section with `prefect_role_arn`; add it or skip tests conditionally |
| `pytest` not found | Run `pip install -r requirements.txt` from the `awscdk/bento/` directory |
| Tests pass locally but fail in CI | The S3 config file may differ from your local copy; compare values using `cdk diff` between tiers |
