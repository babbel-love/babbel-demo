with open("streamlit_babbel_app.py", "r") as f:
    lines = f.readlines()

with open("streamlit_babbel_app.py", "w") as f:
    for line in lines:
        f.write(line.replace("from .", "from "))
