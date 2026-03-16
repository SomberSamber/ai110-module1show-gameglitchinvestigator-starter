from app import check_guess

def test_winning_guess():
    # If the secret is 50 and guess is 50, it should be a win
    result = check_guess(50, 50)
    assert result == "Win"

def test_guess_too_high():
    # If secret is 50 and guess is 60, hint should be "Too High"
    result = check_guess(60, 50)
    assert result == "Too High"

def test_guess_too_low():
    # If secret is 50 and guess is 40, hint should be "Too Low"
    result = check_guess(40, 50)
    assert result == "Too Low"

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
