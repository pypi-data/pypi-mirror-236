# Do not change function name or arguments
def generate(args: list[any]):
    if args is None:
        return ""
    if len(args) == 0:
        return ""
    if isinstance(args, list) == False:
        return ""
    result = args[0]
    if isinstance(result, str) is False:
        result = str(result)
    return result