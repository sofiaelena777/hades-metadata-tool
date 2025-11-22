#!/usr/bin/env python3

import os
import sys
import subprocess
import shutil
from pathlib import Path
from datetime import datetime, timedelta
import time
import re
import random

class Colors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    GRAY = '\033[90m'
    RED = '\033[31m'
    YELLOW = '\033[33m'

FILE_TYPES = {
    'image': ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff', '.tif', '.webp', '.heic', '.raw', '.cr2', '.nef', '.arw', '.dng'],
    'video': ['.mp4', '.avi', '.mov', '.mkv', '.wmv', '.flv', '.webm', '.m4v', '.mpg', '.mpeg', '.3gp', '.mts'],
    'audio': ['.mp3', '.wav', '.flac', '.aac', '.ogg', '.m4a', '.wma', '.opus', '.aiff'],
    'document': ['.pdf', '.doc', '.docx', '.odt', '.rtf', '.txt'],
    'ebook': ['.epub', '.mobi', '.azw', '.azw3'],
    'archive': ['.zip', '.rar', '.7z', '.tar', '.gz'],
    'other': []
}

def print_banner():
    banner = f"""{Colors.RED}
        ,--,                                             
      ,--.'|                                             
   ,--,  | :                 ,---,                       
,---.'|  : '               ,---.'|                       
|   | : _' |               |   | :            .--.--.    
:   : |.'  |  ,--.--.      |   | |   ,---.   /  /    '   
|   ' '  ; : /       \   ,--.__| |  /     \ |  :  /`./   
'   |  .'. |.--.  .-. | /   ,'   | /    /  ||  :  ;_     
|   | :  | ' \__\/: . ..   '  /  |.    ' / | \  \    `.  
'   : |  : ; ," .--.; |'   ; |:  |'   ;   /|  `----.   \ 
|   | '  ,/ /  /  ,.  ||   | '/  ''   |  / | /  /`--'  / 
;   : ;--' ;  :   .'   \   :    :||   :    |'--'.     /  
|   ,/     |  ,     .-./\   \  /   \   \  /   `--'---'   
'---'       `--`---'     `----'     `----'               
{Colors.ENDC}"""
    
    print(banner)
    print(f"{Colors.OKCYAN}{Colors.BOLD}{'='*65}{Colors.ENDC}")
    print(f"{Colors.OKGREEN}{Colors.BOLD}    HADES - Advanced Metadata Manipulation Tool v4.0{Colors.ENDC}")
    print(f"{Colors.GRAY}    Multi-format forensic metadata spoofing utility{Colors.ENDC}")
    print(f"{Colors.OKCYAN}{Colors.BOLD}{'='*65}{Colors.ENDC}\n")

def get_file_type(filepath):
    ext = Path(filepath).suffix.lower()
    for file_type, extensions in FILE_TYPES.items():
        if ext in extensions:
            return file_type
    return 'other'

def check_exiftool():
    if not shutil.which('exiftool'):
        print(f"{Colors.FAIL}[!] ExifTool not found!{Colors.ENDC}")
        print(f"{Colors.WARNING}[*] Install it with:{Colors.ENDC}")
        print(f"{Colors.GRAY}    Linux: sudo apt install libimage-exiftool-perl{Colors.ENDC}")
        print(f"{Colors.GRAY}    Windows: Download from https://exiftool.org/{Colors.ENDC}")
        sys.exit(1)
    print(f"{Colors.OKGREEN}[✓] ExifTool detected{Colors.ENDC}")

def validate_file(filepath):
    path = Path(filepath)
    if not path.exists():
        print(f"{Colors.FAIL}[!] File not found: {filepath}{Colors.ENDC}")
        return False, None
    if not path.is_file():
        print(f"{Colors.FAIL}[!] Not a file: {filepath}{Colors.ENDC}")
        return False, None
    
    file_type = get_file_type(filepath)
    print(f"{Colors.OKGREEN}[✓] File validated: {path.absolute()}{Colors.ENDC}")
    print(f"{Colors.OKCYAN}[*] File type detected: {file_type.upper()}{Colors.ENDC}")
    return True, file_type

