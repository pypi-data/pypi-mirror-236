from bs4 import BeautifulSoup
import requests
import time
import xmltodict
import re

LINK_HTML_TEXT = 'https://eur-lex.europa.eu/legal-content/EN/TXT/HTML/?uri=CELEX:cIdHere&from=EN'
LINK_SUMJURE = 'https://eur-lex.europa.eu/legal-content/EN/TXT/HTML/?uri=CELEX:cIdHere_SUM&from=EN'
LINK_ENTIRE_PAGE = 'https://eur-lex.europa.eu/legal-content/EN/ALL/?uri=CELEX:cIdHere'
CELEX_SUBSTITUTE = 'cIdHere'
LINK_SUMMARY = 'https://eur-lex.europa.eu/legal-content/EN/TXT/HTML/?uri=CELEX:cIdHere_SUM&from=EN'
prog = re.compile(r'^[1234567890CE]\d{4}[A-Z]{1,2}\d{3,4}\d*')


"""
Method for detecting code-words for case law directory codes for cellar.
"""

def is_code(word):
    return word.replace(".", "0").replace("-", "0")[1:].isdigit()


"""
Wrapped method for requests.get().
After 10 retries, it gives up and returns a "404" string.
"""


def response_wrapper(link, num=1):
    if num == 10:
        return "404"
    try:
        response = requests.get(link)
        return response
    except Exception:
        time.sleep(0.5 * num)
        return response_wrapper(link, num + 1)

"""
This method cleans the celex, in case of multiple celex id's existing under one field. 
Returns a single, correct celex id.
"""


def clean_celex(celex):
    if celex == celex:  # nan check
        if ";" in celex:
            idss = celex.split(";")
            for idsss in idss:
                if "_" in idsss:
                    celex = idsss
        else:
            celex = celex
    else:
        return None
    return celex




"""
This method returns the html of a summary page.
Cellar specific, works for celex id's starting a 6 and 8.
"""

def get_summary_html(celex):
    celex = clean_celex(celex)
    if celex is None:
        return "No summary available"
    celex = celex.replace(" ", "")
    if celex.startswith("6"):
        if "INF" in celex:
            link = LINK_HTML_TEXT
        else:
            link = LINK_SUMMARY
        sum_link = link.replace(CELEX_SUBSTITUTE, celex)
        response = response_wrapper(sum_link)
        try:
            if response.status_code == 200:
                if "The requested document does not exist." in response.text:
                    return "No summary available"
                else:
                    return response.text
            else:
                return "No summary available"
        except Exception:
            return "No summary available"
    elif celex.startswith("8"):
        link = LINK_SUMJURE
        sum_link = link.replace(CELEX_SUBSTITUTE, celex)
        response = response_wrapper(sum_link)
        if response.status_code == 200:
            if "The requested document does not exist." in response.text:
                return "No summary available"
            else:
                return "No summary available"
        else:
            return "No summary available"


"""
Method used to extract the summary from a html page.
Cellar specific, uses get_words_from_keywords.
Currently only walking for celex id's starting with a 6 ( EU cases).
"""


def get_summary_from_html(html, starting):
    # This method turns the html code from the summary page into text
    # It has different cases depending on the first character of the CELEX ID
    # Should only be used for summaries extraction
    text = get_full_text_from_html(html)
    if starting == "8":
        return "No summary available"
    elif starting == "6":
        try:
            text2 = text.replace("Summary", "nothing", 1)
            index = text2.index("Summary")
            text2 = text2[index:]
            return text2
        except Exception:
            return text
    return text


"""
Method used to extract the keywords from a html page.
Cellar specific, uses get_words_from_keywords.
"""


def get_keywords_from_html(html, starting):
    # This method turns the html code from the summary page into text
    # It has different cases depending on the first character of the CELEX ID
    # Should only be used for summaries extraction
    text = get_full_text_from_html(html)
    if starting == "8":
        text = "No keywords available"
        return text
    elif starting == "6":
        return get_words_from_keywords(text)


"""

Method used for citations extraction from eurlex webservices.
It reads the SOAP response from the webservices, and adds values to the dictionary based on the results.
Dictionary is using the celex id of a work as key and a list of celex id's of works cited as value.

"""


def extract_dictionary_from_webservice_query(response):
    text = response.text
    read = xmltodict.parse(text)
    results = read['S:Envelope']['S:Body']['searchResults']['result']
    dictionary = dict()
    if type(results) == list:
        for result in results:
            celex, citing = extract_citations_from_soap(result)
            dictionary[celex] = citing
    else:
        celex, citing = extract_citations_from_soap(results)
        dictionary[celex] = citing
    return dictionary


"""

Method used for citations extraction from eurlex webservices.
Reads the individual celex id and documents cited from a single result.

"""


