# 💾 MiniOS — MiniFAT File System

A lightweight **virtual file system and command-line shell** implemented from scratch in Python.

This project simulates the core concepts of an operating system file system, including:

* Virtual disk management
* FAT (File Allocation Table)
* Cluster-based storage
* Directory entries
* File creation and deletion
* File reading and writing
* File appending
* File copying
* File renaming
* A command-line shell
* Persistent storage using a binary disk image

The project was developed to understand how operating systems manage files and storage at a low level.

---

# 🚀 Project Overview

**MiniOS** provides a small command-line environment that behaves similarly to a basic operating system shell.

Instead of using the host operating system's normal file system directly, the project creates and manages its own virtual disk:

```text
minifat.bin
```

The virtual disk is divided into fixed-size clusters.

The file system then manages these clusters using a simplified **FAT (File Allocation Table)** structure.

The overall architecture is:

```text
                MiniOS Shell
                     │
                     ▼
               File System
                     │
          ┌──────────┴──────────┐
          ▼                     ▼
   Directory Manager       FAT Manager
          │                     │
          └──────────┬──────────┘
                     ▼
                Virtual Disk
                     │
                     ▼
                minifat.bin
```

---

# ✨ Main Features

## 📁 File Management

The system supports:

* Create files
* Read files
* Write files
* Append to files
* Delete files
* Copy files
* Rename files
* List directory contents

---

## 💾 Virtual Disk

The project creates a binary file that acts as a virtual disk:

```text
minifat.bin
```

The virtual disk has:

```text
Cluster Size  = 1024 bytes
Cluster Count = 1024
Disk Size     = 1 MB
```

The disk is divided into fixed-size clusters:

```text
1 KB × 1024 clusters = 1,048,576 bytes
```

---

# 🧠 File System Layout

The virtual disk is divided into several regions.

```text
┌──────────────────────────────┐
│ Cluster 0                    │
│ Superblock                   │
├──────────────────────────────┤
│ Clusters 1 - 4               │
│ FAT                          │
├──────────────────────────────┤
│ Cluster 5                    │
│ Root Directory               │
├──────────────────────────────┤
│ Clusters 6 - 1023            │
│ File Content                 │
└──────────────────────────────┘
```

This layout is defined in `fs_constants.py`.

```python
CLUSTER_SIZE = 1024
CLUSTER_COUNT = 1024

SUPERBLOCK_CLUSTER = 0

FAT_START_CLUSTER = 1
FAT_END_CLUSTER = 4

ROOT_DIR_CLUSTER = 5

CONTENT_START_CLUSTER = 6
```

---

# 🗂️ FAT — File Allocation Table

The project uses a simplified FAT structure to keep track of file storage.

Each cluster has an entry in the FAT.

For example:

```text
Cluster     FAT Entry
-------     ---------
6           7
7           8
8           15
15          -1
```

This means the file occupies:

```text
6 → 7 → 8 → 15 → END
```

The FAT manager follows this chain when reading the file.

---

# 🔗 Cluster Allocation

When a file needs storage, the system searches for free clusters.

A free cluster is represented by:

```text
0
```

The end of a file's cluster chain is represented by:

```text
-1
```

For example, if a file requires three clusters:

```text
10 → 11 → 12 → -1
```

The corresponding FAT entries become:

```text
FAT[10] = 11
FAT[11] = 12
FAT[12] = -1
```

---

# 📄 Directory Entries

Each file is represented by a `DirectoryEntry`.

A directory entry stores:

```text
File Name
Attributes
First Cluster
File Size
Reserved Space
```

The structure is serialized using Python's `struct` module.

```python
struct.pack(
    "=12sBii11s",
    name,
    attr,
    first_cluster,
    file_size,
    reserved
)
```

Each directory entry occupies:

```text
32 bytes
```

---

# 🔤 8.3 Filename Format

The project includes a simplified implementation of the classic **8.3 filename format**.

A filename is represented using:

```text
8 characters for the name
3 characters for the extension
```

Example:

```text
document.txt
```

becomes approximately:

```text
DOCUMENTTXT
```

The conversion is handled by:

```text
converter.py
```

Main methods:

```python
Converter.to_83()
Converter.from_83()
```

---

# 🏗️ Project Architecture

