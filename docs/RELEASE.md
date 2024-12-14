# Release Process
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
