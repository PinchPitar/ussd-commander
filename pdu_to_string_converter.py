class PDUDecoder:
    # GSM and extended character sets as class attributes
    gsm = (u"@£$¥èéùìòÇ\nØø\rÅåΔ_ΦΓΛΩΠΨΣΘΞ\x1bÆæßÉ !\"#¤%&'()*+,-./0123456789:;<=>"
           u"?¡ABCDEFGHIJKLMNOPQRSTUVWXYZÄÖÑÜ`¿abcdefghijklmnopqrstuvwxyzäöñüà")
    ext = (u"````````````````````^```````````````````{}`````\\````````````[~]`"
           u"|````````````````````````````````````€``````````````````````````")

    @staticmethod
    def get_bytes(plaintext):
        if type(plaintext) != str:
            plaintext = str(plaintext)
        bytes = []
        for c in plaintext:
            idx = PDUDecoder.gsm.find(c)
            if idx != -1:
                bytes.append(idx)
            else:
                idx = PDUDecoder.ext.find(c)
                if idx != -1:
                    bytes.append(27)  # Escape character
                    bytes.append(idx)
        return bytes

    @staticmethod
    def chunks(l, n):
        if n < 1:
            n = 1
        return [l[i:i + n] for i in range(0, len(l), n)]

    @staticmethod
    def pdu_to_string(codedtext):
        hexparts = PDUDecoder.chunks(codedtext, 2)
        number = 0
        bitcount = 0
        output = ''
        found_external = False

        for byte in hexparts:
            byte = int(byte, 16)
            number |= (byte << bitcount)  # Use bitwise OR to accumulate bits
            bitcount += 8  # Each byte contributes 8 bits

            while bitcount >= 7:
                # Process the 7-bit chunk
                septet = number & 0x7F  # Extract the 7-bit chunk
                if septet == 27:  # Escape character
                    found_external = True
                else:
                    if found_external:
                        character = PDUDecoder.ext[septet]
                        found_external = False
                    else:
                        character = PDUDecoder.gsm[septet]
                    output += character

                number >>= 7  # Discard the processed 7-bit chunk
                bitcount -= 7  # Decrement bitcount by 7 as 7 bits are processed

        return output
