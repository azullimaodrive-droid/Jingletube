"""
YouTube URL Parser Module

This module provides functionality for parsing YouTube URLs, extracting video IDs,
and generating various YouTube-related URLs including video URLs and thumbnail URLs.
"""

import re
from typing import Optional, Dict
from urllib.parse import urlparse, parse_qs


class YouTubeParser:
    """Parser for YouTube URLs and video identifiers."""

    # YouTube URL patterns
    PATTERNS = {
        'youtube_standard': r'(?:https?://)?(?:www\.)?youtube\.com/watch\?.*v=([a-zA-Z0-9_-]{11})',
        'youtube_short': r'(?:https?://)?(?:www\.)?youtu\.be/([a-zA-Z0-9_-]{11})',
        'youtube_embed': r'(?:https?://)?(?:www\.)?youtube\.com/embed/([a-zA-Z0-9_-]{11})',
        'youtube_nocookie': r'(?:https?://)?(?:www\.)?youtube-nocookie\.com/embed/([a-zA-Z0-9_-]{11})',
        'video_id_only': r'^([a-zA-Z0-9_-]{11})$',
    }

    # YouTube base URLs
    BASE_URLS = {
        'video': 'https://www.youtube.com/watch?v=',
        'short': 'https://youtu.be/',
        'embed': 'https://www.youtube.com/embed/',
        'nocookie': 'https://www.youtube-nocookie.com/embed/',
    }

    # Thumbnail URL templates
    THUMBNAIL_URLS = {
        'default': 'https://img.youtube.com/vi/{video_id}/default.jpg',
        'mqdefault': 'https://img.youtube.com/vi/{video_id}/mqdefault.jpg',
        'hqdefault': 'https://img.youtube.com/vi/{video_id}/hqdefault.jpg',
        'sddefault': 'https://img.youtube.com/vi/{video_id}/sddefault.jpg',
        'maxresdefault': 'https://img.youtube.com/vi/{video_id}/maxresdefault.jpg',
    }

    @classmethod
    def extract_video_id(cls, url_or_id: str) -> Optional[str]:
        """
        Extract video ID from a YouTube URL or validate if input is a video ID.

        Args:
            url_or_id: A YouTube URL or video ID string

        Returns:
            The video ID if found, None otherwise

        Examples:
            >>> YouTubeParser.extract_video_id('https://www.youtube.com/watch?v=dQw4w9WgXcQ')
            'dQw4w9WgXcQ'
            >>> YouTubeParser.extract_video_id('https://youtu.be/dQw4w9WgXcQ')
            'dQw4w9WgXcQ'
            >>> YouTubeParser.extract_video_id('dQw4w9WgXcQ')
            'dQw4w9WgXcQ'
        """
        if not url_or_id or not isinstance(url_or_id, str):
            return None

        url_or_id = url_or_id.strip()

        # Try each pattern in order
        for pattern_name, pattern in cls.PATTERNS.items():
            match = re.search(pattern, url_or_id)
            if match:
                return match.group(1)

        return None

    @classmethod
    def is_valid_video_id(cls, video_id: str) -> bool:
        """
        Validate if a string is a valid YouTube video ID.

        Args:
            video_id: The video ID to validate

        Returns:
            True if valid, False otherwise

        Examples:
            >>> YouTubeParser.is_valid_video_id('dQw4w9WgXcQ')
            True
            >>> YouTubeParser.is_valid_video_id('invalid')
            False
        """
        if not video_id or not isinstance(video_id, str):
            return False

        return bool(re.match(cls.PATTERNS['video_id_only'], video_id))

    @classmethod
    def generate_url(cls, video_id: str, url_type: str = 'video') -> Optional[str]:
        """
        Generate a YouTube URL from a video ID.

        Args:
            video_id: The YouTube video ID
            url_type: Type of URL to generate ('video', 'short', 'embed', 'nocookie')

        Returns:
            The generated URL if video_id is valid, None otherwise

        Examples:
            >>> YouTubeParser.generate_url('dQw4w9WgXcQ', 'video')
            'https://www.youtube.com/watch?v=dQw4w9WgXcQ'
            >>> YouTubeParser.generate_url('dQw4w9WgXcQ', 'short')
            'https://youtu.be/dQw4w9WgXcQ'
        """
        if not cls.is_valid_video_id(video_id):
            return None

        if url_type not in cls.BASE_URLS:
            return None

        return cls.BASE_URLS[url_type] + video_id

    @classmethod
    def generate_thumbnail_url(
        cls,
        video_id: str,
        quality: str = 'hqdefault'
    ) -> Optional[str]:
        """
        Generate a YouTube video thumbnail URL.

        Args:
            video_id: The YouTube video ID
            quality: Thumbnail quality ('default', 'mqdefault', 'hqdefault', 'sddefault', 'maxresdefault')

        Returns:
            The thumbnail URL if video_id is valid, None otherwise

        Available qualities:
            - 'default': 120x90 pixels
            - 'mqdefault': 320x180 pixels
            - 'hqdefault': 480x360 pixels (default)
            - 'sddefault': 640x480 pixels
            - 'maxresdefault': 1280x720 pixels (not always available)

        Examples:
            >>> YouTubeParser.generate_thumbnail_url('dQw4w9WgXcQ')
            'https://img.youtube.com/vi/dQw4w9WgXcQ/hqdefault.jpg'
            >>> YouTubeParser.generate_thumbnail_url('dQw4w9WgXcQ', 'maxresdefault')
            'https://img.youtube.com/vi/dQw4w9WgXcQ/maxresdefault.jpg'
        """
        if not cls.is_valid_video_id(video_id):
            return None

        if quality not in cls.THUMBNAIL_URLS:
            return None

        return cls.THUMBNAIL_URLS[quality].format(video_id=video_id)

    @classmethod
    def get_all_thumbnail_urls(cls, video_id: str) -> Optional[Dict[str, str]]:
        """
        Get all available thumbnail URLs for a video.

        Args:
            video_id: The YouTube video ID

        Returns:
            A dictionary with quality keys and thumbnail URLs, or None if video_id is invalid

        Examples:
            >>> urls = YouTubeParser.get_all_thumbnail_urls('dQw4w9WgXcQ')
            >>> urls['hqdefault']
            'https://img.youtube.com/vi/dQw4w9WgXcQ/hqdefault.jpg'
        """
        if not cls.is_valid_video_id(video_id):
            return None

        return {
            quality: url_template.format(video_id=video_id)
            for quality, url_template in cls.THUMBNAIL_URLS.items()
        }

    @classmethod
    def parse_url(cls, url: str) -> Optional[Dict[str, str]]:
        """
        Parse a YouTube URL and extract comprehensive information.

        Args:
            url: A YouTube URL

        Returns:
            A dictionary with parsed information (video_id, video_url, short_url,
            embed_url, thumbnail_url) or None if URL is invalid

        Examples:
            >>> info = YouTubeParser.parse_url('https://www.youtube.com/watch?v=dQw4w9WgXcQ')
            >>> info['video_id']
            'dQw4w9WgXcQ'
            >>> info['short_url']
            'https://youtu.be/dQw4w9WgXcQ'
        """
        video_id = cls.extract_video_id(url)
        if not video_id:
            return None

        return {
            'video_id': video_id,
            'video_url': cls.generate_url(video_id, 'video'),
            'short_url': cls.generate_url(video_id, 'short'),
            'embed_url': cls.generate_url(video_id, 'embed'),
            'nocookie_url': cls.generate_url(video_id, 'nocookie'),
            'thumbnail_url': cls.generate_thumbnail_url(video_id),
            'all_thumbnails': cls.get_all_thumbnail_urls(video_id),
        }

    @classmethod
    def get_video_parameters(cls, url: str) -> Optional[Dict[str, str]]:
        """
        Extract query parameters from a YouTube video URL.

        Args:
            url: A YouTube URL

        Returns:
            A dictionary of query parameters or None if URL is invalid

        Examples:
            >>> params = YouTubeParser.get_video_parameters('https://www.youtube.com/watch?v=dQw4w9WgXcQ&t=10s')
            >>> params.get('t')
            ['10s']
        """
        try:
            parsed = urlparse(url)
            if 'youtube.com' not in parsed.netloc and 'youtu.be' not in parsed.netloc:
                return None

            return parse_qs(parsed.query) if parsed.query else {}
        except Exception:
            return None


# Convenience functions for direct usage
def extract_video_id(url_or_id: str) -> Optional[str]:
    """Extract video ID from a YouTube URL or validate a video ID."""
    return YouTubeParser.extract_video_id(url_or_id)


def generate_url(video_id: str, url_type: str = 'video') -> Optional[str]:
    """Generate a YouTube URL from a video ID."""
    return YouTubeParser.generate_url(video_id, url_type)


def generate_thumbnail_url(video_id: str, quality: str = 'hqdefault') -> Optional[str]:
    """Generate a YouTube thumbnail URL."""
    return YouTubeParser.generate_thumbnail_url(video_id, quality)


def get_all_thumbnail_urls(video_id: str) -> Optional[Dict[str, str]]:
    """Get all available thumbnail URLs for a video."""
    return YouTubeParser.get_all_thumbnail_urls(video_id)


def parse_url(url: str) -> Optional[Dict[str, str]]:
    """Parse a YouTube URL and extract comprehensive information."""
    return YouTubeParser.parse_url(url)
