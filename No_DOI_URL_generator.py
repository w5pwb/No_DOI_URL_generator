
# coding: utf-8

# Imported modules:
#
# os for file handling
#
# urllib for sending and handling server requests.
#
#
# re for regex
#
# requests for sending server requests.
#



import os
import urllib
import re
import requests


# The 'name_converter' method takes the journal name from the citation and converts it into the 3 letter
# abbreviation used by the journal.  It returns the abbreviation which can then be use to generate a URL.
#
# 1. Development = dev
# 2. biol open  = bio
# 3. journal of cell science = jcs
# 4. journal of experimental biology = jeb
# 5. disease models and mechanisms = dmm
#



def name_converter(name):
    convert = {
        'Development': "dev",
        'Biology open': "bio",
        'Journal of Cell Science': "jcs",
        'Journal of Experimental Biology': "jeb",
        'Disease models & mechanisms': "dmm",

    }

    #get value associated with key and return it.
    return (convert.get(name))



# The 'generate_URL' method takes the journal name, issue, volume, and first page from the citation and uses them generate a site specific URL.
# This standardizes all the links to fit the Compnay of Biologists website, thus doing away with any redirects.
#
# if blocks check to see whether the citation is a paper or a supplement and then the proper URL is generated using f strings.
#
#
#



def generate_URL(list):

    journal = name_converter(list[4])
    issue = list[2]
    volume = list[8].rstrip()
    firstpage = list[3].split('-')

    if 'paper' in list[5]:

        webstring = f"http://{journal}.biologists.org/content/{volume}/{issue}/{firstpage[0]}.long"

    if 'supp' in list[5]:

        webstring = f"http://{journal}.biologists.org/content/{volume}/{issue}/{firstpage[0]}.supplemental"

    return(webstring)



# The 'retrieve_URL' method takes the journal name and pubmed ID from citations that lack an issue number.
# this_pmid takes the pubmed ID and this_journal takes the journal name and calls the 'name_converter' method.
#
# An f string generates a Company of Biologists pubmed ID link and then sends a request to the CofB servers.
# The request retrieves the proper C of B URL that is then assigned to the 'data' variable and returned as a URL.


def retrieve_URL(journal, pmid):
    this_pmid = pmid
    this_journal = name_converter(journal)
    try:
        link = f"http://{this_journal}.biologists.org/cgi/pmidlookup?view=long&pmid={this_pmid}"
        data = requests.request("GET", link)

    except urllib.error.HTTPError as e:

        print(e)

    return data.url


# A simple URL test method that can be used in a loop or on its own.
# The method sends a request to the URL and then returns an HTTP code.  If the code recieved = 200, the URL exists.
# All other HTTP errors, including time outs and 404 are handled by the excep block.
#
#
# I added in the print line because without it I was unsure if the python kernal was hung up or if I was still sending requests to the C of B servers.
#
# The idea behind this was to create a loop that tested the URL before adding it to the final proforma.
# I ended up choosing not to because I didn't want to send too many requests at a time.
#
#
# TODO: this method might be better if it accepted a list with the URL to be tested in addition to the FBrf so that exceptions can be
# associated with the specific citation and not just he citation URL.



def test_URL(URL):

    try:
        ret = urllib.request.urlopen(URL)
        if ret.code == 200:
            print('ok')
            return True

    except urllib.error.HTTPError as e:
        print(e)
        print(URL)
        return False




# The main method loops through all the files in a specified directory and places the contents into a list.
#
# no_DOI collects all citations without a DOI into a list.
# no_pmid_or_issue collects the handful of citations that have no pubmed ID or issue number.
# paperID_URL collects the final pair of FB ID and proper URL for QC testing later.
#
# I settled on the following format for supplemental materials:
#
# http://jeb.biologists.org/content/215/18/3254.supplemental - link is more informative and more straightforward than
# the other supplemental format used by C of B.
#
#
#

os.chdir(r"D:\Python\FlyBase_Py\journal_lists")

cross_ref_dict = {}

no_DOI = []
no_pmid_or_issue = []
paperID_URL = []

