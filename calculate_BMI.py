from io import BytesIO, StringIO
from typing import Union
from PIL import Image
import pandas as pd
import streamlit as st
import numpy as np


STYLE = """
<style>
img {
    max-width: 75%;
}
</style>
"""

def get_bmi(img_content):
    """
    Takes an image performs image processing using PIL to get BMI
    """
    img = Image.open(img_content).convert('LA')
    thresh = 250
    fn = lambda x : 0 if x > thresh else 255
    r = img.convert('L').point(fn, mode='1')
    current_width, current_height = r.size
    BMI_list = []

    for i in range(0,8):
        new_width = round(current_width - (current_width * 0.1))
        new_height = round(current_height - (current_height * 0.1))
        r = r.resize((new_width, new_height), Image.ANTIALIAS)
        r.save('resize_result/'+str(i)+'.png')
        current_width = new_width
        current_height = new_height
        # print(current_width,current_height)
        pix_val = list(r.getdata())

        #Calculating the Area 
        area = 0 
        for val in pix_val:
            if val == 255:
                area = area + 1

        # print(f"The area of the silhoutte is {area}")

        #Calculating the Height of the person
        iar = np.asarray(r)
        obj_h = 0 
        for x in iar:
            for y in x:
                if y:
                    obj_h = obj_h + 1
                    break
        H = obj_h
        #Calculating the BMI
        pie = 22/7
        pie = round(pie,4)

        BMI_img = ((pie * (area**2))/(8*(H**3)) - 4.1219)/0.1963

        BMI_list.append(BMI_img)

    return round(np.mean(BMI_list),2)



def main():
    # st.info(__doc__)
    st.info("What's Your BMI")
    st.markdown(STYLE, unsafe_allow_html=True)
 
    file = st.file_uploader("Upload file", type=["png", "jpg"])
    show_file = st.empty()
 
    if not file:
        show_file.info("Please upload a file of type: " + ", ".join(["png", "jpg"]))
        return
 
    content = file.getvalue()
 
    if isinstance(file, BytesIO):
        show_file.image(file)
    else:
        data = pd.read_csv(file)
        st.dataframe(data.head(10))

    bmi = get_bmi(file)

    st.info(f'Looks like BMI is near to {bmi}')
    file.close()

st.set_option('deprecation.showfileUploaderEncoding', False)
main()