# YOLO-label-converter
This script is useful to convert YOLO segmentation label .txt files to standard coordinate labels. These are the coordinate formats for YOLO: xyxy, yxyn, xywh, xywhn

## Features:

### Single File Conversion:
```bash
python polygon_to_bbox.py your_labels.txt
python polygon_to_bbox.py your_labels.txt output_bbox.txt
```

### Batch Processing:
```bash
python polygon_to_bbox.py --batch your_labels_folder/
python polygon_to_bbox.py --batch input_folder/ --output output_folder/
```

### What it does:

#### Reads your polygon format:
``` 2 0.4895833 0.1151315 0.4914108 0.1189692 ...```

#### Converts to bounding box format:
``` 2 0.123456 0.654321 0.234567 0.345678 ```

#### Provides statistics:
- Lines processed
- Objects converted
- Lines skipped (if any errors)

### For your specific data:
Save the script as ```polygon_to_bbox.py```, then save your polygon data in a text file (e.g., ```labels.txt```) and run:
``` bash
python polygon_to_bbox.py labels.txt
```

This will create ```labels.bbox.txt``` with your converted bounding boxes!
The script is robust and handles:
Error checking
✅ Multiple objects per file
✅ Batch processing
✅ Detailed output statistics
✅ Command-line interface