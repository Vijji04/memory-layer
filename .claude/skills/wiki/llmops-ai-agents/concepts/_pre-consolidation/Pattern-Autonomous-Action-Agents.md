---
title: Pattern: Autonomous Action Agents
created: 2026-05-12
updated: 2026-05-12
type: concept
tags: [phase-2, llmops-ai-agents, concept, patterns, autonomous, tool-use, case-studies]
confidence: high
source_files: 1
---

# Pattern: Autonomous Action Agents

When agents move beyond retrieval and conversation into action—making code changes, scheduling shifts, generating configurations—the game changes. You now have to worry about broken systems, violated constraints, and cascading failures. This section covers three real deployments where agents not only reason but execute, and the safeguards that make that viable.

The core challenge: **actions are irreversible or expensive to undo**. A wrong response to a customer is embarrassing. A wrong code change breaks production. A wrong shift assignment leaves a warehouse understaffed. You need verification layers, human approval gates, and rollback capability.

---

## Case Study 1: Spotify — Background Coding Agents for Large-Scale Maintenance

### The Business Problem

Spotify has thousands of microservices, each with hundreds of dependencies. Over time, dependencies drift:
- **Security vulnerabilities** (Log4j, etc.) need patching
- **Deprecated APIs** need migration to new versions
- **Outdated patterns** (old auth, old logging) need refactoring

Manually fixing each repo is untenable. A single engineer can't fix 5,000 repos. Spotify built **autonomous coding agents** that:

1. Take a task (e.g., "upgrade Kotlin from 1.7 to 1.8")
2. Read the codebase (find build files, config, usage)
3. Plan the upgrade (identify all affected files, breaking changes)
4. Make changes (rewrite code, update configs, fix compilation errors)
5. Run tests (ensure nothing breaks)
6. Create PR (with description and reasoning)
7. Wait for human review (no auto-merge)

The system has fixed 100,000+ dependencies with <1% false-positive rate (changes that break tests or violate style).

### Why This Pattern Fits

**Autonomous action agents** solve the scale problem:
- **Deterministic, repeatable task** (dependency upgrade follows a known pattern)
- **Full context available** (codebase, test suite, build system are all accessible)
- **Verification built-in** (tests pass/fail objectively)
- **Human approval gate** (PR review catches edge cases)
- **Rollback capability** (bad PR gets reverted)

Differs from RAG agents (no retrieval needed) and conversational agents (no user interaction needed). Here, the agent is an engineer: reads code, reasons about changes, writes new code, verifies it works.

### Architecture Diagram

```
┌──────────────────────────────────────────────┐
│  Maintenance Task Queue                      │
│  "Upgrade Kotlin from 1.7 to 1.8 in 500 repos" │
└──────────────┬───────────────────────────────┘
               │
     ┌─────────▼─────────────┐
     │  Task Dispatcher      │
     │                       │
     │  Split into 500       │
     │  individual tasks:    │
     │  repo_A: upgrade      │
     │  repo_B: upgrade      │
     │  ...                  │
     └─────────┬─────────────┘
               │
     ┌─────────▼──────────────────┐
     │  Coding Agent Worker       │
     │  (for one repo)            │
     │                            │
     │  1. Clone repo             │
     │  2. Analyze codebase       │
     │  3. Plan changes           │
     │  4. Implement changes      │
     │  5. Run tests              │
     │  6. Create PR              │
     └─────────┬──────────────────┘
               │
     ┌─────────▼──────────────────────────┐
     │  Agent: Analyze & Plan            │
     │                                   │
     │  • Find build.gradle, pom.xml      │
     │  • Find usages of Kotlin API       │
     │  • Identify breaking changes      │
     │  • Plan rewrite (which files)      │
     │                                   │
     │  Output: structured change plan   │
     └─────────┬──────────────────────────┘
               │
     ┌─────────▼──────────────────────────┐
     │  Agent: Implement Changes         │
     │                                   │
     │  • Rewrite files per plan         │
     │  • Update configs                 │
     │  • Verify syntax                  │
     │                                   │
     │  Output: git diff, new code       │
     └─────────┬──────────────────────────┘
               │
     ┌─────────▼──────────────────────────┐
     │  Verify Layer: Run Tests          │
     │                                   │
     │  • ./gradlew test                 │
     │  • Check exit code                │
     │  • Parse output for failures      │
     │  • If FAIL: agent fixes or gives │
     │    up                             │
     └─────────┬──────────────────────────┘
               │
     ┌─────────▼──────────────────────────┐
     │  Create PR                        │
     │                                   │
     │  Branch: kotlin-upgrade-1.7-1.8   │
     │  Title: [AUTO] Upgrade Kotlin 1.7→1.8 │
     │  Description: (AI-generated)      │
     │  Reason: [Security|Tech Debt|etc] │
     │                                   │
     │  Wait for human review + approval │
     └─────────────────────────────────────┘
```

### Implementation: Key Components

#### 1. Codebase Analysis & Planning

```python
from typing import List, Dict
import anthropic
import subprocess
import os

class CodebaseAnalyzer:
    """
    Analyze codebase to understand current state and plan changes.
    
    For dependency upgrade task:
    1. Find build files (gradle, maven, npm, etc.)
    2. Find current dependency version
    3. Find all usages of that dependency
    4. Identify breaking changes from changelog
    5. Plan which files need modification
    """
    
    def __init__(self, repo_path: str):
        self.repo_path = repo_path
        self.client = anthropic.Anthropic()
    
    def analyze_dependency(
        self,
        dependency_name: str,
        current_version: str,
        target_version: str
    ) -> Dict:
        """
        Analyze how a dependency upgrade would impact this repo.
        
        Returns:
            {
                'current_version': str,
                'target_version': str,
                'build_files': List[str],
                'usages': List[Dict],
                'breaking_changes': List[str],
                'risk_level': 'low|medium|high',
                'change_plan': str
            }
        """
        
        # Step 1: Find build files
        build_files = self._find_build_files(dependency_name)
        
        # Step 2: Find usages in source code
        usages = self._find_usages(dependency_name)
        
        # Step 3: Fetch changelog (simplified; would integrate with Maven Central, npm registry, etc.)
        changelog = self._fetch_changelog(dependency_name, current_version, target_version)
        
        # Step 4: Use LLM to plan changes
        plan_prompt = f"""You are a senior developer planning a dependency upgrade.

Dependency: {dependency_name}
Current version: {current_version}
Target version: {target_version}

Build files found:
{json.dumps(build_files, indent=2)}

Usages in code (first 10):
{json.dumps(usages[:10], indent=2)}

Changelog summary:
{changelog}

Create a detailed plan for upgrading this dependency:
1. What files need to be modified?
2. What breaking changes will we face?
3. What's the risk level (low/medium/high)?
4. What's the upgrade sequence?

Be specific: list exact files and the kind of change (update version, API migration, config change, etc.)"""
        
        response = self.client.messages.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens=1500,
            messages=[{"role": "user", "content": plan_prompt}]
        )
        
        plan_text = response.content[0].text
        
        # Extract risk level (heuristic)
        risk_level = "medium"
        if "breaking change" in plan_text.lower():
            risk_level = "high"
        elif "simple" in plan_text.lower() or "backward compatible" in plan_text.lower():
            risk_level = "low"
        
        return {
            'current_version': current_version,
            'target_version': target_version,
            'build_files': build_files,
            'usages': usages,
            'breaking_changes': self._extract_breaking_changes(plan_text),
            'risk_level': risk_level,
            'change_plan': plan_text
        }
    
    def _find_build_files(self, dependency_name: str) -> List[str]:
        """Find all build configuration files."""
        build_patterns = [
            'build.gradle', 'build.gradle.kts',  # Gradle
            'pom.xml',                           # Maven
            'package.json', 'package-lock.json', # npm
            'pyproject.toml', 'requirements.txt' # Python
        ]
        
        found = []
        for root, dirs, files in os.walk(self.repo_path):
            for pattern in build_patterns:
                for file in files:
                    if file == pattern or pattern in file:
                        full_path = os.path.join(root, file)
                        found.append(os.path.relpath(full_path, self.repo_path))
        
        return found
    
    def _find_usages(self, dependency_name: str) -> List[Dict]:
        """Find all files using this dependency."""
        usages = []
        
        # Search for imports/uses of this dependency
        for root, dirs, files in os.walk(self.repo_path):
            # Skip build dirs
            dirs[:] = [d for d in dirs if d not in ['node_modules', 'target', '.gradle']]
            
            for file in files:
                if file.endswith(('.java', '.kt', '.py', '.js', '.ts')):
                    full_path = os.path.join(root, file)
                    try:
                        with open(full_path) as f:
                            content = f.read()
                            if dependency_name in content:
                                # Count occurrences
                                count = content.count(dependency_name)
                                usages.append({
                                    'file': os.path.relpath(full_path, self.repo_path),
                                    'occurrences': count
                                })
                    except:
                        pass
        
        return sorted(usages, key=lambda x: x['occurrences'], reverse=True)
    
    def _fetch_changelog(self, dep: str, old_v: str, new_v: str) -> str:
        """Fetch changelog summary (simplified)."""
        # In production, would call Maven Central, npm registry, etc.
        return f"Changelog for {dep} {old_v} → {new_v}: check official release notes"
    
    def _extract_breaking_changes(self, plan_text: str) -> List[str]:
        """Extract breaking changes mentioned in plan."""
        changes = []
        lines = plan_text.split('\n')
        for line in lines:
            if 'breaking' in line.lower() or 'deprecated' in line.lower():
                changes.append(line.strip())
        return changes

# Usage
analyzer = CodebaseAnalyzer('/path/to/repo')
analysis = analyzer.analyze_dependency(
    'kotlinx-serialization',
    '1.5.0',
    '1.6.0'
)

print(f"Risk level: {analysis['risk_level']}")
print(f"Files affected: {len(analysis['usages'])}")
print(f"Breaking changes: {analysis['breaking_changes']}")
print(f"\nChange plan:\n{analysis['change_plan']}")
```

