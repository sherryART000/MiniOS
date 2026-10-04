from fs_constants import FsConstants
from directory_entry import DirectoryEntry
from converter import Converter

class DirectoryManager:

    def __init__(self, disk, fat):
        self.disk = disk
        self.fat = fat
        self.entries = []
        self.load()

    def load(self):

        data = self.disk.read_cluster(
            FsConstants.ROOT_DIR_CLUSTER
        )

        self.entries = []

        for i in range(0, FsConstants.CLUSTER_SIZE, 32):

            chunk = data[i:i+32]

            if chunk[0] == 0:
                continue

            self.entries.append(
                DirectoryEntry.from_bytes(chunk)
            )

    def flush(self):

        data = bytearray(FsConstants.CLUSTER_SIZE)

        idx = 0

        for e in self.entries:

            data[idx:idx+32] = e.to_bytes()
            idx += 32

        self.disk.write_cluster(
            FsConstants.ROOT_DIR_CLUSTER,
            bytes(data)
        )

    def add(self, entry):

        for e in self.entries:
            if e.name.lower() == entry.name.lower():
                print("File already exists")
                return

        self.entries.append(entry)
        self.flush()

    def list_dir(self):

        print("\n===== DIR =====")

        for e in self.entries:
            print(f"{Converter.from_83(e.name)} | {e.file_size}")
        print("================\n")

    def find(self, name):

        name = Converter.to_83(name).strip().lower()

        for e in self.entries:
          if e.name.strip().lower() == name:
              return e

        return None

    def remove(self, entry):

        if entry in self.entries:
            self.entries.remove(entry)
            self.flush()