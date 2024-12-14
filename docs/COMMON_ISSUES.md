# Common Issues

## Black Setup Troubleshooting

1. If you encounter permission issues:
   - Windows: Run Command Prompt as administrator
   - Linux: Use `sudo` for permissions

2. Virtual Environment Issues:
   - Ensure Python is in your system PATH
   - Try creating the virtual environment manually if the script fails

## Development Environment Issues

1. Port Conflicts:
   - Check if ports 8000 (backend) or 5000 (frontend) are already in use
   - Modify the port numbers in your configuration if needed

2. Database Connectivity:
   - Ensure the demo database is running if using local development
   - Check database credentials in your `.env` file
