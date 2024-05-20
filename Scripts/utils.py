from lxml import etree
import numpy as np
def extract_text(element):
    text = ''
    if element.text:
        text += element.text.strip() + ' '
    for child in element:
        text += extract_text(child)
        if child.tail:
            text += child.tail.strip() + ' '
    return text


def look_for_links(element):
    list = []
    if element.tag.endswith('ptr'):
        if element.attrib.get('target','default')[0:4] == 'http':
            list.append(element.attrib['target'])
    for child in element:

        link = look_for_links(child)
        for l in link:
            list.append(l)
    return list


def count_figure(file_path):
    tree = etree.parse(file_path)

    root = tree.getroot()
    nb_figure = 0

    text = extract_text(root)
    word = ""
    next_word = ""

    # Iterate on the whole text to find the word 'figure' or 'fig' and capture the maximum number behind
    for i, char in enumerate(text):

        # current word
        if (not char.isspace() and char not in '.;,_\n()\""'):
            word += char
        else:
            # find the number of space to pass
            s = 1
            for space in text[i + 1:]:
                if space.isspace():
                    s += 1
                else:
                    break

            # if the word is good, look for the next word behind
            if word.lower() in ('fig', 'figure'):
                for char2 in text[i + s:]:

                    # check if the word behind is ended and if not check if it's a digit
                    if (not char2.isspace() and char2 not in '.;,\n()\""'):
                        if char2.isdigit():
                            next_word += char2
                        else:
                            break
                    else:
                        # when next word is over, compare it to the current nb of figure known
                        if int(next_word) > nb_figure:
                            nb_figure = int(next_word)
                            break
                        else:
                            break
            word = ""
            next_word = ""

    # trying to do it with figures only but some specific cases cause problems
    # nb_figure = 0
    # for sections in root[2][0]:
    #    if sections.tag.endswith('figure'):
    #        #print(sections[0].text)
    #        if sections[0].text[0:3] == 'Fig':
    #            nb_figure+=1

    return nb_figure


def extract_arXiv_id(root):
    list_ID_arXiv = []
    #root[2][1] is the 'back' element of the XML tree
    for div in root[2][1]:
        if div.get('type') == "references":
            for ListBibli in div:
                if ListBibli.tag[29:] == R'listBibl':
                    for bibli in ListBibli:
                        for child in bibli:
                            if child.tag[29:] == R'monogr' or child.tag[29:] == R'analytic':
                                for element in child:
                                    if element.tag[29:] == R'idno':
                                        if element.text[:5].lower() == R'arxiv' and (len(element.text) == 16 or len(element.text) == 15):
                                            list_ID_arXiv.append(element.text[6:])
                                        elif element.get('type') == "arXiv" and len(element.text) < 11:
                                            list_ID_arXiv.append(element.text)
                                        elif element.get('type') == "DOI" and len(element.text) < 11:
                                            list_ID_arXiv.append(element.text[:7])

    return list_ID_arXiv


def text_to_ListSentences(text):
    list_sentences = []
    curr_sentence = ""
    i = 0
    while len(text) != i:

        if text[i] == '.' or text[i] == '...':
            curr_sentence = curr_sentence + text[i]
            list_sentences.append(curr_sentence)
            curr_sentence = ""
        elif text[i] != '\n':
            curr_sentence = curr_sentence + text[i]
        i += 1
    return list_sentences