def validate_date_format(date_str):
    pattern = r'^\d{4}:\d{2}:\d{2} \d{2}:\d{2}:\d{2}$'
    if not re.match(pattern, date_str):
        return False
    try:
        parts = date_str.split()
        date_parts = parts[0].split(':')
        time_parts = parts[1].split(':')
        
        year, month, day = int(date_parts[0]), int(date_parts[1]), int(date_parts[2])
        hour, minute, second = int(time_parts[0]), int(time_parts[1]), int(time_parts[2])
        
        if not (1900 <= year <= 2100):
            return False
        if not (1 <= month <= 12):
            return False
        if not (1 <= day <= 31):
            return False
        if not (0 <= hour <= 23):
            return False
        if not (0 <= minute <= 59):
            return False
        if not (0 <= second <= 59):
            return False
        
        return True
    except:
        return False

def show_metadata(filepath):
    print(f"\n{Colors.OKCYAN}[*] Current Metadata:{Colors.ENDC}")
    try:
        result = subprocess.run(
            ['exiftool', '-charset', 'filename=utf8', filepath],
            capture_output=True,
            text=True,
            check=True,
            encoding='utf-8',
            errors='replace'
        )
        print(f"{Colors.GRAY}{result.stdout}{Colors.ENDC}")
    except subprocess.CalledProcessError as e:
        print(f"{Colors.FAIL}[!] Error reading metadata: {e}{Colors.ENDC}")

def progress_bar(duration=2):
    bar_length = 50
    print(f"{Colors.OKGREEN}", end='')
    for i in range(bar_length + 1):
        progress = '█' * i + '░' * (bar_length - i)
        percentage = int((i / bar_length) * 100)
        print(f'\r[{progress}] {percentage}%', end='', flush=True)
        time.sleep(duration / bar_length)
    print(f"{Colors.ENDC}\n")

def clean_metadata(filepath):
    print(f"\n{Colors.WARNING}[*] Initiating metadata removal...{Colors.ENDC}")
    
    try:
        result = subprocess.run(
            ['exiftool', '-all=', '-overwrite_original', '-charset', 'filename=utf8', filepath],
            capture_output=True,
            text=True,
            check=True,
            encoding='utf-8',
            errors='replace'
        )
        
        progress_bar(2)
        print(f"{Colors.OKGREEN}[✓] Metadata successfully wiped{Colors.ENDC}")
        
        if result.stdout.strip():
            print(f"{Colors.GRAY}[*] ExifTool output:{Colors.ENDC}")
            print(f"{Colors.GRAY}{result.stdout}{Colors.ENDC}")
        
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"{Colors.FAIL}[!] Cleaning failed: {e}{Colors.ENDC}")
        if e.stderr:
            print(f"{Colors.FAIL}{e.stderr}{Colors.ENDC}")
        return False

