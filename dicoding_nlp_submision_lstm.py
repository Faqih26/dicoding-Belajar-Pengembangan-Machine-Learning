# -*- coding: utf-8 -*-
"""dicoding_nlp_submision_lstm.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1rEAuuWSKhpRtn8QOulMXy-dH9GYNFaYv

[Dataset](https://www.kaggle.com/datasets/uciml/news-aggregator-dataset?resource=download)
"""

import pandas as pd
df = pd.read_csv('/content/uci-news-aggregator.csv')
df

df = df[['TITLE','CATEGORY']]
df.head()

df.CATEGORY.value_counts()

# Mapping dictionary
category_mapping = {'b': 'business', 't': 'science and technology', 'e': 'entertainment', 'm': 'health'}

# Function to apply the mapping
df['CATEGORY'] = df['CATEGORY'].apply(lambda x: category_mapping[x] if x in category_mapping else x)

# Filter data for specific categories
desired_categories = ['business', 'science and technology', 'entertainment', 'health']
filtered_df = df[df['CATEGORY'].isin(desired_categories)]

df.dropna()

df = df.rename(columns={'CATEGORY': 'category','TITLE':'title'})
df.head()

"""klo pake nltk pas running semuanya ram ga cukup"""

#import nltk
#from nltk.tokenize import RegexpTokenizer

# Download the NLTK stopwords resource
#nltk.download('stopwords')
#nltk.download('punkt')

# Set of English stopwords
#stop_words = set(nltk.corpus.stopwords.words('english'))

# Your DataFrame (replace df.title with the actual column)
#df['title'] = df['title'].astype(str)

# Tokenize the titles
#tokenizer = RegexpTokenizer(r"\w+")
#df['new_words'] = df['title'].apply(lambda x: tokenizer.tokenize(x.lower()))

# Filter out stopwords
#df['filtered_title'] = df['new_words'].apply(lambda tokens: [w for w in tokens if not w in stop_words])

#df = df[['filtered_title','category']]
#df

#df = df.rename(columns={'category': 'category','filtered_title':'title'})
#df.head()

# One-hot encoding

category = pd.get_dummies(df.category)
df_baru = pd.concat([df, category], axis=1)
df_baru = df_baru.drop(columns='category')
df_baru

text = df_baru['title'].values
label = df_baru[['business', 'entertainment', 'health', 'science and technology']].values

from sklearn.model_selection import train_test_split
title_latih, title_test, label_latih, label_test = train_test_split(text, label, test_size=0.2)

from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences

tokenizer = Tokenizer(num_words=5000, oov_token='x')
tokenizer.fit_on_texts(title_latih)
tokenizer.fit_on_texts(title_test)

sekuens_latih = tokenizer.texts_to_sequences(title_latih)
sekuens_test = tokenizer.texts_to_sequences(title_test)

padded_latih = pad_sequences(sekuens_latih)
padded_test = pad_sequences(sekuens_test)

import tensorflow as tf
model = tf.keras.Sequential([
    tf.keras.layers.Embedding(input_dim=5000, output_dim=16),
    tf.keras.layers.LSTM(64),
    tf.keras.layers.Dense(128, activation='relu'),
    tf.keras.layers.Dense(64, activation='relu'),
    tf.keras.layers.Dense(4, activation='softmax')
])
model.compile(loss='categorical_crossentropy',optimizer='adam',metrics=['accuracy'])

num_epochs = 10
history = model.fit(padded_latih, label_latih, epochs=num_epochs,
                    validation_data=(padded_test, label_test), verbose=2)

import matplotlib.pyplot as plt
plt.plot(history.history['accuracy'])
plt.plot(history.history['val_accuracy'])
plt.title('acc Model')
plt.ylabel('accuracy')
plt.xlabel('epoch')
plt.legend(['train', 'test'], loc='upper left')
plt.show()

plt.plot(history.history['loss'])
plt.plot(history.history['val_loss'])
plt.title('Loss Model')
plt.ylabel('loss')
plt.xlabel('epoch')
plt.legend(['train', 'test'], loc='upper left')
plt.show()

# Melihat akurasi pada data pelatihan
train_accuracy = history.history['accuracy']
print(f'Training Accuracy: {train_accuracy[-1]}')

# Melihat akurasi pada data validasi
val_accuracy = history.history['val_accuracy']
print(f'Validation Accuracy: {val_accuracy[-1]}')