import math

LINE_SEP_EQ = \
    "================================================================================================================="
LINE_SEP_MIN = \
    "-----------------------------------------------------------------------------------------------------------------"

CONV = "to convert"


# map_to_char : Natural -> String
# Takes a character's number value (0 through 36)
# Returns the corresponding 1 character string (returns "-" if number out of valid range)
def map_to_char(num):
    # If the supplied digit is negative or greater than 36, return "-" since no value represents it
    if num < 0 or num > 36:
        return "-"
    # If the number should remain as the supplied digit (0 through 9)
    elif num < 10:
        return str(num)
    # If the number is between 10 and 36, convert it to it's respective uppercase unicode letter
    else:
        # adds how much larger than 10 the number is to the unicode value of A, then convert back to a unicode string
        return chr(ord('A') + num - 10)


# map_from_char : String -> Natural
# Takes a 1 character string
# Returns the character's number value (0 through 36, or -1 if invalid)
def map_from_char(c):
    # Make sure to only process the first character of the string, and convert to uppercase to standardize letters
    o = ord(c[0].upper())
    # If the supplied string is a digit 0 through 9, return it as an integer
    if ord('0') <= o <= ord('9'):
        return int(c)
    # If the string is between A and Z, return the corresponding numbers 10 through 36
    elif ord('A') <= o <= ord('Z'):
        return int(o - ord('A') + 10)
    # Else, the input is invalid hence return -1
    else:
        return -1


# power_of : Natural Natural -> Boolean
# Returns an true if a and b are positive integers, and a to some integer exponent greater than 1 is equal to b
def power_of(a, b):
    log = math.log(b, a)
    return log.is_integer() and log >= 2


# invalid_base : String -> Boolean
# Checks to make sure base is valid (both an integer and in range [2, 36])
def invalid_base(b):
    return (not b.isdigit()) or int(b) > 36 or int(b) < 2


# invalid_number : Natural String -> Boolean
# Checks to make sure all characters in the number are valid in the given base
def invalid_number(b, n):
    # If the number is an empty string, it is not a valid number
    if n == "":
        return True
    # Check each character in the given number
    for ch in n:
        resp = map_from_char(str(ch))
        # If any character in the string is invalid, or greater than what the base allows, return that it is invalid
        if resp == -1 or resp >= b:
            return True
    return False


# convert : Natural Natural String String Boolean -> String
# Converts the supplied number (as a string, to support non-digit bases) from first base to second base, using the
# specified method, and prints the output (skips trying shortcut method if given False)
def convert(from_base, to_base, num, meth, try_shortcut):
    alg = "division algorithm"
    sep = LINE_SEP_MIN
    if try_shortcut:
        sep = LINE_SEP_EQ
    if meth == "l":
        alg = "largest fit"

    print("\n%s\nConverting %s from base %s to base %s using the %s method:\n%s" % (sep, num, from_base, to_base, alg,
                                                                                    sep))
    resp = str(num).lstrip("0")
    # If the number was all zeroes, resp will be ""
    if resp == "":
        print("No conversion is needed since the number is 0")
        resp = "0"
    # If the number was all zeroes, resp will be ""
    elif resp == "1":
        print("No conversion is needed since the number is 1")
        resp = "1"
    # If both bases are equal, return the same answer
    elif from_base == to_base:
        print("The bases are the same, no conversion is needed.")
    # If the second base is a power of the first base, show shortcut method
    elif try_shortcut and power_of(from_base, to_base):
        m = input(
            "The base %s is a power of the base %s, would you like to use the shortcut method (Y/n)?: "
            % (to_base, from_base)
        ).lower()
        if m != "n":
            compress_by_base(from_base, to_base, resp, meth)
            m = input("Would you like to see the non-shortcut method also (Y/n)?: ").lower()
            if m != "n":
                convert(from_base, to_base, resp, meth, False)
        else:
            convert(from_base, to_base, resp, meth, False)
    # If the first base is a power of the second base, show shortcut method
    elif try_shortcut and power_of(to_base, from_base):
        m = input(
            "The base %s is a power of the base %s, would you like to use the shortcut method (Y/n)?: " %
            (from_base, to_base)
        ).lower()
        if m != "n":
            expand_by_base(from_base, to_base, resp, meth)
            m = input("Would you like to see the non-shortcut method also (Y/n)? ")[0].lower()
            if m != "n":
                convert(from_base, to_base, resp, meth, False)
        else:
            convert(from_base, to_base, resp, meth, False)
    # If from base 10, convert to base directly
    elif from_base == 10:
        if meth == "d":
            resp = div_alg_dec2base(to_base, int(resp))
            print("%s\nThe combined result (read from bottom up) is %s (base %s)" % (sep, resp, to_base))
        else:
            resp = largest_fit_dec2base(to_base, int(resp))
            print("%s\nThe combined result (read from top down) is %s (base %s)" % (sep, resp, to_base))
    # If from some base to base 10, convert only from base to decimal
    elif to_base == 10:
        if meth == "d":
            resp = div_alg_base2dec(from_base, resp)
            print("%s\nThe combined result is %s (base 10)" % (sep, resp))
        else:
            resp = largest_fit_base2dec(from_base, resp)
            print("%s\nThe combined result is %s (base 10)" % (sep, resp))
    # Else, convert from_base to base 10, and base 10 to to_base
    else:
        resp = convert(10, to_base, convert(from_base, 10, resp, meth, False), meth, False)
    return str(resp)