def generate_random_metadata(file_type):
    print(f"\n{Colors.WARNING}[*] Generating random metadata for {file_type.upper()} file...{Colors.ENDC}")
    
    first_names = ['James', 'John', 'Robert', 'Michael', 'William', 'David', 'Richard', 'Joseph', 
                   'Thomas', 'Charles', 'Mary', 'Patricia', 'Jennifer', 'Linda', 'Elizabeth', 
                   'Barbara', 'Susan', 'Jessica', 'Sarah', 'Karen', 'Emma', 'Olivia', 'Ava', 'Sophia']
    last_names = ['Smith', 'Johnson', 'Williams', 'Brown', 'Jones', 'Garcia', 'Miller', 'Davis', 
                  'Rodriguez', 'Martinez', 'Hernandez', 'Lopez', 'Gonzalez', 'Wilson', 'Anderson', 
                  'Thomas', 'Taylor', 'Moore', 'Jackson', 'Martin', 'Lee', 'White', 'Harris', 'Clark']
    
    companies = ['Adobe Systems', 'Microsoft Corporation', 'Apple Inc.', 'Google LLC', 'Canon Inc.',
                'Sony Corporation', 'Nikon Corporation', 'Panasonic', 'Samsung Electronics', 
                'Intel Corporation', 'HP Inc.', 'Dell Technologies', 'IBM', 'Oracle Corporation']
    
    cities = ['New York', 'Los Angeles', 'Chicago', 'Houston', 'Phoenix', 'Philadelphia', 
              'San Antonio', 'San Diego', 'Dallas', 'San Jose', 'Austin', 'Jacksonville', 
              'Fort Worth', 'Columbus', 'Charlotte', 'San Francisco', 'Indianapolis', 'Seattle', 
              'Denver', 'Washington', 'Boston', 'Detroit', 'Nashville', 'Portland', 'Las Vegas']
    
    states = ['NY', 'CA', 'IL', 'TX', 'AZ', 'PA', 'FL', 'OH', 'NC', 'WA', 'CO', 'MA', 'MI', 'TN', 'OR', 'NV']
    
    countries = ['USA', 'United States', 'US']
    
    end_date = datetime.now()
    start_date = end_date - timedelta(days=365*5)
    random_days = random.randint(0, (end_date - start_date).days)
    create_datetime = start_date + timedelta(days=random_days)
    modify_datetime = create_datetime + timedelta(days=random.randint(0, 30))
    
    author = f"{random.choice(first_names)} {random.choice(last_names)}"
    city_choice = random.choice(cities)
    
    city_state_map = {
        'New York': 'NY', 'Los Angeles': 'CA', 'Chicago': 'IL', 'Houston': 'TX',
        'Phoenix': 'AZ', 'Philadelphia': 'PA', 'San Antonio': 'TX', 'San Diego': 'CA',
        'Dallas': 'TX', 'San Jose': 'CA', 'Austin': 'TX', 'Jacksonville': 'FL',
        'Fort Worth': 'TX', 'Columbus': 'OH', 'Charlotte': 'NC', 'San Francisco': 'CA',
        'Indianapolis': 'IN', 'Seattle': 'WA', 'Denver': 'CO', 'Washington': 'DC',
        'Boston': 'MA', 'Detroit': 'MI', 'Nashville': 'TN', 'Portland': 'OR', 'Las Vegas': 'NV'
    }
    
    metadata = {
        'author': author,
        'create_date': create_datetime.strftime('%Y:%m:%d %H:%M:%S'),
        'modify_date': modify_datetime.strftime('%Y:%m:%d %H:%M:%S'),
        'city': city_choice,
        'state': city_state_map.get(city_choice, random.choice(states)),
        'country': random.choice(countries),
        'copyright': f'© {create_datetime.year} {author}',
    }
    
    if file_type == 'image':
        camera_makes = ['Canon', 'Nikon', 'Sony', 'Fujifilm', 'Olympus', 'Panasonic', 'Leica', 'Pentax']
        camera_models = {
            'Canon': ['EOS 5D Mark IV', 'EOS R5', 'EOS 90D', 'EOS Rebel T7i', 'PowerShot G7 X'],
            'Nikon': ['D850', 'Z7 II', 'D7500', 'D3500', 'Z50'],
            'Sony': ['Alpha a7 III', 'Alpha a7R IV', 'Alpha a6400', 'RX100 VII', 'Alpha a9 II'],
            'Fujifilm': ['X-T4', 'X-Pro3', 'X-E4', 'X-S10', 'X100V'],
            'Olympus': ['OM-D E-M1 Mark III', 'OM-D E-M5 Mark III', 'PEN E-PL10'],
            'Panasonic': ['Lumix DC-GH5', 'Lumix DC-G9', 'Lumix DC-S1', 'Lumix LX100 II'],
            'Leica': ['Q2', 'M10-R', 'SL2', 'CL'],
            'Pentax': ['K-1 Mark II', 'K-3 III', 'KP']
        }
        software_list = ['Adobe Photoshop CC 2024', 'Adobe Photoshop CS6', 'GIMP 2.10', 
                         'Adobe Lightroom Classic', 'Capture One 23', 'DxO PhotoLab 6',
                         'Affinity Photo 2', 'Luminar AI', 'ON1 Photo RAW 2024']
        titles = ['Untitled', 'Photo', 'Image', 'Capture', 'Moment', 'Memory', 'Snapshot', 
                  'Scene', 'View', 'Landscape', 'Portrait', 'Nature', 'Urban', 'Street']
        
        make = random.choice(camera_makes)
        metadata.update({
            'gps_lat': f"{random.uniform(25.0, 49.0):.6f}",
            'gps_lon': f"{random.uniform(-125.0, -66.0):.6f}",
            'make': make,
            'model': random.choice(camera_models[make]),
            'title': random.choice(titles),
            'description': f'Photograph taken with {make} camera',
            'software': random.choice(software_list)
        })
    
    elif file_type == 'video':
        camera_makes = ['Canon', 'Sony', 'Panasonic', 'Blackmagic', 'RED', 'ARRI', 'GoPro', 'DJI']
        camera_models = {
            'Canon': ['EOS C300 Mark III', 'EOS R5 C', 'XF605', 'EOS C70'],
            'Sony': ['FX6', 'FX3', 'A7S III', 'PXW-Z280', 'FX9'],
            'Panasonic': ['Lumix GH6', 'Lumix S1H', 'AG-CX350', 'HC-X2000'],
            'Blackmagic': ['URSA Mini Pro 12K', 'Pocket Cinema Camera 6K', 'Studio Camera 4K Pro'],
            'RED': ['KOMODO 6K', 'V-RAPTOR 8K VV', 'DSMC2 GEMINI 5K'],
            'ARRI': ['ALEXA Mini LF', 'ALEXA 35', 'AMIRA'],
            'GoPro': ['HERO11 Black', 'HERO10 Black', 'HERO9 Black', 'MAX'],
            'DJI': ['Mavic 3 Cine', 'Air 2S', 'Mini 3 Pro', 'Inspire 3']
        }
        software_list = ['Adobe Premiere Pro 2024', 'Final Cut Pro X', 'DaVinci Resolve 18',
                         'Adobe After Effects 2024', 'Avid Media Composer', 'Vegas Pro 20',
                         'Filmora 12', 'HitFilm Pro', 'Lightworks']
        titles = ['Video', 'Clip', 'Footage', 'Recording', 'Scene', 'Take', 'Sequence']
        
        make = random.choice(camera_makes)
        metadata.update({
            'make': make,
            'model': random.choice(camera_models[make]),
            'title': random.choice(titles),
            'description': f'Video footage recorded with {make} camera',
            'software': random.choice(software_list),
            'duration': f'{random.randint(1, 180)} seconds',
            'video_codec': random.choice(['H.264', 'H.265/HEVC', 'ProRes 422', 'DNxHD']),
            'audio_codec': random.choice(['AAC', 'PCM', 'MP3', 'AC3'])
        })
    
    elif file_type == 'audio':
        software_list = ['Adobe Audition 2024', 'Audacity 3.2', 'FL Studio 21', 'Ableton Live 11',
                         'Logic Pro X', 'Pro Tools 2023', 'Reaper 6.7', 'Cubase 13', 'GarageBand']
        titles = ['Audio', 'Track', 'Recording', 'Sound', 'Music', 'Podcast', 'Voice']
        genres = ['Rock', 'Pop', 'Jazz', 'Classical', 'Electronic', 'Hip Hop', 'Country', 
                  'R&B', 'Folk', 'Blues', 'Podcast', 'Audiobook', 'Speech']
        
        metadata.update({
            'title': random.choice(titles),
            'album': f'Album {random.randint(1, 10)}',
            'artist': author,
            'composer': random.choice([author, f"{random.choice(first_names)} {random.choice(last_names)}"]),
            'genre': random.choice(genres),
            'software': random.choice(software_list),
            'duration': f'{random.randint(30, 600)} seconds',
            'audio_codec': random.choice(['MP3', 'AAC', 'FLAC', 'WAV', 'OGG'])
        })
    
    elif file_type == 'document':
        software_list = ['Microsoft Word 2021', 'LibreOffice Writer 7.4', 'Google Docs', 
                         'Adobe Acrobat DC', 'Apple Pages', 'WPS Office 2023', 
                         'OpenOffice Writer 4.1', 'Foxit PDF Editor', 'Nitro Pro 13']
        titles = ['Document', 'Report', 'Letter', 'Memo', 'Contract', 'Proposal', 
                  'Invoice', 'Resume', 'Agreement', 'Manual', 'Guide', 'Article']
        subjects = ['Business', 'Finance', 'Legal', 'Technical', 'Personal', 'Marketing',
                   'Research', 'Education', 'Medical', 'Engineering', 'Administration']
        
        metadata.update({
            'title': random.choice(titles),
            'subject': random.choice(subjects),
            'creator': author,
            'producer': random.choice(companies),
            'software': random.choice(software_list),
            'pages': str(random.randint(1, 50)),
            'keywords': ', '.join(random.sample(['confidential', 'draft', 'final', 'review', 
                                                 'approved', 'pending', 'urgent', 'archived'], 
                                                k=random.randint(1, 3)))
        })
    
    elif file_type == 'ebook':
        publishers = ['Penguin Random House', 'HarperCollins', 'Simon & Schuster', 'Hachette', 
                     'Macmillan', 'Scholastic', 'Wiley', "O'Reilly Media", 'Springer']
        genres = ['Fiction', 'Non-Fiction', 'Mystery', 'Thriller', 'Romance', 'Science Fiction',
                 'Fantasy', 'Biography', 'History', 'Self-Help', 'Technical', 'Educational']
        
        metadata.update({
            'title': f'Book Title {random.randint(1, 100)}',
            'creator': author,
            'publisher': random.choice(publishers),
            'genre': random.choice(genres),
            'language': random.choice(['en', 'en-US', 'en-GB']),
            'isbn': f'978-{random.randint(0, 9)}-{random.randint(1000, 9999)}-{random.randint(1000, 9999)}-{random.randint(0, 9)}',
        })
    
    progress_bar(1)
    print(f"{Colors.OKGREEN}[✓] Random metadata generated for {file_type.upper()}{Colors.ENDC}")
    
    return metadata

