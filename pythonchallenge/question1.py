"""
reference: http://www.pythonchallenge.com/pc/def/map.html
"""

# given the cipher key
# K == M, O == Q, E == G

# decode the ciphertext

ciphertext = "g fmnc wms bgblr rpylqjyrc gr zw fylb. rfyrq ufyr amknsrcpq ypc dmp. bmgle gr gl zw fylb gq glcddgagclr ylb rfyr'q ufw rfgq rcvr gq qm jmle. sqgle qrpgle.kyicrpylq() gq pcamkkclbcb. lmu ynnjw ml rfc spj. "

alphabet = 'abcdefghijklmnopqrstuvwxyz'

difference = alphabet.index('k') - alphabet.index('m')

def shift_cipher(cipher_text, shift):
    """
    given text and shift
    returns new string
    """

    new_string = ''
    alphabet_len = len(alphabet) - 1
    for character in cipher_text:

        if not character in alphabet: #if the letter is not in alphabet, append
            new_string += character
            continue

        original_index = alphabet.index(character)
        new_index = original_index - shift
        if new_index < 0:
            new_string += alphabet[-new_index]
            continue
        if new_index > alphabet_len:
            new_index -= alphabet_len+1
        new_string += alphabet[new_index]
        print(new_string)
    return new_string

shift_cipher(ciphertext, difference)


























#