#### 2. Autonomous Code Modification

```python
from typing import List, Tuple
import json

class AutonomousCodeModifier:
    """
    Make code changes autonomously based on plan.
    
    Process:
    1. Read files affected by upgrade
    2. For each file: generate modifications using LLM
    3. Apply changes to disk
    4. Verify syntax (compile check)
    5. Return list of modified files
    """
    
    def __init__(self, repo_path: str):
        self.repo_path = repo_path
        self.client = anthropic.Anthropic()
        self.modified_files = []
    
    def apply_changes(
        self,
        analysis: Dict,
        usages: List[Dict]
    ) -> Dict:
        """
        Apply code changes based on analysis.
        
        Returns:
            {
                'success': bool,
                'modified_files': List[str],
                'compilation_errors': List[str],
                'summary': str
            }
        """
        
        compilation_errors = []
        
        # Step 1: Update build files
        for build_file in analysis['build_files']:
            result = self._update_build_file(
                build_file,
                analysis['current_version'],
                analysis['target_version']
            )
            if result['success']:
                self.modified_files.append(build_file)
        
        # Step 2: Update source files
        for usage in usages:
            result = self._update_source_file(
                usage['file'],
                analysis['breaking_changes'],
                analysis['change_plan']
            )
            if result['success']:
                self.modified_files.append(usage['file'])
            else:
                compilation_errors.extend(result.get('errors', []))
        
        # Step 3: Try to compile/verify syntax
        compile_result = self._verify_syntax()
        if not compile_result['success']:
            compilation_errors.extend(compile_result.get('errors', []))
        
        return {
            'success': len(compilation_errors) == 0,
            'modified_files': self.modified_files,
            'compilation_errors': compilation_errors,
            'summary': f"Modified {len(self.modified_files)} files. "
                      f"Compilation: {'✓' if not compilation_errors else '✗'}"
        }
    
    def _update_build_file(
        self,
        build_file: str,
        old_version: str,
        new_version: str
    ) -> Dict:
        """
        Update version in build file (gradle, maven, npm, etc.)
        """
        full_path = os.path.join(self.repo_path, build_file)
        
        try:
            with open(full_path) as f:
                content = f.read()
            
            # Simple regex replacement (production would be more sophisticated)
            updated = content.replace(old_version, new_version)
            
            if updated != content:
                with open(full_path, 'w') as f:
                    f.write(updated)
                
                return {
                    'success': True,
                    'file': build_file,
                    'changes': 1
                }
            else:
                return {
                    'success': False,
                    'file': build_file,
                    'error': 'Version string not found'
                }
        except Exception as e:
            return {
                'success': False,
                'file': build_file,
                'error': str(e)
            }
    
    def _update_source_file(
        self,
        source_file: str,
        breaking_changes: List[str],
        change_plan: str
    ) -> Dict:
        """
        Update source code for API changes.
        """
        full_path = os.path.join(self.repo_path, source_file)
        
        try:
            with open(full_path) as f:
                content = f.read()
            
            # Use LLM to suggest specific changes
            prompt = f"""Update this source file for dependency upgrade.

File: {source_file}
Type: {'Kotlin' if source_file.endswith('.kt') else 'Java' if source_file.endswith('.java') else 'Other'}

Current code:
```
{content[:2000]}  # First 2000 chars
```

Breaking changes:
{json.dumps(breaking_changes, indent=2)}

Change plan summary:
{change_plan[:500]}

Generate the EXACT updated code for this file.
Only output the updated code block, no explanation.
Preserve formatting and comments."""
            
            response = self.client.messages.create(
                model="claude-3-5-sonnet-20241022",
                max_tokens=2000,
                messages=[{"role": "user", "content": prompt}]
            )
            
            updated_content = response.content[0].text
            
            # Extract code block if wrapped in ```
            if '```' in updated_content:
                updated_content = updated_content.split('```')[1]
                if updated_content.startswith(('kotlin', 'java')):
                    updated_content = updated_content[7:]  # Strip language marker
            
            # Write changes
            with open(full_path, 'w') as f:
                f.write(updated_content)
            
            return {
                'success': True,
                'file': source_file,
                'changes': 1
            }
        except Exception as e:
            return {
                'success': False,
                'file': source_file,
                'error': str(e),
                'errors': [str(e)]
            }
    
    def _verify_syntax(self) -> Dict:
        """
        Compile/verify syntax of modified code.
        """
        try:
            # Try to compile (Gradle example)
            result = subprocess.run(
                ['gradle', 'build', '-q'],
                cwd=self.repo_path,
                capture_output=True,
                timeout=300,
                text=True
            )
            
            if result.returncode == 0:
                return {'success': True}
            else:
                # Parse compilation errors
                errors = result.stderr.split('\n')
                return {
                    'success': False,
                    'errors': [e for e in errors if e.strip()][:5]  # First 5 errors
                }
        except subprocess.TimeoutExpired:
            return {
                'success': False,
                'errors': ['Compilation timed out (>5min)']
            }
        except Exception as e:
            return {
                'success': False,
                'errors': [f'Compilation check failed: {str(e)}']
            }

# Usage
modifier = AutonomousCodeModifier('/path/to/repo')
result = modifier.apply_changes(analysis, analysis['usages'])

print(f"Success: {result['success']}")
print(f"Modified files: {result['modified_files']}")
if result['compilation_errors']:
    print(f"Errors: {result['compilation_errors']}")
```

#### 3. Test-Based Verification & Validation

```python
from dataclasses import dataclass

@dataclass
class TestResult:
    passed: bool
    total_tests: int
    failed_tests: int
    flaky_tests: int
    duration_seconds: float
    error_details: List[str]

