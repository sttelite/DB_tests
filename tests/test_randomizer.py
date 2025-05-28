# -*- coding: utf-8 -*-
import pytest

COMPONENTS = {
    "weapon": ["reload_speed", "rotational_speed",
               "diameter", "power_volley", "count"],
    "hull": ["armor", "type", "capacity"],
    "engine": ["power", "type"]
}

ship_ids = [f"Ship-{i}" for i in range(1, 201)]


@pytest.mark.parametrize("ship", ship_ids)
@pytest.mark.parametrize("component", ["weapon", "hull", "engine"])
def test_component_parameter_diff(generate_randomized_db, ship, component):
    original_cursor, temp_cursor = generate_randomized_db

    original_cursor.execute("SELECT weapon, hull, engine "
                            "FROM Ships "
                            "WHERE ship = ?", (ship,))
    row = original_cursor.fetchone()
    component_index = ["weapon", "hull", "engine"].index(component)
    component_name = row[component_index]

    temp_cursor.execute("SELECT weapon, hull, engine "
                        "FROM Ships "
                        "WHERE ship = ?", (ship,))
    temp_row = temp_cursor.fetchone()
    temp_component_name = temp_row[component_index]

    if temp_component_name != component_name:
        print(f"{ship}, {temp_component_name} : expected "
              f"{component_name}, but got {temp_component_name}")
        assert temp_component_name == component_name

    fields = COMPONENTS[component]
    param_list = ", ".join(fields)

    original_cursor.execute(
        f"SELECT {param_list} FROM {component}s WHERE {component} = ?",
        (component_name,)
    )
    original_values = original_cursor.fetchone()

    temp_cursor.execute(
        f"SELECT {param_list} FROM {component}s WHERE {component} = ?",
        (component_name,)
    )
    temp_values = temp_cursor.fetchone()

    for i, field in enumerate(fields):
        if original_values[i] != temp_values[i]:
            print(f"{ship}, {component_name}:\n    {field}: expected "
                  f"{original_values[i]}, was {temp_values[i]}")
            assert original_values[i] == temp_values[i]
