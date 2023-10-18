from ast import literal_eval

from .options import *


def parse_json(json_string: str, allow_partial: Allow = ALL, /):
    if not isinstance(json_string, str):
        raise TypeError(f"expecting str, got {type(json_string).__name__}")
    if not json_string.strip():
        raise ValueError(f"{json_string!r} is empty")
    return _parse_json(json_string.strip(), allow_partial)


class PartialJSON(ValueError):
    pass


class MalformedJSON(ValueError):
    pass


def _parse_json(json_string: str, allow: Allow):
    length = len(json_string)
    index = 0

    def mark_partial_json(msg: str):
        raise PartialJSON(f"{msg} at position {index}")

    def raise_malformed_error(msg: str):
        raise MalformedJSON(f"{msg} at position {index}")

    def parse_any():  # type: () -> str | dict | list | int | float | bool | None
        nonlocal index
        skip_blank()
        if index >= length:
            mark_partial_json("Unexpected end of input")
        if json_string[index] == '"':
            return parse_str()
        if json_string[index] == "{":
            return parse_obj()
        if json_string[index] == "[":
            return parse_arr()
        if json_string[index : index + 4] == "null" or NULL in allow and length - index < 4 and "null".startswith(json_string[index:]):
            index += 4
            return None
        if json_string[index : index + 4] == "true" or BOOL in allow and length - index < 4 and "true".startswith(json_string[index:]):
            index += 4
            return True
        if json_string[index : index + 5] == "false" or BOOL in allow and length - index < 5 and "false".startswith(json_string[index:]):
            index += 5
            return False
        if json_string[index : index + 8] == "Infinity" or INFINITY in allow and length - index < 8 and "Infinity".startswith(json_string[index:]):
            index += 8
            return float("inf")
        if json_string[index : index + 9] == "-Infinity" or _INFINITY in allow and 1 < length - index < 9 and "-Infinity".startswith(json_string[index:]):
            index += 9
            return float("-inf")
        if json_string[index : index + 3] == "NaN" or NAN in allow and length - index < 3 and "NaN".startswith(json_string[index:]):
            index += 3
            return float("nan")
        return parse_num()

    def parse_str():  # type: () -> str
        nonlocal index
        start = index
        escape = False
        index += 1  # skip initial quote
        try:
            while json_string[index] != '"' or escape and json_string[index - 1] == "\\":
                escape = not escape if json_string[index] == "\\" else False
                index += 1
        except IndexError:
            if STR in allow:
                try:
                    return literal_eval(json_string[start : index - escape] + '"')
                except SyntaxError:
                    # SyntaxError: (unicode error) truncated \uXXXX or \xXX escape
                    return literal_eval(json_string[start : json_string.rindex("\\", max(0, index - 5))] + '"')
            mark_partial_json("Unterminated string literal")
        index += 1  # skip final quote
        return literal_eval(json_string[start:index])

    def parse_obj():
        nonlocal index
        index += 1  # skip initial brace
        skip_blank()
        obj = {}
        try:
            while json_string[index] != "}":
                skip_blank()
                if index >= length:
                    return obj
                key = parse_str()
                skip_blank()
                index += 1  # skip colon
                try:
                    value = parse_any()
                except PartialJSON:
                    if OBJ in allow:
                        return obj
                    raise
                obj[key] = value
                skip_blank()
                if json_string[index] == ",":
                    index += 1  # skip comma
        except (IndexError, PartialJSON):
            if OBJ in allow:
                return obj
            mark_partial_json("Expected '}' at end of object")
        index += 1  # skip final brace
        return obj

    def parse_arr():
        nonlocal index
        index += 1  # skip initial bracket
        arr = []
        try:
            while json_string[index] != "]":
                arr.append(parse_any())
                skip_blank()
                if json_string[index] == ",":
                    index += 1  # skip comma
        except (IndexError, PartialJSON):
            if ARR in allow:
                return arr
            mark_partial_json("Expected ']' at end of array")
        index += 1  # skip final bracket
        return arr

    def parse_num():  # type: () -> int | float
        nonlocal index
        if index == 0:
            if json_string == "-":
                mark_partial_json("Not sure what '-' is")
            try:
                return literal_eval(json_string)
            except SyntaxError:
                return literal_eval(json_string[: json_string.rindex("e", index - 2)])
            except ValueError as err:
                raise_malformed_error(str(err).capitalize())
        start = index
        try:
            if json_string[index] == "-":
                index += 1
            while json_string[index] not in ",]}":
                index += 1
        except IndexError:
            if NUM not in allow:
                mark_partial_json("Unterminated number literal")
        try:
            return literal_eval(json_string[start:index])
        except SyntaxError:
            if json_string[start:index] == "-":
                mark_partial_json("Not sure what '-' is")
            return literal_eval(json_string[start : json_string.rindex("e", index - 2)])
        except ValueError:
            raise_malformed_error(f"Unknown entity {json_string[start : index]!r}")

    def skip_blank():
        nonlocal index
        while index < length and (json_string[index] == " " or json_string[index] == "\n"):
            index += 1

    return parse_any()


dumps = decode = parse_json


__all__ = ["dumps", "decode", "parse_json", "PartialJSON", "MalformedJSON", "Allow"]
