# Documentation Setup Guide

This guide will help you set up the local development environment for building and testing the DataDialogue documentation.

## Prerequisites

- Python 3.8 or higher
- pip (Python package installer)
- Git

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/ggeop/DataDialogueLLM.git
   cd DataDialogueLLM
   ```

2. Create a virtual environment (recommended):
   ```bash
   # On Windows
   python -m venv venv
   .\venv\Scripts\activate

   # On Unix or MacOS
   python3 -m venv venv
   source venv/bin/activate
   ```

3. Install documentation dependencies:
   ```bash
   pip install -r docs/documentation/requirements.py
   ```

## Building Documentation

1. Navigate to the project root:
   ```bash
   cd DataDialogueLLM
   ```

2. Build the documentation:
   ```bash
   mkdocs build
   ```

3. Serve the documentation locally:
   ```bash
   mkdocs serve
   ```

4. Access the documentation at `http://127.0.0.1:8000`

## Testing Documentation

1. **Live Preview**
   - Run `mkdocs serve`
   - Open `http://127.0.0.1:8000` in your browser
   - Changes will automatically reload

2. **Build Testing**
   - Run `mkdocs build`
   - Check the `site` directory for the built documentation
   - Verify all pages render correctly

3. **Link Checking**
   - Install link checking tool:
     ```bash
     pip install linkchecker
     ```
   - Run link checker:
     ```bash
     linkchecker http://127.0.0.1:8000
     ```

## Common Issues

1. **Missing Dependencies**
   - Solution: Run `pip install -r docs/documentation/requirements.py`

2. **Build Errors**
   - Check for syntax errors in markdown files
   - Verify all referenced files exist
   - Check mkdocs.yml configuration

3. **Theme Issues**
   - Clear browser cache
   - Restart mkdocs serve
   - Verify theme configuration in mkdocs.yml

## Best Practices

1. **Writing Documentation**
   - Use clear, concise language
   - Follow the established structure
   - Include code examples where relevant
   - Add screenshots for UI-related content

2. **Version Control**
   - Create a new branch for documentation changes
   - Use descriptive commit messages
   - Test changes locally before pushing

3. **Maintenance**
   - Keep dependencies up to date
   - Regularly check for broken links
   - Update screenshots when UI changes

## Additional Resources

- [MkDocs Documentation](https://www.mkdocs.org/)
- [Material for MkDocs](https://squidfunk.github.io/mkdocs-material/)
- [Markdown Guide](https://www.markdownguide.org/) 