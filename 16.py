import functools
import io
import math

import aoc


class EndOfBits(RuntimeError):
    pass


class PacketParseError(RuntimeError):
    pass


class BitStream:
    def __init__(self, input):
        self.__in = input
        self.__byte = 0
        self.__bits = 0
        self.__idx = 0

    def read_int(self, bits):
        '''
        >>> bits = BitStream(io.BytesIO(bytes.fromhex('abcd')))
        >>> bits.read_int(3)
        5
        >>> bits.read_int(5)
        11
        >>> bits.read_int(8)
        205
        '''
        assert(bits > 0)
        out = 0
        for _ in range(bits):
            out = (out << 1) | self.read_bit()
        return out
    
    def read_bit(self):
        '''
        >>> bits = BitStream(io.BytesIO(bytes.fromhex('ab')))
        >>> [bits.read_bit() for _ in range(8)]
        [1, 0, 1, 0, 1, 0, 1, 1]
        >>> bits.read_bit()  # doctest: +IGNORE_EXCEPTION_DETAIL
        Traceback (most recent call last):
        ...
        EndOfBits
        '''
        self.__bits -= 1
        if self.__bits < 0:
            byte = self.__in.read(1)
            if len(byte) == 0:
                raise EndOfBits()
            self.__byte = byte[0]
            self.__bits = 7
        self.__idx += 1
        return (self.__byte >> self.__bits) & 1

    def tell(self):
        return self.__idx


class Packet:

    def __init__(self, version):
        self.version = version

    @classmethod
    @property
    @functools.cache
    def TYPE_ID_MAP(cls):
        return {
            packet_type.TYPE_ID: packet_type
            for packet_type in globals().values()
            if hasattr(packet_type, 'TYPE_ID')
        }

    @classmethod
    def from_hex(cls, hex):
        bits = BitStream(io.BytesIO(bytes.fromhex(hex)))
        packet = cls.from_bit_stream(bits)
        while True:
            try:
                if bits.read_bit() == 1:
                    raise PacketParseError(f'found trailing 1 bit at position {bits.tell()}')
            except EndOfBits:
                break
        return packet

    @classmethod
    def from_bit_stream(cls, bits):
        version = bits.read_int(3)
        type_id = bits.read_int(3)
        try:
            packet_type = cls.TYPE_ID_MAP[type_id]
        except KeyError:
            raise PacketParseError(f'unknown packet type id {type_id} at position {bits.tell() - 6}') from None
        return packet_type.from_bit_stream_contents(version, bits)


class LiteralPacket(Packet):
    TYPE_ID = 4

    def __init__(self, version, value):
        super().__init__(version)
        self.value = value

    @classmethod
    def from_bit_stream_contents(cls, version, bits):
        value = 0
        keep_reading = True
        while keep_reading:
            keep_reading = bits.read_bit() == 1
            value = (value << 4) | bits.read_int(4)
        return cls(version, value)

    def eval(self):
        return self.value


class OperatorPacket(Packet):
    def __init__(self, version, packets):
        super().__init__(version)
        assert(all(isinstance(packet, Packet) for packet in packets))
        self.packets = packets

    @classmethod
    def from_bit_stream_contents(cls, version, bits):
        packets = []
        length_type_id = bits.read_bit()
        if length_type_id == 0:
            total_length = bits.read_int(15)
            end_bit = bits.tell() + total_length
            while bits.tell() < end_bit:
                packets.append(Packet.from_bit_stream(bits))
        else:
            num_packets = bits.read_int(11)
            for _ in range(num_packets):
                packets.append(Packet.from_bit_stream(bits))
        return cls(version, packets)


class SumPacket(OperatorPacket):
    TYPE_ID = 0

    def eval(self):
        sum = 0
        for packet in self.packets:
            sum += packet.eval()
        return sum


class ProductPacket(OperatorPacket):
    TYPE_ID = 1

    def eval(self):
        product = 1
        for packet in self.packets:
            product *= packet.eval()
        return product


class MinimumPacket(OperatorPacket):
    TYPE_ID = 2

    def eval(self):
        minimum = math.inf
        for packet in self.packets:
            minimum = min(minimum, packet.eval())
        return minimum


class MaximumPacket(OperatorPacket):
    TYPE_ID = 3

    def eval(self):
        maximum = -math.inf
        for packet in self.packets:
            maximum = max(maximum, packet.eval())
        return maximum


class GreaterThanPacket(OperatorPacket):
    TYPE_ID = 5

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        assert(len(self.packets) == 2)

    def eval(self):
        return 1 if self.packets[0].eval() > self.packets[1].eval() else 0


class LessThanPacket(OperatorPacket):
    TYPE_ID = 6

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        assert(len(self.packets) == 2)

    def eval(self):
        return 1 if self.packets[0].eval() < self.packets[1].eval() else 0


class EqualToPacket(OperatorPacket):
    TYPE_ID = 7

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        assert(len(self.packets) == 2)

    def eval(self):
        return 1 if self.packets[0].eval() == self.packets[1].eval() else 0


def solve(input):
    return answer1(input), answer2(input)


def answer1(input):
    '''
    >>> answer1('D2FE28')
    6
    >>> answer1('38006F45291200')
    9
    >>> answer1('EE00D40C823060')
    14
    >>> answer1('8A004A801A8002F478')
    16
    >>> answer1('620080001611562C8802118E34')
    12
    >>> answer1('C0015000016115A2E0802F182340')
    23
    >>> answer1('A0016C880162017C3686B18A3D4780')
    31
    '''
    def version_sum(packet):
        s = packet.version
        if isinstance(packet, OperatorPacket):
            for subpacket in packet.packets:
                s += version_sum(subpacket)
        return s
    return version_sum(Packet.from_hex(input.strip()))


def answer2(input):
    '''
    >>> answer2('C200B40A82')
    3
    >>> answer2('04005AC33890')
    54
    >>> answer2('880086C3E88112')
    7
    >>> answer2('CE00C43D881120')
    9
    >>> answer2('D8005AC2A8F0')
    1
    >>> answer2('F600BC2D8F')
    0
    >>> answer2('9C005AC2F8F0')
    0
    >>> answer2('9C0141080250320F1802104A08')
    1
    '''
    return Packet.from_hex(input.strip()).eval()