class TestVerifier:
    """
    Run full test suite to verify changes don't break anything.
    """
    
    def __init__(self, repo_path: str):
        self.repo_path = repo_path
    
    def run_tests(self, timeout: int = 600) -> TestResult:
        """
        Run test suite. Parse results.
        
        Returns:
            {
                'passed': bool,
                'total_tests': int,
                'failed_tests': List[str],
                'duration': float,
                'output': str
            }
        """
        
        try:
            start = time.time()
            
            # Run tests (gradle example; adapt for Maven, npm, etc.)
            result = subprocess.run(
                ['gradle', 'test', '--continue', '-q'],
                cwd=self.repo_path,
                capture_output=True,
                timeout=timeout,
                text=True
            )
            
            duration = time.time() - start
            
            # Parse output
            output = result.stdout + result.stderr
            
            # Extract test counts (heuristic parsing)
            total_tests = self._extract_test_count(output, 'total')
            failed_tests = self._extract_test_count(output, 'failed')
            
            passed = result.returncode == 0 and failed_tests == 0
            
            return TestResult(
                passed=passed,
                total_tests=total_tests,
                failed_tests=failed_tests,
                flaky_tests=0,
                duration_seconds=duration,
                error_details=self._parse_failures(output) if not passed else []
            )
        
        except subprocess.TimeoutExpired:
            return TestResult(
                passed=False,
                total_tests=0,
                failed_tests=0,
                flaky_tests=0,
                duration_seconds=timeout,
                error_details=['Tests timed out (>10min)']
            )
        except Exception as e:
            return TestResult(
                passed=False,
                total_tests=0,
                failed_tests=0,
                flaky_tests=0,
                duration_seconds=0,
                error_details=[f'Test run failed: {str(e)}']
            )
    
    def _extract_test_count(self, output: str, test_type: str) -> int:
        """Extract test count from output."""
        # Simplified; would parse Gradle/Maven output more carefully
        if test_type == 'total':
            match = re.search(r'(\d+) test', output)
        else:
            match = re.search(r'(\d+) failed', output)
        
        return int(match.group(1)) if match else 0
    
    def _parse_failures(self, output: str) -> List[str]:
        """Extract failed test names and error messages."""
        failures = []
        lines = output.split('\n')
        
        for i, line in enumerate(lines):
            if 'FAILED' in line or 'ERROR' in line:
                failures.append(line.strip())
                # Grab next few lines for context
                for j in range(1, 3):
                    if i + j < len(lines):
                        failures.append(lines[i + j].strip())
        
        return failures[:10]  # Return first 10 failures

# Usage
verifier = TestVerifier('/path/to/repo')
test_result = verifier.run_tests()

if test_result.passed:
    print(f"✓ All {test_result.total_tests} tests passed ({test_result.duration_seconds:.1f}s)")
else:
    print(f"✗ {test_result.failed_tests} test(s) failed")
    for error in test_result.error_details[:3]:
        print(f"  - {error}")
```

#### 4. PR Creation & Human Review Gate

```python
import subprocess

class PRCreator:
    """
    Create PR on GitHub/GitLab/etc.
    Wait for human review and approval before merging.
    """
    
    def __init__(self, repo_path: str, repo_url: str, api_token: str):
        self.repo_path = repo_path
        self.repo_url = repo_url
        self.api_token = api_token
        self.client = anthropic.Anthropic()
    
    def create_pr(
        self,
        analysis: Dict,
        test_result: TestResult,
        modified_files: List[str]
    ) -> Dict:
        """
        Create PR with all necessary context for human review.
        
        Returns:
            {
                'pr_url': str,
                'pr_number': int,
                'branch': str,
                'title': str,
                'body': str
            }
        """
        
        # Step 1: Create branch
        branch_name = f"auto/upgrade-{analysis['dependency_name']}-{analysis['target_version']}"
        
        try:
            subprocess.run(
                ['git', 'checkout', '-b', branch_name],
                cwd=self.repo_path,
                check=True,
                capture_output=True
            )
            
            # Step 2: Commit changes
            subprocess.run(
                ['git', 'add', '.'],
                cwd=self.repo_path,
                check=True,
                capture_output=True
            )
            
            commit_message = f"[AUTO] Upgrade {analysis['dependency_name']} {analysis['current_version']} → {analysis['target_version']}"
            
            subprocess.run(
                ['git', 'commit', '-m', commit_message],
                cwd=self.repo_path,
                check=True,
                capture_output=True
            )
            
            # Step 3: Push branch
            subprocess.run(
                ['git', 'push', 'origin', branch_name],
                cwd=self.repo_path,
                check=True,
                capture_output=True
            )
            
        except subprocess.CalledProcessError as e:
            return {
                'success': False,
                'error': f'Git operation failed: {str(e)}'
            }
        
        # Step 4: Generate PR description
        pr_body = self._generate_pr_description(
            analysis,
            test_result,
            modified_files
        )
        
        # Step 5: Create PR via API
        pr_data = self._create_pr_via_api(
            branch_name,
            analysis,
            pr_body
        )
        
        return {
            'success': True,
            'pr_url': pr_data.get('html_url'),
            'pr_number': pr_data.get('number'),
            'branch': branch_name,
            'title': f"[AUTO] Upgrade {analysis['dependency_name']} {analysis['current_version']} → {analysis['target_version']}",
            'body': pr_body
        }
    
    def _generate_pr_description(
        self,
        analysis: Dict,
        test_result: TestResult,
        modified_files: List[str]
    ) -> str:
        """
        Generate detailed PR description for human reviewer.
        """
        
        description = f"""## Automated Dependency Upgrade

**Dependency**: {analysis['dependency_name']}
**From**: {analysis['current_version']} → **To**: {analysis['target_version']}

**Risk Level**: {analysis['risk_level'].upper()}

### Changes
- Modified {len(modified_files)} file(s)
- Updated build configurations: {', '.join(analysis['build_files'])}
- Updated source code in {len(analysis['usages'])} file(s)

### Breaking Changes
"""
        
        if analysis['breaking_changes']:
            for change in analysis['breaking_changes']:
                description += f"- {change}\n"
        else:
            description += "- None detected\n"
        
        ### Test Results
        description += f"""
### Test Results
- Total tests: {test_result.total_tests}
- Passed: {'✓' if test_result.passed else '✗'}
- Duration: {test_result.duration_seconds:.1f}s
"""
        
        if test_result.error_details:
            description += "\n**Failed tests:**\n"
            for error in test_result.error_details[:5]:
                description += f"- {error}\n"
        
        description += """
### Upgrade Plan
"""
        description += analysis['change_plan'][:500] + "...\n"
        
        description += """
---
⚠️ **This PR was created automatically. Please review carefully.**

- [ ] Changes make sense for this repo
- [ ] Breaking changes are handled correctly
- [ ] Tests pass on your CI
- [ ] No unintended modifications

If anything looks wrong, just close this PR and the branch will be cleaned up.
"""
        
        return description
    
    def _create_pr_via_api(
        self,
        branch_name: str,
        analysis: Dict,
        body: str
    ) -> Dict:
        """
        Create PR via GitHub/GitLab API.
        """
        # Example: GitHub API
        # In production, would use PyGithub, python-gitlab, etc.
        
        import requests
        
        repo_parts = self.repo_url.replace('https://github.com/', '').replace('.git', '')
        owner, repo = repo_parts.split('/')
        
        url = f"https://api.github.com/repos/{owner}/{repo}/pulls"
        
        headers = {
            'Authorization': f'token {self.api_token}',
            'Accept': 'application/vnd.github.v3+json'
        }
        
        payload = {
            'title': f"[AUTO] Upgrade {analysis['dependency_name']} {analysis['current_version']} → {analysis['target_version']}",
            'body': body,
            'head': branch_name,
            'base': 'main'
        }
        
        try:
            response = requests.post(url, json=payload, headers=headers, timeout=10)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            return {'success': False, 'error': str(e)}

# Usage
pr_creator = PRCreator(
    repo_path='/path/to/repo',
    repo_url='https://github.com/spotify/backstage.git',
    api_token='ghp_xxx'
)

pr_result = pr_creator.create_pr(analysis, test_result, modifier.modified_files)

if pr_result['success']:
    print(f"✓ PR created: {pr_result['pr_url']}")
    print(f"  Branch: {pr_result['branch']}")
    print(f"  Waiting for human review...")
else:
    print(f"✗ PR creation failed: {pr_result.get('error')}")