```text
MiniOS
│
├── Shell Layer
│      │
│      └── shell.py
│
├── File System Layer
│      │
│      └── file_system.py
│
├── Directory Layer
│      │
│      ├── directory_manager.py
│      └── directory_entry.py
│
├── Allocation Layer
│      │
│      └── fat_table_manager.py
│
├── Storage Layer
│      │
│      └── virtual_disk.py
│
├── Disk Metadata
│      │
│      ├── superblock_manager.py
│      └── fs_constants.py
│
└── Utilities
       │
       └── converter.py
```

---

# 📂 Project Structure

```text
MiniOS/
│
├── converter.py
├── directory_entry.py
├── directory_manager.py
├── fat_table_manager.py
├── file_system.py
├── fs_constants.py
├── shell.py
├── superblock_manager.py
├── virtual_disk.py
│
└── minifat.bin
```

`minifat.bin` is created automatically when the program runs for the first time.

---

# 🧩 Components

## 1. `virtual_disk.py`

Responsible for low-level virtual disk operations.

It creates the binary disk image:

```text
minifat.bin
```

and provides:

```python
read_cluster()
write_cluster()
get_disk_size()
close()
```

Instead of accessing physical disk sectors, the project uses file offsets:

```python
cluster * CLUSTER_SIZE
```

For example:

```text
Cluster 6
    ↓
6 × 1024
    ↓
Offset 6144 bytes
```

This allows the binary file to behave like a small virtual disk.

---

# 2. `fs_constants.py`

Contains the file system configuration.

```python
CLUSTER_SIZE = 1024
CLUSTER_COUNT = 1024
DISK_SIZE = CLUSTER_SIZE * CLUSTER_COUNT
```

It also defines the locations of the major file-system regions.

This keeps the disk layout centralized instead of hard-coding values throughout the project.

---

# 3. `fat_table_manager.py`

Responsible for managing the File Allocation Table.

Main responsibilities:

### Load FAT

Reads the FAT from the virtual disk.

```python
load()
```

### Save FAT

Writes the FAT back to the disk.

```python
flush()
```

### Read Entry

```python
get_fat_entry()
```

### Modify Entry

```python
set_fat_entry()
```

### Follow File Chain

```python
follow_chain()
```

### Allocate Clusters

```python
allocate_chain()
```

### Free Clusters

```python
free_chain()
```

---

# 4. `directory_entry.py`

Represents one file entry in the root directory.

Example:

```python
DirectoryEntry(
    name="HELLO   TXT",
    attr=0,
    first=6,
    size=120
)
```

The entry can be converted to binary data using:

```python
to_bytes()
```

and reconstructed using:

```python
from_bytes()
```

This allows directory information to persist inside the virtual disk.

---

# 5. `directory_manager.py`

Manages the root directory.

Responsibilities include:

```text
Load directory
Add file entry
Remove file entry
Find file
List files
Flush directory to disk
```

For example:

```python
self.dir.find("hello.txt")
```

searches for a file in the directory.

---

# 6. `converter.py`

Contains utility functions for:

### String → Bytes

```python
Converter.string_to_bytes()
```

### Bytes → String

```python
Converter.bytes_to_string()
```

### Filename → 8.3

```python
Converter.to_83()
```

### 8.3 → Filename

```python
Converter.from_83()
```

---

# 7. `file_system.py`

This is the main file-system abstraction.

It connects:

```text
Directory Manager
        +
FAT Manager
        +
Virtual Disk
```

The class provides high-level file operations.

### Create

```python
create_file()
```

### Write

```python
write_file()
```

### Read

```python
read_file()
```

### Delete

```python
delete_file()
```

### Append

```python
append_file()
```

### Rename

```python
rename_file()
```

### Copy

```python
copy_file()
```

---

# 8. `shell.py`

Provides the command-line interface.

The shell creates and connects all major components:

```python
VirtualDisk
FatTableManager
DirectoryManager
FileSystem
```

Then it continuously waits for user commands.

The shell prompt looks like:

```text
MiniOS:/>
```

---

# 🖥️ Available Commands

