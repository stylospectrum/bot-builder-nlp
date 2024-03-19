def evaluate_expression(expression, data: dict, entities: list):
    if expression["operator"] == "And":
        for sub_expression in expression.get("sub_exprs", []):
            if not evaluate_expression(sub_expression, data, entities):
                return False
        return True
    elif expression["operator"] == "Or":
        for sub_expression in expression.get("sub_exprs", []):
            if evaluate_expression(sub_expression, data, entities):
                return True
        return False
    elif expression["operator"] == "Equal":
        attribute_id = expression["attribute"]
        attribute = next(
            (entity for entity in entities if entity["id"] == attribute_id), None
        )
        value = expression["value"]

        if attribute["name"] in data:
            return data[attribute["name"]] == value

        return False
    else:
        raise ValueError(
            "Unsupported expression operator: {}".format(expression["operator"])
        )
