# Lesson 4: Database Relationships and Cascade Deletion

## Key Skills Acquired

* **Table Relationships**: Learned how to logically link databases using `ForeignKey` in PostgreSQL to hold relational IDs and `relationship` in Python for modern data management.
* **Bi-directional Synchronization**: Mastered the `back_populates` flag to establish two-way communication between data models, allowing smooth item nesting via Python's `.append()` method.
* **Cascade Deletion**: Configured `ondelete="CASCADE"` constraints to enforce data integrity, ensuring that when a parent record is removed, all its linked child records are automatically wiped out.
