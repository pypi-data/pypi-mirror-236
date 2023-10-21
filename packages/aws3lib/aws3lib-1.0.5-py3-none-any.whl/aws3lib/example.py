from aws3lib.aws import AWS3

"""
EXAMPLE USING aws3lib
"""

aws = AWS3(bucket="bucket name", default_object_name="none.json")

# Get bucket ACL
print(aws.get_bucket_acl())

# Get bucket CORS
print(aws.get_bucket_cors())

# Download file
aws.download_file("C:\\Users\\pro0xy\\Desktop\\6e3533cc9af69ac71a72f4b0400aebf2.json", "6e3533cc9af69ac71a72f4b0400aebf2.json")

# Upload file
aws.upload_file(file_path="C:\\Users\\pro0xy\\Desktop\\6e3533cc9af69ac71a72f4b0400aebf2.json", object_name="test.json", public=False)

# Create presigned url (Output: https://s3.region.amazonaws.com/****/test.json?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=AKIA*****%2F20231016%2Fregion%2Fs3%2Faws4_request&X-Amz-Date=20***16T195830Z&X-Amz-Expires=3600&X-Amz-SignedHeaders=host&X-Amz-Signature=69558c**********395b8e794c3f****09a6f0f9d3
print(aws.create_presigned_url("test.json"))