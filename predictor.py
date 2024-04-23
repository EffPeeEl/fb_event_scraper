from sklearn.preprocessing import LabelEncoder
import numpy as np
import pandas as pd
import tensorflow as tf
from sklearn.model_selection import train_test_split
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
from  tensorflow.keras.models import load_model


def predict(model_path = "cat_pred/title_prediction_model.h5", input_path = "C:\\Users\\mgf-l\\Desktop\\structured_data.xlsx"):

    # Load the model
    print("Loading model...")
    model = load_model(model_path)
    print("Model loaded successfully")

    print("Loading data...")
    df = pd.read_excel(input_path)
    df = df.dropna(subset=['category', 'title'])
    df = df[['category', 'title']]

    X = df['title']   
    y = df['category']  


    train_X, test_X, train_y, test_y = train_test_split(X, y, test_size=0.2, random_state=42) 

    train_dataset = tf.data.Dataset.from_tensor_slices((train_X, train_y))
    test_dataset = tf.data.Dataset.from_tensor_slices((test_X, test_y))
    train_dataset


    print("Tokenizing and padding sequences...")
    tokenizer = Tokenizer(num_words=10000, oov_token="<OOV>")
    tokenizer.fit_on_texts(train_X)  # Fit only to training data

    train_sequences = tokenizer.texts_to_sequences(train_X)
    test_sequences = tokenizer.texts_to_sequences(test_X)


    max_length = max(len(x) for x in train_sequences)  
    train_padded = pad_sequences(train_sequences, maxlen=max_length, padding='post')
    test_padded = pad_sequences(test_sequences, maxlen=max_length, padding='post')

    print("Encoding labels...")
    encoder = LabelEncoder()
    encoder.fit(train_y)  # Fit encoder on the training labels



    train_labels = encoder.transform(train_y)
    test_labels = encoder.transform(test_y)


    train_labels_one_hot = tf.keras.utils.to_categorical(train_labels)
    test_labels_one_hot = tf.keras.utils.to_categorical(test_labels)


    print("Evaluating model...")
    loss, accuracy = model.evaluate(test_padded, test_labels_one_hot)
    print(f"Test accuracy: {accuracy}")

    print("Predicting categories...")
    predictions = model.predict(test_padded)
    predicted_categories = encoder.inverse_transform([np.argmax(p) for p in predictions])

    print("Saving results...")
    scrape_df = pd.read_excel("C:\\Users\\mgf-l\\Desktop\\structured_data.xlsx", sheet_name="scraped_raw")

    scrape_titles = scrape_df['title']

    scrape_sequences = tokenizer.texts_to_sequences(scrape_titles)
    scrape_padded = pad_sequences(scrape_sequences, maxlen=max_length, padding='post')

    scrape_predictions = model.predict(scrape_padded)
    scrape_predicted_categories = encoder.inverse_transform([np.argmax(p) for p in scrape_predictions])


    print("Saving results...")
    scrape_df['Predicted Category'] = scrape_predicted_categories

    scrape_df.to_excel("C:\\Users\\mgf-l\\Desktop\\title_prediction_output.xlsx", sheet_name="scraped_results", index=False)
