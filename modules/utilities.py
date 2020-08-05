import csv
import requests

def read_csv(csvfile):
    with open(csvfile) as csv_file:
        mylist = list(csv.reader(csv_file))
    return mylist

def getdataheader(arg):
    article = arg
    extract_link = requests.get(
        url="https://data.nonbinary.wiki/w/api.php?action=wbsearchentities&search={0}&language=en&format=json".format(
            article))
    jsonresponse = extract_link.json()
    return jsonresponse

def getdatabody(arg):
    article = arg
    extract_link = requests.get(
        url="https://data.nonbinary.wiki/w/api.php?action=wbgetentities&ids={0}&format=json".format(article))
    jsonresponse = extract_link.json()
    return jsonresponse

def stripstring(arg):
    #arg = str(arg).strip("['")
    #arg = str(arg).strip(",']")

    #return arg
    if arg != None:
       return arg[0]
    else:
        return None

def getitemdata(arg, p=[]):
    # gets all the requested values (p) for a given item (arg) and puts them in plist in the requested order, with title and description first
    plist = []
    # Gets the header information.
    myjson = getdataheader(arg)
    # Uses a class for easier nested searching.
    # Stripstring gets rid of excess chars.
    json_id = stripstring(DictQuery(myjson).get("search/id"))
    json_title = stripstring(DictQuery(myjson).get("search/title"))
    json_desc = stripstring(DictQuery(myjson).get("search/description"))
    plist.append(json_title)
    plist.append(json_desc)
    
    # Gets the actual information for that item
    jsonbody = getdatabody(json_id)
    for i in p:
        try:
            plist.append(DictQuery(jsonbody).get("entities/{0}/claims/{1}/mainsnak/datavalue/value".format(json_id, i)))
        except:
            plist.append("[unknown]")
    
    return plist

class DictQuery(dict):
    def get(self, path, default = None):
        keys = path.split("/")
        val = None

        for key in keys:
            if val:
                if isinstance(val, list):
                    val = [ v.get(key, default) if v else None for v in val]
                else:
                    val = val.get(key, default)
            else:
                val = dict.get(self, key, default)

            if not val:
                break

        return val