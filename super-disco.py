import streamlit as st
import os
import random

# Path to the assets folder
assets_folder = "/home/snuffim/Desktop/super-disco/assets/Terra/"

def list_files(folder):
    """
    Recursively list all files in the given folder.
    """
    files_list = []
    for root, dirs, files in os.walk(folder):
        for file in files:
            files_list.append(os.path.join(root, file))
    return files_list

def choose_random_image(folder):
    """
    Choose one random image from the given folder and its subfolders.
    """
    image_files = list_files(folder)
    if image_files:
        return random.choice(image_files)
    else:
        return None

def main():
    # Path to the folder containing images
    folder_path = "/home/snuffim/Desktop/super-disco/assets/Avatar"

    # Create a row layout to display image and input box side by side
    col1, col2 = st.columns([3, 1])  # Adjust the ratio as needed

    # Add input box at the right side
    with col2:
        st.write("Input Box")
        user_input = st.text_input("Enter something")

        # Add button to randomize
        if st.button("Randomize!"):
            # Handle randomization here
            pass

    # Add a separator
    st.markdown('<hr>', unsafe_allow_html=True)

    # Add a small text
    st.write("This customer may like to buy:")

    # Create a container with additional spaces around it
    container = st.container()
    container.text("")  # Add some space above the container

    # Display random image only if the input box is not empty
    if user_input:
        # Choose a random image
        random_image = choose_random_image(folder_path)
        # Display random image
        col1.image(random_image, width=300)

    # Get list of all files in assets folder and its subfolders
    all_files = list_files(assets_folder)

    # Filter image files
    image_files = [file for file in all_files if file.endswith(('.png', '.jpg', '.jpeg'))]

    # Display images in a grid
    num_columns = 5  # Number of columns in the grid
    col1, col2, col3, col4, col5 = container.columns(num_columns)
    cols = [col1, col2, col3, col4, col5]
    
    for i, image_file in enumerate(image_files):
        with cols[i % num_columns]:
            st.image(image_file, width=128)

    container.text("")  # Add some space below the container

if __name__ == "__main__":
    main()
