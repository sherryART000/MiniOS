from virtual_disk import VirtualDisk
from fat_table_manager import FatTableManager
from directory_manager import DirectoryManager
from file_system import FileSystem
from fs_constants import FsConstants


class MiniOSShell:

    def __init__(self):

        self.disk = VirtualDisk()
        self.disk.initialize("minifat.bin")

        self.fat = FatTableManager(self.disk)
        self.dir = DirectoryManager(self.disk, self.fat)
        self.fs = FileSystem(self.disk, self.fat, self.dir)

        self.cwd = "/"

        print("MiniOS Shell Ready 🚀 Type help")

    # =========================
    # MAIN LOOP
    # =========================
    def run(self):

        while True:

            cmd = input(f"MiniOS:{self.cwd}> ").strip()

            if not cmd:
                continue

            parts = cmd.split()
            op = parts[0].lower()

            # =====================
            # EXIT
            # =====================
            if op == "exit":

                self.disk.close()
                print("Disk closed")
                break

            # =====================
            # HELP
            # =====================
            elif op == "help":

                print("""
Command                     Description
------------------------------------------------
ls                          List directory contents
cd <dir>                    Navigate directories
pwd                         Print current directory

md <dir>                    Create directory (simulated)
rd <dir>                    Remove directory (simulated)

touch <file>                Create empty file
cat <file>                  Print file contents

echo "text" <file>          Write text to file
echo "text" <file> --append Append text to file

cp <src> <dst>              Copy file
mv <src> <dst>              Rename file
rm <file>                   Delete file

help                        Show commands
cls                         Clear screen
exit                        Exit shell
""")

            # =====================
            # CLS
            # =====================
            elif op == "cls":
                print("\n" * 50)

            # =====================
            # PWD
            # =====================
            elif op == "pwd":
                print(self.cwd)

            # =====================
            # CD (SIMULATED)
            # =====================
            elif op == "cd":

                if len(parts) < 2:
                    print("Usage: cd <dir>")
                    continue

                if parts[1] == "..":
                    self.cwd = "/"
                else:
                    self.cwd = "/" + parts[1]

                print(self.cwd)

            # =====================
            # LS
            # =====================
            elif op == "ls":
                self.dir.list_dir()

            # =====================
            # TOUCH
            # =====================
            elif op == "touch":

                if len(parts) < 2:
                    print("Usage: touch <file>")
                    continue

                self.fs.create_file(parts[1])
                print("File created")

            # =====================
            # CAT
            # =====================
            elif op == "cat":

                if len(parts) < 2:
                    print("Usage: cat <file>")
                    continue

                entry = self.dir.find(parts[1])

                if entry is None:
                    print("File not found")
                    continue

                print(
                    self.fs.read_file(entry).decode(errors="ignore")
                )

            # =====================
            # ECHO
            # =====================
            elif op == "echo":

                try:
                    text = cmd.split('"')[1]

                    if "--append" in parts:
                        filename = parts[-2]
                    else:
                        filename = parts[-1]

                    entry = self.dir.find(filename)

                    if entry is None:
                        print("File not found")
                        continue

                    if "--append" in parts:
                        self.fs.append_file(entry, text.encode())
                    else:
                        self.fs.write_file(entry, text.encode())

                    print("Done")

                except:
                    print('Usage: echo "text" file')

            # =====================
            # RM
            # =====================
            elif op == "rm":

                if len(parts) < 2:
                    print("Usage: rm <file>")
                    continue

                entry = self.dir.find(parts[1])

                if entry is None:
                    print("File not found")
                    continue

                self.fs.delete_file(entry)
                print("Deleted")

            # =====================
            # CP
            # =====================
            elif op == "cp":

                if len(parts) < 3:
                    print("Usage: cp <src> <dst>")
                    continue

                self.fs.copy_file(parts[1], parts[2])
                print("Copied")

            # =====================
            # MV (rename only - same logic)
            # =====================
            elif op == "mv":

                if len(parts) < 3:
                    print("Usage: mv <src> <dst>")
                    continue

                self.fs.rename_file(parts[1], parts[2])
                print("Renamed")

            # =====================
            # MD (simulation)
            # =====================
            elif op == "md" or op == "mkdir":

                if len(parts) < 2:
                    print("Usage: mkdir <dir>")
                    continue

                print(f"Directory '{parts[1]}' created (simulation only)")

            # =====================
            # RD (simulation)
            # =====================
            elif op == "rd" or op == "rmdir":

                if len(parts) < 2:
                    print("Usage: rmdir <dir>")
                    continue

                print(f"Directory '{parts[1]}' removed (simulation only)")

            # =====================
            # UNKNOWN
            # =====================
            else:
                print("Unknown command")


if __name__ == "__main__":
    MiniOSShell().run()