def extract_citations_from_soap(results):
    main_content = results['content']['NOTICE']['WORK']
    celex = main_content['ID_CELEX'].get('VALUE')
    try:
        citing = main_content['WORK_CITES_WORK']
    except KeyError:
        return celex, ""
    citing_list = list()
    if type(citing) == list:
        for cited in citing:
            celex_of_citation = get_citation_celex(cited)
            if celex_of_citation != "":
                citing_list.append(celex_of_citation)
        return celex, ";".join(citing_list)
    else:
        return celex, get_citation_celex(citing)


"""

Method used for citations extraction from eurlex webservices.
Goes thru all of the different id's of the document cited, and returns the one that is a celex id.

"""


def get_citation_celex(cited):
    identifiers = cited['SAMEAS']
    if type(identifiers) == list:
        for id in identifiers:
            ident = id['URI']['IDENTIFIER']
            if is_celex_id(ident):
                return ident
    else:
        ident = identifiers['URI']['IDENTIFIER']
        if is_celex_id(ident):
            return ident
    return ""


"""

Method checking if the id passed is a celex id, using regex.

"""


def is_celex_id(id):
    if id is None:
        return False
    if prog.match(id):
        return True
    else:
        return False


"""
This method tries to extract only they keywords from a part of html page containing it.
They keywords on the page are always separated by " - " or other types of dashes.

"""


def get_words_from_keywords_em(text):
    lines = text.split(sep="\n")
    returner = set()
    for line in lines:
        if "—" in line:
            line = line.replace('‛', "")
            line = line.replace("(", "")
            line = line.replace(")", "")
            returner.update(line.split(sep="—"))
        elif "–" in line:
            line = line.replace('‛', "")
            line = line.replace("(", "")
            line = line.replace(")", "")
            returner.update(line.split(sep="–"))
        elif " - " in line:
            line = line.replace('‛', "")
            line = line.replace("(", "")
            line = line.replace(")", "")
            returner.update(line.split(sep=" - "))
    return ";".join(returner)


"""

One of the methods used to extract keywords from summary text.

"""


def get_words_from_keywords(text):
    if "Keywords" in text:
        try:
            index = text.find("Keywords")
            if "Summary" in text[index:index + 25]:
                text2 = text.replace("Summary", "", 1)
                try:
                    indexer = text2.find("Summary")
                    text = text[index:indexer]
                except Exception:
                    text = text
        except Exception:
            text = text
    else:
        if "Summary" in text:
            index = text.find("Summary")
            text = text[:index]
    return get_words_from_keywords_em(text)


"""
  This method turns the html code from the summary page into text.
  It has different cases depending on the first character of the CELEX ID.
  Universal method, also replaces all "," with "_".
"""


def get_full_text_from_html(html_text):
    # This method turns the html code from the summary page into text
    # It has different cases depending on the first character of the CELEX ID
    # Should only be used for summaries extraction
    soup = BeautifulSoup(html_text, "html.parser")
    for script in soup(["script", "style"]):
        script.extract()  # rip it out
    text = soup.get_text()
    # break into lines and remove leading and trailing space on each
    lines = (line.strip() for line in text.splitlines())
    # break multi-headlines into a line each
    chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
    # drop blank lines
    text = '\n'.join(chunk for chunk in chunks if chunk)
    text = text.replace(",", "_")  # Because data stored in a Comma-Separated file
    return text




def get_html_text_by_celex_id(celex):
    link = LINK_ENTIRE_PAGE
    celex = clean_celex(celex)
    if celex is None:
        return '404'
    final_link = link.replace(CELEX_SUBSTITUTE, celex)
    html = response_wrapper(final_link)
    if "The requested document does not exist." in html.text:
        return "404"
    else:
        return html.text


def get_operative_part(text):
    old_docs = "Operative part"
    new_docs = "On those grounds_"
    start = text.rfind(old_docs)
    if start == -1:
        start = text.rfind(new_docs)
    else:
        start = text[start:].find('\n') + start
    if start != -1:
        find_end = text[start:].find("Table of contents")
        if find_end == -1:
            find_end = text[start:].find('[Signatures]')
            if find_end == -1:
                find_end = text[start:].find('×')
                if find_end == -1:
                    find_end = len(text)
        return text[start:find_end+start].replace(' ','')
    return ""




"""
This method gets the page containing all document details for extracting the subject matter and
the case law directory codes. Uses the celex identifier of a case.
"""


def get_entire_page(celex):
    link = LINK_ENTIRE_PAGE
    celex = clean_celex(celex)
    if celex is None:
        return "No data available"
    sum_link = link.replace(CELEX_SUBSTITUTE, celex)
    response = response_wrapper(sum_link)
    try:
        if response.status_code == 200:
            if "The requested document does not exist." in response.text:
                return "No data available"
            else:
                return response.text
        else:
            return "No data available"
    except Exception:
        return "No data available"


