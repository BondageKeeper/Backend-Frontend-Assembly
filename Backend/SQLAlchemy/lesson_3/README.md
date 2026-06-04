# Lesson 3: Integrating Pydantic Validation with SQLAlchemy ORM

## Introduction
In this lesson, I connected Pydantic and SQLAlchemy to build a complete backend data pipeline. Pydantic acts as a protective shield, validating input dictionaries and cleaning user data before it hits the server. Once the data passes validation, SQLAlchemy safely maps it to database models and stores it in PostgreSQL. This combination ensures that the database stays clean and secure from bad or corrupt inputs.

## Key Skills Acquired

* **Data Validation Layer**: Built robust Pydantic schemas (`BaseModel`) with custom `@field_validator` logic and standard regex checks to validate incoming data formats like specific subscription plan names.
* **ORM Mapping**: Successfully converted validated Pydantic model data into native SQLAlchemy entities using model fields directly.
* **Classes relations**: Wrote structure in classes which refer to SQLAlchemy and validated their attributes using Pydantic Structure classes
