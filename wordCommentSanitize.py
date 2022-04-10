import re
import os
import argparse
from zipfile import ZipFile


class DocxZip:
    def __init__(self, filename):
        self.filename = filename
        self.files = self.get_internal_files()

        if "word/comments.xml" in self.files.keys():
            self.simple_comments()

        if "word/commentsExtensible.xml" in self.files.keys():
            self.extensible_comments()

        if "word/document.xml" in self.files.keys():
            self.track_changes()

        self.footnotes()

        self.header1()

        self.replace_file()

    def get_internal_files(self):
        files = dict()

        with ZipFile(self.filename, "r") as document_as_zip:
            for internal_file in document_as_zip.infolist():
                with document_as_zip.open(internal_file.filename, "r") as file_reader:
                    files[internal_file.filename] = file_reader.readlines()
        return files

    def track_changes(self):
        docs = self.files["word/document.xml"]
        docs_new = str()
        for doc in docs:
            if isinstance(doc, bytes):
                new_doc = re.sub(r'w:(author|initials|date)="[^"]*"', "", doc.decode())
                docs_new += new_doc
        self.files["word/document.xml"] = docs_new

    def footnotes(self):
        people = self.files["word/footnotes.xml"]
        ppl_new = str()
        for ppl in people:
            if isinstance(ppl, bytes):
                new_ppl = re.sub(r'w:(author|date)=\"[^"]*\"', "", ppl.decode())
                ppl_new += new_ppl
        self.files["word/footnotes.xml"] = ppl_new

    def people(self):
        people = self.files["word/people.xml"]
        ppl_new = str()
        for ppl in people:
            if isinstance(ppl, bytes):
                new_ppl = re.sub(
                    r'w15:author=\"[^"]*\"', r"w15:author=\"Unknown\"", ppl.decode()
                )
                ppl_new += new_ppl
        self.files["word/people.xml"] = ppl_new

    def header1(self):
        comments = self.files["word/header1.xml"]
        comments_new = str()
        for comment in comments:
            if isinstance(comment, bytes):
                new_comment = comment.decode()
                new_comment = re.sub(
                    r'w:(date|author|initials)="[^"]*"', "", new_comment
                )
                # new_comment = re.sub(r'w:author="[^"]*"', "", new_comment)
                # new_comment = re.sub(r'w:initials="[^"]*"', "", new_comment)
                comments_new += new_comment
        self.files["word/header1.xml"] = comments_new

    def simple_comments(self):
        comments = self.files["word/comments.xml"]
        comments_new = str()
        for comment in comments:
            if isinstance(comment, bytes):
                new_comment = comment.decode()
                new_comment = re.sub(
                    r'w:(date|author|initials)="[^"]*"', "", new_comment
                )
                # new_comment = re.sub(r'w:author="[^"]*"', "", new_comment)
                # new_comment = re.sub(r'w:initials="[^"]*"', "", new_comment)
                comments_new += new_comment
        self.files["word/comments.xml"] = comments_new

    def extensible_comments(self):
        comments_x = self.files["word/commentsExtensible.xml"]
        comments_x_new = str()

        for comment in comments_x:
            if isinstance(comment, bytes):
                new_x_comment = re.sub(r'w16cex:dateUtc="[^"]*"', "", comment.decode())
                new_x_comment = re.sub(
                    r'w:author="[^"]*"', 'w:author=""', new_x_comment
                )
                new_x_comment = re.sub(
                    r'w:initials="[^"]*"', 'w:initials=""', new_x_comment
                )
                comments_x_new += new_x_comment

        self.files["word/commentsExtensible.xml"] = comments_x_new

    def replace_file(self):
        with ZipFile("sanitized" + self.filename, "w") as document_as_zip:
            for internal_file_name in self.files.keys():
                merged_binary_data = str()
                for binary_data in self.files[internal_file_name]:
                    if not isinstance(binary_data, str):
                        binary_data = binary_data.decode()

                    merged_binary_data += binary_data

                document_as_zip.writestr(internal_file_name, merged_binary_data)


# os.remove(docx_file_name)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("file", type=str)
    args = parser.parse_args()
    docx_filename = args.file
    # docx_filename = 'original.docx'
    new_file = DocxZip(docx_filename)
