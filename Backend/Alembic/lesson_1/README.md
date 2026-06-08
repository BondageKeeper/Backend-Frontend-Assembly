# Lesson 1: Database Version Control with Alembic

## Introduction
In this lesson, I started learning Alembic, a lightweight database migration tool for usage with SQLAlchemy. Instead of using destructive workflows like dropping and recreating tables manually (which causes total data loss in production), Alembic acts like Git for databases. It tracks incremental structural changes in Python models, creates historical code blueprints, and safely alters production PostgreSQL schemas while preserving live user records.

## Key Skills Acquired

* **Repository Initialization**: Initialized the migration environment using `alembic init` and manually reconfigured `env.py` to securely hook the configuration pipeline with custom SQLAlchemy metadata and async database URLs (`config.set_main_option`).
* **Migration Lifecycle Execution**: Mastered the standard backend workflow for database schema evolution: generating code blueprints (`alembic revision --autogenerate`), applying structural changes to live databases (`alembic upgrade head`), and reverting faulty increments via sequential rollbacks (`alembic downgrade -1`).
* **Manual Schema Engineering**: Learned how to intercept and manually modify auto-generated version scripts inside the `versions/` directory, implementing complex database instructions like `op.alter_column` with strict PostgreSQL `existing_type` validation.
