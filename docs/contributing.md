# Contributing Guide

Welcome to the Aruba SSID Manager project! We appreciate your interest in contributing. This guide outlines the process for contributing code, documentation, and bug reports.

## Code of Conduct

This project adheres to a Code of Conduct that all contributors are expected to follow. See [CODE_OF_CONDUCT.md](../CODE_OF_CONDUCT.md) for details.

## Getting Started

### Prerequisites
- Python 3.9 or higher
- Git
- Familiarity with SSH and Aruba wireless controllers
- Pexpect library knowledge (optional but helpful)

### Setting Up Development Environment

1. **Fork the Repository**
   ```bash
   # Create a personal fork on GitHub
   # Then clone it locally
git clone https://github.com/YOUR_USERNAME/aruba-ssid-manager.git
cd aruba-ssid-manager
   ```

2. **Create a Virtual Environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install Development Dependencies**
   ```bash
   pip install -e .
   pip install pytest  # For running tests
   ```

4. **Verify Setup**
   ```bash
   python -m pytest tests/
   aruba-ssid-manager --help
   ```

## Development Workflow

### 1. Create a Feature Branch

```bash
git checkout -b feature/your-feature-name
```

Branch naming conventions:
- `feature/` - New features
- `bugfix/` - Bug fixes
- `docs/` - Documentation updates
- `refactor/` - Code refactoring
- `test/` - Test additions

### 2. Make Your Changes

Follow these guidelines:

**Code Style:**
- Follow PEP 8
- Use type hints for all function signatures
- Keep lines under 100 characters
- Use descriptive variable names

**Example:**
```python
def your_function(param: str, count: int = 10) -> Dict[str, Any]:
    """
    Brief description of function.

    Args:
        param (str): Description of param
        count (int): Description of count (default: 10)

    Returns:
        Dict[str, Any]: Description of return value
    """
    result = {}
    # Implementation here
    return result
```

**Documentation:**
- Add docstrings to all functions and classes
- Include parameter and return type documentation
- Provide usage examples for public functions
- Update relevant documentation files in `docs/`

**Testing:**
- Add tests for new features
- Ensure all existing tests pass
- Aim for >80% code coverage

### 3. Write and Run Tests

```bash
# Create test file in tests/ directory
# tests/test_your_feature.py

# Run tests
python -m pytest tests/ -v

# Run with coverage
python -m pytest tests/ --cov=aruba_ssid_manager --cov-report=html
```

Example test:
```python
def test_your_feature():
    from aruba_ssid_manager import your_function
    result = your_function("test")
    assert result is not None
    assert isinstance(result, dict)
```

### 4. Commit Your Changes

```bash
git add .
git commit -m "feat: add your feature description"
```

Commit message format:
- `feat:` - New feature
- `fix:` - Bug fix
- `docs:` - Documentation
- `refactor:` - Code refactoring
- `test:` - Test additions
- `chore:` - Build/dependency updates

Example commit messages:
- `feat: add support for hidden SSID broadcast control`
- `fix: handle SSH timeout on slow networks`
- `docs: add API reference documentation`
- `test: add comprehensive integration tests`

### 5. Push and Create Pull Request

```bash
git push origin feature/your-feature-name
```

Then create a pull request on GitHub with:

**Title:** Brief description of change
```
feat: add support for configuring SSID encryption
```

**Description:**
```markdown
## Summary
- What does this change do?
- Why is it needed?
- What problem does it solve?

## Changes Made
- Bullet list of changes
- Include any breaking changes

## Testing
- How was this tested?
- Provide steps to reproduce
- Include test results

## Related Issues
Closes #123 (if applicable)

## Checklist
- [ ] Code follows project style guidelines
- [ ] All new code includes docstrings
- [ ] Tests added for new functionality
- [ ] All tests pass locally
- [ ] Documentation updated
- [ ] No new warnings or errors introduced
```

## Types of Contributions

### Bug Reports

**Report bugs by creating an issue with:**

1. **Title:** Concise description of bug
2. **Description:** Include:
   - Steps to reproduce
   - Expected behavior
   - Actual behavior
   - Python version and OS
   - Full error message/traceback
   - Verbose logs if available

Example:
```markdown
## Title
SSID configuration fails with timeout on slow network

## Steps to Reproduce
1. Run with --host 10.0.0.1 on 2Mbps connection
2. Try to configure SSID
3. Wait for timeout

## Expected
Should retry or wait longer for response

## Actual
Throws timeout exception after 30 seconds

## Environment
- Python 3.11
- pexpect 4.9
- macOS 13.0
- Network: WiFi with 2Mbps connection

## Error
```
pexpect.exceptions.TIMEOUT: Timeout exceeded
```

## Logs
[Include verbose log output]
```

### Feature Requests

**Request features by creating an issue with:**

1. **Title:** Feature name
2. **Description:**
   - Why this feature is needed
   - Use cases
   - Expected behavior
   - Examples

