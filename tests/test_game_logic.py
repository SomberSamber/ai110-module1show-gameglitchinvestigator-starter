from app import check_guess, get_range_for_difficulty, parse_guess, update_score

def test_winning_guess():
    # check_guess returns a tuple; first element is the outcome
    outcome, _ = check_guess(50, 50)
    assert outcome == "Win"

def test_guess_too_high():
    outcome, _ = check_guess(60, 50)
    assert outcome == "Too High"

def test_guess_too_low():
    outcome, _ = check_guess(40, 50)
    assert outcome == "Too Low"

# --- Tests for integer-vs-integer comparison (regression for the string-coercion bug) ---

def test_check_guess_returns_tuple():
    # check_guess returns (outcome, message), not just a string
    outcome, message = check_guess(50, 50)
    assert outcome == "Win"
    assert isinstance(message, str)

def test_single_digit_guess_less_than_two_digit_secret():
    # 9 < 10 numerically, but "9" > "10" lexicographically.
    # With integer secrets this must report "Too Low", not "Too High".
    outcome, _ = check_guess(9, 10)
    assert outcome == "Too Low"

def test_two_digit_guess_less_than_larger_two_digit_secret():
    # 20 < 99: straightforward numeric case that also fails string comparison
    # ("20" < "99" happens to be correct, but verifying numeric path is reliable)
    outcome, _ = check_guess(20, 99)
    assert outcome == "Too Low"

def test_two_digit_guess_greater_than_single_digit_secret():
    # 20 > 9 numerically, but "20" < "9" lexicographically.
    # Must report "Too High", not "Too Low".
    outcome, _ = check_guess(20, 9)
    assert outcome == "Too High"

def test_boundary_one_below_secret():
    outcome, _ = check_guess(49, 50)
    assert outcome == "Too Low"

def test_boundary_one_above_secret():
    outcome, _ = check_guess(51, 50)
    assert outcome == "Too High"


# --- Tests for get_range_for_difficulty (covers the hardcoded-range new_game bug) ---

def test_range_easy():
    low, high = get_range_for_difficulty("Easy")
    assert low == 1
    assert high == 20

def test_range_normal():
    low, high = get_range_for_difficulty("Normal")
    assert low == 1
    assert high == 100

def test_range_hard():
    low, high = get_range_for_difficulty("Hard")
    assert low == 1
    assert high == 50

def test_range_unknown_defaults_to_normal():
    low, high = get_range_for_difficulty("Unknown")
    assert low == 1
    assert high == 100


# --- Tests for parse_guess ---

def test_parse_guess_valid_integer():
    ok, value, err = parse_guess("42")
    assert ok is True
    assert value == 42
    assert err is None

def test_parse_guess_valid_float_truncates():
    ok, value, err = parse_guess("3.9")
    assert ok is True
    assert value == 3

def test_parse_guess_empty_string():
    ok, value, err = parse_guess("")
    assert ok is False
    assert value is None

def test_parse_guess_none():
    ok, value, err = parse_guess(None)
    assert ok is False
    assert value is None

def test_parse_guess_non_numeric():
    ok, value, err = parse_guess("abc")
    assert ok is False
    assert value is None


# --- Tests for update_score ---

def test_update_score_win_early():
    # Win on attempt 1: 100 - 10*(1+1) = 80 points added
    score = update_score(0, "Win", 1)
    assert score == 80

def test_update_score_win_minimum_points():
    # Win very late: score floor is 10
    score = update_score(0, "Win", 10)
    assert score == 10

def test_update_score_too_high_even_attempt():
    # Even attempt number gets +5
    score = update_score(50, "Too High", 2)
    assert score == 55

def test_update_score_too_high_odd_attempt():
    # Odd attempt number gets -5
    score = update_score(50, "Too High", 3)
    assert score == 45

def test_update_score_too_low():
    score = update_score(50, "Too Low", 1)
    assert score == 45
