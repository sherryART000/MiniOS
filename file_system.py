import math
from directory_entry import DirectoryEntry
from fs_constants import FsConstants
from converter import Converter

class FileSystem:

    def __init__(self, disk, fat, dir):
        self.disk = disk
        self.fat = fat
        self.dir = dir

    def create_file(self, name):

        if self.dir.find(name):
            print("File already exists")
            return None

        entry = DirectoryEntry(Converter.to_83(name), 0, 0, 0)
        self.dir.add(entry)
        return entry

    def write_file(self, entry, data):

        clusters = math.ceil(len(data) / FsConstants.CLUSTER_SIZE)

        start = self.fat.allocate_chain(clusters)

        if start is None:
            print("Not enough space")
            return

        entry.first_cluster = start
        entry.file_size = len(data)

        chain = self.fat.follow_chain(start)

        idx = 0

        for c in chain:
            chunk = data[idx:idx+FsConstants.CLUSTER_SIZE]
            self.disk.write_cluster(c, chunk)
            idx += FsConstants.CLUSTER_SIZE

        self.dir.flush()

    def read_file(self, entry):

        if entry.first_cluster == 0:
            return b""

        data = b""

        for c in self.fat.follow_chain(entry.first_cluster):
            data += self.disk.read_cluster(c)

        return data[:entry.file_size]

    def delete_file(self, entry):

        if entry.first_cluster != 0:
            self.fat.free_chain(entry.first_cluster)

        self.dir.remove(entry)

    def append_file(self, entry, data):

        old = self.read_file(entry)
        new_data = old + data
        self.write_file(entry, new_data)

    def rename_file(self, old, new):

        entry = self.dir.find(old)
        if not entry:
            return

        if self.dir.find(new):
            print("Duplicate name")
            return

        entry.name = new.upper()
        self.dir.flush()

    def copy_file(self, src, new_name):

        entry = self.dir.find(src)
        if not entry:
            return

        data = self.read_file(entry)

        if self.dir.find(new_name):
            print("File exists")
            return

        new_entry = DirectoryEntry(new_name.upper(), 0, 0, len(data))
        self.dir.add(new_entry)

        self.write_file(new_entry, data)