"""
This Method gets the subject matter from a fragment of code containing them.
Used for extracting subject matter for cellar cases only.
"""


def get_subject(text):
    try:
        index_matter = text.index("Subject matter:")
        try:
            index_end = text.index("Case law directory code:")  # if this fails then miscellaneous
        except Exception:
            index_end = text.index("Miscellaneous information")
        extracting = text[index_matter + 16:index_end]
        subject_mat = extracting.split(sep="\n")
        subject = ";".join(subject_mat)
        subject = subject[:len(subject) - 1]
    except Exception:
        subject = ""
    return subject


"""
This Method extracts all eurovocs, from a fragment containing them.
Used for extracting eurovoc for cellar cases.
"""


def get_eurovoc(text):
    try:
        start = text.find("EUROVOC")
        try:
            ending = text.find("Subject matter")
        except Exception:
            try:
                ending = text.find("Directory code")
            except Exception:
                try:
                    ending = text.find("Miscellaneous information")
                except Exception:
                    ending = start
        if ending is start:
            return ""
        else:
            text = text[start:ending]
            texts = text.split("\n")
            lists = []
            for t in texts:
                if "EUROVOC" not in t and t != "":
                    lists.append(t)
            return ";".join(lists)
    except Exception:
        return ""


"""
Method for getting all of the case directory codes for each cellar case.
Extracts them from a string containing the eurlex website containing all document information.
"""


def get_codes(text):
    try:
        index_codes = text.index("Case law directory code:")
        index_end = text.index("Miscellaneous information")
        extracting = text[index_codes + 20:index_end]
        extracting = extracting.rstrip()
        words = extracting.split()
        codes = [x for x in words if is_code(x)]
        codes_full = list(set(codes))
        codes_result = list()
        indexes = [extracting.find(x) for x in codes_full]
        for x in range(len(codes_full)):
            done = False
            index_start = indexes[x]
            getting_ending = extracting[index_start:]
            words_here = getting_ending.split()

            for words in words_here:

                if words is not words_here[0]:

                    if is_code(words):
                        ending = getting_ending[2:].find(words)
                        done = True
                        break
            if done:
                code_text = getting_ending[:ending]
            else:
                code_text = getting_ending

            codes_result.append(code_text.replace("\n", ""))
        code = ";".join(codes_result)
    except Exception:
        code = ""
    return code


def get_advocate_or_judge(text, phrase):
    """
    :param text: full text of the info page of a case from eur-lex website
    :param phrase: Phrase to search for, works for Advocate General and Judge-Rapporteur
    :return: The name of the person with the title of phrase param ( if listed on page)
    """
    try:
        index_matter = text.index(phrase)
        extracting = text[index_matter + len(phrase):]
        extracting = extracting.replace('\n', '', 1)
        ending = extracting.find('\n')
        extracting = extracting[:ending]
        extracting.replace(',', '_')  # In case they ever change it to delimiter
        subject_mat = extracting.split(sep="_")
        subject_mat = [i.strip() for i in subject_mat]
        return ";".join(subject_mat)
    except Exception:
        return ""


def get_case_affecting(text):
    """
    :param text: full text of the info page of a case from eur-lex website
    :return: The celex id's of case affecting listed + entire string data with more information about the case affecting
    """
    phrase = 'Case affecting:'
    try:
        index_matter = text.index(phrase)
        extracting = text[index_matter + len(phrase):]
        extracting = extracting.replace('\n', '', 1)
        phrases = extracting.split(sep='\n')
        full_strings = []
        ids = set()
        for p in phrases:
            if ':' in p:
                break
            else:
                words = p.split()
                if len(words)>1:
                    for w in words:
                        if is_celex_id(w):
                            ids.add(w)
                    full_strings.append(p)
                else:
                    if len(words)==1:
                        last = full_strings.pop()
                        last +="_"+p
                        full_strings.append(last)

        return ';'.join(ids), ';'.join(full_strings)
    except Exception:
        return "", ""

def get_citations_with_extra_info(text):
    """
    :param text: full text of the info page of a case from eur-lex website
    """
    phrase = 'Instruments cited in case law:'
    data_list = []
    try:
        index_matter = text.index(phrase)
        extracting = text[index_matter + len(phrase):]
        extracting = extracting.replace('\n', '', 1)
        sentences = extracting.splitlines()
        for line in sentences:
            words = line.split()
            if is_celex_id(words[0]):
                fixed_line = line.replace(" - ",'-').replace(" ","_")
                data_list.append(fixed_line)
            else:
                return ";".join(data_list)

    except:
        return ''
