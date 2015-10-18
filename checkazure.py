from azure.storage.file import FileService
from azure.storage.blob import BlobService



PACCOUNT_KEY = "primarykey"
ACCOUNT_NAME = "tweetfighthof"

file_service = FileService(ACCOUNT_NAME, PACCOUNT_KEY)
blob_service = BlobService(ACCOUNT_NAME, PACCOUNT_KEY)


#puts it t the blob that the cdn can access
#tweetfighter is directory, fights the file on the CDN, and maybe.avi the local file, with the type being the format

blob_service.put_block_blob_from_path(
    'tweetfighter',
    'fights',
    'maybe.avi',
    x_ms_blob_content_type='video/avi'
)