```

### Design Decisions & Why

**1. Why Test-Based Verification?**
- Tests are objective truth: pass/fail is deterministic
- Failures are specific (which test failed, what was the error)
- If tests pass, high confidence the change is safe
- Alternative (linting, style checks) is not sufficient; code could compile but be wrong

**2. Why PR Instead of Auto-Merge?**
- Humans catch edge cases agents miss (domain-specific logic, business rules)
- PR review is audit trail (why was this approved?)
- Easy rollback: just revert the PR
- Agent can't know every rule (some repos forbid certain changes)

**3. Why Create Branch First, Then PR?**
- Keeps changes isolated (other commits don't interfere)
- If tests fail, only this branch is affected
- If PR is rejected, just delete branch (no cleanup needed)
- CI/CD runs on branch before merge (additional verification)

**4. Why Detailed PR Description?**
- Reviewer needs context: what changed, why, what risks
- Breaking changes are called out explicitly
- Test results are visible (reviewer trusts tests passed)
- Agent's reasoning is documented (why was this change made)

**5. Why Escalate on Failed Tests?**
- Don't auto-merge if tests fail (safety first)
- Agent could try to fix (retry logic), but better to escalate
- Human can debug what broke
- Cost of escalation < cost of broken production

### Key Takeaways

1. **Autonomous code changes need test verification**: tests are your safety net. If tests fail, escalate.

2. **Plan before acting**: analyze codebase, identify breaking changes, plan sequence of changes. Don't just rewrite blindly.

3. **Use PRs as approval gates**: don't auto-merge. Human review catches edge cases. PR is audit trail.

4. **Make descriptions actionable**: reviewer needs to understand what changed, why, and what risks exist.

5. **Fail fast, escalate eagerly**: if tests fail, compilation fails, or syntax is wrong, escalate to human. Better safe than wrong.

---

## Case Study 2: Manchester Airports Group — Automated Absence Reporting & Shift Management

### The Business Problem

Manchester Airports Group runs three airports with thousands of shift-based staff. When someone calls in sick:

1. **HR system** receives absence notification
2. **Staff database** must be updated
3. **Shift schedule** must be redistributed
4. **Replacement staff** must be notified
5. **Facility operations** must be aware (fewer cleaners = might clean less thoroughly)

Doing this manually takes 30+ minutes. An agent calls around, negotiates with staff, updates systems. With 100+ absences per day across three airports, this is untenable.

Manchester built an **automated absence orchestrator** that:
1. Receives absence notification (via HR system webhook)
2. Finds open shifts uncovered by the absence
3. Identifies replacement candidates (available, qualified, nearby)
4. Offers shift to candidates (via SMS/app notification)
5. Updates schedule in real-time
6. Notifies operations teams
7. Logs decision (audit trail)

Success rate: 85% of absences are automatically covered without human intervention. For the 15% that can't be auto-covered, a human gets involved.

### Why This Pattern Fits

**Orchestration pattern** solves the multi-system coordination problem:
- **Event trigger**: absence notification
- **Multi-step workflow**: check schedule → find replacement → notify → update systems
- **Branching logic**: if replacement found, proceed; if not, escalate
- **Rollback capability**: if staff declines, try next candidate
- **Audit trail**: every decision is logged

Differs from Spotify (deterministic upgrade) and both previous patterns:
- Not pure code change (touches 4+ business systems)
- Not pure conversation (no human involved in happy path)
- Highly stateful (must track which candidates were offered, what responses came back)

### Architecture Diagram

```
┌─────────────────────────────────────┐
│  Absence Notification (HR webhook)  │
│  Staff: John Smith, Date: Tomorrow  │
└────────────────┬────────────────────┘
                 │
    ┌────────────▼──────────────┐
    │  Orchestrator Agent       │
    │  - Parse notification     │
    │  - Extract: staff ID, date │
    │  - Determine: shifts lost  │
    └────────────┬───────────────┘
                 │
    ┌────────────▼────────────────────┐
    │  Schedule Query Agent          │
    │                                │
    │  Q: What shifts is John on?    │
    │  A: Terminal 2, 6am-2pm        │
    │     Passenger service,         │
    │     Level 4 clearance          │
    │                                │
    │  Q: What shifts are open now?  │
    │  A: Term 2, 6am-2pm            │
    │      (same slot, must cover)   │
    └────────────┬───────────────────┘
                 │
    ┌────────────▼────────────────────────────────┐
    │  Staff Matching Agent                       │
    │                                            │
    │  Criteria:                                  │
    │  - Available tomorrow 6am-2pm               │
    │  - Terminal 2 assigned (or cross-trained)   │
    │  - Clearance Level 4                        │
    │  - Not already working max hours            │
    │                                            │
    │  Candidates found:                          │
    │  1. Sarah (high match, nearby)              │
    │  2. Mike (medium match, farther)            │
    │  3. Priya (lower match, longer shift)       │
    └────────────┬───────────────────────────────┘
                 │
    ┌────────────▼─────────────────────────────┐
    │  Candidate Notification Agent (Sequential) │
    │                                          │
    │  Try Sarah:                               │
    │  - Send SMS: "Available 6am-2pm Term 2?" │
    │  - Wait 5 minutes for response            │
    │  - If YES → proceed                       │
    │  - If NO → try Mike                       │
    │  - If NO RESPONSE → try next, retry later │
    └────────────┬────────────────────────────┘
                 │
    ┌────────────▼────────────────────────────────┐
    │  Coverage Status                           │
    │                                            │
    │  If covered:                               │
    │  - Update schedule DB                      │
    │  - Notify operations: "Covered by Sarah"   │
    │  - Send confirmation to replacement       │
    │  - Log decision (audit trail)              │
    │                                            │
    │  If not covered:                           │
    │  - Escalate to human shift manager         │
    │  - Send alert: "Manual intervention needed │
    │  - Recommend overtime, external staff      │
    └────────────────────────────────────────────┘
```

### Implementation: Key Components

#### 1. Multi-System Agent Coordination

```python
from enum import Enum
from dataclasses import dataclass
from typing import Optional
import anthropic

class CoverageStatus(Enum):
    COVERED = "covered"
    PARTIALLY_COVERED = "partially_covered"
    UNCOVERED = "uncovered"
    ESCALATED = "escalated"

@dataclass
class ShiftRequirement:
    staff_id: str
    staff_name: str
    date: str
    terminal: str
    start_time: str
    end_time: str
    shift_type: str
    required_clearance: str
    passenger_facing: bool

@dataclass
class ReplacementCandidate:
    staff_id: str
    staff_name: str
    match_score: float  # 0-1, how well they fit
    availability: bool
    clearance_level: str
    current_assignments: List[str]
    location: str  # Which terminal currently based

