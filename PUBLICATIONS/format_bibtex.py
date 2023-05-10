"""
#############################################################################
#                                FORMAT BIBTEX                              #
#############################################################################
Author:     Mohammad Hossain Mohammadi
Date:       November 2017
"""""

import bibtexparser
from bibtexparser.bparser import BibTexParser
from bibtexparser.customization import convert_to_unicode

import sys
reload(sys)
sys.setdefaultencoding('utf-8')

def format_bibtex(pub, format, main_author, initials):
    """
    Format a publication dictionary in a required formatting style
    Args:       -pub is a publication data structure constaining Bibtex fields
                -format is a string for the format required, e.g. 'jemdoc', 'tex', 'html'
                -main_author is a string of the main author's last name
                -initials controls whether the first names are shown as initials {0/1}
    Returns:    -ref is a string of the publication reference
                -entry_type is a string for the Bibtex publication entrytype
                -year is an integer for the publication year (useful for sorting)
    Author:     Mohammad Hossain Mohammadi
    Date:       November 2017
    """""
    # Initialization
    ref = ''
    entry_type = pub["ENTRYTYPE"]
    authors = ''
    title = ''
    journal = ''
    booktitle = ''
    publisher = ''
    school = ''
    address = ''
    volume = ''
    number = ''
    pages = ''
    month = ''
    year = ''
    doi = ''
    link = ''
    pdf = ''
    arxiv = ''
    note = ''
    

    # Set Bibtex Values if Existing in Pub Dictionary
    if entry_type == 'article' or entry_type == 'inproceedings' or entry_type == 'incollection':
        if 'month' in pub:     # e.g. Jan. for January
            month = pub["month"][0:3] + '.'
    if 'doi' in pub:
        doi = pub["doi"]
    if 'address' in pub:
        address = pub["address"]
    if 'title' in pub:
        title = pub["title"]
        title = title.replace('{','')       # Remove curly brackets from string
        title = title.replace('}','')
    if 'publisher' in pub:
        publisher = pub["publisher"]
    if 'year' in pub:
        year = pub["year"]
    if 'volume' in pub:
        volume = pub["volume"]
    if 'pages' in pub:
        pages = pub["pages"]
    if 'number' in pub:
        number = pub["number"]
    if 'journal' in pub:
        journal = pub["journal"]
        journal = journal.replace('}','')
        journal = journal.replace('{','')
    if 'booktitle' in pub:
        booktitle = pub["booktitle"]
        booktitle = booktitle.replace('{','')       # Remove curly brackets from string
        booktitle = booktitle.replace('}','')
    if 'link' in pub:
        link = pub["link"]
    if 'school' in pub:
        school = pub["school"]
    if 'pdf' in pub:
        pdf = pub["pdf"]
    if 'arxiv' in pub:
        arxiv = pub["arxiv"]
    if 'note' in pub:
        note = pub["note"]
        note = note.replace('{','')       # Remove curly brackets from string
        note = note.replace('}','')
        
        

    # Format Author Names based on Formatting Style
    authors_ = pub["author"].split(' and ')
    for iA, author_ in enumerate(authors_):
        if ',' in author_:  # Order: LastName, FirstName
            anames = author_.split(', ')
            fname = anames[1]           # First name string
            lname = anames[0]           # Last name string
        else:               # Order: FirstName LastName
            anames = author_.split(' ')
            lname = anames[-1]          # Last name string
            fname = anames[:-1]         # First name string
            fname = ' '.join(fname)

        # Convert first name into initials (if not already)
        if initials==1 and ('.' not in fname):
            fnames = fname.split(' ')
            fname = ''
            for iF,fn in enumerate(fnames):
                fname = fname + fn[0] + '.'     # Full stop & space after initials
                if iF<(len(fnames)-1):
                    fname += ' '                # Space b/w author's first names

        # Boldify main  author (depends on formatting style)
        author = fname + ' ' + lname
        if main_author == lname:
            if format == 'jemdoc':
                author = '*' + author + '*'
            elif format == 'tex':
                author = '\\textbf{' + author + '}'
            elif format == 'html':
                author = '<strong>' + author + '</strong>'

        # Combine author list into 1 string
        authors += author
        if iA<(len(authors_)-2):
            authors += ', '     # Separation b/w author full names
        elif iA==(len(authors_)-2):
            authors += ' and '  # Separation for last author

    # Format Other Bibtex Fields based on Formatting Style
    if format == 'jemdoc':
        title = '/' + title + '/'
        journal = '/' + journal + '/'
        booktitle = '/' + booktitle + '/'
        link = '[' + link + ' link]'



    # Create Reference based on Formatting Style
    if entry_type == 'book':
        ref = authors + '. ' + title + '. ' + address + ': ' + publisher + ', ' + year + '.'
    elif entry_type == 'article':
        ref = authors + ', "' + title + '," ' + journal 
        if pages != '':
            ref = ref + ', pp. ' + pages
        if volume != '':
            ref = ref + ', vol. ' + volume
        if number != '':
            ref = ref + ', no. ' + number
        if month != '':
            ref = ref + ', ' + month + ' ' + year
        elif year != '':
            ref = ref + ', ' + year
        if note != '':
            ref = ref + ', (' + note + ')'
        if doi != '':
            ref = ref + ' \[[https://doi.org/' + doi + ' paper]\]'
        if arxiv != '':
            ref = ref + ' \[[' + arxiv + ' arXiv]\]'
        if pdf != '':
            ref = ref + ' \[[PAPERS/' + pdf + '.pdf pdf]\]'
        ref = ref + '\n'                                    # add empty line
    elif entry_type == 'inproceedings':
        ref = authors + ', "' + title + '," in ' + booktitle 
        if pages != '':
            ref = ref + ', pp. ' + pages
        if note != '':
            ref = ref + ', (' + note + ')'
        if doi != '':
            ref = ref + ' \[[https://doi.org/' + doi + ' paper]\]'
        if arxiv != '':
            ref = ref + ' \[[' + arxiv + ' arXiv]\]'
        if pdf != '':
            ref = ref + ' \[[PAPERS/' + pdf + '.pdf pdf]\]'
        ref = ref + '\n'                                    # add empty line
    elif entry_type == 'incollection':
        ref = authors + ', "' + title + '," in ' + booktitle
        if pages != '':
            ref = ref + ', pp. ' + pages
        if publisher != '':
            ref = ref + ', ' + publisher
        if year != '':
            ref = ref + ', ' + year
        if note != '':
            ref = ref + ', (' + note + ')'
        if doi != '':
            ref = ref + ' \[[https://doi.org/' + doi + ' link]\]'
        if arxiv != '':
            ref = ref + ' \[[' + arxiv + ' arXiv]\]'
        if pdf != '':
            ref = ref + ' \[[PAPERS/' + pdf + '.pdf pdf]\]'
        ref = ref + '\n'
    elif entry_type == 'mastersthesis':
        ref = authors + '. "' + title + '." Master\'s Thesis, ' + school + ', ' + address + ', ' + year + ' \[[' + doi + ' link]\]' + ' \[[PAPERS/' + pdf + '.pdf pdf]\]\n'
    elif entry_type == 'phdthesis':
        ref = authors + '. "' + title + '." PhD Dissertation, ' + school + ', ' + address + ', ' + year + ' \[[' + doi + ' link]\]' + ' \[[PAPERS/' + pdf + '.pdf pdf]\]\n'

    return ref, entry_type, int(year)


