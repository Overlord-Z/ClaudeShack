# ClaudeShack Repository Setup Guide

This guide will walk you through making ClaudeShack public and configuring it for community collaboration.

## Step 1: Make Repository Public

1. Go to https://github.com/Overlord-Z/ClaudeShack
2. Click **Settings** (top right)
3. Scroll to the bottom of the page to **Danger Zone**
4. Click **Change visibility**
5. Select **Make public**
6. Type the repository name to confirm: `ClaudeShack`
7. Click **I understand, make this repository public**

## Step 2: Configure Repository Settings

### General Settings

In **Settings** → **General**:

**Features** (Enable these):
- ✅ Issues
- ✅ Discussions (for Q&A and community chat)
- ✅ Projects (for tracking feedback)
- ✅ Preserve this repository (to archive if needed)
- ✅ Allow auto-merge
- ❌ Wikis (not needed, we have docs)
- ❌ Sponsorships (unless you want to enable)

**Pull Requests** (Configure these):
- ✅ Allow merge commits
- ✅ Allow squash merging (recommended for clean history)
- ✅ Allow rebase merging
- ✅ Always suggest updating pull request branches
- ✅ Allow auto-merge
- ✅ Automatically delete head branches

**Social Preview** (Optional but recommended):
- Upload a social preview image (1280x640px)
- This shows up when sharing the repo on social media

## Step 3: Set Up Branch Protection

In **Settings** → **Branches**:

1. Click **Add branch protection rule**
2. Branch name pattern: `main`
3. Enable these settings:

**Protect matching branches**:
- ✅ Require a pull request before merging
  - ✅ Require approvals: 1 (for now, can increase later)
  - ✅ Dismiss stale pull request approvals when new commits are pushed
- ✅ Require status checks to pass before merging
  - ❌ Require branches to be up to date (can enable later when you have CI)
- ✅ Require conversation resolution before merging
- ❌ Require signed commits (nice to have but not required)
- ✅ Require linear history (keeps history clean)
- ✅ Include administrators (even you need PRs for main)

4. Click **Create** to save

## Step 4: Enable GitHub Discussions

In **Settings** → **General** → **Features**:

1. Check **Discussions**
2. Click **Set up discussions**
3. Create these discussion categories:

**Categories to Add**:
- **Announcements** - Project updates and releases (locked, maintainers only)
- **General** - General chat and discussions
- **Ideas** - Feature ideas and suggestions
- **Q&A** - Questions and answers
- **Skill Showcase** - Share how you use ClaudeShack skills
- **Telemetry** - Anonymous usage metrics (for Evaluator)

4. Pin important discussions:
   - Welcome message
   - How to contribute
   - FAQ

## Step 5: Set Up GitHub Projects

In **Projects** → **New project**:

### Create "Skill Feedback Tracker" Project

1. Click **New project**
2. Name: "Skill Feedback Tracker"
3. Template: **Board**
4. Create these columns:

**Columns**:
- 📥 **New Feedback** - Newly submitted feedback (triage needed)
- 🔍 **Investigating** - Being reviewed by maintainers
- 📋 **Planned** - Approved for implementation
- 🚧 **In Progress** - Currently being worked on
- ✅ **Completed** - Implemented and released
- 🚫 **Won't Fix** - Decided not to implement (with reason)

5. Configure automation:
   - Auto-add issues with label `feedback`
   - Auto-move to "In Progress" when PR opened
   - Auto-move to "Completed" when PR merged

### Create "Roadmap" Project

1. Name: "ClaudeShack Roadmap"
2. Template: **Roadmap**
3. Add milestones:
   - v1.0 Release
   - Guardian v2
   - Oracle Enhancements
   - New Skills

## Step 6: Configure Issue Templates

✅ Already done! You have:
- `bug_report.yml`
- `feature_request.yml`
- `skill_feedback.yml`
- `config.yml` (directs users to discussions)

### Verify Templates

1. Go to **Issues** → **New issue**
2. You should see:
   - 🐛 Bug Report
   - ✨ Feature Request
   - ⭐ Skill Feedback
   - 💬 Links to Discussions and Docs

