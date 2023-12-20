import math

class PDUEncoder:
    def __init__(self):
        self.seven_bit_default = ['@', '�', '$', '�', '�', '�', '�', '�', '�', '�', '\n', '�', '�', '\r', '�', '�', '\u0394', '_', '\u03a6', '\u0393', '\u039b', '\u03a9', '\u03a0', '\u03a8', '\u03a3', '\u0398', '\u039e', '�', '�', '�', '�', '�', ' ', '!', '"', '#', '�', '%', '&', '\'', '(', ')', '*', '+', ',', '-', '.', '/', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9', ':', ';', '<', '=', '>', '?', '�', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z', '�', '�', '�', '�', '�', '�', 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', '�', '�', '�', '�', '�']

    def bin_to_int(self, binary_string):
        total = 0
        power = len(binary_string) - 1
        for i in range(len(binary_string)):
            if binary_string[i] == '1':
                total += int(math.pow(2, power))
            power -= 1
        return total

    def int_to_hex(self, integer):
        return format(integer, '02x').upper()

    def get_seven_bit_index(self, character):
        for i, char in enumerate(self.seven_bit_default):
            if char == character:
                return i
        print(f"No 7-bit char for {character}")
        return 0

    def int_to_bin(self, number, size):
        bin_str = format(number, 'b')
        return bin_str.zfill(size)

    def string_to_pdu(self, input_string):
        bit_size = 7  # Assuming default bit size is 7
        octet_first = ""
        octet_second = ""
        output = ""

        user_data_size = self.int_to_hex(len(input_string))

        for i in range(len(input_string) + 1):
            if i == len(input_string):
                if octet_second != "":
                    output += self.int_to_hex(self.bin_to_int(octet_second))
                break
            current = self.int_to_bin(self.get_seven_bit_index(input_string[i]), 7)
            if i != 0 and i % 8 != 0:
                octet_first = current[7 - i % 8:]
                current_octet = octet_first + octet_second
                output += self.int_to_hex(self.bin_to_int(current_octet))
                octet_second = current[:7 - i % 8]
            else:
                octet_second = current[:7 - i % 8]

        pdu = output
        return pdu
