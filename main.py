import os
import json
import cv2
import numpy as np
from PIL import Image, ImageChops
import exifread
import io
import hashlib

# Create necessary directories
os.makedirs("outputs/metadata", exist_ok=True)
os.makedirs("outputs/features", exist_ok=True)
os.makedirs("outputs/ela", exist_ok=True)
os.makedirs("outputs/report", exist_ok=True)

def extract_metadata(image_path):
    """Extract metadata (EXIF) from an image with error handling."""
    try:
        with open(image_path, 'rb') as img_file:
            tags = exifread.process_file(img_file, details=False)  # Process EXIF metadata
        
        if not tags:
            print(f"No metadata found in {image_path}")
            return {}

        # Convert metadata to a readable format
        metadata = {tag: str(tags[tag]) for tag in tags if tag not in ("JPEGThumbnail", "TIFFThumbnail")}
        
        # Save metadata to a JSON file
        metadata_path = os.path.join("outputs/metadata", os.path.basename(image_path) + "_metadata.json")
        with open(metadata_path, 'w') as f:
            json.dump(metadata, f, indent=4)
        
        print(f"Metadata extracted and saved to {metadata_path}")
        return metadata

    except Exception as e:
        print(f"Error extracting metadata from {image_path}: {e}")
        return {}


def extract_features(image_path):
    """Extract color histograms, edge maps, and texture features."""
    image = cv2.imread(image_path)
    if image is None:
        raise ValueError(f"Could not read image {image_path}")

    # Color histogram (more bins for finer granularity)
    hist = cv2.calcHist([image], [0, 1, 2], None, [16, 16, 16], [0, 256] * 3)

    # Edge map using Sobel operator
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    sobel_x = cv2.Sobel(gray, cv2.CV_64F, 1, 0, ksize=3)
    sobel_y = cv2.Sobel(gray, cv2.CV_64F, 0, 1, ksize=3)
    sobel_edges = cv2.magnitude(sobel_x, sobel_y)

    # ORB Feature extraction
    orb = cv2.ORB_create()
    keypoints, descriptors = orb.detectAndCompute(image, None)

    # Save features
    features_path = os.path.join("outputs/features", os.path.basename(image_path) + "_features.npz")
    np.savez(features_path, hist=hist, edges=sobel_edges, descriptors=descriptors)
    return hist, sobel_edges, descriptors

def error_level_analysis(image_path, quality=90):
    """Perform Error Level Analysis (ELA) on an image."""
    original = Image.open(image_path).convert('RGB')
    compressed_path = os.path.join("outputs/ela", os.path.basename(image_path) + "_compressed.jpg")
    ela_path = os.path.join("outputs/ela", os.path.basename(image_path) + "_ela.jpg")
    original.save(compressed_path, 'JPEG', quality=quality)
    compressed = Image.open(compressed_path)

    ela_image = ImageChops.difference(original, compressed)
    ela_image = ela_image.point(lambda p: p * 10)  # Enhance differences
    ela_image.save(ela_path)
    return ela_path

def detect_anomaly(ela_image_path, threshold=50):
    """Detect anomalies based on the ELA image."""
    ela_image = Image.open(ela_image_path)
    ela_image_array = np.array(ela_image)

    # Detect if any pixel exceeds the threshold for anomaly
    if np.any(ela_image_array > threshold):
        return True  # Anomaly detected
    return False  # No anomaly detected

def image_to_binary_stream(image_path):
    """Convert an image to a binary stream."""
    with open(image_path, "rb") as file:
        binary_stream = io.BytesIO(file.read())
    return binary_stream

def hash_binary_stream(binary_stream):
    """Generate a hash of the binary stream."""
    binary_stream.seek(0)  # Reset the stream's position
    return hashlib.sha256(binary_stream.read()).hexdigest()

def verify_image_hash(original_path, modified_path):
    """Verify whether an image has been modified using hash comparison."""
    original_hash = hash_binary_stream(image_to_binary_stream(original_path))
    modified_hash = hash_binary_stream(image_to_binary_stream(modified_path))

    print(f"Original Image Hash: {original_hash}")
    print(f"Modified Image Hash: {modified_hash}")

    if original_hash == modified_hash:
        print("The images are identical (no modifications detected).")
        return False  # No modifications detected
    else:
        print("The images are different (modifications detected).")
        return True  # Modifications detected

def compare_binary_streams(original_path, modified_path):
    """Compare the binary streams of two images and visualize differences."""
    original_stream = image_to_binary_stream(original_path)
    modified_stream = image_to_binary_stream(modified_path)

    # Generate hashes for quick comparison
    original_hash = hash_binary_stream(original_stream)
    modified_hash = hash_binary_stream(modified_stream)

    print(f"Original Hash: {original_hash}")
    print(f"Modified Hash: {modified_hash}")

    if original_hash == modified_hash:
        print("The images are identical at the binary level.")
        return None  # No differences
    
    print("The images are different. Visualizing pixel differences...")
    original_image = Image.open(original_path)
    modified_image = Image.open(modified_path)
    diff_image = ImageChops.difference(original_image, modified_image)

    diff_image_path = "outputs/difference_image.png"
    diff_image.save(diff_image_path)
    print(f"Differences saved at {diff_image_path}")
    return diff_image_path

def generate_report(image_path, metadata, hist, edges, ela_path, is_anomalous, features=None):
    """Generate a report consolidating analysis results."""
    report_path = os.path.join("outputs/report", os.path.basename(image_path) + "_report.txt")
    
    with open(report_path, 'w') as f:
        f.write(f"Image Analysis Report for {image_path}\n")
        f.write("="*50 + "\n")
        f.write("Metadata:\n")
        f.write(json.dumps(metadata, indent=4) + "\n")
        f.write("\nFeature Extraction:\n")
        f.write(f"Histogram Shape: {hist.shape}\n")
        f.write(f"Edge Map Shape: {edges.shape}\n")
        f.write(f"ORB Descriptors Shape: {features.shape if features is not None else 'N/A'}\n")
        f.write(f"\nELA Image Path: {ela_path}\n")
        f.write(f"\nAnomaly Detected: {'Yes' if is_anomalous else 'No'}\n")
    print(f"Report generated at: {report_path}")

def main(image1_path, image2_path):
    for image_path in [image1_path, image2_path]:
        # Step 1: Metadata Analysis
        print(f"Processing metadata for {image_path}")
        metadata = extract_metadata(image_path)

        # Step 2: Feature Extraction
        print(f"Extracting features for {image_path}")
        hist, edges, descriptors = extract_features(image_path)

        # Step 3: Error Level Analysis (ELA)
        print(f"Performing ELA for {image_path}")
        ela_path = error_level_analysis(image_path)

        # Step 4: Anomaly Detection based on ELA
        print(f"Detecting anomalies for {image_path}")
        is_anomalous = detect_anomaly(ela_path)

        # Step 5: Generate Report
        print(f"Generating report for {image_path}")
        generate_report(image_path, metadata, hist, edges, ela_path, is_anomalous, descriptors)

    # Step 6: Compare the two images
    print("Comparing the two images...")
    compare_binary_streams(image1_path, image2_path)
    verify_image_hash(image1_path, image2_path)

if __name__ == "__main__":
    image1_path = "images/image.jpg"  # Replace with the path to your first image
    image2_path = "images/image2.jpg"  # Replace with the path to your second image
    main(image1_path, image2_path)
