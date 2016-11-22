def rectangle_area(w,h):
    if type(w) is not int or type(h) is not int:
    	raise TypeError()
    else:
    	return w*h

def strip_stopwords(phrase, stopwords):
    phrase = phrase.split()
    phrase = [w for w in phrase if w not in stopwords]
    phrase = ' '.join(phrase)
    return phrase

