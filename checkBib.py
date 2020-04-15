import bibtexparser, sys, re, codecs, unicodedata
from bibtexparser.customization import homogenize_latex_encoding
warning = 0

def check_if_string_in_file(file_name, string_to_search):
	with open(file_name, 'r') as read_obj:
		i = 0
		for line in read_obj:
			i += 1
			if string_to_search in line:
				return i
	return 0

def erroID(i, ID, default):
    print("\n---------------/\\---------------")
    print("Padrão incorreto no campo ID da referencia:", i, "(", ID,
            ");\nVerifique o(s) nome(s) do(s) autor(es), um possível padrão é:")
    print(default)
    print("---------------\\/---------------")

def erroAno(i, ID, default):
    print("\n---------------/\\---------------")
    print("Padrão incorreto no campo ID da referencia:", i, "(", ID,
            ");\nVerifique ano da publicação, um possível padrão é:")
    print(default)
    print("---------------\\/---------------")

def callWarn(i, ID, default):
    global warning
    warning += 1
    ano = re.findall(r'\d+', ID)
    if ano == [] or str(ano[0]) not in default:
        erroAno(i, ID, default)
    else:
        erroID(i, ID, default)

def with1author(authors, default, i, ID):
    author = authors[0].split(',')
    if(len(author) == 1):
        author = authors[0].split(' ')
        default = author[-1]+year
        if not ID.startswith(default):
            callWarn(i, ID, default)
            return 0

    else:
        author = author[0].split(' ')
        default = author[-1]+year
        if len(author) > 1:
            if author[0]+author[1] in ID:
                return default
        if not ID.startswith(default):
            callWarn(i, ID, default)
            return 0

    return default

def with2authors(authors, default, i, ID):
    author1 = authors[0].split(',')
    author2 = authors[1].split(',')
    if(len(author1) == 1 and len(author2) == 1):
        if len(author1) > 1:
            authors[0] = author1[0]
        if len(author2) > 1:
            authors[1] = author2[0]
        author1 = authors[0].split(' ')
        author2 = authors[1].split(' ')
        default = author1[-1]+'&'+author2[-1]+year
        if not ID.startswith(default):
            callWarn(i, ID, default)
            return 0
    else:
        author1 = author1[0].split(' ')
        author2 = author2[0].split(' ')
        default = author1[-1]+'&'+author2[-1]+year
        if len(author1) > 1:
            if author1[0]+author1[1] in ID:
                return default
        if len(author2) > 1:
            if author2[0]+author2[1] in ID:
                return default
        if not ID.startswith(default):
            callWarn(i, ID, default)
            return 0

    return default

def withmanyauthors(authors, default, i, ID):
    author = authors[0].split(',')
    if(len(author) == 1):
        author = authors[0].split(' ')
        default = author[-1]+'+'+year

        if not ID.startswith(default):
            callWarn(i, ID, default)
            return 0

    else:
        author = author[0].split(' ')
        default = author[-1]+'+'+year
        if len(author) > 1:
            if author[0]+author[1] in ID:
                return default
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
    print("invalid utf-8 next to the line", str(i+1))
    print(e)
    exit()

try:
    for i in range(0, len(bib_database.entries)):
        ID = bib_database.entries[i]['ID']
        default = ''

        unCheck = ['booklet', 'manual', 'proceedings', 'misc']

        if bib_database.entries[i]['ENTRYTYPE'] not in unCheck:
            if 'author' not in bib_database.entries[i]:
                checks = bib_database.entries[i]['editor']
            else:
                checks = bib_database.entries[i]['author']

            if '\"' in checks:
                print("\n---------------/\\---------------")
                print("---------------Uncheckable", ID, ", umlaut encontrado, realize uma checagem manual---------------")
                print("---------------\\/---------------")
                continue

            title = bib_database.entries[i]['title']
            if '{' in title and '}' in title:
                print("\n---------------", ID, ", contem chaves duplas ou em excesso no titulo, linha:", check_if_string_in_file(sys.argv[1], title) , ", verifique a necessassidade delas---------------")
                print("Titulo:", title, end="\n\n")

            for rep in ['\\v', '\\c ', '\\c', '\\`', '\\', '\'', '{', '}', '~', '^']:
                checks = checks.replace(rep, '')

            checks = checks.replace('\n', ' ')
            if '-' in checks and '-' not in ID:
                checks = checks.replace('-', '')

            checks = unicodedata.normalize('NFD', checks).encode('ascii', 'ignore').decode("utf-8")
            authors = checks.split(' and ')
            year = str(int(bib_database.entries[i]['year']))

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

        else:
            print("\n---------------/\\---------------")
            print("---------------Uncheckable", ID, ", tipo de entrada pode não ser padronizada, realize uma checagem manual---------------")
            print("---------------\\/---------------")
except Exception as e:
    print(e ,"faltando no ID:", ID)
    exit()

print("Total de warnings: ", warning, "*")
print("* Nem todos os warnings são necessariamente erros, ainda não encontramos uma boa forma de verificar nomes separados por - e nomes com de, da, do...")
