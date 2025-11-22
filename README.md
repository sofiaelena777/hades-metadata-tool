# 🔥 Hades - Advanced Metadata Manipulation Tool

<div align="center">

![Python](https://img.shields.io/badge/Python-3.8+-3776AB?style=for-the-badge&logo=python&logoColor=white)
![ExifTool](https://img.shields.io/badge/ExifTool-Required-green?style=for-the-badge)
![Forensics](https://img.shields.io/badge/Forensics-OSINT-red?style=for-the-badge&logo=hackaday&logoColor=white)

**Multi-format forensic metadata spoofing and manipulation utility**

[Features](#-features) • [Installation](#-installation) • [Usage](#-usage) • [File Support](#-supported-formats) • [Disclaimer](#-disclaimer)

</div>

---

## ⚠️ DISCLAIMER

This tool is designed for **legitimate forensic analysis, privacy protection, and authorized security testing ONLY**.

**Legal Use Cases:**
- ✅ Personal privacy protection on your own files
- ✅ Forensic research and education
- ✅ Authorized penetration testing
- ✅ OSINT training and demonstrations
- ✅ Digital rights management research
- ❌ Falsifying evidence in legal proceedings
- ❌ Creating misleading information
- ❌ Illegal surveillance or tracking evasion
- ❌ Copyright infringement or fraud

**The author is NOT responsible for any misuse, illegal activities, or consequences resulting from this software.**

---

## 📋 Overview

Hades is a powerful Python-based metadata manipulation tool that provides comprehensive control over file metadata across multiple formats. Built on ExifTool, it offers automated random metadata generation, custom metadata injection, complete metadata removal, and forensic-grade spoofing capabilities for images, videos, audio files, documents, and ebooks.

## ✨ Features

### 🎯 Core Functionality

**Complete Metadata Control:**
- **View** - Display all current metadata fields
- **Clean** - Remove all metadata completely
- **Inject** - Add custom or random metadata
- **Spoof** - Generate realistic fake metadata

**Smart Detection:**
- Automatic file type identification
- Format-specific metadata handling
- Validation of metadata integrity
- Filesystem timestamp modification

### 📸 Multi-Format Support

**Images** (JPEG, PNG, GIF, BMP, TIFF, WebP, HEIC, RAW formats)
- Camera make and model
- GPS coordinates (latitude/longitude)
- Creation/modification dates
- Software/editing tools
- EXIF, IPTC, XMP metadata
- Photographer information
- Copyright and licensing

**Videos** (MP4, AVI, MOV, MKV, WMV, FLV, WebM)
- Recording device information
- Video/audio codecs
- Duration and timestamps
- Editing software
- GPS location data
- Creator and copyright

**Audio** (MP3, WAV, FLAC, AAC, OGG, M4A)
- Artist and composer
- Album and genre
- Track metadata
- Recording software
- Duration information
- Copyright details

**Documents** (PDF, DOC, DOCX, ODT, RTF, TXT)
- Author and creator
- Title and subject
- Keywords and tags
- Creation/modification dates
- Software used
- Page count
- Producer information

**Ebooks** (EPUB, MOBI, AZW, AZW3)
- Author and title
- Publisher information
- ISBN numbers
- Genre and language
- Publication dates

### 🎲 Random Metadata Generation

**Realistic Spoofing with:**
- 24 common first names
- 24 common last names  
- 14 major companies
- 25 US cities with state mapping
- Camera makes and models (8+ brands)
- Professional software names
- Valid date ranges (last 5 years)
- Proper GPS coordinates (US bounds)
- Industry-standard codecs
- Authentic ISBNs and genres

**Camera/Device Database:**
- Canon: 5+ models (EOS series, PowerShot)
- Nikon: 5+ models (D-series, Z-series)
- Sony: 5+ models (Alpha series, RX)
- Fujifilm, Olympus, Panasonic, Leica, Pentax
- Professional video cameras (RED, ARRI, Blackmagic)
- Consumer devices (GoPro, DJI drones)

**Software Database:**
- Adobe Creative Suite (Photoshop, Premiere, Audition)
- Professional tools (Final Cut Pro, Logic Pro, DaVinci Resolve)
- Open source alternatives (GIMP, Audacity, Inkscape)
- Office suites (Microsoft Office, LibreOffice, Google Workspace)

### ✏️ Custom Metadata Editor

**Manual Input for:**
- Author/creator name
- Creation and modification dates
- Title and description
- Copyright information
- Location data (city, state, country)
- GPS coordinates
- Device information
- Technical details (codecs, duration, pages)
- Keywords and tags

**Smart Validation:**
- Date format verification (YYYY:MM:DD HH:MM:SS)
- GPS coordinate validation
- Range checking for numeric values
- Type-specific field requirements

### 🔒 Advanced Features

**Forensic-Grade Operations:**
- Filesystem timestamp modification
- EXIF/IPTC/XMP tag manipulation
- Backup prevention (overwrites originals)
- Progress indicators for operations
- Colored terminal output
- Error handling and validation

**Multi-Standard Support:**
- EXIF (Exchangeable Image File Format)
- IPTC (International Press Telecommunications Council)
- XMP (Extensible Metadata Platform)
- ID3 tags (audio files)
- PDF metadata standards

## 🚀 Installation

### Prerequisites

**System Requirements:**
- Python 3.8 or higher
- ExifTool installed
- Linux, macOS, or Windows
- Terminal with UTF-8 support

### Install ExifTool

**Linux (Debian/Ubuntu):**
```bash
sudo apt update
sudo apt install libimage-exiftool-perl
```

**macOS (Homebrew):**
```bash
brew install exiftool
```

**Windows:**
1. Download from [exiftool.org](https://exiftool.org/)
2. Extract to C:\Windows or add to PATH
3. Rename `exiftool(-k).exe` to `exiftool.exe`

### Install Hades

```bash
# Clone repository
git clone https://github.com/sofiaelena777/hades-metadata-tool.git
cd hades-metadata-tool

# Make executable (Linux/macOS)
chmod +x hades.py

# Run
python3 hades.py
```

## 📖 Usage

### Basic Usage

**Interactive Mode:**
```bash
python3 hades.py
```

**With File Argument:**
```bash
python3 hades.py /path/to/file.jpg
```

### Workflow Example

1. **Launch Hades:**
```bash
python3 hades.py photo.jpg
```

2. **View Current Metadata:**
- Automatically displays on launch
- Shows all EXIF/IPTC/XMP fields

3. **Clean Metadata (Optional):**
```
[?] Clean all metadata? (y/n): y
```

4. **Choose Injection Method:**
```
[1] Manual input    - Enter custom values
[2] Random generation - Auto-generate realistic data
[3] Skip           - No injection
```

5. **Review and Confirm:**
- Summary table displays all changes
- Confirm injection with 'y'

6. **Verify Results:**
- Final metadata state displayed
- File ready for use

### Use Case Examples

**Privacy Protection:**
```bash
# Remove all metadata from personal photos
python3 hades.py vacation_photo.jpg
# Choose: Clean metadata → Skip injection
```

**Forensic Training:**
```bash
# Generate realistic test data
python3 hades.py training_sample.mp4
# Choose: Clean → Random generation
```

**OSINT Research:**
```bash
# Create controlled test files
python3 hades.py research_doc.pdf
# Choose: Clean → Manual input (specific values)
```

**Anonymization:**
```bash
# Remove tracking before sharing
python3 hades.py document.docx
# Clean all metadata
```

## 📂 Supported Formats

### Images
```
.jpg .jpeg .png .gif .bmp .tiff .tif .webp .heic 
.raw .cr2 .nef .arw .dng
```

### Videos
```
.mp4 .avi .mov .mkv .wmv .flv .webm .m4v 
.mpg .mpeg .3gp .mts
```

### Audio
```
.mp3 .wav .flac .aac .ogg .m4a .wma .opus .aiff
```

### Documents
```
.pdf .doc .docx .odt .rtf .txt
```

### Ebooks
```
.epub .mobi .azw .azw3
```

## 🔍 Metadata Fields Reference

### Universal Fields
- **Author/Creator** - File creator name
- **Create Date** - Original creation timestamp
- **Modify Date** - Last modification timestamp
- **Title** - File title or name
- **Description** - File description
- **Copyright** - Copyright notice
- **City/State/Country** - Location information

### Image-Specific
- **Make** - Camera manufacturer
- **Model** - Camera model
- **Software** - Editing software
- **GPS Latitude/Longitude** - Exact coordinates
- **ISO Speed** - Camera sensitivity
- **Aperture** - F-stop value
- **Shutter Speed** - Exposure time

### Video-Specific
- **Duration** - Video length
- **Video Codec** - Compression format
- **Audio Codec** - Audio format
- **Frame Rate** - FPS
- **Resolution** - Video dimensions

### Audio-Specific
- **Artist** - Performing artist
- **Album** - Album name
- **Composer** - Music composer
- **Genre** - Music genre
- **Track Number** - Position in album
- **Bitrate** - Audio quality

### Document-Specific
- **Subject** - Document topic
- **Producer** - Creating software
- **Pages** - Page count
- **Keywords** - Search terms
- **Language** - Document language

## 🛡️ Security & Privacy

### Privacy Considerations

**Metadata Can Reveal:**
- ❌ Your exact location (GPS)
- ❌ Device serial numbers
- ❌ Software versions (vulnerabilities)
- ❌ Editing history
- ❌ Original filenames
- ❌ Camera settings (fingerprinting)
- ❌ Creation timeline

**Hades Helps By:**
- ✅ Removing all identifying information
- ✅ Spoofing location data
- ✅ Randomizing device information
- ✅ Clearing editing history
- ✅ Anonymizing timestamps

### Forensic Traces

**What Hades Modifies:**
- All embedded metadata tags
- Filesystem timestamps (optional)
- EXIF/IPTC/XMP fields
- Format-specific headers

**What Hades Doesn't Touch:**
- File content (pixels, audio, text)
- File size or dimensions
- Compression artifacts
- Steganographic data
- Filesystem journals

## 🔧 Advanced Usage

### Batch Processing Script

```bash
#!/bin/bash
# Clean all images in directory
for file in *.jpg; do
    echo "y" | python3 hades.py "$file" <<EOF
y
3
EOF
done
```

### Automated Random Spoofing

```bash
# Generate random metadata for all files
for file in *; do
    python3 hades.py "$file" <<EOF
y
2
y
EOF
done
```

### GPS Coordinate Generation

Custom coordinates for specific locations:
```python
# US bounds: Lat 25-49, Lon -125 to -66
# Major cities available in random generator
```

## 🐛 Troubleshooting

### ExifTool Not Found
```bash
# Verify installation
which exiftool
exiftool -ver

# Reinstall if needed
sudo apt install --reinstall libimage-exiftool-perl
```

### Permission Denied
```bash
# Check file permissions
ls -l file.jpg

# Make writable
chmod 644 file.jpg
```

### Date Format Errors
```
Correct format: 2024:01:15 14:30:00
Wrong formats: 
  - 2024-01-15 (missing time)
  - 01/15/2024 (wrong separators)
  - 2024:1:15 (missing leading zeros)
```

### Unicode/Encoding Issues
```bash
# Ensure UTF-8 terminal
export LANG=en_US.UTF-8

# Check file encoding
file -i document.txt
```

### Metadata Not Removed
Some formats have protected metadata:
```bash
# Try force mode
exiftool -all= -overwrite_original file.pdf

# Check if file is read-only
ls -l file.pdf
```

## 📊 Comparison

| Tool | Hades | ExifTool CLI | MAT2 | Metadata Cleaner |
|------|-------|--------------|------|------------------|
| GUI | ❌ | ❌ | ❌ | ✅ |
| Random Gen | ✅ | ❌ | ❌ | ❌ |
| Custom Input | ✅ | ✅ | ❌ | ❌ |
| Multi-format | ✅ | ✅ | ✅ | ✅ |
| GPS Spoofing | ✅ | ✅ | ❌ | ❌ |
| Batch Mode | ✅ | ✅ | ✅ | ✅ |
| User Friendly | ✅ | ❌ | ⚠️ | ✅ |
| Open Source | ✅ | ✅ | ✅ | ✅ |

## 🤝 Contributing

Contributions welcome! Areas for improvement:
- Additional file format support
- GUI interface
- Batch processing mode
- Metadata templates
- Profile saving/loading
- Integration with other tools

## 📜 License

MIT License

```
Copyright (c) 2024 sofiaelena777

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
```

## 👤 Author

**sofiaelena777**

- GitHub: [@sofiaelena777](https://github.com/sofiaelena777)

## 🙏 Acknowledgments

- ExifTool by Phil Harvey
- Python community
- Digital forensics researchers
- Privacy advocates

---

<div align="center">

**🔥 Privacy First | 🔒 Forensic Grade | ⚡ Multi-Format**

Made with ❤️ by sofiaelena777

</div>
