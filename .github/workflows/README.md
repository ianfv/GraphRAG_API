# GitHub Actions CI/CD Workflows

This directory contains the CI/CD pipeline configuration for the GraphRAG Clinical Guidelines project.

## Overview

The pipeline is implemented using **GitHub Actions** with three environment-aware workflows:

1. **CI (Continuous Integration)** - Runs on all branches
2. **Staging** - Runs on main branch
3. **Production** - Runs on version tags

## Workflows

### 1. CI Workflow (`ci.yml`)

**Triggers:**
- Push to any branch
- Pull requests to any branch

**Jobs:**
- **Lint**: Code quality checks using Ruff
- **Test**: Run pytest with coverage reporting
- **Security Check**: Dependency vulnerability scanning with Safety
- **Status Check**: Aggregate status of all checks

**Coverage:**
- Generates coverage reports (term, XML, HTML)
- Uploads to Codecov (if configured)
- No minimum threshold enforced (informational)

**When to use:**
- Feature development
- Bug fixes
- Experimental branches

### 2. Staging Workflow (`staging.yml`)

**Triggers:**
- Push to `main` branch

**Jobs:**
- **Full Test Suite**: Comprehensive testing
- **Strict Linting**: No auto-fixes, strict mode
- **Docker Build Placeholder**: Ready for Phase 2 implementation
- **Staging Ready**: Validation summary

**Coverage Threshold:**
- **Minimum: 70%** (enforced, build fails below this)

**When to use:**
- Merged pull requests
- Integration testing
- Pre-production validation

**Future Enhancements:**
- Docker image build and push
- Deploy to staging ECS cluster
- Integration tests against staging environment

### 3. Production Workflow (`production.yml`)

**Triggers:**
- Push tags matching `v*.*.*` (e.g., `v1.0.0`, `v2.1.3`)

**Jobs:**
- **Version Validation**: Ensures semantic versioning
- **Comprehensive Tests**: Full test suite with strict markers
- **Strict Linting**: Production-grade code quality
- **Security Scan**: Safety + Bandit analysis
- **Docker Build Placeholder**: Ready for Phase 3
- **Production Ready**: Deployment readiness check

**Coverage Threshold:**
- **Minimum: 80%** (enforced, build fails below this)

**Security:**
- Blocks deployment if high-severity issues found
- Validates all dependencies

**When to use:**
- Official releases
- Production deployments
- Version milestones

**Future Enhancements:**
- Automated Docker build and ECR push
- Blue-green deployment to ECS
- Automated rollback on failure
- Post-deployment health checks

## Usage Guide

### Development (Feature Branches)

1. Create a feature branch:
```bash
git checkout -b feature/your-feature-name
```

2. Make changes and commit:
```bash
git add .
git commit -m "feat: add your feature"
git push origin feature/your-feature-name
```

3. CI workflow runs automatically
   - ✅ Linting checks
   - ✅ Tests run
   - 📊 Coverage reported (no minimum)

4. Create pull request when ready
   - CI must pass before merge
   - Review code coverage in PR comments

### Staging (Main Branch)

1. Merge PR to main:
```bash
# After PR approval
git checkout main
git pull origin main
```

2. Staging workflow runs automatically
   - ✅ Full test suite
   - ✅ 70% coverage enforced
   - 🚀 Ready for staging deployment

3. Review staging checks:
   - Visit Actions tab
   - Check "Staging" workflow
   - Verify all jobs passed

### Production (Release Tags)

1. Create a release tag:
```bash
# Ensure you're on main with latest changes
git checkout main
git pull origin main

# Create and push tag
git tag -a v1.0.0 -m "Release version 1.0.0"
git push origin v1.0.0
```

2. Production workflow runs automatically
   - ✅ Version validation
   - ✅ 80% coverage enforced
   - ✅ Security scans
   - 🚀 Ready for production

3. Review production checks:
   - Visit Actions tab
   - Check "Production" workflow
   - Review deployment summary

## Adding GitHub Actions Badges

Add these badges to your `README.md`:

