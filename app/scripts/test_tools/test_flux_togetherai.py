from app.tools.image import generate_image

# Test prompt
prompt = "A cozy bookstore in the middle of a magical forest, watercolor style"

# Optional: use specific model
model = "runwayml/stable-diffusion-v1-5"

result = generate_image(prompt=prompt, model=model)

if result["status"] == "success":
    print("✅ Image generated successfully!")
    with open("test_output.png", "wb") as f:
        import base64
        f.write(base64.b64decode(result["data"]["image"]))
    print("🖼️ Saved as test_output.png")
else:
    print("❌ Failed to generate image:")
    print(result["message"])
