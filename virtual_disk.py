import os
from fs_constants import FsConstants


class VirtualDisk:

    def __init__(self):
        self.file = None

    def initialize(self, path):

        if not os.path.exists(path):
            with open(path, "wb") as f:
                f.write(b'\x00' * FsConstants.DISK_SIZE)

        self.file = open(path, "r+b")

    def read_cluster(self, cluster):

        if cluster < 0 or cluster >= FsConstants.CLUSTER_COUNT:
            raise ValueError("Invalid cluster number")

        self.file.seek(cluster * FsConstants.CLUSTER_SIZE)
        return self.file.read(FsConstants.CLUSTER_SIZE)

    def write_cluster(self, cluster, data):

        if cluster < 0 or cluster >= FsConstants.CLUSTER_COUNT:
            raise ValueError("Invalid cluster number")

        self.file.seek(cluster * FsConstants.CLUSTER_SIZE)
        self.file.write(data.ljust(FsConstants.CLUSTER_SIZE, b'\x00'))
        self.file.flush()

    def get_disk_size(self):
        return FsConstants.DISK_SIZE

    def close(self):
        if self.file:
            self.file.close()