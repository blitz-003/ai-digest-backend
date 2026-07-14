import math
import re


def generate_slug(title: str) -> str:
    slug = title.lower().strip()

    slug = re.sub(r"[^\w\s-]", "", slug)

    slug = re.sub(r"\s+", "-", slug)

    return slug


def calculate_reading_time(content: str) -> int:
    words = len(content.split())

    return max(1, math.ceil(words / 200))