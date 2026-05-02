import os
import argparse
import csv
from pathlib import Path

# Optional color support
try:
    from colorama import init, Fore, Style
    init(autoreset=True)
    COLOR = True
except:
    COLOR = False


def c(text, color):
    if not COLOR:
        return text
    return color + text + Style.RESET_ALL


# -----------------------------
# SIZE HELPERS
# -----------------------------
def format_size(size):
    for unit in ["B", "KB", "MB", "GB", "TB"]:
        if size < 1024:
            return f"{size:.2f} {unit}"
        size /= 1024
    return f"{size:.2f} PB"


def get_folder_size(folder):
    total = 0
    try:
        for root, dirs, files in os.walk(folder):
            for file in files:
                fp = os.path.join(root, file)
                if not os.path.islink(fp):
                    try:
                        total += os.path.getsize(fp)
                    except:
                        pass
    except:
        pass
    return total


# -----------------------------
# MAIN SCAN
# -----------------------------
def scan(path=".", top=None, reverse=False):
    items = []

    try:
        names = os.listdir(path)
    except Exception as e:
        print("Cannot access:", e)
        return

    for name in names:
        full = os.path.join(path, name)

        try:
            if os.path.isdir(full):
                size = get_folder_size(full)
                is_dir = True
            else:
                size = os.path.getsize(full)
                is_dir = False

            items.append((size, name, is_dir))

        except:
            pass

    items.sort(reverse=not reverse)

    if top:
        items = items[:top]

    print()
    print(c("📊 SIZE REPORT", Fore.CYAN))
    print("-" * 50)

    for size, name, is_dir in items:
        icon = "📁" if is_dir else "📄"

        if is_dir:
            icon = c(icon, Fore.YELLOW)
        else:
            icon = c(icon, Fore.GREEN)

        print(f"{icon} {format_size(size):>12} | {name}")

    print("-" * 50)
    print(f"Items: {len(items)}")
    print()


# -----------------------------
# TREE VIEW
# -----------------------------
def tree(path=".", level=2, indent=0):
    if level < 0:
        return

    try:
        items = os.listdir(path)
    except:
        return

    for item in items:
        full = os.path.join(path, item)

        prefix = " " * indent

        if os.path.isdir(full):
            size = get_folder_size(full)
            print(f"{prefix}📁 {item} ({format_size(size)})")
            tree(full, level - 1, indent + 4)
        else:
            try:
                size = os.path.getsize(full)
                print(f"{prefix}📄 {item} ({format_size(size)})")
            except:
                pass


# -----------------------------
# LARGEST FILES
# -----------------------------
def largest_files(path=".", limit=10):
    files_list = []

    for root, dirs, files in os.walk(path):
        for file in files:
            fp = os.path.join(root, file)

            try:
                size = os.path.getsize(fp)
                files_list.append((size, fp))
            except:
                pass

    files_list.sort(reverse=True)

    print()
    print(c("🔥 LARGEST FILES", Fore.RED))
    print("-" * 70)

    for size, file in files_list[:limit]:
        print(f"{format_size(size):>12} | {file}")

    print()


# -----------------------------
# EXPORT CSV
# -----------------------------
def export_csv(path=".", filename="sizespy_report.csv"):
    rows = []

    for name in os.listdir(path):
        full = os.path.join(path, name)

        try:
            if os.path.isdir(full):
                size = get_folder_size(full)
                kind = "Folder"
            else:
                size = os.path.getsize(full)
                kind = "File"

            rows.append([name, kind, size, format_size(size)])

        except:
            pass

    with open(filename, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["Name", "Type", "Bytes", "Readable Size"])
        writer.writerows(rows)

    print(c(f"✅ Exported to {filename}", Fore.GREEN))


# -----------------------------
# DELETE FILE
# -----------------------------
def delete_file(file_path):
    if not os.path.isfile(file_path):
        print("Not a file")
        return

    confirm = input(f"Delete {file_path}? (y/n): ")

    if confirm.lower() == "y":
        os.remove(file_path)
        print(c("Deleted successfully", Fore.RED))


# -----------------------------
# MAIN CLI
# -----------------------------
def run():
    parser = argparse.ArgumentParser(
        description="sizespy - Advanced Folder Size Analyzer"
    )

    parser.add_argument("path", nargs="?", default=".")
    parser.add_argument("--top", type=int, help="Show top N items")
    parser.add_argument("--reverse", action="store_true", help="Smallest first")
    parser.add_argument("--tree", action="store_true", help="Show tree view")
    parser.add_argument("--depth", type=int, default=2)
    parser.add_argument("--largest", type=int, help="Largest files")
    parser.add_argument("--export", action="store_true", help="Export CSV")
    parser.add_argument("--delete", help="Delete file safely")

    args = parser.parse_args()

    if args.tree:
        tree(args.path, args.depth)

    elif args.largest:
        largest_files(args.path, args.largest)

    elif args.export:
        export_csv(args.path)

    elif args.delete:
        delete_file(args.delete)

    else:
        scan(args.path, args.top, args.reverse)


if __name__ == "__main__":
    run()