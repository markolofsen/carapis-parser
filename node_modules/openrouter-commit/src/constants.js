export const LIBRARY_NAME = "openrouter-commit";

export const IGNORED_FILES = [
    ".env.openrouter",
    "node_modules/", ".npm/", "package-lock.json",
    "dist/", "venv/", "env/", "__pycache__/", "*.pyc", "*.pyo", "Pipfile.lock", "poetry.lock",
    "logs/", "*.log", "debug.log*", "*.swp", "*.swo",
    ".cache/", ".idea/", ".editorconfig",
    ".DS_Store", "Thumbs.db",
];

export const MAX_FILE_SIZE_MB = 49; // Maximum file size in megabytes
