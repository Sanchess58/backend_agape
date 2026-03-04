from app.api.s3_storage import S3Client
from app.config import settings

HOUR_IN_SECONDS = 3600


async def get_presigned_url(bucket: str, key: str, expires_in: int = HOUR_IN_SECONDS):
    client = S3Client(
        settings.S3_ACCESS_KEY,
        settings.S3_SECRET_KEY,
        settings.S3_URL,
        settings.BUCKET_NAME,
        settings.S3_REGION,
    ).get_client()
    async with client as c:
        return await c.generate_presigned_url(
            "get_object",
            Params={"Bucket": bucket, "Key": key},
            ExpiresIn=expires_in
        )
