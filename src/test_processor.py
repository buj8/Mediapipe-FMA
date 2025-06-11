import os
from external_processor import process_image_to_json
from config.settings import MODEL_PATH

def test_processor():
    # Create test_images directory if it doesn't exist
    test_dir = "test_images"
    if not os.path.exists(test_dir):
        os.makedirs(test_dir)
        print(f"Created {test_dir} directory. Please add some test images there.")
        return

    # Get all image files in the test directory
    image_extensions = ('.jpg', '.jpeg', '.png')
    image_files = [f for f in os.listdir(test_dir) if f.lower().endswith(image_extensions) and "annotated" not in f.lower()]

    if not image_files:
        print(f"No images found in {test_dir}. Please add some test images.")
        return

    # Process each image
    for image_file in image_files:
        image_path = os.path.join(test_dir, image_file)
        output_path = os.path.join(test_dir, f"{os.path.splitext(image_file)[0]}_results.json")
        output_image_path = os.path.join(test_dir, f"{os.path.splitext(image_file)[0]}_annotated.png")
        
        print(f"\nProcessing {image_file}...")
        success = process_image_to_json(
            image_path=image_path,
            model_path=MODEL_PATH,
            output_path=output_path,
            output_image_path=output_image_path
        )
        
        if success:
            print(f"Successfully processed {image_file}")
            print(f"Results saved to {output_path}")
            print(f"Annotated image saved to {output_image_path}")
        else:
            print(f"Failed to process {image_file}")

if __name__ == "__main__":
    test_processor() 