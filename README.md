# Wargaming Task

## Project Structure

```
home_task/
├── create_db.py           # Creates the database
├── populate_db.py         # Fills the database with random data
└── tests/
    ├── conftest.py        # Fixture: copies DB, randomizes values
    └── test_randomizer.py # Pytest tests: compare pre/post-randomization
```

---

## Notes

- The file `temp_database.db` is automatically created and deleted by the fixture `generate_randomized_db`.
- The implementation corresponds to subpoint b) of point 3 from the task — randomizing one parameter of each component of the ship.
- Since the assignment does not clearly prohibit it, I assumed that a parameter can randomly be set to its original value. So on average, 1/20 tests (30 out of 600) will pass.

---

## How to Run

1. Create the initial database:
   ```bash
   python create_db.py
   ```

2. Populate it with random data:
   ```bash
   python populate_db.py
   ```

3. Run the tests:
   ```bash
   pytest tests/
   ```

---

## Expected Output

```
Ship-200, engine-2
    power: expected 14, was 6
F...

FAILED tests/test_randomizer.py::test_component_parameter_diff[engine-Ship-200]
```

A total of 600 tests will be run.

---

