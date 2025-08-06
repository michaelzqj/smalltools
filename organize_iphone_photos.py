import os
import datetime
import shutil
from PIL import Image

def get_creation_date(filename):
    """Tries to get the creation date from the photo's EXIF data, 
       falls back to file creation time if not available.
    """
    try:
        with Image.open(filename) as img:
            exif_data = img._getexif()
            if exif_data and 36867 in exif_data:
                date_str = exif_data[36867]
                return datetime.datetime.strptime(date_str, '%Y:%m:%d %H:%M:%S')
    except Exception:
        pass  # Ignore errors if the file is not an image or has no EXIF data

    # Fallback to file creation time
    creation_time = os.path.getctime(filename)
    return datetime.datetime.fromtimestamp(creation_time)

def organize_photos():
    """
    Organizes photos in the current directory into subdirectories based on their creation year and month.
    """
    for filename in os.listdir('.'):
        if os.path.isfile(filename) and filename != 'organize_photos.py':
            try:
                date = get_creation_date(filename)
                
                # Get the year and month from the date
                year = date.strftime('%Y')
                month = date.strftime('%m')
                
                # Create the year and month directories if they don't exist
                if not os.path.exists(year):
                    os.makedirs(year)
                if not os.path.exists(os.path.join(year, month)):
                    os.makedirs(os.path.join(year, month))
                
                # Move the file to the appropriate directory
                shutil.move(filename, os.path.join(year, month, filename))
                print(f"Moved {filename} to {os.path.join(year, month, filename)}")
            except Exception as e:
                print(f"Could not process {filename}: {e}")

if __name__ == '__main__':
    organize_photos()