import os
import datetime
import shutil
import subprocess
from tqdm import tqdm

count = {}

def get_creation_date(filename):
    """Tries to get the creation date from the photo's EXIF data,
       falls back to file creation time if not available.
    """
    try:
        # Use exiftool to get the creation date
        cmd = ["exiftool", "-s", "-s", "-s", "-DateTimeOriginal", filename]
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        date_str = result.stdout.strip()
        return datetime.datetime.strptime(date_str, '%Y:%m:%d %H:%M:%S')
    except (subprocess.CalledProcessError, FileNotFoundError, ValueError):
        return datetime.datetime.fromtimestamp(os.stat(filename).st_birthtime)


def organize_photos():
    """
    Organizes photos in the current directory and its subdirectories into subdirectories based on their creation year and month.
    """
    files_to_process = []
    for root, _, files in os.walk('.'):
        for filename in files:
            if filename in ['organize_iphone_photos.py', '.DS_Store', 'inspect_exif.py', 'exif_output.txt']:
                continue
            files_to_process.append(os.path.join(root, filename))

    for filepath in tqdm(files_to_process):
        try:
            date = get_creation_date(filepath)

            # Get the year and month from the date
            year = date.strftime('%Y')
            month = date.strftime('%m')

            # Create the year and month directories if they don't exist
            if not os.path.exists(year):
                os.makedirs(year)
            if not os.path.exists(os.path.join(year, month)):
                os.makedirs(os.path.join(year, month))

            # Move the file to the appropriate directory
            filename = os.path.basename(filepath)
            shutil.move(filepath, os.path.join(year, month, filename))
            count[year] = count.get(year, 0) + 1
        except Exception as e:
            print(f"Could not process {filepath}: {e}")
            count['error'] = count.get('error', 0) + 1
    print('count: {}'.format(count))

if __name__ == '__main__':
    organize_photos()