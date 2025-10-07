import random
import string
from typing import List

# Configurables
USE_SYMBOLS = "!@#$%.,_{}[]/<>"
PASSWORD_LEN = 36
UPPER = (1, None)
LOWER = (1, None)
DIGITS = (1, None)
SYMBOLS = (4, 10)


class PassRule:
    def __init__(self, rule_type, minchars, maxchars, charvals):
        self.rule_type = rule_type
        self.minchars = minchars
        self.maxchars = maxchars
        self.charvals = charvals
        self.returned_chars = 0

    def get_min(self):
        chars = [random.choice(self.charvals) for _ in range(self.minchars)]
        self.returned_chars += self.minchars
        return chars

    def get_max(self):
        if self.maxchars is None:
            return ""
        remaining = self.maxchars - self.returned_chars
        chars = [random.choice(self.charvals) for _ in range(remaining)]
        self.returned_chars += remaining
        return chars

    def get_next_char(self):
        if self.maxchars is not None and self.returned_chars >= self.maxchars:
            return ""
        char = random.choice(self.charvals)
        self.returned_chars += 1
        return char

    def get_charvals(self):
        return self.charvals


def rule_validation(rules: List[PassRule], password_length: int):
    all_have_max = all(rule.maxchars is not None for rule in rules)
    if all_have_max:
        total_max = sum(rule.maxchars for rule in rules)
        if total_max < password_length:
            raise ValueError(
                f"Sum of max values ({total_max}) is less than "
                f"password length ({password_length})"
            )


def generate_password():
    length = PASSWORD_LEN
    password_chars = []

    rules = [
        PassRule("Upper", UPPER[0], UPPER[1], string.ascii_uppercase),
        PassRule("Lower", LOWER[0], LOWER[1], string.ascii_lowercase),
        PassRule("Digit", DIGITS[0], DIGITS[1], string.digits),
        PassRule("Symbols", SYMBOLS[0], SYMBOLS[1], USE_SYMBOLS),
    ]

    rule_validation(rules, length)

    for rule in rules:
        password_chars.extend(rule.get_min())

    while len(password_chars) < length:
        rule = random.choice(rules)
        char = rule.get_next_char()
        if char:
            password_chars.append(char)

    random.shuffle(password_chars)
    return "".join(password_chars)


def genpass():
    print(generate_password())


if __name__ == "__main__":
    genpass()