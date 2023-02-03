import tensorflow as tf
import numpy as np
import streamlit as st
import cv2


physical_devices = tf.config.list_physical_devices('GPU')
try:
  tf.config.experimental.set_memory_growth(physical_devices[0], True)
except:
  # Invalid device or cannot modify virtual devices once initialized.
  pass
model = tf.keras.models.load_model("./model.h5")
with open("./descriptions/info.md") as f:
  st.markdown(f.read())
im = st.file_uploader("Choose a file",type="jpg")

diagnose_dict = {0:"akiec",
                 1:"bcc",
                 2:"bkl",
                 3:"df",
                 4:"mel",
                 5:"nv",
                 6:"vasc"}

if im is not None:
    im2 = np.asarray(bytearray(im.read()), dtype=np.uint8)
    im2 = cv2.resize(cv2.imdecode(im2,1),(256,256))
    result = np.argmax(model.predict(tf.expand_dims(im2,axis=0)))
    with open(f"./descriptions/{diagnose_dict[result]}.md") as f:
      description = f.read()
    st.image(im)
    st.write(f"Your result is:")
    st.markdown(description)
    del im