def inject_metadata(filepath, metadata, file_type):
    print(f"\n{Colors.WARNING}[*] Injecting metadata for {file_type.upper()} file...{Colors.ENDC}")
    
    commands = []
    
    if metadata.get('author'):
        commands.extend([
            f'-Artist={metadata["author"]}',
            f'-Creator={metadata["author"]}',
            f'-Author={metadata["author"]}',
            f'-By-line={metadata["author"]}',
            f'-XMP:Creator={metadata["author"]}',
            f'-IPTC:By-line={metadata["author"]}'
        ])
    
    if metadata.get('create_date'):
        commands.extend([
            f'-CreateDate={metadata["create_date"]}',
            f'-DateTimeOriginal={metadata["create_date"]}',
            f'-DateCreated={metadata["create_date"]}',
            f'-XMP:CreateDate={metadata["create_date"]}',
            f'-EXIF:DateTimeOriginal={metadata["create_date"]}',
        ])
    
    if metadata.get('modify_date'):
        commands.extend([
            f'-ModifyDate={metadata["modify_date"]}',
            f'-DateTimeDigitized={metadata["modify_date"]}',
            f'-XMP:ModifyDate={metadata["modify_date"]}',
            f'-FileModifyDate={metadata["modify_date"]}'
        ])
    
    if metadata.get('city'):
        commands.extend([
            f'-City={metadata["city"]}',
            f'-XMP:City={metadata["city"]}',
            f'-IPTC:City={metadata["city"]}'
        ])
    
    if metadata.get('country'):
        commands.extend([
            f'-Country={metadata["country"]}',
            f'-XMP:Country={metadata["country"]}'
        ])
    
    if metadata.get('state'):
        commands.extend([
            f'-State={metadata["state"]}',
            f'-Province-State={metadata["state"]}'
        ])
    
    if metadata.get('gps_lat'):
        commands.append(f'-GPSLatitude={metadata["gps_lat"]}')
        commands.append(f'-GPSLatitudeRef=' + ('N' if float(metadata["gps_lat"]) >= 0 else 'S'))
    
    if metadata.get('gps_lon'):
        commands.append(f'-GPSLongitude={metadata["gps_lon"]}')
        commands.append(f'-GPSLongitudeRef=' + ('E' if float(metadata["gps_lon"]) >= 0 else 'W'))
    
    if metadata.get('make'):
        commands.extend([
            f'-Make={metadata["make"]}',
            f'-XMP:Make={metadata["make"]}'
        ])
    
    if metadata.get('model'):
        commands.extend([
            f'-Model={metadata["model"]}',
            f'-XMP:Model={metadata["model"]}'
        ])
    
    if metadata.get('title'):
        commands.extend([
            f'-Title={metadata["title"]}',
            f'-XMP:Title={metadata["title"]}',
            f'-IPTC:ObjectName={metadata["title"]}'
        ])
    
    if metadata.get('description'):
        commands.extend([
            f'-Description={metadata["description"]}',
            f'-XMP:Description={metadata["description"]}',
            f'-ImageDescription={metadata["description"]}'
        ])
    
    if metadata.get('copyright'):
        commands.extend([
            f'-Copyright={metadata["copyright"]}',
            f'-XMP:Rights={metadata["copyright"]}'
        ])
    
    if metadata.get('software'):
        commands.extend([
            f'-Software={metadata["software"]}',
            f'-XMP:CreatorTool={metadata["software"]}'
        ])
    
    if metadata.get('album'):
        commands.append(f'-Album={metadata["album"]}')
    
    if metadata.get('artist'):
        commands.append(f'-Artist={metadata["artist"]}')
    
    if metadata.get('composer'):
        commands.append(f'-Composer={metadata["composer"]}')
    
    if metadata.get('genre'):
        commands.append(f'-Genre={metadata["genre"]}')
    
    if metadata.get('duration'):
        commands.append(f'-Duration={metadata["duration"]}')
    
    if metadata.get('video_codec'):
        commands.append(f'-VideoCodec={metadata["video_codec"]}')
    
    if metadata.get('audio_codec'):
        commands.append(f'-AudioCodec={metadata["audio_codec"]}')
    
    if metadata.get('subject'):
        commands.append(f'-Subject={metadata["subject"]}')
    
    if metadata.get('producer'):
        commands.append(f'-Producer={metadata["producer"]}')
    
    if metadata.get('pages'):
        commands.append(f'-Pages={metadata["pages"]}')
    
    if metadata.get('keywords'):
        commands.append(f'-Keywords={metadata["keywords"]}')
    
    if metadata.get('publisher'):
        commands.append(f'-Publisher={metadata["publisher"]}')
    
    if metadata.get('language'):
        commands.append(f'-Language={metadata["language"]}')
    
    if metadata.get('isbn'):
        commands.append(f'-ISBN={metadata["isbn"]}')
    
    try:
        result = subprocess.run(
            ['exiftool', '-overwrite_original', '-P', '-charset', 'filename=utf8'] + commands + [filepath],
            capture_output=True,
            text=True,
            check=True,
            encoding='utf-8',
            errors='replace'
        )
        
        progress_bar(1.5)
        
        print(f"{Colors.GRAY}[*] ExifTool output:{Colors.ENDC}")
        if result.stdout.strip():
            for line in result.stdout.strip().split('\n'):
                if 'Warning' in line:
                    print(f"{Colors.WARNING}{line}{Colors.ENDC}")
                else:
                    print(f"{Colors.GRAY}{line}{Colors.ENDC}")
        
        if result.stderr.strip():
            print(f"{Colors.WARNING}[!] Warnings:{Colors.ENDC}")
            print(f"{Colors.WARNING}{result.stderr}{Colors.ENDC}")
        
        if metadata.get('modify_date'):
            print(f"\n{Colors.WARNING}[*] Modifying filesystem timestamps...{Colors.ENDC}")
            try:
                from datetime import datetime
                
                dt = datetime.strptime(metadata['modify_date'], '%Y:%m:%d %H:%M:%S')
                timestamp = dt.timestamp()
                
                os.utime(filepath, (timestamp, timestamp))
                print(f"{Colors.OKGREEN}[✓] Filesystem timestamp modified{Colors.ENDC}")
            except Exception as e:
                print(f"{Colors.WARNING}[!] Filesystem timestamp modification failed: {str(e)}{Colors.ENDC}")
        
        print(f"{Colors.OKGREEN}[✓] Metadata injection complete{Colors.ENDC}")
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"{Colors.FAIL}[!] Injection failed: {e}{Colors.ENDC}")
        if e.stderr:
            print(f"{Colors.FAIL}{e.stderr}{Colors.ENDC}")
        return False