# div_alg_dec2base : Natural Natural -> String
# Division algorithm to convert from base 10 to a provided base (string output to support non-integer digits)
def div_alg_dec2base(to_base, num):
    print("Take the number and perform the modulo of the given base (AKA the remainder when dividing num/to_base).")
    print("Divide the number you're doing this on by the base, take the floor of it, and repeat the previous step on "
          "that until the number is 0.\n")
    # If the number is 0, return "0" in all cases
    if num == 0 or num == 1:
        print("%s: converting %s to any base is still %s" % (num, num, num))
        return str(num)
    ret_str = ""
    while num != 0:
        rem = int(num % to_base)
        rem_map = map_to_char(rem)
        print("%s: next rightmost position is %s %% %s = %s" % (rem_map, num, to_base, rem))
        ret_str = rem_map + ret_str
        num = int(num / to_base)
    return ret_str


# div_alg_base2dec : Natural String-> Natural
# Division algorithm to convert to base 10 from a provided base (string input to support non-integer digits)
def div_alg_base2dec(from_base, num):
    print("Take the leftmost digit, multiply it by the base, and add the next leftmost digit.")
    print("Repeat by taking that result, multiplying it by the base, and adding the next leftmost digit until no digits"
          " remain.\n")
    prev = 0
    # While more digits remain, calculate the leftmost digit
    while num != "":
        # Convert leftmost character into an integer value
        curr_digit = map_from_char(num[0])
        # Modulo of base to get leftmost position digit
        new_prev = int(prev * from_base + curr_digit)
        # print(
        #     "Multiplying the previously calculated number by the base, and adding the leftmost digit value we get: %4s"
        #     " * %2s + %2s = %8s" % (prev, from_base, curr_digit, new_prev))
        print(
            "%s = %s * %s + %s (multiplying the previously calculated number by the base, and adding the next leftmost "
            "digit value)" % (new_prev, prev, from_base, curr_digit))
        num = num[1:]
        prev = new_prev
    return prev


# largest_fit_dec2base : Natural Natural -> String
# Largest fit to convert from base 10 to a provided base (string output to support non-integer digits)
def largest_fit_dec2base(to_base, num):
    print("Find the largest power of the base that isn't greater than the number.")
    print("Divide the number by that, and take the floor of it to get a digit.")
    print("Subtract that power times your result from the number, and repeat the previous steps with that as your new "
          "number until you reach 1 as the power you're testing.\n")
    max_power = to_base
    output = ""
    # Find the first base raised to some power that is greater than to_base
    while max_power <= num:
        max_power *= to_base
    # Divide the result by to_base to get the largest that is less than or equal
    max_power /= to_base
    print(
        "Find how many times the largest power of %s fits into %s, subtract it, and repeat it on the new value"
        % (to_base, num))
    # Try getting how many times the largest base fits into the number, dividing the base by to_base until it is 1
    while max_power >= 1:
        if max_power <= num:
            digit = int(num / max_power)
            print(
                "%s: since %s fits into %s %s times, the new num value is %s - (%s * %s)"
                % (map_to_char(digit), int(max_power), num, digit, num, digit, max_power))
            num = int(num - digit * max_power)
            output += map_to_char(digit)
        else:
            print("0: since %s does not fit into %s" % (int(max_power), num))
            output += "0"
        max_power /= to_base
    return output


