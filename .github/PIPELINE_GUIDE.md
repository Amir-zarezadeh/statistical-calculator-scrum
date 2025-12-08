# GitHub Actions Pipeline Guide

## Overview
This repository uses GitHub Actions for CI/CD automation. Three main workflows are configured:

## Workflows

### 1. CI Pipeline (`ci.yml`)
**Triggers:** Push and Pull Requests to `main` and `develop` branches

**Jobs:**
- **Test** - Runs unit tests across multiple Python versions (3.9, 3.10, 3.11, 3.12)
- **Lint** - Code quality checks using flake8 and pylint
- **Security** - Security scanning with safety and bandit

**Features:**
- Matrix testing across Python versions
- Dependency caching for faster builds
- Test result artifacts
- Security vulnerability scanning

### 2. Deploy Pipeline (`deploy.yml`)
**Triggers:** 
- Push to `main` branch
- Version tags (v*.*.*)
- Manual workflow dispatch

**Jobs:**
- **Test** - Validates all tests pass before deployment
- **Deploy** - Deploys to production (configure based on your platform)

**Deployment Targets (examples included):**
- Heroku
- Azure Web App
- AWS Elastic Beanstalk

### 3. Code Coverage (`code-coverage.yml`)
**Triggers:** Push and Pull Requests to `main` and `develop` branches

**Jobs:**
- Runs tests with coverage measurement
- Generates HTML and XML coverage reports
- Uploads to Codecov (optional)
- Enforces 80% minimum coverage threshold

## Setup Instructions

### Step 1: Push Workflows to GitHub
```bash
git add .github/
git commit -m "Add GitHub Actions CI/CD pipelines"
git push origin main
```

### Step 2: View Workflows
1. Go to your repository on GitHub
2. Click the **Actions** tab
3. You'll see the workflows running automatically

### Step 3: Configure Secrets (for deployment)
If you want to use the deployment pipeline:

1. Go to **Settings** → **Secrets and variables** → **Actions**
2. Click **New repository secret**
3. Add required secrets based on your deployment platform:

#### For Heroku:
- `HEROKU_API_KEY` - Your Heroku API key
- `HEROKU_APP_NAME` - Your app name

#### For Azure:
- `AZURE_WEBAPP_PUBLISH_PROFILE` - Download from Azure Portal

#### For AWS:
- `AWS_ACCESS_KEY_ID` - Your AWS access key
- `AWS_SECRET_ACCESS_KEY` - Your AWS secret key

### Step 4: Enable Workflows
Workflows run automatically on push/PR. To manually trigger:
1. Go to **Actions** tab
2. Select a workflow
3. Click **Run workflow**

## Customizing Workflows

### Change Python Versions
Edit `ci.yml`, line 15:
```yaml
python-version: ['3.9', '3.10', '3.11', '3.12']
```

### Add More Branches
Edit trigger section in any workflow:
```yaml
on:
  push:
    branches: [ main, develop, feature/* ]
```

### Adjust Coverage Threshold
Edit `code-coverage.yml`, last line:
```yaml
coverage report --fail-under=80  # Change 80 to desired %
```

### Configure Deployment
Uncomment and configure the deployment section in `deploy.yml`:

**Example - Heroku:**
```yaml
- name: Deploy to Heroku
  uses: akhileshns/heroku-deploy@v3.12.14
  with:
    heroku_api_key: ${{ secrets.HEROKU_API_KEY }}
    heroku_app_name: "stat-calculator"
    heroku_email: "your-email@example.com"
```

## Status Badges

Add status badges to your `README.md`:

```markdown
![CI Pipeline](https://github.com/dayald434/stat-calculator/workflows/CI%20Pipeline/badge.svg)
![Code Coverage](https://github.com/dayald434/stat-calculator/workflows/Code%20Coverage/badge.svg)
![Deploy](https://github.com/dayald434/stat-calculator/workflows/Deploy%20to%20Production/badge.svg)
```

## Workflow Files Location
```
.github/
└── workflows/
    ├── ci.yml                 # Main CI pipeline
    ├── deploy.yml             # Deployment pipeline
    └── code-coverage.yml      # Coverage reporting
```

## Testing Workflows Locally

### Using Act (GitHub Actions simulator)
```bash
# Install act
# Windows (with Chocolatey):
choco install act-cli

# macOS:
brew install act

# Linux:
curl https://raw.githubusercontent.com/nektos/act/master/install.sh | sudo bash

# Run workflows locally
act push                    # Simulate push event
act pull_request            # Simulate PR
act -j test                 # Run specific job
```

## Troubleshooting

### Workflow Not Running?
- Check that `.github/workflows/` is in the repository root
- Ensure YAML syntax is valid (use online YAML validator)
- Check branch names match trigger configuration

### Tests Failing in CI but Pass Locally?
- Check Python version differences
- Verify all dependencies are in `requirements.txt`
- Review environment variables

### Deployment Failing?
- Verify secrets are configured correctly
- Check deployment platform credentials
- Review deployment logs in Actions tab

## Best Practices

1. **Keep workflows fast** - Use caching for dependencies
2. **Test before deploy** - Always run tests before deployment
3. **Use matrix testing** - Test across multiple Python versions
4. **Secure secrets** - Never commit API keys or passwords
5. **Monitor failures** - Set up email notifications for failures
6. **Version tags** - Use semantic versioning (v1.0.0, v1.0.1, etc.)

## Email Notifications

GitHub sends emails by default for workflow failures. To customize:
1. Go to **Settings** → **Notifications**
2. Configure **Actions** notifications

## Advanced Features

### Scheduled Runs
Add to any workflow:
```yaml
on:
  schedule:
    - cron: '0 0 * * 0'  # Run every Sunday at midnight
```

### Manual Triggers with Inputs
```yaml
on:
  workflow_dispatch:
    inputs:
      environment:
        description: 'Deployment environment'
        required: true
        default: 'staging'
        type: choice
        options:
          - staging
          - production
```

### Conditional Jobs
```yaml
jobs:
  deploy:
    if: github.ref == 'refs/heads/main'
    runs-on: ubuntu-latest
```

## Resources

- [GitHub Actions Documentation](https://docs.github.com/en/actions)
- [Workflow Syntax](https://docs.github.com/en/actions/reference/workflow-syntax-for-github-actions)
- [Marketplace](https://github.com/marketplace?type=actions) - Browse pre-built actions
- [Community Forum](https://github.community/c/code-to-cloud/github-actions/41)

## Support

For issues with workflows:
1. Check the **Actions** tab for error details
2. Review this guide
3. Consult GitHub Actions documentation
4. Ask in repository issues