def create_research_file(db, format, outname, main_author, initials):
    """
    Creates a file of research publications
    Args:       -db is the publication data structure containing Bibtex fields
                -format is a string for the format required, e.g. 'jemodoc', 'tex', 'html'
                -outname is a string for the output file name, e.g. 'research'
                -main_author is the main author's last name string
                -initials controls whether the first names are shown as initials {0/1}
    Author:     Mohammad Hossain Mohammadi
    Date:       November 2017
    """""
    # Sorting Key
    def access_year(elem):
        return elem[2]

    # Initialization
    books = []
    journals = []
    conferences = []
    theses = []
    bookChapters = []

    # Create Separate Lists for Publication Type
    for pub in db.entries:
        # Format publication dictionary using a formatting style
        ref, entry_type, year = format_bibtex(pub, format, main_author, initials)
        

        # Append publication reference into lists
        if entry_type == 'book':
            books.append([ref, entry_type, year])
        elif entry_type == 'article':
            journals.append([ref, entry_type, year])
        elif entry_type == 'inproceedings':
            conferences.append([ref, entry_type, year])
        elif entry_type == 'mastersthesis' or entry_type == 'phdthesis':
            theses.append([ref, entry_type, year])
        elif entry_type == 'incollection':
            bookChapters.append([ref, entry_type, year])


    # Create Sorted Research File
    outfile = outname + '.' + format
    with open(outfile, 'w') as the_file:
        if format == 'jemdoc':
            the_file.write('# jemdoc: menu{MENU}{'+ outname + '.html}, notime\n')
            the_file.write('== Gianluca Bianchin -- Publications\n\n')

            if books:
                books.sort(reverse=True, key=access_year)
                the_file.write('== Books\n')
                for book in books:
                    the_file.write('. ' + book[0] )
                the_file.write('\n')

            if journals:
                journals.sort(reverse=True, key=access_year)
                the_file.write('== Journals\n')
                for journal in journals:
                    the_file.write('. ' + journal[0])
                the_file.write('\n')

            if conferences:
                conferences.sort(reverse=True, key=access_year)
                the_file.write('== Conferences\n')
                for conference in conferences:
                    the_file.write('. ' + conference[0] )
                the_file.write('\n')
        
            if bookChapters:
                bookChapters.sort(reverse=True, key=access_year)
                the_file.write('== Book Chapters\n')
                for bookChapters in bookChapters:
                    the_file.write('. ' + bookChapters[0] )
                the_file.write('\n')

            if theses:
                theses.sort(reverse=True, key=access_year)
                the_file.write('== Theses\n')
                for thesis in theses:
                    the_file.write('. ' + thesis[0] )
                the_file.write('\n')

        




def main(format, outname, main_author, initials):
    """
    Format publication references in a formatting style
    Args:       -initials is an integer which controls whether the first names are shown as initials {0/1}
    """""
    # Concatenate Alias.bib file with GB.bib file
    filenames = ['PUBLICATIONS/alias.bib', "PUBLICATIONS/GB.bib"]
    with open('PUBLICATIONS/aux_combined.bib', 'w') as outfile:
        for fname in filenames:
            with open(fname) as infile:
                outfile.write(infile.read())
                
                
    # Load Bibtex File
    with open('PUBLICATIONS/aux_combined.bib') as bibtex_file:
        parser = BibTexParser()
        parser.customization = convert_to_unicode
        db = bibtexparser.load(bibtex_file, parser=parser)

    # Creates a Research File of Publication References
    create_research_file(db, format, outname, main_author, initials)


# Handle Arguments & Call Main Function
if __name__ == '__main__':
    format = 'jemdoc'
    outname = 'publications'
    main_author = 'Bianchin'
    initials = int(sys.argv[1])

    sys.exit(main(format, outname, main_author, initials))
