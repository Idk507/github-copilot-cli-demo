# Security Review

1. **Unauthenticated read and delete endpoints** — `GET /tasks`, `GET /tasks/{task_id}`, and `DELETE /tasks/{task_id}` are exposed with no authentication or authorization checks in `routes/tasks.py`. If this service is reachable by untrusted clients, any caller can enumerate all tasks and delete arbitrary tasks.

2. **Unbounded in-memory storage enables trivial denial of service** — `POST /tasks` accepts arbitrary `title` and `description` values from `TaskCreate` in `models.py` with no size or count limits, and `routes/tasks.py` stores every task in the global `tasks` list indefinitely. A client can submit many large requests and exhaust process memory.

3. **Race condition on task creation and deletion** — the shared global `tasks` list in `routes/tasks.py` is mutated without synchronization. Concurrent requests can compute the same `next_id`, interleave deletes and reads, and produce duplicate IDs or inconsistent state, which is an integrity issue under multi-request load.

4. **No direct injection sink found in the current code** — the reviewed Python files do not pass user input into SQL, shell commands, or template rendering, so there is no obvious SQL, command, or template injection path in the current implementation.