def get_custom_metadata(file_type):
    print(f"\n{Colors.OKCYAN}{Colors.BOLD}[*] Custom Metadata Editor - {file_type.upper()}{Colors.ENDC}")
    print(f"{Colors.GRAY}[*] Press Enter to skip any field{Colors.ENDC}")
    print(f"{Colors.GRAY}[*] Date format: YYYY:MM:DD HH:MM:SS{Colors.ENDC}\n")
    
    metadata = {}
    
    value = input(f"{Colors.OKBLUE}[>] Author/Creator{Colors.ENDC}: ").strip()
    if value:
        metadata['author'] = value
    
    while True:
        value = input(f"{Colors.OKBLUE}[>] Creation Date{Colors.ENDC} {Colors.GRAY}(YYYY:MM:DD HH:MM:SS){Colors.ENDC}: ").strip()
        if not value:
            break
        if validate_date_format(value):
            metadata['create_date'] = value
            break
        else:
            print(f"{Colors.FAIL}[!] Invalid date format{Colors.ENDC}")
    
    while True:
        value = input(f"{Colors.OKBLUE}[>] Modification Date{Colors.ENDC} {Colors.GRAY}(YYYY:MM:DD HH:MM:SS){Colors.ENDC}: ").strip()
        if not value:
            break
        if validate_date_format(value):
            metadata['modify_date'] = value
            break
        else:
            print(f"{Colors.FAIL}[!] Invalid date format{Colors.ENDC}")
    
    value = input(f"{Colors.OKBLUE}[>] Title{Colors.ENDC}: ").strip()
    if value:
        metadata['title'] = value
    
    value = input(f"{Colors.OKBLUE}[>] Description{Colors.ENDC}: ").strip()
    if value:
        metadata['description'] = value
    
    value = input(f"{Colors.OKBLUE}[>] Copyright{Colors.ENDC}: ").strip()
    if value:
        metadata['copyright'] = value
    
    if file_type == 'image':
        value = input(f"{Colors.OKBLUE}[>] Camera Make{Colors.ENDC}: ").strip()
        if value:
            metadata['make'] = value
        
        value = input(f"{Colors.OKBLUE}[>] Camera Model{Colors.ENDC}: ").strip()
        if value:
            metadata['model'] = value
        
        value = input(f"{Colors.OKBLUE}[>] Software{Colors.ENDC}: ").strip()
        if value:
            metadata['software'] = value
        
        value = input(f"{Colors.OKBLUE}[>] GPS Latitude{Colors.ENDC}: ").strip()
        if value:
            try:
                float(value)
                metadata['gps_lat'] = value
            except ValueError:
                print(f"{Colors.WARNING}[!] Invalid latitude{Colors.ENDC}")
        
        value = input(f"{Colors.OKBLUE}[>] GPS Longitude{Colors.ENDC}: ").strip()
        if value:
            try:
                float(value)
                metadata['gps_lon'] = value
            except ValueError:
                print(f"{Colors.WARNING}[!] Invalid longitude{Colors.ENDC}")
    
    elif file_type == 'video':
        value = input(f"{Colors.OKBLUE}[>] Camera/Device Make{Colors.ENDC}: ").strip()
        if value:
            metadata['make'] = value
        
        value = input(f"{Colors.OKBLUE}[>] Camera/Device Model{Colors.ENDC}: ").strip()
        if value:
            metadata['model'] = value
        
        value = input(f"{Colors.OKBLUE}[>] Editing Software{Colors.ENDC}: ").strip()
        if value:
            metadata['software'] = value
        
        value = input(f"{Colors.OKBLUE}[>] Duration (seconds){Colors.ENDC}: ").strip()
        if value:
            metadata['duration'] = value
        
        value = input(f"{Colors.OKBLUE}[>] Video Codec{Colors.ENDC}: ").strip()
        if value:
            metadata['video_codec'] = value
        
        value = input(f"{Colors.OKBLUE}[>] Audio Codec{Colors.ENDC}: ").strip()
        if value:
            metadata['audio_codec'] = value
    
    elif file_type == 'audio':
        value = input(f"{Colors.OKBLUE}[>] Artist{Colors.ENDC}: ").strip()
        if value:
            metadata['artist'] = value
        
        value = input(f"{Colors.OKBLUE}[>] Album{Colors.ENDC}: ").strip()
        if value:
            metadata['album'] = value
        
        value = input(f"{Colors.OKBLUE}[>] Composer{Colors.ENDC}: ").strip()
        if value:
            metadata['composer'] = value
        
        value = input(f"{Colors.OKBLUE}[>] Genre{Colors.ENDC}: ").strip()
        if value:
            metadata['genre'] = value
        
        value = input(f"{Colors.OKBLUE}[>] Software{Colors.ENDC}: ").strip()
        if value:
            metadata['software'] = value
    
    elif file_type == 'document':
        value = input(f"{Colors.OKBLUE}[>] Subject{Colors.ENDC}: ").strip()
        if value:
            metadata['subject'] = value
        
        value = input(f"{Colors.OKBLUE}[>] Producer/Company{Colors.ENDC}: ").strip()
        if value:
            metadata['producer'] = value
        
        value = input(f"{Colors.OKBLUE}[>] Software{Colors.ENDC}: ").strip()
        if value:
            metadata['software'] = value
        
        value = input(f"{Colors.OKBLUE}[>] Number of Pages{Colors.ENDC}: ").strip()
        if value:
            metadata['pages'] = value
        
        value = input(f"{Colors.OKBLUE}[>] Keywords (comma-separated){Colors.ENDC}: ").strip()
        if value:
            metadata['keywords'] = value
    
    elif file_type == 'ebook':
        value = input(f"{Colors.OKBLUE}[>] Publisher{Colors.ENDC}: ").strip()
        if value:
            metadata['publisher'] = value
        
        value = input(f"{Colors.OKBLUE}[>] Genre{Colors.ENDC}: ").strip()
        if value:
            metadata['genre'] = value
        
        value = input(f"{Colors.OKBLUE}[>] Language (e.g., en, en-US){Colors.ENDC}: ").strip()
        if value:
            metadata['language'] = value
        
        value = input(f"{Colors.OKBLUE}[>] ISBN{Colors.ENDC}: ").strip()
        if value:
            metadata['isbn'] = value
    
    value = input(f"{Colors.OKBLUE}[>] City{Colors.ENDC}: ").strip()
    if value:
        metadata['city'] = value
    
    value = input(f"{Colors.OKBLUE}[>] State/Province{Colors.ENDC}: ").strip()
    if value:
        metadata['state'] = value
    
    value = input(f"{Colors.OKBLUE}[>] Country{Colors.ENDC}: ").strip()
    if value:
        metadata['country'] = value
    
    return metadata

