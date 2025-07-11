from Trie import Trie


def check_is_prime(n: int):
    """
    n is prime if it has only 2 divisors 1 and itself
    :param n: integer
    :return: True if n is prime, False otherwise
    """
    if n < 2:
        return False
    for i in range(2, int(n ** 0.5) + 1):
        if n % i == 0:
            return False
    return True


def test_check_is_prime():
    assert (check_is_prime(17) == True)
    assert (check_is_prime(248) == False)
    assert (check_is_prime(-3) == False)
    assert (check_is_prime(2) == True)


def check_string_is_palindrome(s: str):
    """
    s is palindrome if it is the same with his oglindit
    :param s: string
    :return: True if s is palindrome, False otherwise
    """
    reversed_s = ''.join(reversed(s))
    if s == reversed_s:
        return True
    return False


def test_check_string_is_palindrome():
    assert (check_string_is_palindrome("121") == True)
    assert (check_string_is_palindrome("32") == False)


def cmmdc(a, b):
    while b != 0:
        r = a % b
        a = b
        b = r
    return a


def test_cmmdc():
    assert (cmmdc(34, 12) == 2)
    assert (cmmdc(23, 17) == 1)


def nth_prime_number(n):
    if n < 1:
        raise ValueError("invalid")
    candidate = 2
    count = 0
    while count < n:
        if check_is_prime(candidate):
            count += 1
        if count == n:
            return candidate
        candidate += 1


def test_nth_prime_number():
    assert (nth_prime_number(2) == 3)
    assert (nth_prime_number(5) == 11)
    try:
        nth_prime_number(-32)
        assert False
    except ValueError as e:
        assert str(e) == "invalid"


def letter_freq(file):
    dict = {}
    with open(file, "r") as f:
        for line in f:
            current_line = line.strip()
            for char in current_line:
                if char not in dict:
                    dict[char] = 1
                else:
                    dict[char] += 1
    return dict


def test_letter_freq(file):
    dict = letter_freq(file)
    assert (dict['n'] == 1)
    assert (dict['e'] == 6)


def test_trie():
    trie = Trie()
    trie.insert("ted")
    trie.insert("tad")
    assert(trie.search("tad") == True)
    assert(trie.search("32") == False)


if __name__ == '__main__':
    test_check_is_prime()
    test_check_string_is_palindrome()
    test_cmmdc()
    test_nth_prime_number()
    path_to_file = "basic.txt"
    test_letter_freq(path_to_file)
    test_trie()
