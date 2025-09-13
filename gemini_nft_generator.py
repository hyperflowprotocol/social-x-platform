#!/usr/bin/env python3
"""
Gemini NFT Generator - Creates professional Naruto NFT artwork using Google Gemini AI
"""

import os
import json
from google import genai
from google.genai import types

# Initialize Gemini client
client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))

def generate_naruto_nft(character_name, nft_id, output_path):
    """Generate a professional Naruto NFT using Gemini AI"""
    
    # Character-specific prompts for authentic designs
    character_prompts = {
        "naruto": "Naruto Uzumaki with spiky blonde hair, blue eyes, orange ninja outfit, whisker marks on cheeks, confident smile, Leaf Village headband",
        "sasuke": "Sasuke Uchiha with black hair, dark eyes with Sharingan pattern, dark blue ninja outfit, serious expression, calm pose",
        "itachi": "Itachi Uchiha with long black hair, red Sharingan eyes, black Akatsuki cloak with red clouds, serious expression",
        "kakashi": "Kakashi Hatake with silver hair, one visible eye, ninja mask covering lower face, dark blue ninja outfit, relaxed pose",
        "sakura": "Sakura Haruno with pink hair, green eyes, red outfit, confident medical ninja pose",
        "gaara": "Gaara with red hair, pale skin, dark circles around eyes, Sand Village headband, calm expression",
        "rock_lee": "Rock Lee with bowl cut black hair, thick eyebrows, green jumpsuit, energetic pose",
        "hinata": "Hinata Hyuga with long dark blue hair, pale lavender eyes with Byakugan, dark outfit, gentle expression"
    }
    
    # Base prompt for professional anime style
    base_prompt = """
    Create a professional anime-style NFT artwork featuring {character_description}.
    
    Style requirements:
    - High-quality anime/manga art style similar to official Naruto artwork
    - Professional digital art with clean lines and vibrant colors
    - Detailed character design with authentic features
    - Dynamic pose showing the character's personality
    - Clean background with subtle ninja village elements
    - Professional lighting and shading
    - Square format suitable for NFT (1:1 aspect ratio)
    
    The artwork should look like official Naruto merchandise quality, with professional anime studio production values.
    """
    
    try:
        character_desc = character_prompts.get(character_name.lower(), f"{character_name} from Naruto anime")
        prompt = base_prompt.format(character_description=character_desc)
        
        print(f"Generating NFT #{nft_id}: {character_name}...")
        
        response = client.models.generate_content(
            model="gemini-2.0-flash-preview-image-generation",
            contents=prompt,
            config=types.GenerateContentConfig(
                response_modalities=['TEXT', 'IMAGE']
            )
        )
        
        if not response.candidates:
            print(f"No content generated for {character_name}")
            return False
            
        content = response.candidates[0].content
        if not content or not content.parts:
            print(f"No parts in response for {character_name}")
            return False
            
        # Save the generated image
        for part in content.parts:
            if part.inline_data and part.inline_data.data:
                with open(output_path, 'wb') as f:
                    f.write(part.inline_data.data)
                print(f"✅ Saved NFT #{nft_id}: {output_path}")
                return True
            elif part.text:
                print(f"Generated description: {part.text}")
        
        print(f"❌ No image data found for {character_name}")
        return False
        
    except Exception as e:
        print(f"❌ Error generating {character_name}: {e}")
        return False

def create_gemini_collection():
    """Create a complete Naruto NFT collection using Gemini AI"""
    
    collection_dir = f"gemini_naruto_collection_{int(os.time.time() * 1000) if hasattr(os, 'time') else '1755600000'}"
    images_dir = os.path.join(collection_dir, "images")
    metadata_dir = os.path.join(collection_dir, "metadata")
    
    # Create directories
    os.makedirs(images_dir, exist_ok=True)
    os.makedirs(metadata_dir, exist_ok=True)
    
    # Define character collection
    characters = [
        "naruto", "sasuke", "itachi", "kakashi", "sakura",
        "gaara", "rock_lee", "hinata", "naruto", "sasuke",
        "itachi", "kakashi", "sakura", "gaara", "rock_lee",
        "hinata", "naruto", "sasuke", "itachi", "kakashi"
    ]
    
    successful_generations = 0
    
    for i, character in enumerate(characters, 1):
        image_path = os.path.join(images_dir, f"{i}.png")
        
        if generate_naruto_nft(character, i, image_path):
            # Create metadata
            metadata = {
                "name": f"Professional Naruto NFT #{i}",
                "description": f"High-quality AI-generated {character.title()} artwork created with Gemini AI",
                "image": f"images/{i}.png",
                "attributes": [
                    {"trait_type": "Character", "value": character.title()},
                    {"trait_type": "Generation", "value": "Gemini AI"},
                    {"trait_type": "Style", "value": "Professional Anime"},
                    {"trait_type": "Quality", "value": "Reference Grade"},
                    {"trait_type": "Format", "value": "PNG"}
                ]
            }
            
            metadata_path = os.path.join(metadata_dir, f"{i}.json")
            with open(metadata_path, 'w') as f:
                json.dump(metadata, f, indent=2)
                
            successful_generations += 1
        else:
            print(f"Failed to generate NFT #{i}")
    
    # Create collection metadata
    collection_metadata = {
        "name": "Professional Naruto NFT Collection",
        "description": "High-quality Naruto NFT collection generated with Google Gemini AI",
        "total_supply": len(characters),
        "successful_generations": successful_generations,
        "generator": "Google Gemini AI",
        "style": "Professional Anime",
        "created": f"{int(os.time.time() * 1000) if hasattr(os, 'time') else '1755600000'}"
    }
    
    with open(os.path.join(collection_dir, "collection.json"), 'w') as f:
        json.dump(collection_metadata, f, indent=2)
    
    print(f"🎨 Generated {successful_generations}/{len(characters)} NFTs")
    print(f"📁 Collection saved to: {collection_dir}")
    return collection_dir

if __name__ == "__main__":
    print("🎨 Starting Gemini AI NFT Generation")
    print("=" * 50)
    
    if not os.environ.get("GEMINI_API_KEY"):
        print("❌ GEMINI_API_KEY not found")
        exit(1)
    
    collection_path = create_gemini_collection()
    print(f"✅ Professional Naruto NFT collection created at: {collection_path}")