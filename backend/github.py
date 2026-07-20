import os
import requests
import tempfile
from urllib.parse import urlparse


def download_repository_zip(url: str) -> tuple[str, str]:
    """
    Downloads a GitHub repository as a ZIP.

    Returns:
        (zip_path, temp_dir)
    """

    parsed = urlparse(url)
    owner, repo = parsed.path.strip("/").split("/")[:2]

    temp_dir = tempfile.mkdtemp(prefix="repo_")

    zip_path = os.path.join(temp_dir, f"{repo}.zip")

    download_url = f"https://api.github.com/repos/{owner}/{repo}/zipball"

    response = requests.get(download_url, stream=True)

    response.raise_for_status()

    with open(zip_path, "wb") as f:
        for chunk in response.iter_content(8192):
            if chunk:
                f.write(chunk)

    return zip_path, temp_dir