class MultiSystemOrchestrator:
    """
    Coordinate across HR, Schedule, Notification, and Ops systems.
    """
    
    def __init__(self, hr_api, schedule_db, notification_service, ops_system):
        self.hr = hr_api
        self.schedule = schedule_db
        self.notifier = notification_service
        self.ops = ops_system
        self.client = anthropic.Anthropic()
    
    def handle_absence(
        self,
        staff_id: str,
        date: str,
        reason: str = None
    ) -> Dict:
        """
        End-to-end absence handling:
        1. Determine shifts to cover
        2. Find replacement candidates
        3. Try to cover shifts
        4. Update systems
        5. Log decision
        """
        
        # Step 1: Get shift requirements
        requirement = self._get_shift_requirement(staff_id, date)
        print(f"[1] Shift requirement: {requirement.staff_name} "
              f"{requirement.terminal} {requirement.start_time}-{requirement.end_time}")
        
        # Step 2: Find replacement candidates
        candidates = self._find_candidates(requirement)
        print(f"[2] Found {len(candidates)} candidate(s)")
        
        if not candidates:
            return self._escalate_absence(requirement, reason="No candidates available")
        
        # Step 3: Try to cover shifts with candidates (sequential)
        for candidate in candidates:
            print(f"[3] Trying: {candidate.staff_name} (match: {candidate.match_score:.2f})")
            
            # Offer shift to candidate
            response = self._offer_shift(candidate, requirement)
            
            if response['accepted']:
                print(f"[4] Accepted by {candidate.staff_name}")
                
                # Update systems
                self._update_systems(requirement, candidate)
                
                # Log decision
                self._log_coverage_decision(
                    requirement, candidate, response, "COVERED"
                )
                
                return {
                    'status': CoverageStatus.COVERED,
                    'replacement': candidate,
                    'shift_requirement': requirement
                }
            else:
                print(f"[4] Declined: {response.get('reason')}")
                # Try next candidate
                continue
        
        # If we get here, no one accepted
        return self._escalate_absence(requirement, reason="All candidates declined")
    
    def _get_shift_requirement(self, staff_id: str, date: str) -> ShiftRequirement:
        """Query schedule DB for staff's shifts on this date."""
        shifts = self.schedule.get_shifts(staff_id, date)
        
        if not shifts:
            raise ValueError(f"No shifts found for {staff_id} on {date}")
        
        # Take first shift (if multiple, would handle separately)
        shift = shifts[0]
        
        staff_info = self.hr.get_staff(staff_id)
        
        return ShiftRequirement(
            staff_id=staff_id,
            staff_name=staff_info['name'],
            date=date,
            terminal=shift['terminal'],
            start_time=shift['start'],
            end_time=shift['end'],
            shift_type=shift['type'],
            required_clearance=shift.get('clearance', 'Level 1'),
            passenger_facing=shift.get('passenger_facing', False)
        )
    
    def _find_candidates(self, requirement: ShiftRequirement) -> List[ReplacementCandidate]:
        """
        Find staff who could cover this shift.
        Score by fit: clearance, availability, location, experience.
        """
        
        # Query staff DB for candidates
        all_staff = self.hr.query_staff(
            terminal=requirement.terminal,
            clearance_min=requirement.required_clearance,
            active=True
        )
        
        candidates = []
        
        for staff in all_staff:
            # Check availability
            availability = self.schedule.is_available(
                staff['id'],
                requirement.date,
                requirement.start_time,
                requirement.end_time
            )
            
            if not availability:
                continue
            
            # Calculate match score
            match_score = self._calculate_match_score(staff, requirement)
            
            candidates.append(ReplacementCandidate(
                staff_id=staff['id'],
                staff_name=staff['name'],
                match_score=match_score,
                availability=True,
                clearance_level=staff['clearance'],
                current_assignments=staff.get('current_shifts', []),
                location=staff.get('location', requirement.terminal)
            ))
        
        # Sort by match score (highest first)
        candidates.sort(key=lambda c: c.match_score, reverse=True)
        
        return candidates[:5]  # Try top 5
    
    def _calculate_match_score(self, staff: Dict, requirement: ShiftRequirement) -> float:
        """
        Score staff member's fit for this shift.
        
        Factors:
        - Clearance level match
        - Experience with shift type
        - Current workload
        - Location (same terminal is better)
        - Overtime rules (can't exceed max hours)
        """
        
        score = 0.0
        
        # Clearance match (max 0.3 points)
        staff_clearance_level = int(staff['clearance'].split()[-1])
        required_level = int(requirement.required_clearance.split()[-1])
        if staff_clearance_level >= required_level:
            score += 0.3
        
        # Experience with shift type (0.2 points)
        if requirement.shift_type in staff.get('qualified_shifts', []):
            score += 0.2
        
        # Location bonus (0.2 points)
        if staff.get('location') == requirement.terminal:
            score += 0.2
        
        # Workload check (up to 0.2 points)
        current_hours = self.schedule.get_hours_this_week(staff['id'])
        max_weekly = 40
        available_capacity = max(0, max_weekly - current_hours)
        shift_hours = self._calculate_shift_hours(
            requirement.start_time,
            requirement.end_time
        )
        if shift_hours <= available_capacity:
            score += 0.2
        
        return min(score, 1.0)
    
    def _offer_shift(
        self,
        candidate: ReplacementCandidate,
        requirement: ShiftRequirement
    ) -> Dict:
        """
        Offer shift to candidate and wait for response.
        """
        
        message = f"""Hi {candidate.staff_name},

Are you available for a shift tomorrow?
{requirement.terminal}, {requirement.start_time}-{requirement.end_time}
Type: {requirement.shift_type}

Shift: {requirement.date}

Reply: YES or NO"""
        
        # Send notification
        contact = self.hr.get_contact(candidate.staff_id)
        response = self.notifier.send_and_wait(
            recipient=contact['phone'],  # SMS
            message=message,
            timeout_seconds=300  # Wait up to 5 minutes
        )
        
        # Parse response
        if response['replied']:
            replied_yes = 'yes' in response['text'].lower()
            return {
                'accepted': replied_yes,
                'response_time': response['time_seconds'],
                'reason': response.get('text', '') if not replied_yes else None
            }
        else:
            return {
                'accepted': False,
                'response_time': 300,
                'reason': 'No response within timeout'
            }
    
    def _update_systems(
        self,
        requirement: ShiftRequirement,
        candidate: ReplacementCandidate
    ):
        """
        Update all systems with new assignment.
        """
        
        # Update schedule
        self.schedule.assign_shift(
            staff_id=candidate.staff_id,
            shift_date=requirement.date,
            shift_start=requirement.start_time,
            shift_end=requirement.end_time,
            terminal=requirement.terminal,
            shift_type=requirement.shift_type
        )
        
        # Update HR (payroll tracking)
        self.hr.record_assignment(
            staff_id=candidate.staff_id,
            shift_id=f"{requirement.date}_{requirement.start_time}",
            coverage_for=requirement.staff_id
        )
        
        # Notify operations
        self.ops.update_staffing(
            terminal=requirement.terminal,
            date=requirement.date,
            coverage_status="COVERED",
            assigned_staff=candidate.staff_name
        )
    
    def _log_coverage_decision(
        self,
        requirement: ShiftRequirement,
        candidate: ReplacementCandidate,
        response: Dict,
        status: str
    ):
        """
        Write audit trail of coverage decision.
        """
        
        entry = {
            'timestamp': datetime.utcnow().isoformat(),
            'absence_staff_id': requirement.staff_id,
            'absence_staff_name': requirement.staff_name,
            'date': requirement.date,
            'shift_start': requirement.start_time,
            'shift_end': requirement.end_time,
            'terminal': requirement.terminal,
            'coverage_status': status,
            'replacement_staff_id': candidate.staff_id if status == 'COVERED' else None,
            'replacement_staff_name': candidate.staff_name if status == 'COVERED' else None,
            'match_score': candidate.match_score if status == 'COVERED' else None,
            'decision_agent': 'auto_orchestrator_v1'
        }
        
        self.schedule.log_coverage_decision(entry)
    
    def _escalate_absence(
        self,
        requirement: ShiftRequirement,
        reason: str
    ) -> Dict:
        """
        Escalate to human shift manager.
        """
        
        manager_alert = f"""MANUAL INTERVENTION REQUIRED

Absence: {requirement.staff_name}
Date: {requirement.date}
Shift: {requirement.terminal} {requirement.start_time}-{requirement.end_time}

Reason no auto-coverage: {reason}

Action: Assign manually or arrange overtime."""
        
        # Send alert to shift manager
        self.notifier.alert_manager(manager_alert)
        
        # Update ops
        self.ops.update_staffing(
            terminal=requirement.terminal,
            date=requirement.date,
            coverage_status="ESCALATED",
            notes=reason
        )
        
        # Log escalation
        self._log_coverage_decision(requirement, None, {}, "ESCALATED")
        
        return {
            'status': CoverageStatus.ESCALATED,
            'reason': reason,
            'shift_requirement': requirement
        }
    
    def _calculate_shift_hours(self, start: str, end: str) -> float:
        """Parse times and calculate hours."""
        from datetime import datetime
        start_dt = datetime.strptime(start, '%H:%M')
        end_dt = datetime.strptime(end, '%H:%M')
        return (end_dt - start_dt).total_seconds() / 3600

# Usage
orchestrator = MultiSystemOrchestrator(
    hr_api=hr_system,
    schedule_db=shift_database,
    notification_service=sms_notifications,
    ops_system=operations_dashboard
)

result = orchestrator.handle_absence(
    staff_id='emp_12345',
    date='2026-04-24',
    reason='Sick leave'
)

