# long arguments
normal_name = normal_function_name(
    "but with super long string arguments that on their own exceed the line limit so there's no way it can ever fit",
    "eggs with spam and eggs and spam with eggs with spam and eggs and spam with eggs with spam and eggs and spam with eggs",
    this_is_a_ridiculously_long_name_and_nobody_in_their_right_mind_would_use_one_like_it=0,
)

print(
    "This is a really long string inside of a print statement with extra arguments"
    " attached at the end of it.",
    x,
    y,
    z,
)

arg_comment_string = print(
    "Long lines with inline comments which are apart of (and not the only member of) an"
    " argument list should have their comments appended to the reformatted string's"
    " enclosing left parentheses.",  # This is a comment
    "Arg #2",
    "Arg #3",
    "Arg #4",
    "Arg #5",
)

already_wrapped_in_parens(
    (
        " lorem ipsum dolor sit amet consectetur adipiscing elit sed do eiusmod"
        " tempor incididunt ut labore et dolore magna aliqua Ut enim ad minim"
    ),
    " lorem ipsum dolor sit amet consectetur adipiscing elit sed do eiusmod tempor",
)

already_wrapped_in_parens_but_short(
    (
        "short"
        " string"
    ),
    another_arg,
)


# output


# long arguments
normal_name = normal_function_name(
    "but with super long string arguments that on their own exceed the line"
    " limit so there's no way it can ever fit",
    "eggs with spam and eggs and spam with eggs with spam and eggs and spam"
    " with eggs with spam and eggs and spam with eggs",
    this_is_a_ridiculously_long_name_and_nobody_in_their_right_mind_would_use_one_like_it=0,
)

print(
    "This is a really long string inside of a print statement with extra"
    " arguments attached at the end of it.",
    x,
    y,
    z,
)

arg_comment_string = print(
    "Long lines with inline comments which are apart of (and not the only"
    " member of) an argument list should have their comments appended to the"
    " reformatted string's enclosing left parentheses.",  # This is a comment
    "Arg #2",
    "Arg #3",
    "Arg #4",
    "Arg #5",
)

already_wrapped_in_parens(
    (
        " lorem ipsum dolor sit amet consectetur adipiscing elit sed do eiusmod"
        " tempor incididunt ut labore et dolore magna aliqua Ut enim ad minim"
    ),
    " lorem ipsum dolor sit amet consectetur adipiscing elit sed do eiusmod"
    " tempor",
)

already_wrapped_in_parens_but_short(
    "short string",
    another_arg,
)
