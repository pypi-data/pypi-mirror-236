from social_validator.telegram import (
    CHAT_NAME_MAX_LENGTH,
    COMMAND_MAX_LENGTH,
    DESCRIPTION_BOT_MAX_LENGTH,
    DESCRIPTION_CHANNEL_MAX_LENGTH,
    DESCRIPTION_GROUP_MAX_LENGTH,
    DESCRIPTION_USER_MAX_LENGTH,
    FIRST_NAME_MAX_LENGTH,
    ID_MAX_LENGTH,
    ID_MIN_LENGTH,
    LAST_NAME_MAX_LENGTH,
    MEDIA_MESSAGE_MAX_LENGTH,
    MESSAGE_MAX_LENGTH,
)

RANDOM_UNICODE_STRING = "➷⡞⍄⪮ⴱ⧕⭀₃⵽▊⯛⪔⸠Ⱀ❠∭⯲⮈ⅈ⭐ℭ⥙⑼"

VALID_IDS = (
    "A" * ID_MAX_LENGTH,
    "A" * ID_MIN_LENGTH,
    "B12345",
    "Z12345",
    "Q_t_e_s_t",
    "Q_1_2_3_4_5",
)

INVALID_IDS = (
    "A" * (ID_MIN_LENGTH - 1),
    "A" * (ID_MAX_LENGTH + 1),
    "123456",
    "_test",
    "__test",
    "test__",
    "t__q__",
    "t______",
    "1_test",
    "тест_ид",
    RANDOM_UNICODE_STRING,
)

VALID_BOT_IDS = (
    f"{'A' * 2}bot",
    f"{'A' * (ID_MAX_LENGTH - 3)}bot",
    "B12345bot",
    "Z12345_bot",
    "Q_1_2_3_4_5bot",
)

INVALID_BOT_IDS = (
    "Abot",
    f"{'A' * (ID_MAX_LENGTH - 2)}bot",
    "123456bot",
    "_testbot",
    "__testbot",
    "test__bot",
    "t__q__bot",
    "t______bot",
    "1_testbot",
    "тестовый_идbot",
    f"{RANDOM_UNICODE_STRING}bot",
    "correct_name_without_suffix",
)

VALID_DESCRIPTIONS = (
    ("", "user"),
    ("a" * DESCRIPTION_USER_MAX_LENGTH, "user"),
    (RANDOM_UNICODE_STRING, "user"),
    ("", "group"),
    ("a" * DESCRIPTION_GROUP_MAX_LENGTH, "group"),
    (RANDOM_UNICODE_STRING, "group"),
    ("", "channel"),
    ("a" * DESCRIPTION_CHANNEL_MAX_LENGTH, "channel"),
    (RANDOM_UNICODE_STRING, "channel"),
    ("", "bot"),
    ("a" * DESCRIPTION_BOT_MAX_LENGTH, "bot"),
    (RANDOM_UNICODE_STRING, "bot"),
)

INVALID_DESCRIPTIONS = (
    ("A" * (DESCRIPTION_USER_MAX_LENGTH + 1), "user"),
    ("A" * (DESCRIPTION_GROUP_MAX_LENGTH + 1), "group"),
    ("A" * (DESCRIPTION_CHANNEL_MAX_LENGTH + 1), "channel"),
    ("A" * (DESCRIPTION_BOT_MAX_LENGTH + 1), "bot"),
)

VALID_CHAT_NAMES = (
    "A",
    "A" * CHAT_NAME_MAX_LENGTH,
    RANDOM_UNICODE_STRING,
)

INVALID_CHAT_NAMES = (
    "",
    "A" * (CHAT_NAME_MAX_LENGTH + 1),
)

VALID_FIRST_NAMES = (
    "A",
    "A" * FIRST_NAME_MAX_LENGTH,
    RANDOM_UNICODE_STRING,
)

INVALID_FIRST_NAMES = (
    "",
    "A" * (FIRST_NAME_MAX_LENGTH + 1),
)

VALID_LAST_NAMES = (
    "",
    "A" * LAST_NAME_MAX_LENGTH,
    RANDOM_UNICODE_STRING,
)

INVALID_LAST_NAMES = ("A" * (LAST_NAME_MAX_LENGTH + 1),)

VALID_FULL_NAMES = (
    # this may be a bit hard to read,
    # but here we just map each first_name to each last_name
    *(
        (first_name, last_name)
        for last_name in VALID_LAST_NAMES
        for first_name in VALID_FIRST_NAMES
    ),
    # map valid first names to empty last name
    *((first_name, "") for first_name in VALID_FIRST_NAMES),
)

INVALID_FULL_NAMES = (
    # this may be even more difficult to read,
    # but here we simply map the correct and incorrect first and last names
    # in order to get a validation error in the final result
    *(
        (first_name, last_name)
        for last_name in INVALID_LAST_NAMES
        for first_name in VALID_FIRST_NAMES
    ),
    *(
        (first_name, last_name)
        for last_name in VALID_LAST_NAMES
        for first_name in INVALID_FIRST_NAMES
    ),
    *(
        (first_name, last_name)
        for last_name in INVALID_LAST_NAMES
        for first_name in INVALID_FIRST_NAMES
    ),
    # map invalid first names to empty last name
    *((first_name, "") for first_name in INVALID_FIRST_NAMES),
)

VALID_MESSAGES = (
    # (text: str, include_media: bool)
    ("A", False),
    ("A" * MESSAGE_MAX_LENGTH, False),
    (RANDOM_UNICODE_STRING, False),
    ("A", True),
    ("A" * MEDIA_MESSAGE_MAX_LENGTH, True),
    (RANDOM_UNICODE_STRING, True),
)

INVALID_MESSAGES = (
    # (text: str, include_media: bool)
    ("", False),
    ("A" * (MESSAGE_MAX_LENGTH + 1), False),
    ("", True),
    ("A" * (MEDIA_MESSAGE_MAX_LENGTH + 1), True),
)

VALID_COMMANDS = (
    "A",
    "A" * COMMAND_MAX_LENGTH,
    "12345",
    "_",
    "_____",
    "_test",
    "__test",
    "_12345",
    "__12345",
    "another__test__",
    "double_underscore__",
    "t_e_s_t_u_n_d_e_r_s_c_o_r_e_s",
    "1_2_3_4_5",
    "test12345withDIGITS",
)

INVALID_COMMANDS = (
    "",
    "A" * (COMMAND_MAX_LENGTH + 1),
    RANDOM_UNICODE_STRING,
)