def remove_stopwords(text):
# filter out words that are in the stopword list
# also lowercasing text entries
    STOPWORDS = ["a","a's","able","about","above","according","accordingly","across","actually","after","afterwards","again","against","ain't","all","allow","allows","almost","alone","along","already","also","although","always","am","among","amongst","an","and","another","any","anybody","anyhow","anyone","anything","anyway","anyways","anywhere","apart","appear","appreciate","appropriate","are","aren't","around","as","aside","ask","asking","associated","at","available","away","awfully","b","be","became","because","become","becomes","becoming","been","before","beforehand","behind","being","believe","below","beside","besides","best","better","between","beyond","both","brief","but","by","c","c'mon","c's","came","can","can't","cannot","cant","cause","causes","certain","certainly","changes","clearly","co","com","come","comes","concerning","consequently","consider","considering","contain","containing","contains","corresponding","could","couldn't","course","currently","d","definitely","described","despite","did","didn't","different","do","does","doesn't","doing","don't","done","down","downwards","during","e","each","edu","eg","eight","either","else","elsewhere","enough","entirely","especially","et","etc","even","ever","every","everybody","everyone","everything","everywhere","ex","exactly","example","except","f","far","few","fifth","first","five","followed","following","follows","for","former","formerly","forth","four","from","further","furthermore","g","get","gets","getting","given","gives","go","goes","going","gone","got","gotten","greetings","h","had","hadn't","happens","hardly","has","hasn't","have","haven't","having","he","he's","hello","help","hence","her","here","here's","hereafter","hereby","herein","hereupon","hers","herself","hi","him","himself","his","hither","hopefully","how","howbeit","however","i","i'd","i'll","i'm","i've","ie","if","ignored","immediate","in","inasmuch","inc","indeed","indicate","indicated","indicates","inner","insofar","instead","into","inward","is","isn't","it","it'd","it'll","it's","its","itself","j","just","k","keep","keeps","kept","know","known","knows","l","last","lately","later","latter","latterly","least","less","lest","let","let's","like","liked","likely","little","look","looking","looks","ltd","m","mainly","many","may","maybe","me","mean","meanwhile","merely","might","more","moreover","most","mostly","much","must","my","myself","n","name","namely","nd","near","nearly","necessary","need","needs","neither","never","nevertheless","new","next","nine","no","nobody","non","none","noone","nor","normally","not","nothing","novel","now","nowhere","o","obviously","of","off","often","oh","ok","okay","old","on","once","one","ones","only","onto","or","other","others","otherwise","ought","our","ours","ourselves","out","outside","over","overall","own","p","particular","particularly","per","perhaps","placed","please","plus","possible","presumably","probably","provides","q","que","quite","qv","r","rather","rd","re","really","reasonably","regarding","regardless","regards","relatively","respectively","right","s","said","same","saw","say","saying","says","second","secondly","see","seeing","seem","seemed","seeming","seems","seen","self","selves","sensible","sent","serious","seriously","seven","several","shall","she","should","shouldn't","since","six","so","some","somebody","somehow","someone","something","sometime","sometimes","somewhat","somewhere","soon","sorry","specified","specify","specifying","still","sub","such","sup","sure","t","t's","take","taken","tell","tends","th","than","thank","thanks","thanx","that","that's","thats","the","their","theirs","them","themselves","then","thence","there","there's","thereafter","thereby","therefore","therein","theres","thereupon","these","they","they'd","they'll","they're","they've","think","third","this","thorough","thoroughly","those","though","three","through","throughout","thru","thus","to","together","too","took","toward","towards","tried","tries","truly","try","trying","twice","two","u","un","under","unfortunately","unless","unlikely","until","unto","up","upon","us","use","used","useful","uses","using","usually","uucp","v","value","various","very","via","viz","vs","w","want","wants","was","wasn't","way","we","we'd","we'll","we're","we've","welcome","well","went","were","weren't","what","what's","whatever","when","whence","whenever","where","where's","whereafter","whereas","whereby","wherein","whereupon","wherever","whether","which","while","whither","who","who's","whoever","whole","whom","whose","why","will","willing","wish","with","within","without","won't","wonder","would","wouldn't","x","y","yes","yet","you","you'd","you'll","you're","you've","your","yours","yourself","yourselves","z","zero"]

    text = [x.lower() for x in text.split() if x.lower() not in STOPWORDS]
# text is a collection of non-stopwords (in lowercase)
# now join the words with space separator and return them as a string
    return " ".join(text)


def cosine(u, v):
    return np.dot(u, v) / (np.linalg.norm(u) * np.linalg.norm(v))