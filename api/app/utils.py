import hashlib
import os


def allowed_file(filename):
    """
    Checks if the format for the file received is acceptable. For this
    particular case, we must accept only image files. This is, files with
    extension ".png", ".jpg", ".jpeg" or ".gif".

    Parameters
    ----------
    filename : str
        Filename from werkzeug.datastructures.FileStorage file.

    Returns
    -------
    bool
        True if the file is an image, False otherwise.
    """
    # Check if the file extension of the filename received is in the set of allowed extensions (".png", ".jpg", ".jpeg", ".gif")
    allowed_extensions = [".png", ".jpg", ".jpeg", ".gif"]

    return (
        os.path.splitext(filename)[1].lower() in allowed_extensions
    )  # Alternatively use Path.suffix


async def get_file_hash(file):
    """
    Returns a new filename based on the file content using MD5 hashing.
    It uses hashlib.md5() function from Python standard library to get
    the hash.

    Parameters
    ----------
    file : werkzeug.datastructures.FileStorage
        File sent by user.

    Returns
    -------
    str
        New filename based in md5 file hash.
    """
    # Read file content (byte string)
    content = await file.read()

    # Generate MD5 hash from content
    file_hash = hashlib.md5(  # Apply MD5 hash
        content
    ).hexdigest()  # hexdigest converts the result into a readable hex string

    # Get the file extension
    _, ext = os.path.splitext(file.filename)

    # Reset file pointer to the beginning
    await file.seek(0)

    return f"{file_hash}{ext}"
