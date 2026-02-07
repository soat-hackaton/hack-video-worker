from dataclasses import dataclass


@dataclass
class VideoJob:
    filename: str
    s3_path: str
