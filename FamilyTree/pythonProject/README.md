Family Tree: A FastAPI based Python application

[//]: # (Setup Instructions)
git clone https://github.com/shravanikyasaram/family_tree.git
cd <project-folder>

[//]: # (Create a Virtual Environment and install the dependencies)
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

[//]: # (Run the application)
uvicorn main:app --reload
