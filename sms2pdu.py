
# Config params
DEFAULT_SMSC = '0794999000'
DEFAULT_COMMAND = '11'
DEFAULT_MSG_REF = '00'
DEFAULT_TPID = '00'
DEFAULT_TPVALIDITY = 'AA'


class Sms:
    def __init__(self, smsc, source, dest, message):
        self.smsc = smsc
        self.source = source
        self.dest = dest
        self.message = message

    def get_source_len(self):
        return len(self.source)

    def get_source_type(self):
        return '91'

    def get_dest_len(self):
        return len(self.dest)

    def get_dest_type(self):
        return '91'


class Sms2PduConverter:

    def __init__(self, sms):
        self.sms = sms

    def to_hex_string(self, number):
        return format(number, '02x')

    def to_binary_string(self, bin):
        return format(bin, '0b')

    def semi_octed_to_string(self, number):
        inverted_number = ''
        if len(number) % 2 != 0:
            number += 'F'

        for i in xrange(0, len(number), 2):
            s1, s2 = number[i:i+2]
            inverted_number += s2 + s1

        return inverted_number

    def get_message_length(self, message):
        return format(len(message), '02x')

    def encode_message(self, message):
        message = self._convert_message_to_binary(message)
        message = self._convert_octet_to_hex(message)
        return message

    def _convert_message_to_binary(self, message):
        converted_message = ''
        for i in range(0, len(message)):
            c = message[i]
            bin_str = self.to_binary_string(ord(c))
            bin_str = bin_str.zfill(7)
            converted_message += bin_str[::-1]

        return converted_message

    def _convert_octet_to_hex(self, binary_message):
        converted_message = ''
        for i in range(0, len(binary_message), 8):
            encoded_octet = binary_message[i:i+8][::-1].zfill(8)
            encoded_octet_hex = format(int(encoded_octet, 2), 'x')
            converted_message += encoded_octet_hex.upper()

        return converted_message

    def get_pdu(self):
        return '00' \
            + DEFAULT_COMMAND \
            + DEFAULT_MSG_REF \
            + self.to_hex_string(sms.get_dest_len()) \
            + self.semi_octed_to_string(sms.dest) \
            + DEFAULT_TPID \
            + DEFAULT_TPVALIDITY \
            + self.get_message_length(sms.message) \
            + self.encode_message(sms.message)


if __name__ == "__main__":

    smsc_number = raw_input('SMSC number (hit ENTER for default)> ')
    source_number = raw_input('Source number> ')
    destination_number = raw_input('Destination number> ')
    user_data = raw_input('Message> ')

    sms = Sms(smsc_number, source_number, destination_number, user_data)
    converter = Sms2PduConverter(sms)

    #msg = converter.encode_message(sms.message)
    #print msg
    print converter.get_pdu()