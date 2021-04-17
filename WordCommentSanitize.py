import re
import os
import argparse
from zipfile import ZipFile

class DocxZip:

    def __init__(self, filename):
        self.filename = filename
        self.files = self.get_internal_files()

        if 'word/comments.xml' in self.files.keys():
            self.simple_comments()

        if 'word/commentsExtensible.xml' in self.files.keys():
            self.extensible_comments()

        self.replace_file()

    def get_internal_files(self):
        files = dict()

        with ZipFile(self.filename, 'r') as document_as_zip:
            for internal_file in document_as_zip.infolist():
                with document_as_zip.open(internal_file.filename, 'r') as file_reader:
                    files[internal_file.filename] = file_reader.readlines()
        return files

    def simple_comments(self):
        comments = self.files['word/comments.xml']
        comments_new = str()

        for comment in comments:
            if isinstance(comment, bytes):
                comments_new += re.sub(r'w:date="[^"]*"', '', comment.decode())

        self.files['word/comments.xml'] = comments_new

    def extensible_comments(self):
        comments_x = self.files['word/commentsExtensible.xml']
        comments_x_new = str()

        for comment in comments_x:
            if isinstance(comment, bytes):
                comments_x_new += re.sub(r'w16cex:dateUtc="[^"]*"', '', comment.decode())

        self.files['word/commentsExtensible.xml'] = comments_x_new

    def replace_file(self):
        with ZipFile('sanitized'+self.filename, 'w') as document_as_zip:
            for internal_file_name in self.files.keys():
                merged_binary_data = str()
                for binary_data in self.files[internal_file_name]:
                    if not isinstance(binary_data, str):
                        binary_data = binary_data.decode()

                    merged_binary_data += binary_data

                document_as_zip.writestr(internal_file_name, merged_binary_data)
    
# os.remove(docx_file_name)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('file', type=str)
    args = parser.parse_args()
    docx_filename = args.file
    # docx_filename = 'original.docx'
    new_file = DocxZip(docx_filename)