| Command                       | Description                 |
| ----------------------------- | --------------------------- |
| `ls`                          | List files                  |
| `cd <dir>`                    | Change simulated directory  |
| `pwd`                         | Show current path           |
| `touch <file>`                | Create an empty file        |
| `cat <file>`                  | Display file contents       |
| `echo "text" <file>`          | Write text                  |
| `echo "text" <file> --append` | Append text                 |
| `cp <src> <dst>`              | Copy a file                 |
| `mv <src> <dst>`              | Rename a file               |
| `rm <file>`                   | Delete a file               |
| `md <dir>`                    | Simulate directory creation |
| `rd <dir>`                    | Simulate directory removal  |
| `cls`                         | Clear the screen            |
| `help`                        | Show available commands     |
| `exit`                        | Exit the shell              |

---

# 💻 Example Usage

Start the system:

```bash
python shell.py
```

You should see:

```text
MiniOS Shell Ready 🚀 Type help
MiniOS:/>
```

---

## Create a File

```text
MiniOS:/> touch hello.txt
File created
```

---

## Write Data

```text
MiniOS:/> echo "Hello from MiniOS" hello.txt
Done
```

---

## Read Data

```text
MiniOS:/> cat hello.txt
Hello from MiniOS
```

---

## List Files

```text
MiniOS:/> ls
```

Example output:

```text
===== DIR =====
HELLO.TXT | 17
================
```

---

## Append Data

```text
MiniOS:/> echo " Welcome!" hello.txt --append
Done
```

Then:

```text
MiniOS:/> cat hello.txt
Hello from MiniOS Welcome!
```

---

## Copy a File

```text
MiniOS:/> cp hello.txt copy.txt
Copied
```

---

## Rename a File

```text
MiniOS:/> mv copy.txt backup.txt
Renamed
```

---

## Delete a File

```text
MiniOS:/> rm backup.txt
Deleted
```

---

# 🔄 File Write Process

When writing data to a file, the system performs the following steps:

```text
User Command
     │
     ▼
FileSystem.write_file()
     │
     ▼
Calculate Required Clusters
     │
     ▼
FAT.allocate_chain()
     │
     ▼
Find Free Clusters
     │
     ▼
Create Cluster Chain
     │
     ▼
Write Data to Virtual Disk
     │
     ▼
Update Directory Entry
     │
     ▼
Flush Changes
```

For example, if a file contains 2500 bytes:

```text
Cluster Size = 1024 bytes

2500 / 1024 ≈ 2.44
```

Therefore:

```text
Required Clusters = 3
```

The FAT might create:

```text
10 → 11 → 12 → END
```

---

# 📖 File Read Process

Reading a file works in the opposite direction:

```text
User Command
     │
     ▼
Find Directory Entry
     │
     ▼
Get First Cluster
     │
     ▼
Follow FAT Chain
     │
     ▼
Read Every Cluster
     │
     ▼
Combine Data
     │
     ▼
Trim to File Size
     │
     ▼
Return File Content
```

The file size stored in the directory entry is used to remove unused padding bytes from the last cluster.

---

# 🗑️ File Deletion

When a file is deleted:

```text
File
 │
 ▼
Find First Cluster
 │
 ▼
Follow FAT Chain
 │
 ▼
Mark Each Cluster FREE
 │
 ▼
Update FAT
 │
 ▼
Remove Directory Entry
```

A free cluster is represented by:

```text
0
```

---

# 📋 Example FAT Chain

Suppose `hello.txt` contains enough data to require three clusters.

The FAT could contain:

```text
Cluster 20 → 21
Cluster 21 → 25
Cluster 25 → -1
```

The file system interprets this as:

```text
hello.txt
   │
   ▼
Cluster 20
   │
   ▼
Cluster 21
   │
   ▼
Cluster 25
   │
   ▼
  END
```

---

# 💾 Persistence

The file system stores its state in:

```text
minifat.bin
```

This means the virtual disk is represented by an actual binary file on the host operating system.

When the application starts:

```text
minifat.bin
     ↓
VirtualDisk
     ↓
FAT
     ↓
Directory
```

When the application modifies the file system, changes are flushed back to the binary disk image.

---

# 🛠️ Technologies

| Technology   | Purpose                     |
| ------------ | --------------------------- |
| Python       | Core implementation         |
| `struct`     | Binary data serialization   |
| File I/O     | Virtual disk implementation |
| FAT          | Cluster allocation          |
| Binary files | Persistent virtual storage  |
| CLI          | User interaction            |
| OOP          | System architecture         |

---

# 📦 Requirements

The project uses Python's standard library.

No external Python packages are required.

Recommended:

```text
Python 3.9+
```

---

# ▶️ Installation & Setup

## 1. Clone the Repository

