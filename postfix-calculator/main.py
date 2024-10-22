def postfix_calculator(expression: str) -> float:
    """
    Evaluates a postfix expression and returns the result.
    Args:
        expression (str): A string containing a postfix expression where tokens are separated by spaces.
                          Tokens can be numbers or operators (+, -, *, /, ^).
    Returns:
        float: The result of evaluating the postfix expression.
    Raises:
        IndexError: If the expression is invalid and there are not enough operands for an operator.
        ValueError: If the token cannot be converted to a float.
    Example:
        >>> postfix_calculator("2 4 * 2 -")
        6.0

        >>> postfix_calculator("13 15 2 * 1 51 - 3 2 ^ ^ / +")
        12.999999999999984
    """

    operators = ("+", "-", "*", "/", "^")
    stack = []

    for token in expression.split():
        if token not in operators:
            stack.append(float(token))
        else:
            b = stack.pop()
            a = stack.pop()

            if token == "+":
                stack.append(a + b)
            elif token == "-":
                stack.append(a - b)
            elif token == "*":
                stack.append(a * b)
            elif token == "/":
                stack.append(a / b)
            elif token == "^":
                stack.append(a**b)

    return stack.pop()


if __name__ == "__main__":
    expression = input("Enter a postfix expression: ")
    result = postfix_calculator(expression)
    print(f"Result: {result}")
