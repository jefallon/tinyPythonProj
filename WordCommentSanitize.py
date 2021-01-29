# This is adapted from the solution to StackOverflow question 37955062 about
# removing personal information from comments in a .docx file, accessible at

# https://stackoverflow.com/a/37956562

import re
import os
from zipfile import ZipFile

import re
import os
from zipfile import ZipFile


docx_file_name = "document.docx"

files = dict()
with ZipFile(docx_file_name, 'r') as document_as_zip:
    for internal_file in document_as_zip.infolist():
        file_reader = document_as_zip.open(internal_file.filename, "r")
        files[internal_file.filename] = file_reader.readlines()
        file_reader.close()
        
if "word/comments.xml" in files.keys():
    # We will be working on comments file...
    comments = files["word/comments.xml"]

    comments_new = str()

    # Files contents have been read as list of byte strings.
    for comment in comments:
        if isinstance(comment, bytes):
            # Change every author to "Unknown Author".
            comments_new += re.sub(r'w:date="[^"]*"', '', comment.decode())

    files["word/comments.xml"] = comments_new
    
if "word/commentsExtensible.xml" in files.keys():
    # We will be working on comments file...
    comments = files["word/commentsExtensible.xml"]

    comments_new = str()

    # Files contents have been read as list of byte strings.
    for comment in comments:
        if isinstance(comment, bytes):
            # Change every author to "Unknown Author".
            comments_new += re.sub(r'w16cex:dateUtc="[^"]*"', '', comment.decode())

    files["word/commentsExtensible.xml"] = comments_new
    
os.remove(docx_file_name)

with ZipFile(docx_file_name, 'w') as document_as_zip:
    for internal_file_name in files.keys():
        # Those are lists of byte strings, so we merge them...
        merged_binary_data = str()
        for binary_data in files[internal_file_name]:
            # If the file was not edited (therefore is not the comments.xml file).
            if not isinstance(binary_data, str):
                binary_data = binary_data.decode()

            # Merge file contents.
            merged_binary_data += binary_data

        # We write old file contents to new file in new .docx.
        document_as_zip.writestr(internal_file_name, merged_binary_data)