If they don't show up, ensure files are in `.github/ISSUE_TEMPLATE/`

## Step 7: Add Topics/Tags

In the **About** section (top right of repo):

1. Click the ⚙️ gear icon
2. Add these topics:

```
claude-code
ai-tools
code-review
developer-tools
productivity
python
knowledge-management
code-quality
automation
ai-agents
```

3. Add description:
```
🏛️ Production-ready skills for Claude Code: Oracle (knowledge), Guardian (quality gates), Summoner (orchestration), Evaluator (telemetry). Privacy-first, community-driven.
```

4. Add website (if you have docs hosted)
5. Save changes

## Step 8: Create Initial Releases

### Tag Current State

```bash
# Tag the current version
git tag -a v1.0.0 -m "Initial public release

- Oracle skill: Knowledge management
- Guardian skill: Quality gates and session monitoring
- Summoner skill: Subagent orchestration
- Evaluator skill: Privacy-first telemetry
- Complete documentation
- Issue templates and PR templates
- Contributing guidelines"

git push origin v1.0.0
```

### Create GitHub Release

1. Go to **Releases** → **Draft a new release**
2. Choose tag: `v1.0.0`
3. Release title: `v1.0.0 - Initial Public Release`
4. Description:

```markdown
# ClaudeShack v1.0.0

First public release of ClaudeShack! 🎉

## What's Included

### Core Skills

- **Oracle**: Knowledge management and pattern storage
- **Guardian**: Automatic quality gates and session health monitoring
- **Summoner**: Subagent orchestration (stub)
- **Evaluator**: Privacy-first telemetry and feedback collection

### Guardian Templates

- Security Review (OWASP Top 10)
- Performance Review (optimization focus)
- Feature Planning (task breakdown)

### Infrastructure

- Comprehensive documentation
- Issue templates (bug, feature, feedback)
- Pull request template
- Contributing guidelines
- Code of conduct
- Privacy-first telemetry framework

## Key Features

✅ **Privacy First**: Opt-in telemetry, no PII collection
✅ **Minimal Context Passing**: Efficient subagent usage
✅ **Read-Only Subagents**: Safety by design
✅ **Community-Driven**: GitHub-native feedback system
✅ **Production Ready**: Code reviewed, tested, documented

## Installation

```bash
git clone https://github.com/Overlord-Z/ClaudeShack.git
cd ClaudeShack
# See README.md for usage
```

## Documentation

- [README](README.md)
- [Contributing Guidelines](CONTRIBUTING.md)
- [Code of Conduct](CODE_OF_CONDUCT.md)

## Feedback

We want to hear from you!
- 📝 [Submit Feedback](https://github.com/Overlord-Z/ClaudeShack/issues/new/choose)
- 💬 [Join Discussions](https://github.com/Overlord-Z/ClaudeShack/discussions)

## What's Next

See our [Roadmap](https://github.com/Overlord-Z/ClaudeShack/projects) for planned features.
```

5. Click **Publish release**

## Step 9: Set Up Repository Labels

Go to **Issues** → **Labels**, add these:

**Priority Labels**:
- `priority: critical` (red)
- `priority: high` (orange)
- `priority: medium` (yellow)
- `priority: low` (green)

**Type Labels**:
- `bug` (red) - Something isn't working
- `enhancement` (blue) - New feature or request
- `documentation` (blue) - Documentation improvements
- `feedback` (purple) - User feedback
- `skill` (green) - Related to a specific skill

**Skill Labels**:
- `skill: oracle` (teal)
- `skill: guardian` (teal)
- `skill: summoner` (teal)
- `skill: evaluator` (teal)

**Status Labels**:
- `triage` (yellow) - Needs initial review
- `in-progress` (blue) - Being worked on
- `blocked` (red) - Blocked by something
- `wont-fix` (gray) - Won't be implemented

**Special Labels**:
- `good first issue` (green) - Good for newcomers
- `help wanted` (green) - Extra attention needed
- `question` (pink) - Further information requested
- `duplicate` (gray) - Duplicate of another issue

