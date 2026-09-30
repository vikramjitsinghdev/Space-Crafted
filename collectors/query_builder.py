def build_equipment_queries(
    equipment_name: str
):
    name = equipment_name.strip()

    queries = [
        f'"{name}" engineering',
        f'"{name}" specifications',
        f'"{name}" design',
        f'"{name}" mass dimensions',
        f'"{name}" power electrical',
        f'"{name}" mobility',
        f'"{name}" performance',
        f'"{name}" thermal',
        f'"{name}" operations',
        f'"{name}" autonomous behavior',
        f'"{name}" mechanical',
    ]

    # Mission-specific aliases for known equipment.
    normalized = name.lower()

    if normalized in {
        "perseverance",
        "perseverance rover",
    }:

        queries.extend([
            '"Mars 2020" Perseverance engineering',
            '"Mars 2020" Perseverance rover design',
            '"Mars 2020" Perseverance rover mobility',
            '"Mars 2020" Perseverance rover power',
            '"Mars 2020" Perseverance rover thermal',
            '"Mars 2020" rover mechanical',
        ])

    return queries