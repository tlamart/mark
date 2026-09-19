import sys
import requests

def main():
    title = input("title: ")
    data = {
        "title": title,
        "author": "test",
        "current_page": 0,
        "total_page": 100,
        "id": 42
    }
    r = requests.post("http://127.0.0.1:8000/books", json=data)
    print(r.text)


if __name__ == "__main__":
    main()