## Step 10: Configure Notifications

For yourself (repo owner):

1. Click **Watch** → **Custom**
2. Enable:
   - ✅ Issues
   - ✅ Pull requests
   - ✅ Discussions
   - ✅ Releases
3. Click **Apply**

## Step 11: Add README Badges

Update your README.md with badges:

```markdown
# ClaudeShack

[![GitHub Stars](https://img.shields.io/github/stars/Overlord-Z/ClaudeShack?style=social)](https://github.com/Overlord-Z/ClaudeShack/stargazers)
[![GitHub Issues](https://img.shields.io/github/issues/Overlord-Z/ClaudeShack)](https://github.com/Overlord-Z/ClaudeShack/issues)
[![GitHub Pull Requests](https://img.shields.io/github/issues-pr/Overlord-Z/ClaudeShack)](https://github.com/Overlord-Z/ClaudeShack/pulls)
[![License](https://img.shields.io/github/license/Overlord-Z/ClaudeShack)](LICENSE)
[![Code of Conduct](https://img.shields.io/badge/Contributor%20Covenant-2.0-4baaaa.svg)](CODE_OF_CONDUCT.md)
```

## Step 12: Social Media & Promotion (Optional)

### Share on Social Media

**Twitter/X**:
```
🎉 Excited to announce ClaudeShack - a collection of production-ready skills for @AnthropicAI Claude Code!

✨ Oracle: Knowledge management
🛡️ Guardian: Quality gates
🤖 Summoner: Orchestration
📊 Evaluator: Privacy-first telemetry

Check it out: https://github.com/Overlord-Z/ClaudeShack

#AI #ClaudeCode #DeveloperTools
```

**Reddit** (r/ClaudeAI, r/programming):
```
Title: ClaudeShack - Production-ready skills for Claude Code

Body: I've been working on a collection of skills for Claude Code and just made it public. Includes knowledge management (Oracle), automatic quality gates (Guardian), and privacy-first telemetry (Evaluator).

All designed with privacy first, minimal context passing, and community feedback in mind.

Would love to hear your thoughts!
```

### Submit to Relevant Lists

- Awesome Claude Code lists
- Awesome AI Tools lists
- Product Hunt (if you want visibility)

## Step 13: Set Up Continuous Integration (Optional but Recommended)

Create `.github/workflows/lint.yml`:

```yaml
name: Lint

on: [push, pull_request]

jobs:
  lint:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-python@v4
        with:
          python-version: '3.11'
      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          pip install flake8 mypy
      - name: Lint with flake8
        run: |
          flake8 skills/ --count --select=E9,F63,F7,F82 --show-source --statistics
      - name: Type check with mypy
        run: |
          mypy skills/ --ignore-missing-imports || true
```

## Verification Checklist

After completing all steps, verify:

- [ ] Repository is public
- [ ] Issues are enabled and templates show up
- [ ] Discussions are enabled with proper categories
- [ ] Projects are set up for feedback tracking
- [ ] Branch protection rules are active on `main`
- [ ] Labels are created and organized
- [ ] Topics/tags are added
- [ ] README has badges
- [ ] v1.0.0 release is published
- [ ] Contributing guide is comprehensive
- [ ] Code of conduct is present
- [ ] Pull request template works
- [ ] Notifications are configured

## Ongoing Maintenance

### Weekly Tasks
- Review new issues and apply labels
- Triage feedback
- Respond to discussions

### Monthly Tasks
- Review and merge PRs
- Update roadmap
- Publish aggregate telemetry (if using Evaluator)
- Tag new releases as needed

### Quarterly Tasks
- Publish transparency report (for Evaluator users)
- Review and update documentation
- Clean up stale issues
- Celebrate contributors!

---

## Need Help?

If you run into issues:
1. Check GitHub's documentation: https://docs.github.com
2. Open a discussion in the repo
3. Reach out to the community

**Congratulations!** Your repository is now ready for the community! 🎉
