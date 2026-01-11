#!/usr/bin/env python3
import os
import mimetypes
import hashlib
from pathlib import Path
import boto3


BUCKET = 'todoapp-bucket'
ENDPOINT = 'https://storage.yandexcloud.net'
ACCESS_KEY = ''
SECRET_KEY = ''
CACHE_CONTROL = 'public, max-age=604800'
LOCAL_DIR = Path("static")
PREFIX = 'static/'


def file_md5(p: Path) -> str:
    h = hashlib.md5()
    with p.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()

def guess_content_type(p: Path) -> str:
    ctype, _ = mimetypes.guess_type(str(p))
    return ctype or "application/octet-stream"

def main():
    if not LOCAL_DIR.exists():
        raise SystemExit(f"Local dir not found: {LOCAL_DIR.resolve()}")

    s3 = boto3.client(
        "s3",
        endpoint_url=ENDPOINT,
        aws_access_key_id=ACCESS_KEY,
        aws_secret_access_key=SECRET_KEY,
    )

    uploaded = 0
    for root, _, files in os.walk(LOCAL_DIR):
        for name in files:
            local_path = Path(root) / name
            rel = local_path.relative_to(LOCAL_DIR).as_posix()
            key = f"{PREFIX.rstrip('/')}/{rel}"

            extra = {
                "ContentType": guess_content_type(local_path),
                "CacheControl": CACHE_CONTROL,
            }

            if local_path.suffix.lower() == ".html":
                extra["CacheControl"] = "no-cache"

            s3.upload_file(
                Filename=str(local_path),
                Bucket=BUCKET,
                Key=key,
                ExtraArgs=extra,
            )
            uploaded += 1

    print(f"Done. Uploaded {uploaded} files to s3://{BUCKET}/{PREFIX}")

if __name__ == "__main__":
    main()