```markdown
![CI](https://github.com/ianfv/elec_498a_graph_rag/workflows/CI/badge.svg)
![Staging](https://github.com/ianfv/elec_498a_graph_rag/workflows/Staging/badge.svg)
![Production](https://github.com/ianfv/elec_498a_graph_rag/workflows/Production/badge.svg)
[![codecov](https://codecov.io/gh/ianfv/elec_498a_graph_rag/branch/main/graph/badge.svg)](https://codecov.io/gh/ianfv/elec_498a_graph_rag)
```

## Branch Protection Rules

Recommended settings for `main` branch:

1. Go to: **Settings** → **Branches** → **Branch protection rules**
2. Add rule for `main`:
   - ✅ Require pull request reviews before merging
   - ✅ Require status checks to pass before merging
     - Select: `Lint Code`
     - Select: `Run Tests`
   - ✅ Require branches to be up to date before merging
   - ✅ Include administrators

## Local Testing

Run the same checks locally before pushing:

```bash
# Install dependencies
pip install -r requirements.txt

# Run linting
ruff check src/ tests/
ruff format --check src/ tests/

# Run tests with coverage
pytest tests/ -v --cov=src --cov-report=term-missing

# Check coverage threshold (staging: 70%, production: 80%)
pytest tests/ --cov=src --cov-fail-under=70
```

## Migration Path

### Current State (Phase 1) ✅
- [x] Linting with Ruff
- [x] Testing with pytest
- [x] Coverage reporting
- [x] Environment-aware workflows
- [x] Security scanning

### Phase 2 (Coming Soon) 🔄
- [ ] Docker image building
- [ ] Push to GitHub Container Registry
- [ ] Container security scanning
- [ ] Multi-stage Docker builds

### Phase 3 (AWS Integration) 🚀
- [ ] AWS ECR integration
- [ ] ECS Fargate deployment
- [ ] AWS CDK integration
- [ ] Infrastructure as Code

### Phase 4 (Advanced) 🎯
- [ ] Integration with AWS CodeBuild
- [ ] Blue-green deployments
- [ ] Automated rollback
- [ ] Performance testing
- [ ] Load testing

## Troubleshooting

### CI Workflow Fails

**Linting errors:**
```bash
# Auto-fix most issues
ruff check src/ tests/ --fix
ruff format src/ tests/
```

**Test failures:**
```bash
# Run tests locally to debug
pytest tests/ -v -s
```

**Coverage too low:**
```bash
# Check which files need more tests
pytest tests/ --cov=src --cov-report=html
# Open htmlcov/index.html in browser
```

### Staging Workflow Fails

**Coverage below 70%:**
- Add more unit tests
- Focus on untested modules
- Use `htmlcov/index.html` to identify gaps

**Strict linting fails:**
- Fix all linting issues (no auto-fix in staging)
- Review Ruff output carefully

### Production Workflow Fails

**Invalid version tag:**
- Ensure tag format is `vX.Y.Z` (e.g., `v1.0.0`)
- Delete and recreate tag if needed:
  ```bash
  git tag -d v1.0.0
  git push origin :refs/tags/v1.0.0
  git tag -a v1.0.0 -m "Release 1.0.0"
  git push origin v1.0.0
  ```

**Coverage below 80%:**
- Production requires higher coverage
- Add comprehensive tests before release
- Consider integration and E2E tests

**Security vulnerabilities:**
- Update vulnerable dependencies
- Check Safety and Bandit reports
- Address high-severity issues before release

## Environment Variables & Secrets

Currently no secrets required for basic CI/CD.

**Future secrets (Phase 3+):**
- `AWS_ACCESS_KEY_ID` - AWS credentials
- `AWS_SECRET_ACCESS_KEY` - AWS credentials
- `ECR_REPOSITORY` - ECR repository name
- `ECS_CLUSTER` - ECS cluster name
- `ECS_SERVICE` - ECS service name

To add secrets:
1. Go to **Settings** → **Secrets and variables** → **Actions**
2. Click **New repository secret**
3. Add secret name and value

## Contact

For questions about the CI/CD pipeline:
- **Team Lead**: Check team Discord or Notion
- **DevOps**: Omar Afify
- **Testing**: Ian Fairfield, Omar Afify

## References

- [GitHub Actions Documentation](https://docs.github.com/en/actions)
- [pytest Documentation](https://docs.pytest.org/)
- [Ruff Documentation](https://docs.astral.sh/ruff/)
- [CLAUDE.md](../../CLAUDE.md) - Full project documentation