for files in os.walk("."):
    file_list = (files[2])

for file in file_list:

    with open (file) as file_object:
        for line in file_object:

            pub = line.split('\t')
            #The cross_ref_dict takes the FBrf of each paper, turnes it into a key, then uses a list
            #containing the page number and FBrf of the associated paper as the value.  Thus when a supplement
            #FBrf is used as a key, it will return a list with the supplement's parent paper and page number.
            cross_ref_dict[pub[0]] = [pub[3].split('-')[0],pub[7]]

            if '10' not in pub[1] and 'paper' in pub[5] or 'supp' in pub[5]:
                no_DOI.append(pub)



# I decided that there were four cases that needed to be addressed.
# 1. papers with full info that could be easily converted to URLs.
# 2. papers with no issue number but that have a PMID.
# 3. suppplements.
# 4. papers with no PMID or issue number.
#
# Each case gets an 'if' block that sends the citation information to correct method or list.
# The final product is a standardized C of B URL for all  the papers.
#
# The header of the files I used for reference:
# #SUBMITTED ID[0]	DOI	ISSUE[1]	PAGES[2]	PARENT_PUBLICATION_TITLE[3]	PUBLICATION_TYPE[4]	PUBMED_ID[5]	RELATED_PUBLICATIONS[6]	VOLUME[7]
#
#
# TODO: I really dislike the way the f strings that generate the proforma look but I didn't want to go down a rabbit hole looking for another way to produce them.
# A short method that takes the proper data and returns the string might make this look prettier but is probably unnecessary.


#change directory up one to write new file.
os.chdir(r'D:\Python\FlyBase_Py')

with open ('URL_list.txt', 'w+') as newf:

    for citation in no_DOI:

        if not (citation[2].isnumeric()) and citation[6].isnumeric(): #no issue, has pmid

            paperID_URL.append([citation[0], retrieve_URL(citation[4], citation[6])])
            newf.write((
                            f'!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!\n'
                            f'! PUBLICATION PROFORMA               	Version 48:  21 May 2018\n'
                            f'! P22.  FlyBase reference ID (FBrf) or "new"  *U :{citation[0]}\n'
                            f'! P11b. URL                                   *R :{retrieve_URL(citation[4], citation[6])}\n'))



        if not (citation[2].isnumeric()) and not(citation[6].isnumeric()): #no issue, no pmid

            no_pmid_or_issue.append(citation[0]) #collects the FBrfs of trouble papers for later.

        if 'paper' in citation[5] and citation[2].isnumeric(): #paper, has issue

             paperID_URL.append([citation[0], generate_URL(citation)])

             newf.write((
                            f'!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!\n'
                            f'! PUBLICATION PROFORMA               	Version 48:  21 May 2018\n'
                            f'! P22.  FlyBase reference ID (FBrf) or "new"  *U :{citation[0]}\n'
                            f'! P11b. URL                                   *R :{generate_URL(citation)}\n'))

        if 'supp' in citation[5] and citation[2].isnumeric(): #supplement, has issue. No supplement has a pmid or page.

            citation[3] = cross_ref_dict.get(cross_ref_dict.get(citation[0])[1])[0]  #returns a page number using the
            #cross_ref_dict created earlier.  Replaces the blank spot in the citation with the page number.
            #The dicitonary takes the FBrf of the supplement, gets the associated value, which is the FBrf of the paper
            #the supplement is attached to, then pulls out the page number from the citation of the parent paper.
            paperID_URL.append([citation[0], generate_URL(citation)])

            newf.write((
                            f'!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!\n'
                            f'! PUBLICATION PROFORMA               	Version 48:  21 May 2018\n'
                            f'! P22.  FlyBase reference ID (FBrf) or "new"  *U :{citation[0]}\n'
                            f'! P11b. URL                                   *R :{generate_URL(citation)}\n'))





newf.close()

print ('Papers without DOIs: ',len(no_DOI))
print ('Final tally of papers handled by this script: ',len( paperID_URL))
print ('Trouble papers: ',len( no_pmid_or_issue))
