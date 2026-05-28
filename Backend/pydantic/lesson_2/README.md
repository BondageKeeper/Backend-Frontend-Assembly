# Lesson 2: Advanced Validation & Configuration

In this lesson, I integrated some advanced Pydantic v2 tools to handle some AI application settings.

### Key Skills Acquired:
* **Field Restrictions**: Set up precise numeric limits (`ge`, `le`) and text lengths (`min_length`) for AI inputs.
* **Model Validator**: Implemented cross-field business logic (`mode='after'`) to control premium feature dependencies.
* **JSON Parsing**: Used `model_validate_json()` to stream raw server data directly into strict Python shapes.
* **Strict Mode**: Configured `ConfigDict(extra='forbid')` to completely block malicious or hidden JSON fields.
