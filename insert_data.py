from pymongo import MongoClient

# 1. Connect to MongoDB
client = MongoClient("mongodb://localhost:27017/")

# 2. Select Database & Collection
db = client["gi_marketplace"]
collection = db["artisans"]

# 3. Karnataka GI-tag Artisan Data
artisans_data = [
    {
        "name": "Ilkal Saree Weavers",
        "location": "Bagalkot, Karnataka",
        "gi_tag": "Ilkal Saree",
        "category": "Handloom",
        "description": "Traditional Ilkal sarees woven using cotton and silk with the unique 'tope teni' technique.",
        "image": "https://upload.wikimedia.org/wikipedia/commons/8/8d/Ilkal_Saree.jpg"
    },
    {
        "name": "Channapatna Toy Makers",
        "location": "Channapatna, Karnataka",
        "gi_tag": "Channapatna Toys",
        "category": "Handicraft",
        "description": "Handcrafted wooden toys and dolls, also called 'Gombegala Ooru'.",
        "image": "https://upload.wikimedia.org/wikipedia/commons/6/61/Channapatna_toys.jpg"
    },
    {
        "name": "Mysore Silk Weavers",
        "location": "Mysuru, Karnataka",
        "gi_tag": "Mysore Silk",
        "category": "Textile",
        "description": "Premium silk sarees woven with pure mulberry silk and gold zari.",
        "image": "https://upload.wikimedia.org/wikipedia/commons/f/f0/Mysore_Silk.jpg"
    },
    {
        "name": "Bidriware Artisans",
        "location": "Bidar, Karnataka",
        "gi_tag": "Bidriware",
        "category": "Metal Craft",
        "description": "Decorative metal handicrafts made with blackened alloy and silver inlay.",
        "image": "https://upload.wikimedia.org/wikipedia/commons/5/52/Bidriware.jpg"
    },
    {
        "name": "Mysore Rosewood Inlay",
        "location": "Mysuru, Karnataka",
        "gi_tag": "Mysore Rosewood Inlay",
        "category": "Wood Craft",
        "description": "Intricate wooden inlay work depicting mythological and floral designs.",
        "image": "https://upload.wikimedia.org/wikipedia/commons/3/3e/Rosewood_inlay_Mysore.jpg"
    }
]

# 4. Insert Data into MongoDB
collection.insert_many(artisans_data)

print("✅ Data inserted successfully into gi_marketplace.artisans")
