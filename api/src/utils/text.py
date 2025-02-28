import random
import string


def generate_profile_invite_path_string():
    char_set = string.ascii_letters
    part1 = (
        "".join(random.choice(char_set) for _ in range(4))
        + "-"
        + "".join(random.choice(char_set) for _ in range(4))
    )
    part2 = "".join(random.choice(char_set) for _ in range(8))
    generated_string = part1.lower() + "/" + part2.upper()
    return generated_string