if result['status'] == CoverageStatus.COVERED:
    print(f"✓ Covered by {result['replacement'].staff_name}")
else:
    print(f"✗ Escalated: {result.get('reason')}")
```

### Design Decisions & Why

**1. Why Sequential Candidate Offering?**
- Try candidates in order (best match first)
- If candidate declines, try next (no wasted time waiting for all)
- Timeout on each offer (5 min) prevents hanging indefinitely
- Stateful tracking: which candidates have been offered (don't re-offer)

**2. Why Score-Based Matching?**
- Clearance, experience, location, workload all matter
- Single score lets you prioritize objectively
- Easy to explain why Sarah was offered before Mike
- Can tune weights over time (e.g., "location bonus too high, people travel")

**3. Why Update All Systems Atomically?**
- Schedule, HR, Ops must all be consistent
- If schedule updates but ops doesn't, operations won't know they're covered
- Use transactional updates or explicit commit gates

**4. Why Escalate on Timeout?**
- Don't wait forever for staff to respond
- Better to escalate after 5min than wait 2 hours for someone to check phone
- Can implement retry logic (try again in 30 min if still no response)

### Key Takeaways

1. **Orchestration coordinates multiple systems**: absence touches schedule, HR, notifications, operations. Need explicit handoffs.

2. **Score-based matching is better than rules**: rather than "must be at terminal X", score based on all factors. Humans can override.

3. **Sequential candidate offering avoids wasted time**: offer to best match first. If they decline, try next. Don't wait for all responses.

4. **Escalate on hard failures**: no candidates, all declined, timeout. Let human decide what to do.

5. **Log every decision**: audit trail shows why shifts were covered/escalated. Essential for HR review and improvement.

---

## Case Study 3: Wipro PARI — PLC Code Generation for Factory Automation

### The Business Problem

Wipro PARI provides factory automation. Engineers write Programmable Logic Controller (PLC) code by hand. Typical task:

- "When pressure > 50 PSI AND temperature < 100°C, open valve for 3 seconds"

This involves:
1. Reading pressure/temperature sensors
2. Applying logic
3. Controlling output valve
4. Logging events
5. Safety interlocks (never exceed max pressure, always shutoff if emergency stop)

PLC code is **safety-critical**. A bug doesn't just cause data loss; it can injure workers. Regulations (ISO 13849, IEC 61508) require rigorous verification.

Wipro built a **code generation agent** that:
1. Engineer writes requirement in pseudo-natural language
2. Agent generates PLC code
3. Safety validation layer checks for violations (pressure limits, emergency stop handling, etc.)
4. If valid: saves draft for engineer to review
5. Engineer reviews + approves
6. Code is deployed

The agent can generate ~70% of routine code. Engineer still reviews and signs off (non-negotiable).

### Why This Pattern Fits

**Safety-critical code generation** is the hardest autonomous action pattern:
- **Consequences of failure are severe** (injuries, death, legal liability)
- **Verification must be formal** (can't just run tests; need to prove safety properties)
- **Human approval is non-negotiable** (engineer signature required)
- **Regulatory requirements** (auditors must be able to trace how code was generated and validated)

Different from Spotify (code can be reverted) and Manchester Airports (worst case is understaffing). Here, you're controlling physical systems with safety interlocks.

### Architecture Diagram

```
┌──────────────────────────────────────┐
│  Engineer Requirement (pseudo-code)  │
│                                      │
│  "When pressure > 50 PSI and         │
│   temperature < 100C, open valve     │
│   for 3 seconds. Max pressure: 80."  │
└──────────────┬───────────────────────┘
               │
    ┌──────────▼────────────────┐
    │  Code Generation Agent    │
    │                          │
    │  Inputs:                 │
    │  - Requirement text      │
    │  - Equipment specs       │
    │  - Safety constraints    │
    │                          │
    │  Generates:              │
    │  - PLC ladder logic      │
    │  - Variable declarations │
    │  - Safety interlocks     │
    │  - Comments              │
    └──────────┬───────────────┘
               │
   ┌───────────▼──────────────────────────┐
   │  Safety Validation Agent             │
   │                                      │
   │  Checks:                             │
   │  ✓ Pressure limits respected        │
   │  ✓ Emergency stop always works      │
   │  ✓ No infinite loops                │
   │  ✓ All sensors monitored            │
   │  ✓ Proper error handling            │
   │  ✓ Shutdown sequences correct       │
   │                                      │
   │  If FAIL:                            │
   │  - Reject with specific reason       │
   │  - Don't let it through              │
   └──────────┬──────────────────────────┘
              │
   ┌──────────▼────────────────────────┐
   │  If Valid: Draft Code Review       │
   │                                    │
   │  Display:                          │
   │  - Generated ladder logic          │
   │  - Safety violations checked: ✓    │
   │  - Requirement trace               │
   │  - Estimated runtime               │
   │                                    │
   │  Engineer must explicitly approve  │
   │  (no auto-apply)                   │
   └──────────┬───────────────────────┘
              │
   ┌──────────▼──────────────────────┐
   │  If Approved: Deploy with Audit │
   │                                 │
   │  Log:                           │
   │  - Requirement text             │
   │  - Generated code               │
   │  - Validation results           │
   │  - Approver ID + timestamp      │
   │  - Deployment target            │
   │                                 │
   │  All auditable for regulators   │
   └─────────────────────────────────┘
```

### Implementation: Key Components

#### 1. PLC Code Generation

```python
from typing import List, Dict
import anthropic

class PLCCodeGenerator:
    """
    Generate PLC (Programmable Logic Controller) ladder logic code
    from engineer's requirement.
    
    Outputs Structured Text (IEC 61131-3 standard) or ladder logic.
    """
    
    def __init__(self):
        self.client = anthropic.Anthropic()
        self.equipment_specs = {}  # Sensor/valve specs
    
    def generate_code(
        self,
        requirement: str,
        equipment_context: Dict,
        safety_limits: Dict
    ) -> Dict:
        """
        Generate PLC code from requirement.
        
        Args:
            requirement: Engineer's pseudo-code description
            equipment_context: Available sensors, valves, etc.
            safety_limits: Pressure limits, temperature ranges, etc.
        
        Returns:
            {
                'plc_code': str,
                'variables': List[str],
                'diagram': str (ASCII),
                'execution_time_ms': float,
                'reasoning': str
            }
        """
        
        equipment_text = self._format_equipment(equipment_context)
        safety_text = self._format_safety_limits(safety_limits)
        
        prompt = f"""You are an expert PLC programmer. Generate IEC 61131-3 Structured Text code
from the engineer's requirement.

REQUIREMENT:
{requirement}

AVAILABLE EQUIPMENT:
{equipment_text}

SAFETY CONSTRAINTS:
{safety_text}

CRITICAL RULES:
1. Emergency stop (E_STOP input) MUST immediately close all outputs
2. Pressure MUST never exceed max_pressure, even with sensor fault
3. All sensor inputs must be debounced (filter out noise)
4. All outputs must timeout (if command sent but no confirmation in 5s, fault)
5. Log all state changes for audit trail
6. Include comments explaining each section
7. Assume 100ms scan time

Generate complete, production-ready code:

```structured_text
PROGRAM main
VAR
    -- Your variable declarations
END_VAR

-- Your logic here

END_PROGRAM
```

Also provide:
1. A text summary of what the logic does
2. Estimated cycle time (ms)
3. Any assumptions you made"""
        
        response = self.client.messages.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens=2000,
            messages=[{"role": "user", "content": prompt}]
        )
        
        code_text = response.content[0].text
        
        # Extract code block
        plc_code = self._extract_code_block(code_text)
        variables = self._extract_variables(plc_code)
        
        return {
            'plc_code': plc_code,
            'variables': variables,
            'reasoning': code_text,
            'execution_time_ms': self._estimate_execution_time(plc_code),
            'language': 'IEC 61131-3 Structured Text'
        }
    
    def _format_equipment(self, equipment: Dict) -> str:
        """Format equipment specs for LLM."""
        text = ""
        for name, specs in equipment.items():
            text += f"\n{name}:\n"
            text += f"  Type: {specs.get('type')}\n"
            text += f"  Range: {specs.get('range')}\n"
            text += f"  Input/Output: {specs.get('io_type')}\n"
            if 'response_time_ms' in specs:
                text += f"  Response time: {specs['response_time_ms']}ms\n"
        return text
    
    def _format_safety_limits(self, limits: Dict) -> str:
        """Format safety constraints."""
        text = ""
        for name, value in limits.items():
            text += f"- {name}: {value}\n"
        return text
    
    def _extract_code_block(self, text: str) -> str:
        """Extract code block from response."""
        if '```' in text:
            parts = text.split('```')
            if len(parts) >= 3:
                return parts[1]
        return text
    
    def _extract_variables(self, code: str) -> List[str]:
        """Parse variable declarations from code."""
        import re
        # Find VAR ... END_VAR blocks
        pattern = r'VAR\s+(.*?)\s+END_VAR'
        match = re.search(pattern, code, re.DOTALL)
        if match:
            var_block = match.group(1)
            # Parse variable names
            var_pattern = r'(\w+)\s*:\s*(\w+)'
            vars = re.findall(var_pattern, var_block)
            return [f"{name}: {type}" for name, type in vars]
        return []
    
    def _estimate_execution_time(self, code: str) -> float:
        """Rough estimate of code execution time."""
        # Simplified; real estimate requires simulation
        line_count = len(code.split('\n'))
        # Assume ~0.1ms per line on modern PLC
        return line_count * 0.1

