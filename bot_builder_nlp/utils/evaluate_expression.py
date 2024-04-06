def evaluate_expression(expression, data: dict, variables: list):
    if expression["operator"] == "And":
        for sub_expression in expression.get("sub_exprs", []):
            if not evaluate_expression(sub_expression, data, variables):
                return False
        return True
    elif expression["operator"] == "Or":
        for sub_expression in expression.get("sub_exprs", []):
            if evaluate_expression(sub_expression, data, variables):
                return True
        return False
    elif expression["operator"] in ["Equal", "NotEqual"]:
        variable = next(
            (
                variable
                for variable in variables
                if variable.get("id", "") == expression["variable_id"]
            ),
            None,
        )
        if variable and variable["name"] in data:
            if expression["operator"] == "Equal":
                return data[variable["name"]] == expression.get('value')
            elif expression["operator"] == "NotEqual":
                return data[variable["name"]] != expression.get('value')

        return False
    else:
        raise ValueError(
            "Unsupported expression operator: {}".format(expression["operator"])
        )
