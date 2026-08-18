import fitz  # PyMuPDF
import os

pdf_path = r"C:\Users\Raufb\Downloads\Enhanced_SSH_Pivoting_Lab_Documentation_with_Screenshots.pdf"
output_dir = r"c:\Users\Raufb\Desktop\portfolio-main\portfolio-main\assets\research\ssh-pivoting"

os.makedirs(output_dir, exist_ok=True)

doc = fitz.open(pdf_path)
print(f"PDF has {len(doc)} pages")

image_count = 0
for page_num in range(len(doc)):
    page = doc[page_num]
    image_list = page.get_images(full=True)
    print(f"Page {page_num + 1}: {len(image_list)} images")
    
    for img_index, img in enumerate(image_list):
        xref = img[0]
        try:
            base_image = doc.extract_image(xref)
            image_bytes = base_image["image"]
            ext = base_image["ext"]
            image_count += 1
            filename = f"page{page_num + 1:02d}_img{img_index + 1}.{ext}"
            filepath = os.path.join(output_dir, filename)
            with open(filepath, "wb") as f:
                f.write(image_bytes)
            print(f"  Saved: {filename} ({len(image_bytes)} bytes)")
        except Exception as e:
            print(f"  Error extracting image {xref}: {e}")

print(f"\nTotal images extracted: {image_count}")
doc.close()