# largest_fit_base2dec : Natural String -> Natural
# Largest fit to convert to base 10 from a provided base (string input to support non-integer digits)
def largest_fit_base2dec(from_base, num):
    print("Find the corresponding exponent values of each digit position, and multiply by the value at that "
          "position.\n")
    prev = 0
    # While the number has more digits, calculate the leftmost digit
    while num != "":
        curr_digit = map_from_char(num[0])
        num_len = len(num)
        position_val = int(from_base ** (num_len - 1))
        # If the current digit has a non-zero value, add it accordingly
        if curr_digit != 0:
            prev = int(position_val * curr_digit + prev)
            print("The %s from right digit (%s ^ %s position) is %s hence: %s * %s = %s" % (
                num_len, from_base, (num_len - 1), num[0], curr_digit, position_val, position_val * curr_digit))
        num = str(num[1:])
    print("The sum of those yields %s" % prev)
    return prev


# compress_by_base : Natural Natural String String -> String
# if to_base is a power of from_base, compress the characters of num into one character in the from_base output
def compress_by_base(from_base, to_base, num, meth):
    bits = int(math.log(to_base, from_base))
    num_out = ""
    print("Converting each %s characters going right to left from the number into 1 character in base %s"
          % (bits, to_base))
    # While there is more bits to compress
    while num != "":
        right = (num[-bits:])
        num = num[:-bits]
        res = convert(from_base, 10, right, meth, False)
        res_map = map_to_char(int(res))
        print("Which is %s in base %s" % (res_map, to_base))
        num_out = res_map + num_out
    print("\nCombining those results from right to left, the complete number is %s (base %s)" % (num_out, to_base))
    return num_out


# expand_by_base : Natural Natural String String -> String
# if from_base if a power of to_base, this function will expand each character of the input number into the amount of
# bits needed for to_base
def expand_by_base(from_base, to_base, num, meth):
    bits = int(math.log(from_base, to_base))
    num_out = ""
    print("Converting each character going left to right into %s characters in base %s"
          % (bits, to_base))
    for ch in num:
        ch_num = map_from_char(ch)
        print("\nThe next leftmost digit %s represents %s in base %s, hence convert %s from base 10 to base %s: " % (
            ch, ch_num, from_base, ch_num, to_base))
        curr = convert(10, to_base, str(ch_num), meth, False).rjust(bits, '0')
        print("Write 0's to the left if needed (to reach %s bits) to get %s" % (bits, curr))
        num_out += curr
    num_out = num_out.lstrip("0")
    print(
        "\nCombining those results from left to right, and removing the extra 0's on the left of the result, the "
        "complete number is %s (base %s)"
        % (num_out, to_base))
    return num_out


# in_twos_complement_range : Integer Natural -> Boolean
# Checks if the supplied integer can be represented in the given amount of bits in two's complement
def in_twos_complement_range(num, bits):
    return -(2 ** (bits - 1)) <= num < (2 ** (bits - 1))


# is_integer : String -> Boolean
# Checks if a number is an integer
def is_integer(n):
    try:
        int(n)
        return True
    except ValueError:
        return False


# flip_bits : String -> Boolean
# replaces all bits from 1->0 and 0->1 for a binary string
def flip_bits(n):
    str_out = ""
    for ch in n:
        if ch == "0":
            str_out += "1"
        else:
            str_out += "0"
    return str_out


# binary_add1 : String -> String
# adds 1 to a binary string
def binary_add1(n):
    index = 1
    length = len(n)
    while index <= length:
        if n[-index] == "0":
            break
        index += 1
    # If 0 in leftmost position, or no zero (overflow case), print a 1 then index amount of 0's
    if index == (length + 1) or index == length:
        str_out = "1" + "0" * (index - 1)
    # Otherwise, take the part of the string before the rightmost 0, append a "1", then all 0's to the right
    else:
        str_out = n[:(length - index)] + "1" + "0" * (index - 1)
    return str_out


# to_twos_complement : Integer Natural String -> String
# Converts a number from base 10 to 2's complement in the given amount of bits using the provided method
def to_twos_complement(num, bits, meth):
    if num < 0:
        print("The provided number is negative, so we deal with the positive version and remember the -\n\n")
        result = convert(10, 2, str(-num), meth, True).rjust(bits, '0')
        print("The result of converting positive %s is %s (padded with 0's to fit in %s bits)" % (-num, result, bits))
        result = flip_bits(result)
        print("Flipping the bits, the result is %s" % result)
        result = binary_add1(result)
        print("Adding 1 we get %s" % result)
    else:
        print("The provided number is positive, so we do regular binary to decimal conversion\n\n")
        result = convert(10, 2, str(num), meth, True).rjust(bits, '0')
        print("The result of converting %s is %s (padded with 0's to fit in %s bits)" % (num, result, bits))
    return result


