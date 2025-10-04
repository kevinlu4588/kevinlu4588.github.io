"""
Download GitHub and LinkedIn icons for website buttons
"""
import urllib.request
import os

icons = {
    'github.svg': 'https://cdn.simpleicons.org/github/1a2332',
    'linkedin.svg': 'https://cdn.simpleicons.org/linkedin/1a2332',
    'email.svg': 'https://cdn.simpleicons.org/gmail/1a2332'
}

os.makedirs('icons', exist_ok=True)

for filename, url in icons.items():
    try:
        print(f"Downloading {filename}...")
        urllib.request.urlretrieve(url, f'icons/{filename}')
        print(f"✓ {filename} downloaded")
    except Exception as e:
        print(f"✗ Failed to download {filename}: {e}")

print("\nIcons saved to icons/ directory")
