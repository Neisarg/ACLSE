import sys
import os
import requests
import shutil
import bibtexparser
import xml.etree.ElementTree as ET

DATA = "/mnt/d/Data/Projects/IR/Data"
FPATH_PDF = os.path.join(DATA, "scrapy_data_pdf")
FPATH_BIB = os.path.join(DATA, "scrapy_data_bib")
FPATH_XML = os.path.join(DATA, "scrapy_data_xml")

FPATH_M_PDF = os.path.join(DATA, "scrapy_data_m_pdf")
FPATH_M_BIB = os.path.join(DATA, "scrapy_data_m_bib")
FPATH_M_XML = os.path.join(DATA, "scrapy_data_m_xml")

if not os.path.exists(FPATH_M_PDF):
    os.makedirs(FPATH_M_PDF)

if not os.path.exists(FPATH_M_BIB):
    os.makedirs(FPATH_M_BIB)

if not os.path.exists(FPATH_M_XML):
    os.makedirs(FPATH_M_XML)




def lemmatize(name):
    name = name.split(".")[0]
    return name.lower()


def get_pdf_name(lemma):
    return lemma.upper() + ".pdf"


def get_bib_name(lemma):
    return lemma + ".bib"


def get_xml_name(lemma):
    return lemma + ".xml"


def get_pdf_url(lemma):
    return "http://www.aclweb.org/anthology/{0}".format(lemma.upper())


def get_old_pdf_url(lemma):
    ulemma = lemma.upper()
    letter = ulemma[0]
    prefix = ulemma.split("-")[0]
    return "http://aclweb.org/anthology/{0}/{1}/{2}.pdf".format(letter, prefix, ulemma)


def get_pdf_url_from_bib(bib_path):
    with open(bib_path) as bibtex_file:
        bib_database = bibtexparser.load(bibtex_file)
    return bib_database.entries[0]["url"]


def get_pdf_url_from_xml(xml_path):
    tree = ET.parse(xml_path)
    root = tree.getroot()
    return root.findall('location')[0].find('url').text


def get_bib_url(lemma):
    return "https://aclanthology.coli.uni-saarland.de/papers/{0}/{1}.bib".format(lemma.upper(), lemma)


def get_old_bib_url(lemma):
    ulemma = lemma.upper()
    letter = ulemma[0]
    prefix = ulemma.split("-")[0]
    return "https://aclweb.org/anthology/{0}/{1}/{2}.bib".format(letter, prefix, ulemma)


def get_xml_url(lemma):
    return "https://aclanthology.coli.uni-saarland.de/papers/{0}/{1}.xml".format(lemma.upper(), lemma)


def get_missing_lemmas():
    pdf_lemma = set(map(lemmatize, os.listdir(FPATH_PDF)))
    bib_lemma = set(map(lemmatize, os.listdir(FPATH_BIB)))
    xml_lemma = set(map(lemmatize, os.listdir(FPATH_XML)))

    union_set = pdf_lemma.union(bib_lemma, xml_lemma)
    pdf_need_lemma = union_set - pdf_lemma
    bib_need_lemma = union_set - bib_lemma
    xml_need_lemma = union_set - xml_lemma

    print("Total files : ", len(union_set))
    print("PDF not downloaded : ", len(pdf_need_lemma))
    print("BIB not downloaded : ", len(bib_need_lemma))
    print("XML not downloaded : ", len(xml_need_lemma))

    return pdf_need_lemma, bib_need_lemma, xml_need_lemma


def get_missing_pdf_from_bib():
    pdf_lemma = set(map(lemmatize, os.listdir(FPATH_PDF)))
    bib_lemma = set(map(lemmatize, os.listdir(FPATH_BIB)))

    pdf_need_lemma = bib_lemma - pdf_lemma

    print("PDF not downloaded : ", len(pdf_need_lemma))
    return pdf_need_lemma


def get_missing_pdf_from_xml():
    pdf_lemma = set(map(lemmatize, os.listdir(FPATH_PDF)))
    xml_lemma = set(map(lemmatize, os.listdir(FPATH_XML)))

    pdf_need_lemma = xml_lemma - pdf_lemma

    print("PDF not downloaded : ", len(pdf_need_lemma))
    return pdf_need_lemma


def download_file(url, fpath):
    r = requests.get(url, stream=True)
    print(r.status_code, r.url)
    try:
        maybe_invalid = int(r.url.split('/')[-1].split('.')[0])
    except:
        maybe_invalid = 200

    if(r.status_code == 404 or  maybe_invalid == 404 ):
        print("invalid")
        return False
    else:
        with open(fpath, 'wb') as fd:
            #shutil.copyfileobj(r.raw, f)
            fd.write(r.content)

        return True


def download_missing_bib(bib_need_lemma):
    for lemma in list(bib_need_lemma):
        url = get_bib_url(lemma)
        fpath = os.path.join(FPATH_M_BIB, get_bib_name(lemma))
        print(url, fpath)
        if(not download_file(url, fpath)):
            ourl = get_old_bib_url(lemma)
            print(ourl, fpath)
            download_file(ourl, fpath)
        print()


def download_missing_xml(xml_need_lemma):
    for lemma in list(xml_need_lemma):
        url = get_xml_url(lemma)
        fpath = os.path.join(FPATH_M_XML, get_xml_name(lemma))
        print(url, fpath)
        download_file(url, fpath)
        print()


def download_missing_pdf(pdf_need_lemma):
    for lemma in list(pdf_need_lemma):
        url = get_pdf_url(lemma)
        fpath = os.path.join(FPATH_M_PDF, get_pdf_name(lemma))
        print(url, fpath)
        if not download_file(url, fpath):
            ourl = get_old_pdf_url(lemma)
            print(ourl, fpath)
            download_file(ourl, fpath)
        print()


def download_missing_pdf_from_bib(pdf_need_lemma):
    url = get_pdf_url_from_bib(os.path.join(FPATH_BIB, get_bib_name(pdf_need_lemma)))
    fpath = os.path.join(FPATH_M_PDF, get_pdf_name(pdf_need_lemma))
    print(url, fpath)
    download_file(url, fpath)


def download_missing_pdf_from_xml(pdf_need_lemma):
    url = get_pdf_url_from_xml(os.path.join(FPATH_XML, get_xml_name(pdf_need_lemma)))
    fpath = os.path.join(FPATH_M_PDF, get_pdf_name(pdf_need_lemma))
    print(url, fpath)
    download_file(url, fpath)


if __name__ == "__main__":
    for pnl in list(get_missing_pdf_from_bib()):
        download_missing_pdf_from_bib(pnl)

    for pnl in list(get_missing_pdf_from_xml()):
        download_missing_pdf_from_xml(pnl)




    #

    #
