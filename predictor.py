from sklearn.preprocessing import LabelEncoder
import numpy as np
import pandas as pd
import tensorflow as tf
from sklearn.model_selection import train_test_split
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
from  tensorflow.keras.models import load_model
import json
import pickle

def predict(model_path = "cat_pred/title_prediction_model.h5", input_path ="C:\\Users\\mgf-l\\Desktop\\structured_data.xlsx"):

    # Load the model
    print("Loading model...")
    model = load_model(model_path)
    print("Model loaded successfully")

    print("Loading data...")
    train_df = pd.read_excel(input_path)
    train_df = train_df.dropna(subset=['category', 'title'])

    X = train_df['title']   
    y = train_df['category']  



    train_X, test_X, train_y, test_y = train_test_split(X, y, test_size=0.2, random_state=42) 

    train_dataset = tf.data.Dataset.from_tensor_slices((train_X, train_y))
    test_dataset = tf.data.Dataset.from_tensor_slices((test_X, test_y))
    train_dataset


    print("Tokenizing and padding sequences...")
    tokenizer = Tokenizer(num_words=10000, oov_token="<OOV>")
    tokenizer.fit_on_texts(train_X)  # Fit only to training data



    df = pd.read_excel(input_path, sheet_name="scraped_raw")

  
    train_sequences = tokenizer.texts_to_sequences(df['title'])


    max_length = max(len(x) for x in train_sequences)  
    train_padded = pad_sequences(train_sequences, maxlen=max_length, padding='post')



    print("Encoding labels...")
    encoder = LabelEncoder()
    encoder.fit(train_y)  # Fit encoder on the training labels



    train_labels = encoder.transform(train_y)
    test_labels = encoder.transform(test_y)


    train_labels_one_hot = tf.keras.utils.to_categorical(train_labels)
    test_labels_one_hot = tf.keras.utils.to_categorical(test_labels)



    print("Predicting categories...")
    predictions = model.predict(train_padded)
    predicted_categories = encoder.inverse_transform([np.argmax(p) for p in predictions])

    print("Saving results...")

  
    scrape_titles = df['title']

    scrape_sequences = tokenizer.texts_to_sequences(scrape_titles)
    scrape_padded = pad_sequences(scrape_sequences, maxlen=max_length, padding='post')

    scrape_predictions = model.predict(scrape_padded)
    scrape_predicted_categories = encoder.inverse_transform([np.argmax(p) for p in scrape_predictions])


    print("Saving results...")
    df['category'] = scrape_predicted_categories

    df.to_excel("title_prediction_output.xlsx", sheet_name="scraped_results", index=False)


    df['date'] = df['date'].astype(str)
    df['time'] = df['time'].astype(str)
    df = df.astype(str)
    p = df.to_dict(orient='records')## HÄR ÄR DET NÅGOT LURT

    with open('events_with_cats.json', 'w', encoding="utf-16") as f: # meow
        json.dump(p, f, ensure_ascii=False, indent=4)


# from tensorflow.keras.preprocessing.text import Tokenizer
# from tensorflow.keras.preprocessing.sequence import pad_sequences
# from tensorflow.keras.models import load_model
# import pandas as pd
# import numpy as np
# import json

# def predict(model_path="cat_pred/title_prediction_model.h5", input_path="events.json",
#             categories = [
# "Fika"
# ,"Reception hours" 
# ,"Pub"
# ,"Other"
# ,"Gasque"
# ,"Brunch"
# ,"Sport"
# ,"Club"
# ,"Lunch"
# ,"Breakfast"
# ,"Restaurant"

# ]
# ):
    

#     # Load the model
#     print("Loading model...")
#     model = load_model(model_path)
#     print("Model loaded successfully")

#     # Load and prepare data
#     print("Loading data...")
#     df = pd.read_json(input_path, encoding="utf-16")
#     df = df.dropna(subset=['title'])  # Assuming 'title' needs to be non-null for predictions

#     titles = df['title']
#     print("Data loaded with {} entries".format(len(titles)))

#     # Tokenizing and padding sequences
#     print("Tokenizing and padding sequences...")
#     tokenizer = Tokenizer(num_words=10000, oov_token="<OOV>")
#     tokenizer.fit_on_texts(titles)  # Assuming we need to fit tokenizer to our prediction data

#     sequences = tokenizer.texts_to_sequences(titles)
#     max_length = max(len(x) for x in sequences)  # Determine max length of sequences
#     padded_sequences = pad_sequences(sequences, maxlen=max_length, padding='post')
    
#     # Predicting categories
#     print("Predicting categories...")
#     predictions = model.predict(padded_sequences)
#     predicted_categories = [np.argmax(p) for p in predictions]  # Placeholder for actual label decoding

#     with open('cat_pred\\encoder.pkl', 'rb') as file:
#         loaded_encoder = pickle.load(file)

#     scrape_predicted_categories = loaded_encoder.inverse_transform(predicted_categories)
    
#     # Saving results

#     print("Saving results...")
#     df['category'] = scrape_predicted_categories  # Adjust this if you have a way to convert indices back to labels
#     df = df.astype(str)


#     result_file_path = 'predictions.json'
#     with open(result_file_path, 'w', encoding='utf-16') as f:
#         json.dump(df.to_dict(orient='records'), f, ensure_ascii=False, indent=4)
    
#     print(f"Results saved to {result_file_path}")