def show_summary(metadata, file_type):
    print(f"\n{Colors.OKCYAN}{Colors.BOLD}{'='*65}{Colors.ENDC}")
    print(f"{Colors.OKGREEN}{Colors.BOLD}[*] Metadata Summary - {file_type.upper()}:{Colors.ENDC}\n")
    
    field_names = {
        'author': 'Author/Creator',
        'create_date': 'Creation Date',
        'modify_date': 'Modification Date',
        'city': 'City',
        'state': 'State/Province',
        'country': 'Country',
        'gps_lat': 'GPS Latitude',
        'gps_lon': 'GPS Longitude',
        'make': 'Make/Manufacturer',
        'model': 'Model',
        'title': 'Title',
        'description': 'Description',
        'copyright': 'Copyright',
        'software': 'Software',
        'artist': 'Artist',
        'album': 'Album',
        'composer': 'Composer',
        'genre': 'Genre',
        'duration': 'Duration',
        'video_codec': 'Video Codec',
        'audio_codec': 'Audio Codec',
        'subject': 'Subject',
        'producer': 'Producer',
        'pages': 'Pages',
        'keywords': 'Keywords',
        'publisher': 'Publisher',
        'language': 'Language',
        'isbn': 'ISBN'
    }
    
    for key, value in metadata.items():
        display_name = field_names.get(key, key.replace('_', ' ').title())
        print(f"{Colors.OKCYAN}  {display_name:.<30}{Colors.ENDC} {Colors.GRAY}{value}{Colors.ENDC}")
    
    print(f"{Colors.OKCYAN}{Colors.BOLD}{'='*65}{Colors.ENDC}")

