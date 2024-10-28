# Contributing to Data Dialogue

First off, thank you for considering contributing to Data Dialogue! 🎉 As an AI-powered data interaction tool, we're excited to have your input in making our project even better.

## Table of Contents
- [Code of Conduct](#code-of-conduct)
- [Development Process](#development-process)
- [Branching Strategy](#branching-strategy)
- [Commit Convention](#commit-convention)
- [Pull Request Process](#pull-request-process)
- [Development Setup](#development-setup)
- [Release Process](#release-process)

## Code of Conduct

Our project is committed to providing a welcoming and inspiring community for all. We expect all participants to:
- Be respectful and inclusive
- Be collaborative
- Focus on what is best for the community
- Show empathy towards other community members

## Development Process

1. Fork the repository
2. Create your feature branch from `develop`
3. Write your code and tests
4. Follow our commit message convention
5. Push to your fork
6. Submit a pull request

## Branching Strategy

We use the following branches:
- `main`: Production-ready code
- `develop`: Integration branch for features
- `feature/*`: New features
- `fix/*`: Bug fixes
- `hotfix/*`: Emergency fixes for production

## Commit Convention

We use [Conventional Commits](https://www.conventionalcommits.org/) to automate versioning and release notes.

### Format
```
<type>(<scope>): <description>

[optional body]

[optional footer]
```

### Types
- `feat`: New feature (MINOR version bump)
- `fix`: Bug fix (PATCH version bump)
- `docs`: Documentation changes
- `style`: Code style changes
- `refactor`: Code restructuring
- `perf`: Performance improvements
- `test`: Adding/updating tests
- `chore`: Maintenance tasks

### Examples
```bash
# Add new LLM feature
feat(backend): add support for new LLM model

# Fix database connection
fix(database): resolve PostgreSQL timeout issue

# Breaking API change
feat!: redesign query generation API

# Update documentation
docs: update installation guide
```

## Pull Request Process

1. Create a PR from your feature branch to `develop`
2. Ensure your PR title follows commit convention
3. Update documentation if needed
4. Get at least one code review
5. All checks must pass before merging

### PR Title Convention
Follow the same convention as commit messages:
```
feat: add new language model integration
fix: resolve memory leak in query processor
docs: update deployment guide
```

## Development Setup

1. Clone the repository:
```bash
git clone https://github.com/ggeop/DataDialogueLLM.git
cd DataDialogueLLM
```

2. Set up local development environment:

### Running with Docker Compose (Recommended)

For local development with volume mounting:
```bash
docker-compose up try-demo-db-local backend-local frontend-local --build
```

This starts:
- `try-demo-db-local`: PostgreSQL database with sample data
- `backend-local`: Python backend service
- `frontend-local`: Flask frontend service

Access:
- Frontend: http://localhost:5000
- Backend: http://localhost:8000

### Environment Setup

Create a `.env` file based on `.env.example`:
```bash
cp .env.example .env
# Edit .env with your configurations
```

## Project Structure

```
data-dialogue/
├── backend/              # LLM and API service
│   ├── app/
│   │   ├── api/         # API endpoints
│   │   ├── core/        # Core functionality
│   │   ├── services/    # Service layer
│   │   └── main.py
│   ├── Dockerfile
│   └── requirements.txt
├── frontend/            # User interface
│   ├── static/
│   │   ├── css/
│   │   ├── images/
│   │   ├── js/
│   │   └── templates/
│   ├── app.py
│   └── Dockerfile
├── database/           # Database setup and sample data
└── docker-compose.yml
```

## Release Process

Releases are automated using semantic-release based on conventional commits.

### Version Calculation
- Breaking Change → MAJOR version bump
- New Feature → MINOR version bump
- Bug Fix → PATCH version bump


### Release Flow
1. Changes are merged to `develop`
2. PR from `develop` to `main` creates release
3. Automated process:
   - Calculates version
   - Generates changelog
   - Creates GitHub release
   - Pushes Docker images

## Need Help?

Feel free to:
- Open an issue on GitHub
- Ask questions in pull requests
- Contact project maintainers

## License

By contributing to Data Dialogue, you agree that your contributions will be licensed under the MIT License.

Thank you for contributing to Data Dialogue! 🚀