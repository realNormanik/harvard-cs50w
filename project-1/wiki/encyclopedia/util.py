import os
import requests

from vercel_blob import put, list as blob_list, delete


# Vercel Blob token
BLOB_READ_WRITE_TOKEN = os.environ.get("BLOB_READ_WRITE_TOKEN")

# Directory where all wiki entries are stored
BLOB_PREFIX = "wiki/entries/"


def list_entries():
    """
    Returns a sorted list of all encyclopedia entry names.
    Entries are stored in Vercel Blob as: wiki/entries/Title.md
    """

    entries = []
    cursor = None

    while True:
        options = {
            "token": BLOB_READ_WRITE_TOKEN,
            "prefix": BLOB_PREFIX,
        }

        if cursor:
            options["cursor"] = cursor

        result = blob_list(options)

        for blob in result.get("blobs", []):
            pathname = blob.get("pathname", "")

            if pathname.startswith(BLOB_PREFIX) and pathname.endswith(".md"):

                # Remove "wiki/entries/" prefix
                filename = pathname[len(BLOB_PREFIX):]

                # Remove ".md" extension
                title = filename[:-3]

                entries.append(title)

        cursor = result.get("cursor")

        if not cursor:
            break

    return sorted(entries)


def save_entry(title, content):
    """
    Saves an encyclopedia entry to Vercel Blob.
    Existing entries are overwritten.
    """

    pathname = f"{BLOB_PREFIX}{title}.md"

    return put(
        pathname,
        content.encode("utf-8"),
        {
            "allowOverwrite": "true",
        }
    )


def get_entry(title):
    """
    Retrieves an encyclopedia entry from Vercel Blob.
    Returns:
        str: Markdown content if the entry exists.
        None: If the entry does not exist.
    """

    pathname = f"{BLOB_PREFIX}{title}.md"
    cursor = None

    while True:
        options = {
            "token": BLOB_READ_WRITE_TOKEN,
            "prefix": pathname,
        }

        if cursor:
            options["cursor"] = cursor

        result = blob_list(options)

        for blob in result.get("blobs", []):

            if blob.get("pathname") == pathname:

                url = blob.get("url")

                if not url:
                    return None

                response = requests.get(url)
                response.raise_for_status()

                return response.text

        cursor = result.get("cursor")

        if not cursor:
            break

    return None