```bash
git clone https://github.com/YOUR_USERNAME/YOUR_REPOSITORY.git
cd YOUR_REPOSITORY
```

## 2. Run the Shell

```bash
python shell.py
```

The virtual disk will be created automatically:

```text
minifat.bin
```

---

# 🧪 Example Session

```text
MiniOS Shell Ready 🚀 Type help

MiniOS:/> touch notes.txt
File created

MiniOS:/> echo "Operating Systems Project" notes.txt
Done

MiniOS:/> cat notes.txt
Operating Systems Project

MiniOS:/> echo " - MiniFAT" notes.txt --append
Done

MiniOS:/> cat notes.txt
Operating Systems Project - MiniFAT

MiniOS:/> cp notes.txt backup.txt
Copied

MiniOS:/> ls

===== DIR =====
NOTES.TXT | 33
BACKUP.TXT | 33
================

MiniOS:/> mv backup.txt copy.txt
Renamed

MiniOS:/> rm copy.txt
Deleted

MiniOS:/> exit
Disk closed
```

---

# ⚠️ Current Limitations

This project is an educational file-system simulation rather than a production operating system.

### Directory Support

The commands:

```text
mkdir / md
rmdir / rd
cd
```

are currently simulated.

They do not create or manage real hierarchical directory structures.

The current implementation uses a single root directory.

---

### Superblock

A `SuperblockManager` is included for reading and writing cluster `0`, but the current implementation does not define a complete superblock metadata structure.

---

### File Attributes

The directory entry contains an attribute field, but advanced file attributes are not currently implemented.

---

### Error Handling

The shell uses simple command validation and some broad exception handling. A production file system would require more robust error handling and corruption detection.

---

### File Name Handling

The filename conversion follows a simplified 8.3-style format and is not a complete implementation of Microsoft's FAT filename rules.

---

# 🔮 Future Improvements

Possible extensions include:

* [ ] Implement real hierarchical directories
* [ ] Implement real `mkdir`, `rmdir`, and `cd`
* [ ] Add parent directory references
* [ ] Implement a complete superblock
* [ ] Add file attributes
* [ ] Add timestamps
* [ ] Add file permissions
* [ ] Add disk formatting
* [ ] Add free-space reporting
* [ ] Add `stat` command
* [ ] Add `tree` command
* [ ] Add `df` command
* [ ] Add better filename validation
* [ ] Add FAT consistency checks
* [ ] Add file-system recovery
* [ ] Add unit tests
* [ ] Add disk corruption simulation
* [ ] Add support for nested directories
* [ ] Improve shell command parsing

---

# 🎓 Learning Objectives

This project demonstrates practical understanding of several **Operating Systems** concepts:

### File Systems

Understanding how files can be represented and organized on storage.

### FAT

Understanding how a File Allocation Table tracks the clusters belonging to each file.

### Disk Blocks / Clusters

Understanding how files are divided into fixed-size storage units.

### Binary Storage

Understanding how structured information can be serialized into raw bytes.

### Directory Entries

Understanding how metadata about files can be stored.

### File Allocation

Understanding how free storage is allocated and released.

### Persistence

Understanding how an in-memory representation can be synchronized with persistent storage.

### Operating System Shells

Understanding the relationship between user commands and system-level operations.

---

# 🧠 Key Concepts Demonstrated

```text
                    MiniOS
                       │
          ┌────────────┼────────────┐
          │            │            │
          ▼            ▼            ▼
       Shell       File System    Storage
          │            │            │
          │       ┌────┴────┐       │
          │       ▼         ▼       │
          │     FAT      Directory  │
          │       │         │       │
          └───────┴─────────┴───────┘
                       │
                       ▼
                 Virtual Disk
                       │
                       ▼
                  minifat.bin
```

The project demonstrates how these components can work together to build a simplified file system from scratch.

---

# 👩‍💻 Author

**Sherry Adel Riad Tawfik**

AI Engineering Student | Computer Science & Artificial Intelligence

---

# ⭐ Project Purpose

This project was created as an educational implementation of a simplified file system to explore how operating systems handle:

**Storage → Allocation → Metadata → Files → Directories → User Commands**

Rather than relying on the host operating system's file-management APIs, the project implements the core storage and allocation logic itself using Python and a custom virtual disk.

---

## 📄 License

This project is intended for educational and portfolio purposes.
