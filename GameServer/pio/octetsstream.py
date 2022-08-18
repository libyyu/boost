from struct import pack, unpack
from pio.octets import Octets
from pio.marshal import MarshalException

MAXSPARE = 16384


class OctetsStream(Octets):
    def __init__(self, size=Octets.DEFAULT_SIZE, order='!'):
        Octets.__init__(self, size)
        self.pos = 0
        self.tranpos = 0
        self.order = order

    def wrap(self, octs):
        os = OctetsStream()
        os.order = self.order
        os.swap(octs)
        return os

    def __deepcopy__(self, memo):
        os = Octets.__deepcopy__(self, memo)
        os.pos = self.pos
        os.tranpos = self.pos
        os.order = self.order
        return os

    def __str__(self):
        return Octets.__str__(self)

    def byteorder(self, b):
        return self.order + b

    def eos(self):
        return self.size() == self.pos

    def marshal_int8(self, b):
        # b &= 0xff
        return self.push_back(pack(self.byteorder('b'), b))

    def marshal_uint8(self, b):
        # b &= 0xff
        return self.push_back(pack(self.byteorder('B'), b))

    def marshal_int16(self, b):
        # b &= 0xffff
        return self.push_back(pack(self.byteorder('h'), b))

    def marshal_uint16(self, b):
        # b &= 0xffff
        return self.push_back(pack(self.byteorder('H'), b))

    def marshal_int32(self, b):
        return self.push_back(pack(self.byteorder('i'), b))

    def marshal_uint32(self, b):
        # b &= 0xffffffffL
        return self.push_back(pack(self.byteorder('I'), b))

    def marshal_int64(self, b):
        # b &= 0xffffffffFFFFFFFFL
        return self.push_back(pack(self.byteorder('q'), b))

    def marshal_uint64(self, b):
        # b &= 0xffffffffFFFFFFFFL
        return self.push_back(pack(self.byteorder('Q'), b))

    def marshal_float(self, b):
        return self.push_back(pack(self.byteorder('f'), b))

    def marshal_double(self, b):
        return self.push_back(pack(self.byteorder('d'), b))

    def compact_uint32(self, x):
        # x &= 0xffffffffL
        if x < 0x40: return self.marshal_uint8(x)
        if x < 0x4000: return self.marshal_uint16(x | 0x8000)
        if x < 0x20000000: return self.marshal_uint32(x | 0xc0000000L)
        self.marshal_uint8(0xe0)
        return self.marshal_uint32(x)

    def compact_sint32(self, x):
        if x >= 0:
            if x < 0x40: return self.marshal_uint8(x)
            if x < 0x2000: return self.marshal_uint16(x | 0x8000)
            if x < 0x10000000: return self.marshal_uint32(x | 0xc0000000L)
            self.marshal_uint8(0xe0)
            return self.marshal_uint32(x)
        if -x > 0:
            x = -x
            if x < 0x40: return self.marshal_uint8(x | 0x40)
            if x < 0x2000: return self.marshal_uint16(x | 0xa000)
            if x < 0x10000000: return self.marshal_uint32(x | 0xd0000000L)
            self.marshal_uint8(0xf0)
            return self.marshal_uint32(x)

    def unmarshal_int8(self):
        if self.pos + 1 > self.size(): raise MarshalException()
        self.pos += 1
        return unpack(self.byteorder('b'), self.getstr(self.pos - 1, self.pos))[0]

    def unmarshal_uint8(self):
        if self.pos + 1 > self.size(): raise MarshalException()
        self.pos += 1
        return unpack(self.byteorder('B'), self.getstr(self.pos - 1, self.pos))[0]

    def unmarshal_int16(self):
        if self.pos + 2 > self.size(): raise MarshalException()
        self.pos += 2
        return unpack(self.byteorder('h'), self.getstr(self.pos - 2, self.pos))[0]

    def unmarshal_uint16(self):
        if self.pos + 2 > self.size(): raise MarshalException()
        self.pos += 2
        return unpack(self.byteorder('H'), self.getstr(self.pos - 2, self.pos))[0]

    def unmarshal_int32(self):
        if self.pos + 4 > self.size(): raise MarshalException()
        self.pos += 4
        return unpack(self.byteorder('i'), self.getstr(self.pos - 4, self.pos))[0]

    def unmarshal_uint32(self):
        if self.pos + 4 > self.size(): raise MarshalException()
        self.pos += 4
        return unpack(self.byteorder('I'), self.getstr(self.pos - 4, self.pos))[0]

    def unmarshal_int64(self):
        if self.pos + 8 > self.size(): raise MarshalException()
        self.pos += 8
        return unpack(self.byteorder('q'), self.getstr(self.pos - 8, self.pos))[0]

    def unmarshal_uint64(self):
        if self.pos + 8 > self.size(): raise MarshalException()
        self.pos += 8
        return unpack(self.byteorder('Q'), self.getstr(self.pos - 8, self.pos))[0]

    def unmarshal_float(self):
        if self.pos + 4 > self.size(): raise MarshalException()
        self.pos += 4
        return unpack(self.byteorder('f'), self.getstr(self.pos - 4, self.pos))[0]

    def unmarshal_double(self):
        if self.pos + 8 > self.size(): raise MarshalException()
        self.pos += 8
        return unpack(self.byteorder('d'), self.getstr(self.pos - 8, self.pos))[0]

    def uncompact_uint32(self):
        if self.pos == self.size(): raise MarshalException()
        x = ord(self.getbyte(self.pos)) & 0xe0
        if x == 0xe0:
            self.unmarshal_uint8()
            return self.unmarshal_uint32()
        if x == 0xc0:
            return self.unmarshal_uint32() & ~0xc0000000L
        if x == 0xa0 or x == 0x80:
            return self.unmarshal_uint16() & ~0x8000
        return self.unmarshal_uint8()

    def uncompact_sint32(self):
        if self.pos == self.size(): raise MarshalException()
        x = ord(self.getbyte(self.pos)) & 0xf0
        if x == 0xf0:
            self.unmarshal_uint8()
            return -(self.unmarshal_uint32())
        if x == 0xe0:
            self.unmarshal_uint8()
            return self.unmarshal_uint32()
        if x == 0xd0:
            return -(self.unmarshal_uint32() & ~0xd0000000L)
        if x == 0xc0:
            return self.unmarshal_uint32() & ~0xc0000000L
        if x == 0xb0 or x == 0xa0:
            return -(self.unmarshal_uint16() & ~0xa000)
        if x == 0x90 or x == 0x80:
            return self.unmarshal_uint16() & ~0x8000
        if x == 0x70 or x == 0x60 or x == 0x50 or x == 0x40:
            return -(self.unmarshal_uint8() & ~0x40)
        return self.unmarshal_uint8()

    def marshal(self, m):
        return m.marshal(self)

    def marshalos(self, o):
        self.compact_uint32(o.size())
        self.append(o)
        return self

    def unmarshalos(self, o):
        size = self.uncompact_uint32()
        if self.pos + size > self.size(): raise MarshalException()
        o.replace2(self, self.pos, size)
        self.pos = self.pos + size
        return self

    def unmarshal_os(self):
        size = self.uncompact_uint32()
        if self.pos + size > self.size(): raise MarshalException()
        os = Octets().replace2(self, self.pos, size)
        self.pos = self.pos + size
        return os

    def unmarshal(self, m):
        if isinstance(m, Octets):
            return self.unmarshalos(m)
        return m.unmarshal(self)

    def begin(self):
        self.tranpos = self.pos
        return self

    def rollback(self):
        self.pos = self.tranpos
        return self

    def commit(self):
        if self.pos >= MAXSPARE:
            self.erase(0, self.pos)
            self.pos = 0
        return self


