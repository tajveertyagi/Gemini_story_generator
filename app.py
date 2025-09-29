import streamlit as st
from PIL import Image
from story_generation import generate_story_from_images, narrate_story

st.title("AI Story Generator from Images")
st.markdown("Upload 1 to 10 images, choose a style, and let AI write and narrate the story!")

with st.sidebar:
    st.header("Controls")

    # Sidebar option to upload the images
    uploaded_files = st.file_uploader(
        "Upload the images...",
        type=["png", "jpg", "jpeg","webp"],
        accept_multiple_files=True,
        key="image_uploader"
    )

    # Select story style
    story_style = st.selectbox(
        "Choose a story style",
        ("Comedy", "Thriller", "Fairy Tale", "Sci-Fi", "Mystery", "Adventure", "Morale")
    )

    generate_button = st.button("Generate Story and Narration", type="primary")

# Main logic
if generate_button:
    if not uploaded_files:
        st.warning("Please upload at least one image.")
    elif len(uploaded_files) > 10:
        st.warning("Please upload a maximum of 10 images.")
    else:
        with st.spinner("The AI is writing and narrating your story... This may take a few moments."):
            try:
                # Open images
                pil_images = [Image.open(uploaded_file) for uploaded_file in uploaded_files]

                # Display uploaded images
                st.subheader("Your Visual Inspiration:")
                image_columns = st.columns(min(len(pil_images), 10))  # Avoid too many columns

                for i, image in enumerate(pil_images):
                    with image_columns[i]:
                        st.image(image, use_column_width=True)

                # Generate story
                generated_story = generate_story_from_images(pil_images, story_style)

                # Check for common error indicators in the response
                if any(err in generated_story for err in ["Error", "failed", "API key"]):
                    st.error(f"Story generation failed: {generated_story}")
                else:
                    st.subheader(f"Your {story_style} Story:")
                    st.success(generated_story)

                    # Narrate the story
                    st.subheader("Listen to Your Story:")
                    audio_file = narrate_story(generated_story)
                    if audio_file:
                        st.audio(audio_file, format="audio/mp3")
                    else:
                        st.warning("Audio narration could not be generated.")

            except Exception as e:
                st.error(f"An application error occurred: {e}")