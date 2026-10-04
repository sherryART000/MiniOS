import struct

class DirectoryEntry:

    def __init__(self, name="", attr=0, first=0, size=0):
        self.name = name
        self.attr = attr
        self.first_cluster = first
        self.file_size = size

    def to_bytes(self):

        name = self.name.encode().ljust(12, b'\x00')

        return struct.pack(
            "=12sBii11s",
            name,
            self.attr,
            self.first_cluster,
            self.file_size,
            b'\x00' * 11
        )

    @staticmethod
    def from_bytes(data):

        n, a, f, s, _ = struct.unpack(
            "=12sBii11s",
            data
        )

        return DirectoryEntry(
            n.decode().rstrip("\x00"),
            a,
            f,
            s
        )