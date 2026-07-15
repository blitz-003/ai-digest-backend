from pathlib import Path


seed_file = (
    Path(__file__)
    .resolve()
    .parent
    / "seed_articles.py"
)


if not seed_file.exists():
    raise FileNotFoundError(
        "seed_articles.py not found"
    )


content = seed_file.read_text(
    encoding="utf-8"
)


old = """
import sys
import os

sys.path.append(
    os.path.dirname(
        os.path.dirname(
            os.path.abspath(__file__)
        )
    )
)
"""


new = """
import sys
import os
from pathlib import Path
from dotenv import load_dotenv


BASE_DIR = Path(__file__).resolve().parent.parent


sys.path.append(
    str(BASE_DIR)
)


load_dotenv(
    BASE_DIR / ".env"
)
"""


if "load_dotenv" not in content:

    content = content.replace(
        old,
        new
    )


    seed_file.write_text(
        content,
        encoding="utf-8"
    )


    print(
        "✅ Seed script environment fixed"
    )

else:

    print(
        "✅ Environment loading already exists"
    )