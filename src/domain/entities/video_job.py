from dataclasses import dataclass


@dataclass
class VideoJob:
    task_id: str
    filename: str
    s3_path: str
    user_email: str
