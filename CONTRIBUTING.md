# Contributing to ContextOptimizer

Thank you for your interest in contributing to ContextOptimizer! This document provides guidelines and information for contributors.

## 🚀 Quick Start

1. **Fork the repository** on GitHub
2. **Clone your fork** locally
3. **Set up the development environment** (see README.md)
4. **Create a feature branch** for your changes
5. **Make your changes** following our guidelines
6. **Test your changes** thoroughly
7. **Submit a pull request** with a clear description

## 📋 Table of Contents

- [Code of Conduct](#code-of-conduct)
- [How to Contribute](#how-to-contribute)
- [Development Setup](#development-setup)
- [Coding Standards](#coding-standards)
- [Testing Guidelines](#testing-guidelines)
- [Pull Request Process](#pull-request-process)
- [Issue Reporting](#issue-reporting)
- [Community](#community)

## 📜 Code of Conduct

This project adheres to a code of conduct that we expect all contributors to follow. Please read and follow these guidelines:

- **Be respectful** and inclusive in all interactions
- **Be collaborative** and help others learn and grow
- **Be constructive** in feedback and discussions
- **Be patient** with newcomers and different perspectives
- **Be professional** in all communications

## 🤝 How to Contribute

### 🐛 Bug Reports

Found a bug? Help us fix it!

1. **Check existing issues** to avoid duplicates
2. **Use the bug report template** when creating new issues
3. **Include detailed information**:
   - Steps to reproduce the bug
   - Expected vs actual behavior
   - Environment details (OS, Python version, etc.)
   - Screenshots or logs if applicable

### 💡 Feature Requests

Have an idea for a new feature?

1. **Search existing feature requests** to avoid duplicates
2. **Use the feature request template**
3. **Explain the use case** and benefits
4. **Provide mockups or examples** if applicable
5. **Be open to discussion** and feedback

### 🔧 Code Contributions

Ready to contribute code?

1. **Start with good first issues** if you're new
2. **Discuss major changes** in issues before implementing
3. **Follow our coding standards** (see below)
4. **Write tests** for new functionality
5. **Update documentation** as needed

## 🛠️ Development Setup

### Prerequisites

- Python 3.12+
- Node.js 18+
- Git

### Local Development

```bash
# 1. Fork and clone the repository
git clone https://github.com/YOUR_USERNAME/ContextOptimizer.git
cd ContextOptimizer

# 2. Set up the development environment
./scripts/dev.sh setup

# 3. Create a feature branch
git checkout -b feature/your-feature-name

# 4. Start development servers
./scripts/dev.sh dev
```

### Environment Variables

Copy `.env.example` to `.env` and configure:

```bash
cp .env.example .env
# Edit .env with your OpenAI API key
```

## 📏 Coding Standards

### Python (Backend)

- **Style**: Follow PEP 8 guidelines
- **Formatter**: Use Black for code formatting
- **Linting**: Use Ruff for linting
- **Type Hints**: Use type hints for all functions
- **Docstrings**: Use Google-style docstrings

```python
def example_function(param: str) -> dict:
    """
    Example function with proper documentation.
    
    Args:
        param: Description of the parameter
        
    Returns:
        Dictionary with results
        
    Raises:
        ValueError: If param is invalid
    """
    pass
```

### TypeScript (Frontend)

- **Style**: Use ESLint and Prettier
- **Types**: Prefer explicit types over `any`
- **Components**: Use functional components with hooks
- **Naming**: Use PascalCase for components, camelCase for functions

```typescript
interface ExampleProps {
  title: string;
  onClick: () => void;
}

const ExampleComponent: React.FC<ExampleProps> = ({ title, onClick }) => {
  return (
    <button onClick={onClick}>
      {title}
    </button>
  );
};
```

### General Guidelines

- **Commit Messages**: Use conventional commits format
  ```
  feat: add new optimization algorithm
  fix: resolve session timeout issue
  docs: update API documentation
  test: add unit tests for evaluator
  ```
- **File Organization**: Keep files focused and well-organized
- **Error Handling**: Implement proper error handling and logging
- **Performance**: Consider performance implications of changes

## 🧪 Testing Guidelines

### Backend Tests

```bash
# Run all backend tests
cd backend
python -m pytest tests/ -v

# Run specific test file
python -m pytest tests/unit/test_evaluator.py -v

# Run with coverage
python -m pytest tests/ --cov=app --cov-report=html
```

### Frontend Tests

```bash
# Type checking
cd frontend
npm run type-check

# Linting
npm run lint

# Build test
npm run build
```

### Test Requirements

- **Unit Tests**: Write unit tests for new functions and classes
- **Integration Tests**: Add integration tests for API endpoints
- **Edge Cases**: Test edge cases and error conditions
- **Coverage**: Maintain good test coverage (aim for >80%)

## 📬 Pull Request Process

### Before Submitting

1. **Test your changes** thoroughly
2. **Run linting and formatting** tools
3. **Update documentation** if needed
4. **Write/update tests** for new functionality
5. **Ensure all tests pass**

### Pull Request Template

When submitting a PR, include:

- **Description**: Clear description of changes
- **Type**: Bug fix, feature, documentation, etc.
- **Testing**: How you tested the changes
- **Screenshots**: If UI changes are involved
- **Breaking Changes**: Any breaking changes
- **Related Issues**: Link to related issues

### Review Process

1. **Automated checks** must pass (CI/CD)
2. **Code review** by maintainers
3. **Address feedback** promptly
4. **Merge** after approval

## 🐛 Issue Reporting

### Bug Report Template

```markdown
## Bug Description
A clear description of the bug.

## Steps to Reproduce
1. Go to '...'
2. Click on '....'
3. Scroll down to '....'
4. See error

## Expected Behavior
What you expected to happen.

## Actual Behavior
What actually happened.

## Environment
- OS: [e.g., macOS 12.0]
- Python: [e.g., 3.12.0]
- Node.js: [e.g., 18.17.0]
- Browser: [e.g., Chrome 120.0]

## Additional Context
Any other context about the problem.
```

### Feature Request Template

```markdown
## Feature Description
A clear description of the feature you'd like to see.

## Problem Statement
What problem does this feature solve?

## Proposed Solution
How would you like this feature to work?

## Alternatives Considered
Other solutions you've considered.

## Additional Context
Any other context or screenshots.
```

## 💬 Community

### Communication Channels

- **GitHub Issues**: For bug reports and feature requests
- **GitHub Discussions**: For questions and general discussion
- **Pull Requests**: For code contributions

### Getting Help

- **Documentation**: Check the README and docs first
- **Search Issues**: Look for existing solutions
- **Ask Questions**: Use GitHub Discussions for questions
- **Be Patient**: Maintainers are volunteers

### Recognition

We appreciate all contributions! Contributors will be:

- **Acknowledged** in release notes
- **Listed** in the contributors section
- **Thanked** publicly for their contributions

## 📚 Resources

### Documentation

- [README.md](README.md) - Project overview and setup
- [API Documentation](http://localhost:8000/docs) - API reference
- [Architecture Guide](Concept_Design.md) - System architecture

### Tools

- [Black](https://black.readthedocs.io/) - Python code formatter
- [Ruff](https://docs.astral.sh/ruff/) - Python linter
- [ESLint](https://eslint.org/) - TypeScript linter
- [Prettier](https://prettier.io/) - Code formatter

### Learning Resources

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Next.js Documentation](https://nextjs.org/docs)
- [React Documentation](https://react.dev/)
- [TypeScript Documentation](https://www.typescriptlang.org/docs/)

---

## 🙏 Thank You

Thank you for contributing to ContextOptimizer! Your contributions help make this project better for everyone in the multi-agent systems community.

If you have any questions about contributing, please don't hesitate to ask in GitHub Discussions or open an issue.

Happy coding! 🚀 