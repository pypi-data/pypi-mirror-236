import builtins


def check(rabbit: str):
    """
    Checks the input for potential issues such as:
     - encoding problems,
     - SQL queries,
     - Python/JS-related issues.

    :param rabbit: The input to be validated.
    """


    try:
        rabbit.encode('utf-8')
    except UnicodeEncodeError:
        return {False:"The encoding should be utf-8!"}

    if type(rabbit) is not builtins.str:
        return {False: f"Not string input!"}


    rabbit = rabbit.strip()
    rabbit = rabbit.lower()

    __py_forbidden_chars = (
        "\'", '\"', '=', 'or', 'in', 'for', 'while', 'true', 'false', '$', '#', ';', '(', ')', '-', '&', '%', '<', '>')

    sql_forbidden_queries = (
        "select",
        "insert",
        "update",
        "delete",
        "drop table",
        "create table",
        "alter table",
        "union"
    )

    forbidden = __py_forbidden_chars + sql_forbidden_queries

    for forbidden_item in forbidden:
        if forbidden_item in rabbit:
            return {False: f"Using {forbidden_item} is disallowed."}

    for char in rabbit:
        if char in forbidden:
            return {False:f"Using {char} is disallowed."}

    return {True:rabbit}