# from_twos_complement : String String -> String
# Converts a number from 2's complement to base 10 using the given method
def from_twos_complement(num, meth):
    if num[0] == "0":
        print("\nThe provided number is positive since the leftmost bit is 0, hence use regular binary conversion:")
        result = convert(2, 10, num, meth, False)
    else:
        print("\nThe provided number is negative since the leftmost bit is 1.")
        resp = flip_bits(num)
        print("First, flip the bits of the number to get from %s to %s" % (num, resp))
        resp = binary_add1(resp)
        print("Next, add 1 to the resulting binary number (puts a 1 in rightmost 0 position, with everything to the "
              "right becoming 0, or overflows into all 0's and an extra 1 on the left).")
        print("In this case the result is %s" % resp)
        print("Now, convert that number into base 10 and append the - sign since it was negative:"
              "")
        result = -int(convert(2, 10, resp, meth, False))
        print("Since we stated the number would be negative, add the minus sign back yielding %s" % result)
    return str(result)


# get_method : None -> String
# Prompts the user to enter a method until a valid method is supplied
def get_method():
    m = input("Enter method to use (d)ivision alg or (l)argest fit: ").lower()
    while m != "d" and m != "l":
        m = input("Invalid method, enter \"d\" or \"l\" for (d)ivision alg or (l)argest fit: ").lower()
    return m


# get_base : String -> Natural
# Prompts the user to enter a base until a valid base is supplied (natural number between 2 and 36)
def get_base(s):
    b = input("Enter the base [2, 36] you want to convert %s (eg. 2): " % s)
    while invalid_base(b):
        b = input("Invalid base, enter base [2, 36] you want to convert %s (eg. 2): " % s)
    return int(b)


# get_num : String Natural -> String
# Prompts the user to enter a number until a valid number in the given base is supplied
def get_num(s, b):
    n = input("Enter the number %s: " % s)
    while invalid_number(b, n):
        n = input(
            "Invalid number. Make sure each digit is valid in this base (digits between 0 and %s): "
            % map_to_char(b - 1))
    return str(n)


# get_int : None -> Integer
# Prompts the user to enter a number until a valid integer is supplied
def get_int():
    n = input("Enter the number to convert: ")
    while not is_integer(n):
        n = input("Invalid number. Make sure each digit is valid in this base (digits between 0 and 10): ")
    return int(n)


def main():
    ret_val = "-1"
    while True:
        print("%s\nWhich subject would you like to know more about?\n%s" % (LINE_SEP_EQ, LINE_SEP_EQ))
        print("(1) Base Conversion")
        print("(2) Two's Complement conversion (2's comp <--> Decimal)")
        print("(q) to quit")
        p = input("%s\nType the key corresponding to which option you'd like: " % LINE_SEP_MIN)
        if p == "1":
            # Get the from_base, to_base, number, and method
            fb = get_base("FROM")
            tb = get_base("TO")
            n = get_num(CONV, fb)
            m = get_method()
            # Convert
            ret_val = convert(int(fb), int(tb), str(n), str(m), True)
            print("\n\n")
        elif p == "2":
            b = "-1"
            while b != "2" and b != "1":
                b = input(
                    "Do you want to:\n"
                    "(1) Convert 2's complement -> base 10 (decimal)\n"
                    "(2) Convert base 10 (decimal) -> 2's complement\n")
                if b == "1":
                    comp_num = get_num(CONV, 2)
                    m = get_method()
                    ret_val = from_twos_complement(comp_num, m)
                    break
                elif b == "2":
                    dec_num = get_int()
                    bits = int(get_num("of bits", 10))
                    while not in_twos_complement_range(dec_num, bits):
                        print(
                            "The given number was out of range. For %s bits, select a different number between %s and "
                            "%s: " % (
                                bits, -(2 ** (bits - 1)), ((2 ** (bits - 1)) - 1)))
                        dec_num = get_int()
                    m = get_method()
                    ret_val = to_twos_complement(dec_num, bits, m)
                    break
                else:
                    print("Invalid option, please select 1 or 2")
        elif p == "q":
            print("\nThank you for using my software, goodbye!")
            break
        else:
            print("Invalid input, please try another option")
        print("\n")
    return ret_val


if __name__ == "__main__":
    main()
