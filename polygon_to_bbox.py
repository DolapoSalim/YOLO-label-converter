"""
YOLO Polygon to Bounding Box Converter

This script converts YOLO segmentation format (polygon coordinates) to 
YOLO detection format (bounding boxes).

Input format:  class_id x1 y1 x2 y2 x3 y3 ... xn yn
Output format: class_id center_x center_y width height

Usage:
    python polygon_to_bbox.py input_file.txt [output_file.txt]
    python polygon_to_bbox.py --help

Author: Dolapo Olatoye
Tools: Claude AI for code generation assistance and debugging
"""

import sys
import argparse
import os
from pathlib import Path


def polygon_to_bbox(polygon_coords):
    """
    Convert polygon coordinates to bounding box format.
    
    Args:
        polygon_coords (list): List of normalized coordinates [x1, y1, x2, y2, ...]
        
    Returns:
        tuple: (center_x, center_y, width, height) in normalized format
    """
    if len(polygon_coords) < 6:  # Need at least 3 points (6 coordinates)
        raise ValueError("Polygon must have at least 3 points")
    
    # Separate x and y coordinates
    x_coords = [float(polygon_coords[i]) for i in range(0, len(polygon_coords), 2)]
    y_coords = [float(polygon_coords[i]) for i in range(1, len(polygon_coords), 2)]
    
    # Find bounding box
    min_x = min(x_coords)
    max_x = max(x_coords)
    min_y = min(y_coords)
    max_y = max(y_coords)
    
    # Calculate center and dimensions
    center_x = (min_x + max_x) / 2
    center_y = (min_y + max_y) / 2
    width = max_x - min_x
    height = max_y - min_y
    
    return center_x, center_y, width, height


def process_line(line):
    """
    Process a single line from the input file.
    
    Args:
        line (str): Input line containing class_id and polygon coordinates
        
    Returns:
        str: Output line in bounding box format
    """
    parts = line.strip().split()
    
    if len(parts) < 7:  # class_id + at least 6 coordinates (3 points)
        print(f"Warning: Skipping invalid line (too few coordinates): {line.strip()}")
        return None
    
    class_id = parts[0]
    polygon_coords = parts[1:]
    
    try:
        center_x, center_y, width, height = polygon_to_bbox(polygon_coords)
        return f"{class_id} {center_x:.6f} {center_y:.6f} {width:.6f} {height:.6f}"
    except ValueError as e:
        print(f"Warning: Error processing line: {e}")
        return None


def convert_file(input_file, output_file):
    """
    Convert an entire file from polygon to bounding box format.
    
    Args:
        input_file (str): Path to input file
        output_file (str): Path to output file
    """
    if not os.path.exists(input_file):
        raise FileNotFoundError(f"Input file not found: {input_file}")
    
    converted_lines = []
    skipped_lines = 0
    
    with open(input_file, 'r') as f:
        lines = f.readlines()
    
    print(f"Processing {len(lines)} lines from {input_file}...")
    
    for i, line in enumerate(lines, 1):
        line = line.strip()
        if not line:  # Skip empty lines
            continue
            
        converted_line = process_line(line)
        if converted_line:
            converted_lines.append(converted_line)
        else:
            skipped_lines += 1
    
    # Write output
    with open(output_file, 'w') as f:
        for line in converted_lines:
            f.write(line + '\n')
    
    print(f" Conversion complete!")
    print(f" Statistics:")
    print(f"   - Input lines processed: {len(lines)}")
    print(f"   - Objects converted: {len(converted_lines)}")
    print(f"   - Lines skipped: {skipped_lines}")
    print(f"   - Output saved to: {output_file}")


def batch_convert(input_dir, output_dir=None):
    """
    Convert all .txt files in a directory.
    
    Args:
        input_dir (str): Directory containing input files
        output_dir (str): Directory for output files (optional)
    """
    input_path = Path(input_dir)
    if not input_path.exists():
        raise FileNotFoundError(f"Input directory not found: {input_dir}")
    
    if output_dir is None:
        output_dir = input_path / "bbox_converted"
    
    output_path = Path(output_dir)
    output_path.mkdir(exist_ok=True)
    
    txt_files = list(input_path.glob("*.txt"))
    if not txt_files:
        print(f"No .txt files found in {input_dir}")
        return
    
    print(f"Found {len(txt_files)} .txt files to convert...")
    
    for txt_file in txt_files:
        output_file = output_path / txt_file.name
        try:
            convert_file(str(txt_file), str(output_file))
            print(f"✅ {txt_file.name} -> {output_file}")
        except Exception as e:
            print(f" Error processing {txt_file.name}: {e}")


def main():
    parser = argparse.ArgumentParser(
        description="Convert YOLO polygon segmentation to bounding box format",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Convert single file
  python polygon_to_bbox.py labels.txt
  python polygon_to_bbox.py labels.txt output_bbox.txt
  
  # Batch convert all files in directory
  python polygon_to_bbox.py --batch input_folder/
  python polygon_to_bbox.py --batch input_folder/ --output output_folder/
        """
    )
    
    parser.add_argument('input', help='Input file or directory')
    parser.add_argument('output', nargs='?', help='Output file (optional)')
    parser.add_argument('--batch', action='store_true', 
                       help='Batch process all .txt files in input directory')
    
    args = parser.parse_args()
    
    try:
        if args.batch:
            batch_convert(args.input, args.output)
        else:
            input_file = args.input
            output_file = args.output
            
            if output_file is None:
                # Generate output filename
                input_path = Path(input_file)
                output_file = str(input_path.with_suffix('.bbox.txt'))
            
            convert_file(input_file, output_file)
            
    except Exception as e:
        print(f" Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()


# Example usage as a module
def convert_polygon_to_bbox_string(polygon_string):
    """
    Convert a polygon string directly to bbox format.
    Useful for API/library usage.
    
    Args:
        polygon_string (str): "class_id x1 y1 x2 y2 ..."
        
    Returns:
        str: "class_id center_x center_y width height"
    """
    return process_line(polygon_string)


# Test the conversion with your data
if __name__ == "__main__":
    # If called without arguments, run the example
    if len(sys.argv) == 1:
        print(" YOLO Polygon to Bounding Box Converter")
        print("=" * 50)
        print()
        
        # Test with this sample data
        test_data = [
            "2 0.4895833333333333 0.11513157894736842 0.49141081871345027 0.11896929824561403 0.4903143274853801 0.1230811403508772",
            "0 0 0.9764254385964912 0.005116959064327485 0.9747807017543859 0.0062134502923976605"
        ]
        
        print("Sample conversion:")
        for line in test_data:
            converted = convert_polygon_to_bbox_string(line)
            if converted:
                print(f"Input:  {line[:50]}...")
                print(f"Output: {converted}")
                print()
        
        print("Usage: python polygon_to_bbox.py input_file.txt [output_file.txt]")
        print("       python polygon_to_bbox.py --batch input_folder/")
        print("       python polygon_to_bbox.py --help")
    else:
        main()