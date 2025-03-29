import random

def gen(bin_input, month=None, year=None, cvv=None, amount=10):
    generated_cards = set()  # Store unique card numbers
    bin_template = bin_input.replace('x', '#')

    if '#' not in bin_template:
        bin_template += '#' * (16 - len(bin_template))  # Ensure it's a full card number

    # Detect card type
    if bin_template.startswith('4'):
        card_type = 'VISA'
    elif bin_template.startswith(('51', '52', '53', '54', '55')):
        card_type = 'MASTERCARD'
    elif bin_template.startswith(('34', '37')):
        card_type = 'AMEX'
    elif bin_template.startswith('6'):
        card_type = 'DISCOVER'
    else:
        card_type = 'UNKNOWN'

    while len(generated_cards) < amount:
        card_number = list(bin_template)

        # Replace # with random digits
        for i in range(len(card_number)):
            if card_number[i] == '#':
                card_number[i] = str(random.randint(0, 9))

        card_number = ''.join(card_number)

        # Luhn Algorithm Calculation
        luhn_sum = 0
        reverse_digits = list(map(int, card_number[:-1]))[::-1]

        for i, digit in enumerate(reverse_digits):
            if i % 2 == 0:
                digit *= 2
                if digit > 9:
                    digit -= 9
            luhn_sum += digit

        check_digit = (10 - (luhn_sum % 10)) % 10
        full_card_number = card_number[:-1] + str(check_digit)

        if full_card_number not in generated_cards:
            generated_cards.add(full_card_number)

    # Generate Expiry Date & CVV
    generated_results = []
    for card in generated_cards:
        exp_month = month if month else str(random.randint(1, 12)).zfill(2)
        exp_year = year if year else str(random.randint(24, 30))
        cvv_code = (
            cvv if cvv 
            else str(random.randint(100, 999)).zfill(3) if card_type != 'AMEX' 
            else str(random.randint(1000, 9999)).zfill(4)
        )
        generated_results.append(f"<code>{card}|{exp_month}|{exp_year}|{cvv_code}</code>")

    return '\n'.join(generated_results)