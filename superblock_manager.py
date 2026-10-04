from fs_constants import FsConstants


class SuperblockManager:

    def __init__(self, disk):
        self.disk = disk

    def read_superblock(self):
        return self.disk.read_cluster(FsConstants.SUPERBLOCK_CLUSTER)

    def write_superblock(self, data):
        self.disk.write_cluster(FsConstants.SUPERBLOCK_CLUSTER, data)