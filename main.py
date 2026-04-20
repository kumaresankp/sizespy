import os

def get_folder_size(path):
    total = 0
    for root, dirs, files in os.walk(path):
        for f in files:
            fp = os.path.join(root, f)
            if not os.path.islink(fp):
                total += os.path.getsize(fp)
    return total

def format_size(size):
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if size < 1024:
            return f"{size:.2f} {unit}"
        size /= 1024

def scan(path='.', indent=0):
    items = []
    for name in os.listdir(path):
        full_path = os.path.join(path, name)
        if os.path.isdir(full_path):
            size = get_folder_size(full_path)
        else:
            size = os.path.getsize(full_path)
        items.append((size, name, os.path.isdir(full_path)))
    
    # Sort by size (largest first)
    items.sort(reverse=True)
    
    for size, name, is_dir in items:
        prefix = "📁" if is_dir else "📄"
        print(f"{'  ' * indent}{prefix} {format_size(size):>12} | {name}")

scan('D:\\ScreenRecordings')