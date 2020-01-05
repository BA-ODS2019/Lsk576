import json
import os
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
import nltk
from nltk.corpus import stopwords as sw
nltk.download('stopwords')

# Importing my Data-set
directory_name = "theguardian/collection/"

terms = ['Politics, Boris Johnson, Donald Trump']

ids = list()
texts = list()
for filename in os.listdir(directory_name):
    if filename.endswith(".json"):
        with open(directory_name + filename) as json_file:
            data = json.load(json_file)
            for article in data:
                id = article['id']
                fields = article['fields']
                text = fields['bodyText'] if fields['bodyText'] else ""
                ids.append(id)
                texts.append(text)

print("Number of ids: %d" % len(ids))
print("Number of texts: %d" % len(texts))



# Train and apply the model

# Make my bag of words, with minimal difference and english stop-words. 
model_vect = CountVectorizer(min_df = 1, stop_words=sw.words('english'), token_pattern=r'[a-zA-Z\-][a-zA-Z\-]{2,}')
# Training the bag of words
data_vect = model_vect.fit_transform(texts)

# Initiating my inverse frequency algorithm
model_tfidf = TfidfTransformer()
# Applying my inverse frequency to my data matrix
data_tfidf = model_tfidf.fit_transform(data_vect)

print('Shape: (%i, %i)' % data_vect.shape)

# Making a query template, and joining them with my search terms
query = " ".join(terms)

# Transforming my data matrix with my query
query_vect_counts = model_vect.transform([query])
# Applying TFIDF to my query data matrix. 
query_vect = model_tfidf.transform(query_vect_counts)

# Importing my LDA 
from sklearn.decomposition import LatentDirichletAllocation
# Applying my LDA to deliver an explicit representation of my data matrix, 
# suitable for word cloud analysis
model_lda = LatentDirichletAllocation(n_components=4, random_state=0)
#Fitting my LDA With my search query. 
data_lda = model_lda.fit_transform(query_vect)

np.shape(data_lda)
#Importing wordcloud and motplotlib to create a wordcloud
from wordcloud import WordCloud
import matplotlib.pyplot as plt

#Looping over my topic encoded data set and sorting by the 10 most popular words
#Printing out the top_words and also printing my wordcloud with 7 words in the graph
for i, term_weights in enumerate(model_lda.components_):
    top_idxs = (-term_weights).argsort()[:10]
    print(top_idxs)
    top_words = [model_vect.get_feature_names()[idx] for idx in top_idxs]
    word_freqs = dict(zip(top_words, term_weights[top_idxs]))
    print("Topic %d: %s" % (i, ", ".join(top_words)))
    wc = WordCloud(background_color="white",width=600,height=600, max_words=7).generate_from_frequencies(word_freqs)
    plt.subplot(2, 2, i+1)
    plt.imshow(wc)