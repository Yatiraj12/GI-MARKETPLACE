from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from pymongo import MongoClient
from bson import ObjectId
from google import genai

app = Flask(__name__)
CORS(app)

# ---------- GEMINI CONFIG ----------
client = genai.Client(api_key="AIzaSyAKSEanriab4-BwM235Ow1EbFYbs1AhmZ4")

# ---------- MONGO CONFIG ----------
mongo_client = MongoClient("mongodb://localhost:27017/")
db = mongo_client["gi_marketplace"]
collection = db["artisans"]

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/artisans", methods=["GET"])
def get_artisans():
    artisans = list(collection.find())
    for artisan in artisans:
        artisan["_id"] = str(artisan["_id"])
    return jsonify(artisans)

@app.route("/ai-search", methods=["POST"])
def ai_search():
    user_query = request.json.get("query", "")

    # Call Gemini
    response = client.models.generate_content(
        model="gemini-2.0-flash",   # ✅ or "gemini-1.5-flash" depending on availability
        contents=f"Extract keywords from this query about GI products: {user_query}"
    )

    keywords_str = response.text.strip() if hasattr(response, "text") else ""
    keywords_str = keywords_str.replace("Keywords:", "").strip()
    keyword_list = [kw.strip() for kw in keywords_str.split(",") if kw.strip()]

    # MongoDB search
    query_conditions = []
    for kw in keyword_list:
        query_conditions.extend([
            {"name": {"$regex": kw, "$options": "i"}},
            {"gi_tag": {"$regex": kw, "$options": "i"}},
            {"category": {"$regex": kw, "$options": "i"}},
            {"location": {"$regex": kw, "$options": "i"}},
        ])

    mongo_query = {"$or": query_conditions} if query_conditions else {}
    results = list(collection.find(mongo_query))
    for artisan in results:
        artisan["_id"] = str(artisan["_id"])

    return jsonify({
        "query": user_query,
        "keywords": keyword_list,
        "results": results
    })

if __name__ == "__main__":
    app.run(debug=True)
