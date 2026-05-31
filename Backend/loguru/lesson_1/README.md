# Lesson 1: Logging with Loguru

In this lesson, I learned how to track and protect backend applications using the Loguru library instead of the standard `print()` function.

### What is this tool for:
Loguru acts as a "flight recorder" for the server. It saves everything that happens in the application into files on the disk, adding precise time, code lines, and severity levels. This is critical for fixing background bugs when the app runs live on a server.

### Key Skills Acquired:
* **Logging Levels**: Learned how to categorize logs by priority (`DEBUG`, `INFO`, `WARNING`, `ERROR`, `CRITICAL`).
* **File Pipelines (`logger.add`)**: Configured automatic history saving with custom string formatting, file rotation (`rotation`), and old file cleanup (`retention`).
* **Automated Defense (`@logger.catch`)**: Applied guards to capture heavy crashes and tracebacks inside asynchronous AI functions without breaking the server.
