class Converter:

    @staticmethod
    def string_to_bytes(text, size):
        data = text.encode()
        return data.ljust(size, b'\x00')

    @staticmethod
    def bytes_to_string(data):
        return data.decode().rstrip('\x00')

    # =========================
    # 8.3 FORMAT
    # =========================
    @staticmethod
    def to_83(name):

        name = name.upper()

        if "." in name:
            base, ext = name.split(".", 1)
        else:
            base, ext = name, ""

        base = base[:8]
        ext = ext[:3]

        return f"{base:<8}{ext:<3}"

    @staticmethod
    def from_83(name):

        base = name[:8].strip()
        ext = name[8:11].strip()

        if ext:
            return base + "." + ext
        return base