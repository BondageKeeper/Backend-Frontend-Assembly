# Lesson 2: HTTP Methods & Request Validation in FastAPI

This section covers the core HTTP methods used to build RESTful APIs and how FastAPI handles route definitions and data operations.

## Covered Methods

* **GET:** Retrieve data from the server without modifying its state.
* **POST:** Send new data to the server to create a new resource.
* **PUT:** Completely replace an existing resource with a new data payload.
* **PATCH:** Partially update specific fields of an existing resource.
* **DELETE:** Remove a specific resource from the server by its ID.
* **HEAD:** Fetch response headers only to check resource availability or size without downloading the body.
* **OPTIONS:** Check server communication rules and allowed HTTP methods (CORS preflight).

## Key Takeaways

* Path parameters are used to target specific resources (e.g., `/items/{id}`).
* Pydantic schemas ensure inbound data shapes match backend expectations for write/update operations.
