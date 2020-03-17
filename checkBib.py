import bibtexparser, sys, re, codecs
from bibtexparser.customization import homogenize_latex_encoding
warning = 0

def erroID(i, ID, default):
    print("Padrão incorreto no campo ID da referencia:", i, "(", ID,
            ");\nVerifique o(s) nome(s) do(s) autor(es), um possível padrão é colocar o sobrenome capitalizado e depois o ano:")
    print(default)
    print("---------------\\/---------------")

def callWarn(i, ID, default):
    global warning
    warning += 1
    erroID(i, ID, default)

def with1author(authors, default, i, ID):
    author = authors[0].split(',')
    if(len(author) == 1):
        author = authors[0].split(' ')
        default = author[-1].capitalize()+year
        if not ID.startswith(default):
            callWarn(i, ID, default)
            return 0

    else:
        author = author[0].split(' ')
        default = author[-1].capitalize()+year
        if not ID.startswith(default):
            callWarn(i, ID, default)
            return 0

    return default

def with2authors(authors, default, i, ID):
    author1 = authors[0].split(',')
    author2 = authors[1].split(',')
    if(len(author1) == 1 or len(author2) == 1):
        author1 = authors[0].split(' ')
        author2 = authors[1].split(' ')
        default = author1[-1].capitalize()+'&'+author2[-1].capitalize()+year
        if not ID.startswith(default):
            callWarn(i, ID, default)
            return 0

    else:
        default = author1[0].capitalize()+'&'+author2[0].capitalize()+year
        if not ID.startswith(default):
            callWarn(i, ID, default)
            return 0

    return default

def withmanyauthors(authors, default, i, ID):
    author = authors[0].split(',')
    if(len(author) == 1):
        author = authors[0].split(' ')
        default = author[-1].capitalize()+'+'+year

        if not ID.startswith(default):
            callWarn(i, ID, default)
            return 0

    else:
        author = author[0].split(' ')
        default = author[-1].capitalize()+'+'+year
        if not ID.startswith(default):
            callWarn(i, ID, default)
            return 0

    return default

try:
    f = codecs.open(sys.argv[1], encoding='utf-8', errors='strict')
    i = 1
    for line in f:
        i += 1
        pass
    with open(sys.argv[1]) as bibtex_file:
        bib_database = bibtexparser.bparser.BibTexParser(common_strings=True, ignore_nonstandard_types=False, interpolate_strings=False).parse_file(bibtex_file)
except UnicodeDecodeError as e:
    print("invalid utf-8 at line", str(i+1))
    print(e)
    exit()

try:
    for i in range(0, len(bib_database.entries)):
        ID = bib_database.entries[i]['ID']
        default = ''

        print("\n---------------/\\---------------")
        unCheck = ['booklet', 'manual', 'proceedings']

        if bib_database.entries[i]['ENTRYTYPE'] not in unCheck:
            checks = bib_database.entries[i]['author']
            for rep in ['\\v', '\\c', '\\', '\'', '\"', '{', '}', '~', '^']:
                checks = checks.replace(rep, '')
            checks = checks.replace('\n', ' ')

            authors = checks.split(' and ')
            year = bib_database.entries[i]['year']

            if len(authors) == 1:
                if ("et al" in authors[0]):
                    default = withmanyauthors(authors, default, i, ID)
                    if (default == 0):
                        continue
                else:
                    default = with1author(authors, default, i, ID)
                    if (default == 0):
                        continue

            elif len(authors) == 2:
                default = with2authors(authors, default, i, ID)
                if (default == 0):
                    continue

            elif len(authors) > 2:
                default = withmanyauthors(authors, default, i, ID)
                if (default == 0):
                    continue

            print(default, "OK")
            print("---------------\\/---------------")
        else:
            print("---------------Uncheckable", ID, "manual check---------------")
            print("---------------\\/---------------")
except Exception as e:
    print(e ,"faltando no ID:", ID)
    exit()

print("Total de warnings: ", warning, "*")
print("* Nem todos os warnings são necessariamente erros, ainda não encontramos uma boa forma de verificar nomes separados por - e nomes com de, da, do...")
