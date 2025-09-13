#!/usr/bin/env python3
"""
Blueprint Gemini NFT Generator using existing working setup
"""

import json
import os
import time
from google import genai
from google.genai import types

# Initialize client with API key
client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))

def generate_naruto_artwork(character_prompt, output_path):
    """Generate Naruto artwork using Gemini image generation"""
    try:
        response = client.models.generate_content(
            model="gemini-2.0-flash-preview-image-generation",
            contents=character_prompt,
            config=types.GenerateContentConfig(
                response_modalities=['TEXT', 'IMAGE']
            )
        )

        if not response.candidates:
            return False

        content = response.candidates[0].content
        if not content or not content.parts:
            return False

        for part in content.parts:
            if part.text:
                print(f"Generated description: {part.text}")
            elif part.inline_data and part.inline_data.data:
                with open(output_path, 'wb') as f:
                    f.write(part.inline_data.data)
                print(f"✅ Image saved: {output_path}")
                return True

        return False

    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def create_professional_collection():
    """Create professional Naruto NFT collection"""
    
    timestamp = int(time.time())
    collection_dir = f"professional_naruto_{timestamp}"
    images_dir = os.path.join(collection_dir, "images")
    metadata_dir = os.path.join(collection_dir, "metadata")
    
    os.makedirs(images_dir, exist_ok=True)
    os.makedirs(metadata_dir, exist_ok=True)
    
    # Professional character prompts
    characters = [
        "Professional anime artwork of Naruto Uzumaki with spiky blonde hair, blue eyes, orange ninja jumpsuit, whisker marks, confident smile, Leaf Village headband, dynamic action pose, high-quality digital art, vibrant colors, official anime studio style",
        
        "Professional anime artwork of Sasuke Uchiha with black hair, red Sharingan eyes, dark blue ninja outfit, serious expression, lightning chakra effects, confident pose, high-quality digital art, official anime studio style",
        
        "Professional anime artwork of Itachi Uchiha with long black hair, red Sharingan eyes, black Akatsuki cloak with red clouds, calm serious expression, mystical aura, high-quality digital art, official anime studio style",
        
        "Professional anime artwork of Kakashi Hatake with silver hair, one visible eye with Sharingan, ninja mask, dark blue outfit, relaxed confident pose, high-quality digital art, official anime studio style",
        
        "Professional anime artwork of Sakura Haruno with pink hair, green eyes, red ninja outfit, medical ninja pose, determined expression, chakra glow effects, high-quality digital art, official anime studio style",
        
        "Professional anime artwork of Gaara with red hair, pale skin, dark eye markings, Sand Village headband, sand manipulation effects, calm expression, high-quality digital art, official anime studio style",
        
        "Professional anime artwork of Rock Lee with black bowl cut hair, thick eyebrows, green jumpsuit, energetic fighting pose, dynamic action lines, high-quality digital art, official anime studio style",
        
        "Professional anime artwork of Hinata Hyuga with long dark blue hair, pale lavender Byakugan eyes, ninja outfit, gentle confident pose, chakra effects, high-quality digital art, official anime studio style"
    ]
    
    successful_count = 0
    
    # Generate 20 NFTs using character rotation
    for i in range(1, 21):
        character_prompt = characters[(i-1) % len(characters)]
        image_path = os.path.join(images_dir, f"{i}.png")
        
        print(f"Generating NFT #{i}...")
        
        if generate_naruto_artwork(character_prompt, image_path):
            # Create metadata
            character_name = character_prompt.split("of ")[1].split(" with")[0] if "of " in character_prompt else f"Character {i}"
            
            metadata = {
                "name": f"Professional Naruto NFT #{i}",
                "description": f"High-quality AI-generated {character_name} artwork created with Google Gemini AI. Professional anime studio quality with authentic character design.",
                "image": f"images/{i}.png",
                "attributes": [
                    {"trait_type": "Character", "value": character_name},
                    {"trait_type": "Generation", "value": "Gemini AI"},
                    {"trait_type": "Style", "value": "Professional Anime"},
                    {"trait_type": "Quality", "value": "Studio Grade"},
                    {"trait_type": "Format", "value": "PNG"},
                    {"trait_type": "Resolution", "value": "High"}
                ]
            }
            
            metadata_path = os.path.join(metadata_dir, f"{i}.json")
            with open(metadata_path, 'w') as f:
                json.dump(metadata, f, indent=2)
                
            successful_count += 1
            print(f"✅ NFT #{i} complete")
        else:
            print(f"❌ NFT #{i} failed")
        
        # Rate limiting delay
        time.sleep(3)
    
    # Collection summary
    collection_info = {
        "name": "Professional Naruto NFT Collection",
        "description": "High-quality Naruto NFT collection generated with Google Gemini AI featuring authentic character designs and professional anime studio art style",
        "total_nfts": 20,
        "successful_generations": successful_count,
        "generator": "Google Gemini AI",
        "style": "Professional Anime Studio",
        "created_timestamp": timestamp
    }
    
    with open(os.path.join(collection_dir, "collection.json"), 'w') as f:
        json.dump(collection_info, f, indent=2)
    
    print(f"\n🎨 Collection Generation Complete!")
    print(f"📊 Success Rate: {successful_count}/20 NFTs")
    print(f"📁 Collection Directory: {collection_dir}")
    
    return collection_dir, successful_count

if __name__ == "__main__":
    print("🎨 Professional Naruto NFT Generation with Gemini AI")
    print("=" * 60)
    
    if not os.environ.get("GEMINI_API_KEY"):
        print("❌ GEMINI_API_KEY environment variable not found")
        exit(1)
    
    print("🚀 Starting generation process...")
    collection_path, success_count = create_professional_collection()
    
    if success_count > 0:
        print(f"✅ Successfully created {success_count} professional Naruto NFTs!")
        print(f"🎯 Collection ready at: {collection_path}")
    else:
        print("❌ No NFTs were successfully generated")