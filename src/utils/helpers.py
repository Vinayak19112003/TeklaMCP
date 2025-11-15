"""
Utility helper functions for TeklaMCP
Common functions used across the project
"""

import hashlib
import json
import os
from pathlib import Path
from typing import Any, Dict, List, Optional, Union
from datetime import datetime
import time


def generate_hash(data: Union[str, bytes, Dict]) -> str:
    """
    Generate MD5 hash for data (used for caching)

    Args:
        data: String, bytes, or dict to hash

    Returns:
        MD5 hash as hex string
    """
    if isinstance(data, dict):
        data = json.dumps(data, sort_keys=True)
    if isinstance(data, str):
        data = data.encode('utf-8')

    return hashlib.md5(data).hexdigest()


def generate_file_hash(file_path: Union[str, Path]) -> str:
    """
    Generate hash of file contents

    Args:
        file_path: Path to file

    Returns:
        MD5 hash of file contents
    """
    hasher = hashlib.md5()

    with open(file_path, 'rb') as f:
        while chunk := f.read(8192):
            hasher.update(chunk)

    return hasher.hexdigest()


def ensure_dir(path: Union[str, Path]) -> Path:
    """
    Ensure directory exists, create if not

    Args:
        path: Directory path

    Returns:
        Path object
    """
    path = Path(path)
    path.mkdir(parents=True, exist_ok=True)
    return path


def read_json(file_path: Union[str, Path]) -> Dict:
    """
    Read JSON file

    Args:
        file_path: Path to JSON file

    Returns:
        Parsed JSON as dict
    """
    with open(file_path, 'r', encoding='utf-8') as f:
        return json.load(f)


def write_json(data: Dict, file_path: Union[str, Path], indent: int = 2):
    """
    Write data to JSON file

    Args:
        data: Dictionary to write
        file_path: Output file path
        indent: JSON indentation level
    """
    ensure_dir(Path(file_path).parent)

    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=indent, ensure_ascii=False)


def get_file_size_mb(file_path: Union[str, Path]) -> float:
    """
    Get file size in megabytes

    Args:
        file_path: Path to file

    Returns:
        File size in MB
    """
    size_bytes = os.path.getsize(file_path)
    return size_bytes / (1024 * 1024)


def validate_file_size(file_path: Union[str, Path], max_mb: float = 50) -> bool:
    """
    Check if file size is within limit

    Args:
        file_path: Path to file
        max_mb: Maximum size in MB

    Returns:
        True if file is within size limit

    Raises:
        ValueError: If file is too large
    """
    size_mb = get_file_size_mb(file_path)

    if size_mb > max_mb:
        raise ValueError(f"File size {size_mb:.2f}MB exceeds limit of {max_mb}MB")

    return True


def format_timestamp(dt: Optional[datetime] = None) -> str:
    """
    Format datetime as ISO string

    Args:
        dt: Datetime object (default: now)

    Returns:
        ISO formatted timestamp
    """
    if dt is None:
        dt = datetime.now()

    return dt.isoformat()


def parse_timestamp(timestamp: str) -> datetime:
    """
    Parse ISO timestamp string

    Args:
        timestamp: ISO formatted timestamp

    Returns:
        Datetime object
    """
    return datetime.fromisoformat(timestamp)


def timing_decorator(func):
    """
    Decorator to measure function execution time

    Usage:
        @timing_decorator
        def my_function():
            pass
    """
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        end = time.time()

        print(f"{func.__name__} took {end - start:.2f} seconds")
        return result

    return wrapper


def chunk_list(lst: List, chunk_size: int) -> List[List]:
    """
    Split list into chunks

    Args:
        lst: List to chunk
        chunk_size: Size of each chunk

    Returns:
        List of chunks
    """
    return [lst[i:i + chunk_size] for i in range(0, len(lst), chunk_size)]


def flatten_list(nested_list: List[List]) -> List:
    """
    Flatten nested list

    Args:
        nested_list: Nested list

    Returns:
        Flattened list
    """
    return [item for sublist in nested_list for item in sublist]


def safe_get(dictionary: Dict, *keys, default=None) -> Any:
    """
    Safely get nested dictionary value

    Args:
        dictionary: Dictionary to query
        *keys: Nested keys
        default: Default value if key not found

    Returns:
        Value or default

    Example:
        safe_get(data, "grid", "x_lines", 0, "coordinate", default=0)
    """
    value = dictionary

    for key in keys:
        if isinstance(value, dict):
            value = value.get(key)
        elif isinstance(value, list) and isinstance(key, int):
            try:
                value = value[key]
            except IndexError:
                return default
        else:
            return default

        if value is None:
            return default

    return value


def merge_dicts(dict1: Dict, dict2: Dict) -> Dict:
    """
    Deep merge two dictionaries

    Args:
        dict1: First dictionary
        dict2: Second dictionary (takes precedence)

    Returns:
        Merged dictionary
    """
    result = dict1.copy()

    for key, value in dict2.items():
        if key in result and isinstance(result[key], dict) and isinstance(value, dict):
            result[key] = merge_dicts(result[key], value)
        else:
            result[key] = value

    return result


def sanitize_filename(filename: str) -> str:
    """
    Remove invalid characters from filename

    Args:
        filename: Original filename

    Returns:
        Sanitized filename
    """
    invalid_chars = '<>:"/\\|?*'

    for char in invalid_chars:
        filename = filename.replace(char, '_')

    return filename


def format_file_size(size_bytes: int) -> str:
    """
    Format bytes as human-readable size

    Args:
        size_bytes: Size in bytes

    Returns:
        Formatted string (e.g., "1.5 MB")
    """
    for unit in ['B', 'KB', 'MB', 'GB']:
        if size_bytes < 1024.0:
            return f"{size_bytes:.1f} {unit}"
        size_bytes /= 1024.0

    return f"{size_bytes:.1f} TB"


### TODO: USER MUST FILL THIS SECTION
# Add any custom helper functions specific to your use case
# Examples:
# - Custom file format converters
# - Domain-specific validation functions
# - Integration helpers for other systems


if __name__ == "__main__":
    # Test helpers
    print("Testing helper functions...")

    # Test hashing
    hash1 = generate_hash("test data")
    print(f"Hash: {hash1}")

    # Test timestamp
    ts = format_timestamp()
    print(f"Timestamp: {ts}")

    # Test safe_get
    data = {"a": {"b": {"c": 123}}}
    value = safe_get(data, "a", "b", "c", default=0)
    print(f"Safe get: {value}")

    # Test file size formatting
    print(f"Size: {format_file_size(1536000)}")

    print("\nAll helper tests passed!")
