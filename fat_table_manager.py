import struct
from fs_constants import FsConstants


class FatTableManager:

    def __init__(self, disk):
        self.disk = disk
        self.fat = [0] * FsConstants.CLUSTER_COUNT
        self.load()

    # =========================
    # LOAD FAT FROM DISK
    # =========================
    def load(self):

        data = b""

        for i in range(FsConstants.FAT_START_CLUSTER,
                       FsConstants.FAT_END_CLUSTER + 1):
            data += self.disk.read_cluster(i)

        for i in range(FsConstants.CLUSTER_COUNT):
            self.fat[i] = struct.unpack("i", data[i*4:i*4+4])[0]

    # =========================
    # FLUSH FAT TO DISK
    # =========================
    def flush(self):

        data = b"".join([struct.pack("i", x) for x in self.fat])

        idx = 0

        for i in range(FsConstants.FAT_START_CLUSTER,
                       FsConstants.FAT_END_CLUSTER + 1):

            self.disk.write_cluster(
                i,
                data[idx:idx + FsConstants.CLUSTER_SIZE]
            )
            idx += FsConstants.CLUSTER_SIZE

    # =========================
    # GET / SET FAT ENTRY
    # =========================
    def get_fat_entry(self, index):
        return self.fat[index]

    def set_fat_entry(self, index, value):
        self.fat[index] = value

    # =========================
    # READ ALL FAT
    # =========================
    def read_all_fat(self):
        return self.fat

    # =========================
    # WRITE ALL FAT
    # =========================
    def write_all_fat(self, entries):

        if len(entries) != FsConstants.CLUSTER_COUNT:
            raise ValueError("Invalid FAT size")

        self.fat = entries[:]
        self.flush()

    # =========================
    # FOLLOW CHAIN
    # =========================
    def follow_chain(self, start):

        chain = []

        while start != -1:
            chain.append(start)
            start = self.fat[start]

        return chain

    # =========================
    # ALLOCATE CHAIN
    # =========================
    def allocate_chain(self, count):

        free = []

        for i in range(FsConstants.CONTENT_START_CLUSTER,
                       FsConstants.CLUSTER_COUNT):

            if i < FsConstants.FAT_END_CLUSTER + 1:
                continue

            if self.get_fat_entry(i) == 0:
                free.append(i)

            if len(free) == count:
                break

        if len(free) < count:
            return None

        for i in range(len(free) - 1):
            self.set_fat_entry(free[i], free[i + 1])

        self.set_fat_entry(free[-1], -1)

        self.flush()
        return free[0]

    # =========================
    # FREE CHAIN
    # =========================
    def free_chain(self, start):

        while start != -1:
            nxt = self.get_fat_entry(start)
            self.set_fat_entry(start, 0)
            start = nxt

        self.flush()