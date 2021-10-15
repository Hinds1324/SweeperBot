# Dictionary that remembers arguments that users previously passed to certain commands.
# Allows users to repeat commands with previous arguments so they don't have to type the arguments again.
last_user_inputs = {}


def get_last_user_input(user, key):
    input_dict = last_user_inputs.get(user)
    if input_dict is None:
        return
    else:
        return input_dict.get(key)


def set_last_user_input(user, key, value):
    input_dict = last_user_inputs.get(user) or {}
    input_dict[key] = value
    last_user_inputs[user] = input_dict


def resolve_input(user, key, value, default_value):
    value = value or get_last_user_input(user, key) or default_value
    set_last_user_input(user, key, value)

    return value
