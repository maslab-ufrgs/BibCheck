import bibtexparser, sys, re
from bibtexparser.customization import homogenize_latex_encoding

def erroAuthor(i, ID):
    print("Padrão incorreto no campo Author da referencia:", i, "(", ID,
            "), coloque o sobrenome antes do nome separando-os por virgula\n")

def erroID(i, ID):
    print("Padrão incorreto no campo ID da referencia:", i, "(", ID,
            "), coloque o sobrenome capitalizado e depois o ano:")

with open(sys.argv[1]) as bibtex_file:
    bib_database = bibtexparser.bparser.BibTexParser(common_strings=True, ignore_nonstandard_types=False, interpolate_strings=False).parse_file(bibtex_file)

for i in range(0, len(bib_database.entries)):
    ID = bib_database.entries[i]['ID']
    default = ''

    print("\n---------------/\\---------------")
    unCheck = ['booklet', 'manual', 'proceedings']

    if bib_database.entries[i]['ENTRYTYPE'] not in unCheck:
        if "author" not in bib_database.entries[i]:
            print("Uncheckable", ID, "manual check")
            print("---------------\\/---------------")
            continue
        if "year" not in bib_database.entries[i]:
            print("Uncheckable", ID, "manual check")
            print("---------------\\/---------------")
            continue

        checks = bib_database.entries[i]['author']
        for rep in ['\\', '\'', '\"', '{', '}', '~', '^']:
            checks = checks.replace(rep, '')
        checks = checks.replace('\n', ' ')

        authors = checks.split(' and ')
        year = bib_database.entries[i]['year']
        if len(authors) == 1:
            author = authors[0].split(',')

            if(len(author) == 1):
                print("Não foi possível separar por virgula o sobrenome do autor, vamos tentar checar se está ok com o último nome")
                author = authors[0].split(' ')
                default = author[-1].capitalize()+year

                if not ID.startswith(default):
                    erroAuthor(i, ID)
                    print(default)
                    print("---------------\\/---------------")
                    continue

            else:
                default = author[0].capitalize()+year
                if not ID.startswith(default):
                    erroID(i, ID)
                    print(default)
                    print("---------------\\/---------------")
                    continue

        elif len(authors) == 2:
            author1 = authors[0].split(',')
            author2 = authors[1].split(',')
            if(len(author1) == 1 or len(author2) == 1):
                print("Não foi possível separar por virgula o sobrenome do autor, vamos tentar checar se está ok com o último nome")
                author1 = authors[0].split(' ')
                author2 = authors[1].split(' ')
                default = author1[-1].capitalize()+'&'+author2[-1].capitalize()+year

                if not ID.startswith(default):
                    erroAuthor(i, ID)
                    print(default)
                    print("---------------\\/---------------")
                    continue

            else:
                default = author1[0].capitalize()+'&'+author2[0].capitalize()+year
                if not ID.startswith(default):
                    erroID(i, ID)
                    print(default)
                    print("---------------\\/---------------")
                    continue

        elif len(authors) > 2:

            author = authors[0].split(',')
            if(len(author) == 1):
                print("Não foi possível separar por virgula o sobrenome do autor, vamos tentar checar se está ok com o último nome")
                author = authors[0].split(' ')
                default = author[-1].capitalize()+'+'+year

                if not ID.startswith(default):
                    erroAuthor(i, ID)
                    print(default)
                    print("---------------\\/---------------")
                    continue

            else:
                default = author[0].capitalize()+'+'+year
                if not ID.startswith(default):
                    erroID(i, ID)
                    print(default)
                    print("---------------\\/---------------")
                    continue

        print(default, "OK")
        print("---------------\\/---------------")
    else:
        print("Uncheckable", ID, "manual check")
        print("---------------\\/---------------")
