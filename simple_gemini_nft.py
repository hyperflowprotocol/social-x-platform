#!/usr/bin/env python3
"""
Simple Gemini NFT Generator - Creates Naruto NFTs using Gemini AI
"""

import os
import json
import time
import requests

def generate_with_gemini(prompt, output_path):
    """Generate image using Gemini API directly"""
    
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        print("❌ GEMINI_API_KEY not found")
        return False
        
    try:
        # Using Gemini image generation endpoint
        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash-preview-image-generation:generateContent"
        
        headers = {
            "Content-Type": "application/json",
            "x-goog-api-key": api_key
        }
        
        data = {
            "contents": [{
                "parts": [{
                    "text": prompt
                }]
            }],
            "generationConfig": {
                "response_modalities": ["TEXT", "IMAGE"]
            }
        }
        
        print(f"Generating image with prompt: {prompt[:100]}...")
        response = requests.post(url, headers=headers, json=data, timeout=30)
        
        if response.status_code == 200:
            result = response.json()
            
            # Extract image data from response
            if 'candidates' in result and result['candidates']:
                candidate = result['candidates'][0]
                if 'content' in candidate and 'parts' in candidate['content']:
                    for part in candidate['content']['parts']:
                        if 'inlineData' in part and 'data' in part['inlineData']:
                            # Decode base64 image data
                            import base64
                            image_data = base64.b64decode(part['inlineData']['data'])
                            
                            with open(output_path, 'wb') as f:
                                f.write(image_data)
                            print(f"✅ Saved image to: {output_path}")
                            return True
        else:
            print(f"❌ API Error: {response.status_code} - {response.text}")
            
    except Exception as e:
        print(f"❌ Error generating image: {e}")
    
    return False

def create_naruto_collection():
    """Create Naruto NFT collection using Gemini"""
    
    collection_name = f"gemini_naruto_{int(time.time())}"
    images_dir = os.path.join(collection_name, "images")
    metadata_dir = os.path.join(collection_name, "metadata")
    
    os.makedirs(images_dir, exist_ok=True)
    os.makedirs(metadata_dir, exist_ok=True)
    
    # Character prompts for variety
    characters = [
        {
            "name": "Naruto Uzumaki",
            "prompt": "Professional anime artwork of Naruto Uzumaki with spiky blonde hair, blue eyes, orange ninja jumpsuit, whisker marks on cheeks, confident smile, Leaf Village headband, dynamic pose, high-quality digital art, vibrant colors, official anime style"
        },
        {
            "name": "Sasuke Uchiha", 
            "prompt": "Professional anime artwork of Sasuke Uchiha with black hair, dark eyes with red Sharingan pattern, dark blue ninja outfit, serious expression, calm confident pose, high-quality digital art, official anime style"
        },
        {
            "name": "Itachi Uchiha",
            "prompt": "Professional anime artwork of Itachi Uchiha with long black hair, red Sharingan eyes, black Akatsuki cloak with red clouds, serious calm expression, mysterious aura, high-quality digital art, official anime style"
        },
        {
            "name": "Kakashi Hatake",
            "prompt": "Professional anime artwork of Kakashi Hatake with silver spiky hair, one visible eye with Sharingan, ninja mask covering lower face, dark blue ninja outfit, relaxed pose, high-quality digital art, official anime style"
        },
        {
            "name": "Sakura Haruno",
            "prompt": "Professional anime artwork of Sakura Haruno with pink hair, green eyes, red ninja outfit, confident medical ninja pose, determined expression, high-quality digital art, official anime style"
        }
    ]
    
    successful = 0
    
    for i, character in enumerate(characters * 4, 1):  # Repeat for 20 NFTs
        if i > 20:
            break
            
        image_path = os.path.join(images_dir, f"{i}.png")
        
        if generate_with_gemini(character["prompt"], image_path):
            # Create metadata
            metadata = {
                "name": f"Naruto NFT #{i}",
                "description": f"Professional AI-generated {character['name']} artwork",
                "image": f"images/{i}.png",
                "attributes": [
                    {"trait_type": "Character", "value": character["name"]},
                    {"trait_type": "Generation", "value": "Gemini AI"},
                    {"trait_type": "Style", "value": "Professional Anime"},
                    {"trait_type": "Quality", "value": "High Resolution"}
                ]
            }
            
            with open(os.path.join(metadata_dir, f"{i}.json"), 'w') as f:
                json.dump(metadata, f, indent=2)
                
            successful += 1
            print(f"✅ Created NFT #{i}: {character['name']}")
        else:
            print(f"❌ Failed to create NFT #{i}")
        
        # Small delay to avoid rate limiting
        time.sleep(2)
    
    # Collection metadata
    collection_data = {
        "name": "Professional Naruto NFT Collection",
        "description": "High-quality Naruto NFT collection generated with Google Gemini AI",
        "total": 20,
        "successful": successful,
        "generator": "Google Gemini AI"
    }
    
    with open(os.path.join(collection_name, "collection.json"), 'w') as f:
        json.dump(collection_data, f, indent=2)
    
    print(f"🎨 Collection complete: {successful}/20 NFTs generated")
    print(f"📁 Saved to: {collection_name}")
    return collection_name

if __name__ == "__main__":
    print("🎨 Starting Gemini Naruto NFT Generation")
    print("=" * 50)
    
    collection = create_naruto_collection()
    print(f"✅ Professional Naruto NFT collection created: {collection}")