import nltk
nltk.download()
from nltk.book import *

# fdist1 = FreqDist(text1)
# vocabulary1 = fdist1.keys()
# vocabulary1 = vocabulary1[: 50]
#
# a = fdist1['whale']
# print a

from nltk.corpus import brown , inaugural , udhr
cfd = nltk.ConditionalFreqDist(
    (genre , word)
    for genre in brown.categories()
    for word in brown.words(categories= genre)
)

genre_word = [(genre , word)
    for genre in ['news' , 'romance']
    for word in brown.words(categories=genre)
]
a = len(genre_word)
print a

cdf1 = nltk.ConditionalFreqDist(
    (target , fileid[: 4])
    for fileid in inaugural.fileids()
    for w in inaugural.words(fileid)
    for target in ['america' , 'citizen']
    if w.lower().startswith(target)
)

languages = ['Chickasaw' , 'English' , 'German_Deutsch' ]
cdf2 = nltk.ConditionalFreqDist(
    (lang , len(word))
    for lang in languages
    for word in udhr.words(lang + '-Latin1')
)

cdf2.tabulate(conditions=['English' , 'German_Deutsch'] , samples = range(10) , cumulative=True)