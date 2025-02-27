from flask import Flask, render_template, request
from whoosh.index import open_dir
from whoosh.qparser import QueryParser

app = Flask(__name__)
ix = open_dir("index")

@app.route("/", methods=["GET", "POST"])
def search():
    results = []
    query_str = ""
    
    if request.method == "POST":
        query_str = request.form.get("query")
        with ix.searcher() as searcher:
            parser = QueryParser("content", ix.schema)
            query = parser.parse(query_str)
            results = searcher.search(query, limit=10)
    
    return render_template("index.html", results=results, query=query_str)

if __name__ == "__main__":
    app.run(debug=True)