def main():
    print_banner()
    check_exiftool()
    
    if len(sys.argv) > 1:
        filepath = sys.argv[1]
    else:
        filepath = input(f"{Colors.OKBLUE}[>] Enter file path{Colors.ENDC}: ").strip()
    
    valid, file_type = validate_file(filepath)
    if not valid:
        sys.exit(1)
    
    show_metadata(filepath)
    
    print(f"\n{Colors.WARNING}[?] Clean all metadata? (y/n){Colors.ENDC}: ", end='')
    if input().lower() == 'y':
        if not clean_metadata(filepath):
            sys.exit(1)
    
    print(f"\n{Colors.OKBLUE}[?] Inject custom metadata?{Colors.ENDC}")
    print(f"{Colors.GRAY}  [1] Manual input{Colors.ENDC}")
    print(f"{Colors.GRAY}  [2] Random generation{Colors.ENDC}")
    print(f"{Colors.GRAY}  [3] Skip{Colors.ENDC}")
    choice = input(f"{Colors.OKBLUE}[>] Select option (1/2/3){Colors.ENDC}: ").strip()
    
    metadata = None
    
    if choice == '1':
        metadata = get_custom_metadata(file_type)
    elif choice == '2':
        metadata = generate_random_metadata(file_type)
    
    if metadata:
        show_summary(metadata, file_type)
        print(f"\n{Colors.WARNING}[?] Confirm injection? (y/n){Colors.ENDC}: ", end='')
        if input().lower() == 'y':
            inject_metadata(filepath, metadata, file_type)
    
    print(f"\n{Colors.OKCYAN}[*] Final Metadata State:{Colors.ENDC}")
    show_metadata(filepath)
    
    print(f"\n{Colors.OKGREEN}{Colors.BOLD}[✓] Operation completed successfully{Colors.ENDC}")
    print(f"{Colors.GRAY}[*] Exiting Hades...{Colors.ENDC}\n")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n\n{Colors.WARNING}[!] Operation cancelled by user{Colors.ENDC}")
        sys.exit(0)
    except Exception as e:
        print(f"\n{Colors.FAIL}[!] Critical error: {e}{Colors.ENDC}")
        sys.exit(1)