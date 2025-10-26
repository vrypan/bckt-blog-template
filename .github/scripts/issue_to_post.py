#!/usr/bin/env python3
"""
Convert a GitHub issue to a bckt blog post.

This script extracts issue metadata, downloads images, and creates a properly
formatted blog post in the bckt folder structure.
"""

import json
import os
import re
import sys
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from urllib.parse import urlparse

import requests
import yaml


def slugify(text: str) -> str:
    """Convert text to a URL-friendly slug."""
    text = text.lower()
    text = re.sub(r'[^a-z0-9]+', '-', text)
    text = text.strip('-')
    return text


def parse_frontmatter(body: str) -> Tuple[Optional[Dict], str]:
    """
    Parse frontmatter from issue body if present.

    Returns:
        Tuple of (frontmatter_dict, remaining_body)
    """
    if not body.startswith('---\n'):
        return None, body

    # Find the closing ---
    parts = body.split('\n---\n', 2)
    if len(parts) < 2:
        return None, body

    try:
        frontmatter = yaml.safe_load(parts[1])
        remaining_body = parts[2] if len(parts) > 2 else ''
        return frontmatter, remaining_body
    except yaml.YAMLError as e:
        print(f"Warning: Failed to parse frontmatter: {e}", file=sys.stderr)
        return None, body


def extract_image_urls(markdown: str) -> List[str]:
    """Extract all image URLs from markdown content."""
    # Match markdown images: ![alt](url)
    markdown_images = re.findall(r'!\[([^\]]*)\]\((https://[^)]+)\)', markdown)
    urls = [url for _, url in markdown_images]

    # Also match HTML img tags: <img src="url">
    html_images = re.findall(r'<img[^>]+src=["\'](https://[^"\']+)["\']', markdown)
    urls.extend(html_images)

    return urls


def download_image(url: str, output_path: Path) -> bool:
    """
    Download an image from URL to output_path.

    Returns:
        True if successful, False otherwise
    """
    try:
        response = requests.get(url, timeout=30)
        response.raise_for_status()

        output_path.parent.mkdir(parents=True, exist_ok=True)
        with open(output_path, 'wb') as f:
            f.write(response.content)

        print(f"Downloaded: {url} -> {output_path}")
        return True
    except Exception as e:
        print(f"Warning: Failed to download {url}: {e}", file=sys.stderr)
        return False


def get_file_extension(url: str) -> str:
    """Extract file extension from URL, defaulting to .png."""
    parsed = urlparse(url)
    path = parsed.path

    # Remove query parameters
    path = path.split('?')[0]

    # Get extension
    ext = Path(path).suffix
    if ext and len(ext) <= 5:  # Valid extension like .jpg, .png, .jpeg
        return ext

    return '.png'


def process_images(body: str, post_folder: Path) -> Tuple[str, List[str]]:
    """
    Download images and update markdown references.

    Returns:
        Tuple of (updated_body, list_of_image_filenames)
    """
    image_urls = extract_image_urls(body)
    if not image_urls:
        return body, []

    image_filenames = []
    updated_body = body

    for i, url in enumerate(image_urls, 1):
        ext = get_file_extension(url)
        filename = f"image{i}{ext}"
        output_path = post_folder / filename

        if download_image(url, output_path):
            # Replace URL with relative filename in body
            updated_body = updated_body.replace(url, filename)
            image_filenames.append(filename)

    return updated_body, image_filenames


def create_post_frontmatter(
    issue: Dict,
    custom_frontmatter: Optional[Dict],
    attached_files: List[str],
    slug: str
) -> Dict:
    """
    Create the post frontmatter by merging auto-generated and custom fields.
    """
    # Auto-generated frontmatter
    frontmatter = {
        'title': issue['title'],
        'date': issue['created_at'],
        'author': issue['user']['login'],
        'issue': issue['number'],
        'slug': slug
    }

    # Extract tags from labels (excluding 'publish')
    tags = [label['name'] for label in issue['labels'] if label['name'] != 'publish']
    if tags:
        frontmatter['tags'] = tags

    # Add attached files if any
    if attached_files:
        frontmatter['attached'] = attached_files

    # Merge with custom frontmatter (custom takes precedence for non-auto fields)
    if custom_frontmatter:
        # Don't let custom frontmatter override issue number or attached files
        protected_fields = {'issue', 'attached'}
        for key, value in custom_frontmatter.items():
            if key not in protected_fields:
                frontmatter[key] = value

    return frontmatter


def write_post(post_folder: Path, frontmatter: Dict, body: str):
    """Write the post to index.md with proper frontmatter."""
    index_path = post_folder / 'index.md'

    with open(index_path, 'w', encoding='utf-8') as f:
        f.write('---\n')
        yaml.dump(frontmatter, f, default_flow_style=False, allow_unicode=True, sort_keys=False)
        f.write('---\n\n')
        f.write(body)

    print(f"Created post: {index_path}")


def main():
    """Main entry point."""
    # Get issue data from environment
    issue_json = os.getenv('ISSUE_JSON')
    if not issue_json:
        print("Error: ISSUE_JSON environment variable not set", file=sys.stderr)
        sys.exit(1)

    try:
        issue = json.loads(issue_json)
    except json.JSONDecodeError as e:
        print(f"Error: Failed to parse ISSUE_JSON: {e}", file=sys.stderr)
        sys.exit(1)

    # Extract date components for folder structure
    created_at = datetime.fromisoformat(issue['created_at'].replace('Z', '+00:00'))
    year = created_at.strftime('%Y')
    date_prefix = created_at.strftime('%y%m%d')

    # Create slug from title
    slug = slugify(issue['title'])

    # Create post folder: posts/YYYY/YYMMDD-slug/
    post_folder = Path('posts') / year / f"{date_prefix}-{slug}"
    post_folder.mkdir(parents=True, exist_ok=True)

    print(f"Processing issue #{issue['number']}: {issue['title']}")
    print(f"Post folder: {post_folder}")

    # Parse frontmatter from issue body
    custom_frontmatter, body = parse_frontmatter(issue['body'] or '')

    # Process images
    body, image_filenames = process_images(body, post_folder)

    # Create frontmatter
    frontmatter = create_post_frontmatter(issue, custom_frontmatter, image_filenames, slug)

    # Write post
    write_post(post_folder, frontmatter, body)

    # Export post folder path for workflow
    github_env = os.getenv('GITHUB_ENV')
    if github_env:
        with open(github_env, 'a') as f:
            f.write(f"POST_FOLDER={post_folder}\n")

    print(f"✅ Successfully created post at {post_folder}")


if __name__ == '__main__':
    main()
