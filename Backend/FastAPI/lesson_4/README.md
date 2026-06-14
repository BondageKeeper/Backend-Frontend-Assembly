# Lesson 4: Advanced Validation, Loguru Integration & Process Lifecycle Management

This lesson focuses on production-ready data validation techniques using Pydantic field validators, integrating robust asynchronous logging, and handling critical development environment deadlocks on Windows.

## 🚀 Key Implementations

* **Deep Nesting Validation (`mode='after'`):** Implemented advanced Pydantic field validators with `mode='after'` to guarantee that custom business logic triggers *after* structural verification.
* **Malicious Input Filtering:** Integrated Python's `re` module directly into Pydantic models to screen inputs and catch blacklisted keywords (like `spam`, `bot`, `lottery`, `nitro`) dynamically before saving data to PostgreSQL.
* **Asynchronous File Logging:** Configured `loguru` to capture real-time application behavior. Error events and malicious input attempts are automatically routed to a rotating log file (`Unsafe_users.log`).

---

## 🛑 Critical Fix: Handling Ghost Python Processes on Windows

During rapid code changes with Uvicorn's `--reload` flag in an asynchronous environment, background workers often fail to terminate correctly. They turn into **ghost processes** that keep holding the network port (`8000`, `6767`, etc.) and serving stale, cached code. 

If your Swagger UI behaves like code changes are ignored, or fails with a 500 error, the port is locked.

### 🛠 The Kill Command
To completely free up your environment and force-terminate all locked background processes, run this command in your terminal **before** restarting the server:

```bash
taskkill /f /im python.exe
```

* **`taskkill`**: Windows built-in utility to terminate active tasks.
* **`/f`**: **Force** flag. Instantly terminates the process without waiting for a clean exit.
* **`/im python.exe`**: Target by **Image Name**. Drops all background Python workers instantly, completely clearing out port conflicts.

---

## 🏁 How to Run the App Safely

To ensure you are running the fresh version of your code on a clean, dedicated port, execute the following workflow:

1. **Clear ghost processes:**
   ```bash
   taskkill /f /im python.exe
   ```
2. **Start the FastAPI server on a custom port:**
   ```bash
   uvicorn exp_FastAPI_tasks:app --reload --port 6767
   ```
3. **Open the interactive documentation:**
   Go to your browser and access: `http://127.0.0`
