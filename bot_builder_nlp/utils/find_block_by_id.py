def find_block_by_id(data, target_id: str):
    if data["id"] == target_id:
        return data

    for child in data.get("children", []):
        result = find_block_by_id(child, target_id)
        if result is not None:
            return result

    return None
