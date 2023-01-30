from essential_generators import DocumentGenerator
import requests
import json

TOKEN = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIzZGJlYmIzMy02YjgwLTQ4MjQtYTA0Ni1mYWVkNmFjZTk1YWEiLCJleHAiOjE2NzUwNzYwNjZ9.hPS4QOYSDaMfYXI05YPTN5-PTFN3gyykJw0OWve__ME"
headers = {
    "Authorization": "Bearer {}".format(TOKEN),
    "Content-Type": "application/json",
}
URL = "http://127.0.0.1:8000"


def generate_posts():
    post_template = {
        "title": "sentence",
        "content": "paragraph",
    }
    gen = DocumentGenerator()
    gen.set_template(post_template)
    documents = gen.documents(10)

    for doc in documents:
        req = requests.post(URL + "/posts/", data=json.dumps(doc), headers=headers)
        if req.status_code == 200:
            print("Create a post successfully.")
        else:
            req.raise_for_status()


generate_posts()
