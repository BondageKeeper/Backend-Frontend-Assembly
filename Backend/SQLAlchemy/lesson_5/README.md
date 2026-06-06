# Lesson 5: Advanced Grouping and Query Optimization

## Introduction
In this lesson, I focused on advanced data analysis and performance optimization inside SQLAlchemy 2.0. I learned how to separate database records into logical groups, filter the results of mathematical calculations, and solve the critical "N+1 queries" performance issue to keep the server running fast and efficient under heavy load.

## Key Skills Acquired

* **Data Grouping & Aggregation Filters**: Mastered the use of `.group_by()` to split rows into custom categories and implemented `.having()` to filter these categorized groups based on calculated mathematical results.
* **Relationship Eager Loading**: Learned how to use `.options(selectinload(...))` to solve the N+1 query problem, fetching all connected table data in a single smart request instead of creating hundreds of hidden database hits.
