from .version import __version__

ZERO = 0
ONE = 1
TWO = 2
TEN = 10
HUNDRED = 100


def is_odd(num):
    return num % TWO != ZERO


class GeezNumber:
    geez_one = "፩"
    geez_ten = "፲"
    geez_hundred = "፻"
    geez_ten_thousand = "፼"
    blank = ""

    def to_geez(self, number):
        digit = ZERO
        last_answer = self.blank
        
        while number > ZERO:
            left = number % HUNDRED
            number //= HUNDRED
            geez_num = self.guess_number(left)
            dividend = self.guess_divisor(digit)
            last_answer = self.mix_number(left, dividend, number, geez_num) + last_answer
            digit += 1
            
        return last_answer.replace("", "")
        
    def guess_number(self, number):
        tenth = int(number / TEN)
        one = int(number % TEN)
        geez = ""
        geez += chr(tenth + ord(self.geez_ten) - ONE) if tenth > ZERO else ""
        geez += chr(one + ord(self.geez_one) - ONE) if one > ZERO else ""
        return geez
    
    def guess_divisor(self, digit):
        if digit == ZERO:
            dividend = ""
        elif is_odd(digit):
            dividend = self.geez_hundred 
        else:
            dividend = self.geez_ten_thousand
        return dividend

    def mix_number(self, left, div, number, gz_number):
        if self.div_should_be_deleted(left, div):
            div = ""
        if self.geez_number_should_be_deleted(left, div, number):
            gz_number = ""
        
        return gz_number + div
    
    def geez_number_should_be_deleted(self, left, div, number):
        return (left == 1 and div == self.geez_hundred) or \
               (number == ZERO and div == self.geez_ten_thousand and left == 1)
        
    def div_should_be_deleted(self, left, div):
        return left == ZERO and (div == self.geez_hundred)