# Usage
generator = PLCCodeGenerator()

requirement = """When pressure sensor reads > 50 PSI AND temperature < 100C,
open the valve output for exactly 3 seconds. If pressure exceeds 80 PSI at any time,
close valve immediately regardless of temperature."""

equipment = {
    'pressure_sensor': {
        'type': 'analog input',
        'range': '0-150 PSI',
        'io_type': 'input',
        'response_time_ms': 50
    },
    'temperature_sensor': {
        'type': 'analog input',
        'range': '0-200 C',
        'io_type': 'input',
        'response_time_ms': 100
    },
    'control_valve': {
        'type': 'digital output',
        'io_type': 'output',
        'response_time_ms': 20
    }
}

safety_limits = {
    'max_pressure_psi': 80,
    'min_temperature_c': 0,
    'max_temperature_c': 150,
    'valve_timeout_ms': 5000
}

result = generator.generate_code(requirement, equipment, safety_limits)
print(result['plc_code'])
print(f"\nEstimated execution time: {result['execution_time_ms']:.1f}ms")
```

#### 2. Safety Validation Layer

```python
from enum import Enum
import re

class SafetyViolation(Enum):
    NO_EMERGENCY_STOP_HANDLING = "E-stop not properly handled"
    PRESSURE_LIMIT_EXCEEDED = "Pressure safety limit not checked"
    NO_TIMEOUT = "Output has no timeout mechanism"
    INFINITE_LOOP = "Code contains potential infinite loop"
    UNINITIALIZED_VARIABLE = "Variable used before initialization"
    MISSING_SENSOR_MONITORING = "Safety-critical sensor not monitored"

class SafetyValidator:
    """
    Validate generated PLC code against safety rules.
    
    This is NOT general code checking; it's domain-specific safety validation
    for industrial control systems.
    """
    
    MANDATORY_RULES = [
        SafetyViolation.NO_EMERGENCY_STOP_HANDLING,
        SafetyViolation.PRESSURE_LIMIT_EXCEEDED,
        SafetyViolation.INFINITE_LOOP
    ]
    
    def validate(
        self,
        plc_code: str,
        equipment_context: Dict,
        safety_limits: Dict
    ) -> Dict:
        """
        Validate generated code against safety rules.
        
        Returns:
            {
                'valid': bool,
                'violations': List[Dict],
                'warnings': List[Dict],
                'checks_passed': int,
                'checks_failed': int
            }
        """
        
        violations = []
        warnings = []
        checks_passed = 0
        checks_failed = 0
        
        # Check 1: Emergency stop handling (MANDATORY)
        check = self._check_emergency_stop(plc_code)
        if check['passed']:
            checks_passed += 1
        else:
            violations.append(check)
            checks_failed += 1
        
        # Check 2: Pressure limits (MANDATORY)
        check = self._check_pressure_limits(plc_code, safety_limits)
        if check['passed']:
            checks_passed += 1
        else:
            violations.append(check)
            checks_failed += 1
        
        # Check 3: Infinite loops (MANDATORY)
        check = self._check_infinite_loops(plc_code)
        if check['passed']:
            checks_passed += 1
        else:
            violations.append(check)
            checks_failed += 1
        
        # Check 4: Output timeouts
        check = self._check_output_timeouts(plc_code, equipment_context)
        if check['passed']:
            checks_passed += 1
        else:
            warnings.append(check)  # Non-blocking warning
        
        # Check 5: Sensor monitoring
        check = self._check_sensor_monitoring(plc_code, equipment_context)
        if check['passed']:
            checks_passed += 1
        else:
            warnings.append(check)
        
        # Overall: pass only if no violations
        valid = len(violations) == 0
        
        return {
            'valid': valid,
            'violations': violations,
            'warnings': warnings,
            'checks_passed': checks_passed,
            'checks_failed': checks_failed,
            'summary': f"Passed {checks_passed}/5 safety checks. "
                      f"{'Ready for review.' if valid else 'Safety issues found.'}"
        }
    
    def _check_emergency_stop(self, code: str) -> Dict:
        """
        Check that emergency stop input is properly handled.
        
        RULE: Any emergency stop must immediately shut down all outputs.
        """
        
        # Look for E_STOP or similar handling
        has_estop_check = any(
            pattern in code.upper()
            for pattern in ['E_STOP', 'EMERGENCY', 'ESTOP_INPUT']
        )
        
        # Look for immediate shutdown of outputs
        shutdown_patterns = ['IF.*ESTOP', 'WHEN.*ESTOP']
        has_shutdown = any(
            re.search(pattern, code, re.IGNORECASE)
            for pattern in shutdown_patterns
        )
        
        passed = has_estop_check and has_shutdown
        
        return {
            'passed': passed,
            'rule': SafetyViolation.NO_EMERGENCY_STOP_HANDLING,
            'finding': "Emergency stop is properly monitored and shuts down outputs" if passed
                      else "Emergency stop handling missing or incomplete",
            'severity': 'CRITICAL'
        }
    
    def _check_pressure_limits(self, code: str, limits: Dict) -> Dict:
        """
        Check that pressure safety limit is enforced in code.
        """
        
        max_pressure = limits.get('max_pressure_psi')
        if not max_pressure:
            return {'passed': True, 'finding': 'No max pressure limit defined'}
        
        # Look for pressure check in code
        pressure_pattern = rf'pressure.*{max_pressure}'
        has_pressure_check = bool(re.search(pressure_pattern, code, re.IGNORECASE))
        
        # Look for override: if pressure exceeds, shut down immediately
        override_pattern = r'if.*pressure.*>.*\d+.*shut|close'
        has_override = bool(re.search(override_pattern, code, re.IGNORECASE))
        
        passed = has_pressure_check or has_override
        
        return {
            'passed': passed,
            'rule': SafetyViolation.PRESSURE_LIMIT_EXCEEDED,
            'finding': f"Code checks pressure against limit ({max_pressure} PSI)" if passed
                      else f"Max pressure limit ({max_pressure} PSI) not enforced in code",
            'severity': 'CRITICAL'
        }
    
    def _check_infinite_loops(self, code: str) -> Dict:
        """
        Check for patterns that might cause infinite loops.
        """
        
        # Look for while loops without exit condition
        while_pattern = r'WHILE\s+TRUE'
        has_infinite_while = bool(re.search(while_pattern, code, re.IGNORECASE))
        
        # Look for unguarded loops
        loop_pattern = r'FOR.*DO'
        has_loop = bool(re.search(loop_pattern, code, re.IGNORECASE))
        
        passed = not has_infinite_while  # while true is only OK with timeout
        
        return {
            'passed': passed,
            'rule': SafetyViolation.INFINITE_LOOP,
            'finding': "No obvious infinite loops detected" if passed
                      else "Potential infinite loop (WHILE TRUE) without timeout",
            'severity': 'CRITICAL'
        }
    
    def _check_output_timeouts(self, code: str, equipment: Dict) -> Dict:
        """
        Check that outputs have timeout mechanisms.
        """
        
        # Look for timeout logic
        timeout_pattern = r'timer|timeout|duration'
        has_timeout = bool(re.search(timeout_pattern, code, re.IGNORECASE))
        
        passed = has_timeout
        
        return {
            'passed': passed,
            'rule': 'Output timeouts',
            'finding': "Outputs have timeout mechanisms" if passed
                      else "Consider adding timeout to prevent stuck outputs",
            'severity': 'WARNING'
        }
    
    def _check_sensor_monitoring(self, code: str, equipment: Dict) -> Dict:
        """
        Check that all sensors are properly monitored.
        """
        
        # For each input device, verify it's read
        missing_sensors = []
        for device_name in equipment.keys():
            if equipment[device_name]['io_type'] == 'input':
                if device_name.upper() not in code.upper():
                    missing_sensors.append(device_name)
        
        passed = len(missing_sensors) == 0
        
        return {
            'passed': passed,
            'rule': 'Sensor monitoring',
            'finding': "All sensors are monitored" if passed
                      else f"Sensors not referenced: {missing_sensors}",
            'severity': 'WARNING'
        }

