from flytekit.types.directory import FlyteDirectory
from flytekit.types.file import FlyteFile

import os
import zipfile
import re
import xml.etree.ElementTree as ET


nsmap = {"w": "http://schemas.openxmlformats.org/wordprocessingml/2006/main"}


def qn(tag: str) -> str:
    """
    Stands for 'qualified name', a utility function to turn a namespace
    prefixed tag name into a Clark-notation qualified tag name for lxml. For
    example, ``qn('p:cSld')`` returns ``'{http://schemas.../main}cSld'``.
    Source: https://github.com/python-openxml/python-docx/
    """
    prefix, tagroot = tag.split(":")
    uri = nsmap[prefix]
    return "{{{}}}{}".format(uri, tagroot)


def xml2text(xml: bytes) -> str:
    """
    A string representing the textual content of this run, with content
    child elements like ``<w:tab/>`` translated to their Python
    equivalent.
    Adapted from: https://github.com/python-openxml/python-docx/
    """
    text = ""
    root = ET.fromstring(xml)
    for child in root.iter():
        if child.tag == qn("w:t"):
            t_text = child.text
            text += t_text if t_text is not None else ""
        elif child.tag == qn("w:tab"):
            text += "\t"
        elif child.tag in (qn("w:br"), qn("w:cr")):
            text += "\n"
        elif child.tag == qn("w:p"):
            text += "\n\n"
    return text


def extract_text(docx: FlyteFile) -> str:
    """
    This function takes a docx file as input and returns the text content
    of the file as a string. It does this by unzipping the docx file in
    memory, and then extracting the text content from the document.xml
    file and any header and footer files that may be present. The extracted
    text is then returned as a string.

    Adapted from: https://github.com/ankushshah89/python-docx2txt
    """
    text = ""

    # unzip the docx in memory
    zipf = zipfile.ZipFile(docx)
    filelist = zipf.namelist()

    # get header text
    # there can be 3 header files in the zip
    header_xmls = "word/header[0-9]*.xml"
    for fname in filelist:
        if re.match(header_xmls, fname):
            text += xml2text(zipf.read(fname))

    # get main text
    doc_xml = "word/document.xml"
    text += xml2text(zipf.read(doc_xml))

    # get footer text
    # there can be 3 footer files in the zip
    footer_xmls = "word/footer[0-9]*.xml"
    for fname in filelist:
        if re.match(footer_xmls, fname):
            text += xml2text(zipf.read(fname))

    zipf.close()
    return text.strip()


def extract_images(docx: FlyteFile, bucket_name: str) -> FlyteDirectory:
    """
    This function takes a docx file as input, along with a bucket name,
    and returns a FlyteDirectory object containing all the images
    present in the docx file. It does this by unzipping the docx file
    in memory, and then extracting any image files that may be present
    in the file. The extracted images are then saved to a subdirectory
    in the specified S3 bucket, with the subdirectory name being based
    on the name of the input docx file. The function returns a FlyteDirectory
    object containing the extracted images.

    Adapted from: https://github.com/ankushshah89/python-docx2txt
    """
    # unzip the docx in memory
    zipf = zipfile.ZipFile(docx)  # gives error if in_fd contains a directory
    filelist = zipf.namelist()
    folder_name = os.path.splitext(os.path.basename(docx))[0]
    out_fd = FlyteDirectory(f"s3://{bucket_name}/output/{folder_name}")

    # extract images
    for fname in filelist:
        _, extension = os.path.splitext(fname)
        if extension in [".jpg", ".jpeg", ".png", ".bmp"]:
            out_file = out_fd.new_file(os.path.basename(fname))
            with out_file.open("wb") as o:
                o.write(zipf.read(fname))
    zipf.close()
    return out_fd
