import sys, logging, inspect, re
logging.basicConfig(level=logging.DEBUG, filename='biblebot.log',
    format="[%(asctime)s %(module)s - %(name)s] {%(levelname)s} %(message)s")
import requests

book_patterns = ["Genesis", "Exodus", "Leviticus", "Numbers", "Deuteronomy",
"Joshua", "Judges", "Ruth", "1 Samuel", "2 Samuel", "1 Kings", "2 Kings", 
"1 Chronicles", "2 Chronicles", "Ezra", "Nehemiah", "Esther", "Job", "Psalms",
"Proverbs", "Ecclesiastes", "Song of Solomon", "Isaiah", "Jeremiah",
"Lamentations", "Ezekiel", "Daniel", "Hosea", "Joel", "Amos", "Obadiah",
"Jonah", "Micah", "Nahum", "Habakkuk", "Zephaniah", "Haggai", "Zechariah",
"Malachi", "Matthew", "Mark", "Luke", "John", "Acts ", "Romans", 
"1 Corinthians", "2 Corinthians", "Galatians", "Ephesians", "Philippians",
"Colossians", "1 Thessalonians", "2 Thessalonians", "1 Timothy", "2 Timothy",
"Titus", "Philemon", "Hebrews", "James", "1 Peter", "2 Peter", "1 John", 
"2 John", "3 John", "Jude", "Revelation", "Am.", "1 Chron.", "1 Chr.", "2 Chron.",
"2 Chr.", "Dan.", "Dn.", "Deut.", "Dt.", "Eccles.", "Eccl.", "Est.", "Exod.",
"Ex.", "Ezek.", "Ez.", "Ezra.", "Ezr.", "Gen.", "Gn.", "Hab.", "Hb.", "Hag.",
"Hg.", "Hosea.", "Hos.", "Isa.", "Is.", "Jer.", "Jer.", "Job.", "Jb.", "Joel.",
"Jl.", "Jon.", "Jon.", "Josh.", "Jo.", "Judg.", "Jgs.", "1 Kgs.", "2 Kgs.",
"Lam.", "Lam.", "Lev.", "Lv.", "Mal.", "Mal.", "Mic.", "Mi.", "Nah.", "Na.",
"Neh.", "Neh.", "Num.", "Nm.", "Obad.", "Ob.", "Prov.", "Prv.", "Ps.", "Pss.",
"Ru.", "1 Sam.", "1 Sm.", "2 Sam.", "2 Sm.", "Song of Sol.", "Sg.", "Zech.",
"Zec.", "Zeph.", "Zep.", "Apoc.", "Col.", "Col.", "1 Cor.", "1 Cor.", "2 Cor.",
"2 Cor.", "Eph.", "Eph.", "Gal.", "Heb.", "Heb.", "Jas.", "Jn.", "1 John.", 
"1 Jn.", "2 Jn.", "3 Jn.", "Lk.", "Mk.", "Matt.", "Mt.", "1 Pet.", "1 Pt.", 
"2 Pet.", "2 Pt.", "Philem.", "Phlm.", "Phil.", "Phil.", "Rev.", "Rv.", "Rom.",
"Rom.", "1 Thess.", "1 Thes.", "2 Thess.", "2 Thes.", "1 Tim.", "1 Tm.", 
"2 Tim.", "2 Tm.", "Ti."]


def parse_references(in_str):
    reference_list = []
    for book_pattern in book_patterns:
        for ref in re.findall(book_pattern+"\s+\d{1,3}:\d{1,3}", in_str):
            reference_list.append(ref)

    reference_list = list(set(reference_list)) # remove any duplicates
    return reference_list

class Bible(object):
    def __init__(self, name, url):
        self.name = name
        self.url = url
        self.config = {}

    def lookup(self, reference):
        logging.info("Looking up %s in %s" % (reference, self.name))


class ESVBible(Bible):
    def __init__(self):
        super(ESVBible, self).__init__("ESV",
                "http://esvapi.org/v2/rest/passageQuery?%(options)s&passage=%(reference)s")
        self.config = { 
                "key" : "IP",
                "output-format": "plain-text",
                "include-passage-horizontal-lines": 0,
                "include-heading-horizontal-lines": 0,
                "include-footnotes": 0,
                "include-headings": 0,
                "include-subheadings": 0,
                }



    def lookup(self, reference):
        super(ESVBible, self).lookup(reference)
        urlopts = {
                "options": '&'.join(["%s=%s" % (opt[0], opt[1]) for opt in
            self.config.items()]),
                "reference": '+'.join(reference.split())
                }
        logging.debug("Requesting " + (self.url % urlopts))
        page = requests.get(self.url % urlopts)
        page_html = page.text.strip()
        return page_html

def get_translations():
    dict_translations = {}
    for name, obj in inspect.getmembers(sys.modules[__name__]):
        if inspect.isclass(obj) and issubclass(obj, Bible):
            if name != "Bible":
                current = obj()
                dict_translations[current.name] = current 

    return dict_translations 

translations = get_translations()