# Usage
validator = SafetyValidator()

validation_result = validator.validate(
    result['plc_code'],
    equipment,
    safety_limits
)

print(f"Valid: {validation_result['valid']}")
print(f"Checks: {validation_result['checks_passed']}/{validation_result['checks_passed'] + validation_result['checks_failed']}")

if validation_result['violations']:
    print("\nVIOLATIONS:")
    for v in validation_result['violations']:
        print(f"  ✗ {v['rule'].value}: {v['finding']}")

if validation_result['warnings']:
    print("\nWARNINGS:")
    for w in validation_result['warnings']:
        print(f"  ⚠ {w['rule']}: {w['finding']}")
```

#### 3. Engineer Review & Approval Gate

```python
from datetime import datetime

class CodeReviewGate:
    """
    Present generated code to engineer for review and explicit approval.
    
    Non-negotiable: no auto-deployment. Human must review and sign off.
    """
    
    def __init__(self, audit_db):
        self.audit_db = audit_db
    
    def present_for_review(
        self,
        generation_result: Dict,
        validation_result: Dict,
        requirement: str,
        equipment: Dict,
        engineer_id: str
    ) -> Dict:
        """
        Display code and collect engineer approval.
        
        Returns:
            {
                'approved': bool,
                'approval_timestamp': str,
                'engineer_id': str,
                'notes': str,
                'audit_id': str
            }
        """
        
        # Display dashboard
        review_dashboard = self._build_dashboard(
            generation_result,
            validation_result,
            requirement,
            equipment
        )
        
        print(review_dashboard)
        print("\n" + "="*80)
        print("ENGINEER REVIEW REQUIRED")
        print("="*80)
        print(f"\nEngineer {engineer_id}, please review the generated code above.")
        print("\nQuestions to answer:")
        print("1. Does the logic correctly implement the requirement?")
        print("2. Are the safety checks adequate?")
        print("3. Are there any edge cases or issues?")
        print("\nType 'APPROVE' to accept, or 'REJECT' with notes to refuse.")
        
        # In production, this would be a web form with e-signature
        # For now, simulate:
        approval_input = input("\nEngineer decision: ").strip().upper()
        
        if approval_input.startswith("APPROVE"):
            approved = True
            notes = ""
        elif approval_input.startswith("REJECT"):
            approved = False
            notes = input("Rejection reason: ")
        else:
            approved = False
            notes = "No clear decision provided"
        
        # Log approval decision
        approval_timestamp = datetime.utcnow().isoformat()
        audit_id = self.audit_db.log_approval(
            engineer_id=engineer_id,
            timestamp=approval_timestamp,
            approved=approved,
            notes=notes,
            requirement=requirement,
            generated_code=generation_result['plc_code'],
            validation_result=validation_result
        )
        
        return {
            'approved': approved,
            'approval_timestamp': approval_timestamp,
            'engineer_id': engineer_id,
            'notes': notes,
            'audit_id': audit_id
        }
    
    def _build_dashboard(
        self,
        generation_result: Dict,
        validation_result: Dict,
        requirement: str,
        equipment: Dict
    ) -> str:
        """
        Build text dashboard for engineer review.
        """
        
        dashboard = f"""
╔════════════════════════════════════════════════════════════════════════════╗
║                       PLC CODE GENERATION REVIEW                           ║
╚════════════════════════════════════════════════════════════════════════════╝

REQUIREMENT:
────────────────────────────────────────────────────────────────────────────
{requirement}

SAFETY VALIDATION:
────────────────────────────────────────────────────────────────────────────
Status: {'✓ PASSED' if validation_result['valid'] else '✗ FAILED'}
Checks: {validation_result['checks_passed']}/{validation_result['checks_passed'] + validation_result['checks_failed']} passed
"""
        
        if validation_result['violations']:
            dashboard += "\nVIOLATIONS (must fix):\n"
            for v in validation_result['violations']:
                dashboard += f"  ✗ {v['rule'].value}\n"
                dashboard += f"    {v['finding']}\n"
        
        if validation_result['warnings']:
            dashboard += "\nWARNINGS (review):\n"
            for w in validation_result['warnings']:
                dashboard += f"  ⚠ {w['rule']}\n"
                dashboard += f"    {w['finding']}\n"
        
        dashboard += f"""
GENERATED CODE:
────────────────────────────────────────────────────────────────────────────
{generation_result['plc_code']}

EXECUTION ESTIMATE:
  Cycle time: {generation_result['execution_time_ms']:.1f}ms
  Language: {generation_result['language']}
"""
        
        return dashboard

# Usage
gate = CodeReviewGate(audit_db)

approval = gate.present_for_review(
    generation_result=result,
    validation_result=validation_result,
    requirement=requirement,
    equipment=equipment,
    engineer_id="eng_789"
)

if approval['approved']:
    print(f"✓ Approved by {approval['engineer_id']}")
    print(f"  Audit ID: {approval['audit_id']}")
    print(f"  Timestamp: {approval['approval_timestamp']}")
    # Proceed to deployment
else:
    print(f"✗ Rejected: {approval['notes']}")
    # Return to engineer for refinement
```

### Design Decisions & Why

**1. Why Agent Generates, Validator Checks, Human Approves (Three Gates)?**
- Agent is creative: generates plausible code quickly
- Validator is rigorous: checks safety rules deterministically
- Human is accountable: engineer takes responsibility for deployment
- Separates concerns: each stage has different job

**2. Why Formal Safety Checks?**
- Safety isn't subjective. E-stop MUST shut down outputs (hard rule).
- Pressure MUST not exceed limit (hard rule).
- No timeout → stuck output → potential hazard (hard rule).
- These can be checked programmatically; don't rely on human to catch them

**3. Why Blocklist-Based Validation?**
- Instead of trying to prove code is correct (intractable), check for known unsafe patterns
- E-stop not handled? Block it.
- Pressure limit not checked? Block it.
- Infinite loop detected? Block it.
- If validators pass, probability of safety issue drops dramatically

**4. Why Explicit Human Approval?**
- PLC code controls physical systems. Agency matters.
- Engineer signature is insurance: they take responsibility.
- Audit trail: can trace who approved what and when.
- "The agent generated it" is not a defense; "engineer reviewed and approved" is.

### Key Takeaways

1. **Safety-critical code needs multiple gates**: generation → validation → human approval. Each gate has different job.

2. **Formal validation checks for known unsafe patterns**: don't try to prove code is correct, just block known-bad patterns.

3. **Human approval is non-negotiable**: autonomous systems can generate and validate, but human must review and sign off on safety-critical code.

4. **Audit trail matters**: log requirement, generated code, validation results, approver, timestamp. Regulators will ask for this.

5. **Fail safe**: if validation fails or human rejects, don't deploy. Better to delay than risk safety incident.
