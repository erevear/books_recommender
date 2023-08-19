import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)

import tensorflow as tf
import numpy as np
import streamlit as st
from PIL import Image
import requests
from io import BytesIO

st.set_option('deprecation.showfileUploaderEncoding', False)
st.title("Book Recommender")
st.text("Provide a user ID to get book recommendations")

@st.cache(allow_output_mutation=True)
def load_model():
  model = tf.saved_model.load('/app/models/')
  # tf.saved_model.load
  return model

with st.spinner('Loading Model Into Memory....'):
  model = load_model()



path = st.text_input('Enter a user ID for recommendations.. ','8842281e1d1347389f2ab93d60773d4d')
if path is not None:
    content = requests.get(path).content

    st.write("Pulling recommendations :")
    with st.spinner('classifying.....'):
      # label =np.argmax(model.predict(decode_img(content)),axis=1)
      scores, titles = loaded(["42"])
      # st.write(classes[label[0]])    
    st.write("")
    # image = Image.open(BytesIO(content))
    # st.image(image, caption='Classifying Image', use_column_width=True)
    st.write(', '.join(titles))