Example:
```markdown
## Title
Support for multiple VLAN assignment per SSID

## Need
Currently can only assign one VLAN per SSID, but need to support
multiple VLANs for policy-based routing.

## Expected Behavior
Allow comma-separated VLAN IDs or multiple --vlan arguments

## Example
```bash
aruba-ssid-manager --host 10.0.0.1 \
  --ssid MultiVLAN --vlan 10,20,30 --wlan-profile default
```
```

### Documentation Improvements

1. **Fix Typos or Clarity**
   - Edit relevant `.md` file
   - Create PR with changes

2. **Add Examples**
   - Add to `docs/` or docstrings
   - Include realistic scenarios

3. **Add Missing Docs**
   - Identify gaps
   - Create new files in `docs/`
   - Link from appropriate places

### Code Refactoring

1. **Maintain Backward Compatibility**
   - Don't break existing APIs
   - Deprecate before removing

2. **Improve Performance**
   - Profile before/after
   - Include benchmark results in PR

3. **Improve Code Quality**
   - Reduce complexity
   - Improve test coverage
   - Remove technical debt

## Code Review Process

### What to Expect

1. **Initial Review:** 1-3 days
2. **Feedback:** May request changes
3. **Re-review:** After changes made
4. **Approval:** When ready
5. **Merge:** Into main branch

### How to Respond to Feedback

1. **Read carefully** - Understand reviewer's concern
2. **Discuss if unclear** - Ask questions
3. **Make changes** - Address feedback
4. **Re-request review** - Notify reviewer
5. **Don't be discouraged** - Feedback makes code better

## Project Structure

```
aruba-ssid-manager/
├── docs/                         # Architecture, API, deployment, troubleshooting
├── scripts/                      # Automation helpers (smoke tests)
├── src/
│   └── aruba_ssid_manager/       # Library + CLI package
├── tests/                        # Pytest suite
│   └── test_aruba_ssid_manager.py
├── CHANGELOG.md                  # Release history
├── LICENSE                       # MIT License
├── pyproject.toml                # Packaging metadata
└── README.md                     # Project overview
```

## Documentation Standards

### File Headers
```python
#!/usr/bin/env python3
"""
Project Title: Description

Brief description of module/script purpose.

Author: Kris Armstrong
"""
```

### Function Docstrings
```python
def function_name(param1: str, param2: int = 10) -> Dict[str, Any]:
    """
    One-line description of function.

    Longer description if needed, explaining behavior,
    edge cases, and important details.

    Args:
        param1 (str): Description of first parameter
        param2 (int): Description of second parameter (default: 10)

    Returns:
        Dict[str, Any]: Description of return value

    Raises:
        ValueError: When param1 is empty
        TypeError: When param2 is not an integer

    Example:
        >>> result = function_name("test", 20)
        >>> print(result)
        {'key': 'value'}
    """
```

### Markdown Documentation

```markdown
# Section Title

Brief introduction.

## Subsection

Detailed explanation with code examples.

### Code Example
\`\`\`python
code_here()
\`\`\`

### Expected Output
\`\`\`
output_here
\`\`\`
```

## Testing Guidelines

### Test File Location
```
tests/
└── test_aruba-ssid-manager
```

### Test Structure
```python
import pytest
from aruba_ssid_manager import function_to_test

def test_function_basic():
    """Test basic functionality."""
    result = function_to_test()
    assert result is not None

def test_function_with_params():
    """Test with specific parameters."""
    result = function_to_test("test_param")
    assert isinstance(result, dict)

def test_function_error_handling():
    """Test error conditions."""
    with pytest.raises(ValueError):
        function_to_test("invalid")
```

### Running Tests
```bash
# Run all tests
python -m pytest tests/ -v

# Run specific test
python -m pytest tests/test_aruba_ssid_manager::test_function_name -v

# Run with coverage
python -m pytest tests/ --cov=aruba_ssid_manager

# Run with coverage report
python -m pytest tests/ --cov=aruba_ssid_manager --cov-report=html
```

## Versioning

The project uses Semantic Versioning (MAJOR.MINOR.PATCH):

- **MAJOR**: Breaking changes
- **MINOR**: New features (backward compatible)
- **PATCH**: Bug fixes

Update version in:
1. `aruba-ssid-manager` - `__version__` variable

Or use the version bumper:
```bash
```

## Common Mistakes to Avoid

1. **Not running tests** - Always run `pytest` before submitting
2. **Missing docstrings** - Document all public functions
3. **Hardcoded values** - Use parameters and configuration
4. **Ignoring type hints** - Use proper type annotations
5. **Large commits** - Keep commits focused and atomic
6. **Poor commit messages** - Be descriptive and clear
7. **Breaking changes** - Maintain backward compatibility
8. **Not updating docs** - Documentation must match code

## Questions or Need Help?

1. Check [troubleshooting.md](troubleshooting.md)
2. Review [api.md](api.md) for API details
3. Check existing issues/PRs
4. Create a new issue with your question

---

Author: Kris Armstrong

## License

By contributing, you agree that your contributions will be licensed under the MIT License.
