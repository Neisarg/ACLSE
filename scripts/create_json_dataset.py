import os
import json

doc_home = '/mnt/c/Users/neisa/Documents/Data/Projects/IR/ACLSE/WebApp/documents/'
text_path = os.path.join(doc_home,'text_data')
json_path = os.path.join(doc_home,'json_data')
url_home = os.path.join(doc_home, 'nlp-data/aclweb.org/anthology')

def multiple_try(func, param_list):
    for p in param_list:
        try:
            out = func(p)
        except:
            continue
        else:
            return out
    return None

def get_variations(word):
    out = []
    out.append(word)
    out.append(word.lower())
    out.append(word.upper())
    out.append(" ".join(list(word)))
    out.append(" ".join(list(word.lower())))
    out.append(" ".join(list(word.upper())))

    return out

def extract_title(content):
    return content.split("\n")[0]

def extract_references(content):
    ref = ""
    c_split = content.split("\n")
    ref_idx = multiple_try(c_split.index, get_variations("References"))
    if ref_idx is not None:
        ref = "\n".join(c_split[ref_idx + 1 :])

    return ref

def extract_authors(content):
    auth_line = content.split("\n")[1]
    #print(auth_line)
    _authors = auth_line.split(',')
    #print(_authors)
    authors = []
    for auth in _authors:
        #print(auth)
        ll = auth.split("and")
        #print(ll)
        try:
            ll.remove(" ")
        except:
            pass
        authors.extend(ll)

    for a in authors:
        if len(a) > 20:
            try:
                authors.remove(a)
            except:
                pass
    return authors

def extract_abstract(content):
    abstract = ""
    c_split = content.split("\n")
    ref_idx = multiple_try(c_split.index, get_variations("Abstract"))
    if ref_idx is not None:
        _lidx = c_split.index('', ref_idx+1)
        abstract = "\n".join(c_split[ref_idx+1: _lidx])

    return abstract


if __name__=="__main__":
    if not os.path.exists(json_path):
        os.makedirs(json_path)

    count = 0
    for root, subfolders, files in os.walk(text_path):
        for f in files:
            count +=1
            #print(count)
            f_split = f.split('.')
            pdf_name = '.'.join(f_split[:-1])
            json_name = pdf_name.split(".")[0] + ".json"
            abc_folder = f_split[0][0]
            sub_folder = f_split[0].split('-')[0]
            #idx = int(f_split[0].split('-')[1])
            url = os.path.join( os.path.join(os.path.join(url_home, abc_folder), sub_folder), pdf_name)
            print(url)

            json_url = os.path.join(json_path, json_name)
            text_url = os.path.join(root, f)
            json_data = {}
            json_data["url"] = url

            with open(text_url, 'r+', encoding = "ISO-8859-1") as tfile:
                content = tfile.read()
                if len(content.split("\n")) < 10:
                    continue
                json_data["title"] = extract_title(content)
                json_data["content"] = content
                json_data["references"] = extract_references(content)
                json_data["authors"] = extract_authors(content)
                json_data["summary"] = extract_abstract(content)

            with open(json_url, 'w+') as jfile:
                json.dump(json_data, jfile, indent=4)
