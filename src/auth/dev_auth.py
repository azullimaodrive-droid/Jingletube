"""
Development mode authentication module.

This module provides a DevAuth class for handling authentication
in development environments with simplified credentials and debugging features.
"""

import logging
from typing import Optional, Dict, Any
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)


class DevAuth:
    """
    Development mode authentication handler.
    
    Provides simplified authentication for development and testing purposes,
    with built-in debugging capabilities and relaxed security constraints.
    """
    
    # Default development credentials
    DEFAULT_DEV_USER = "dev_user"
    DEFAULT_DEV_PASSWORD = "dev_password"
    DEFAULT_DEV_TOKEN = "dev_token_12345"
    DEFAULT_TOKEN_EXPIRY_HOURS = 24
    
    def __init__(
        self,
        username: Optional[str] = None,
        password: Optional[str] = None,
        token_expiry_hours: int = DEFAULT_TOKEN_EXPIRY_HOURS,
        debug: bool = True
    ):
        """
        Initialize DevAuth instance.
        
        Args:
            username: Development username (defaults to DEFAULT_DEV_USER)
            password: Development password (defaults to DEFAULT_DEV_PASSWORD)
            token_expiry_hours: Token expiration time in hours
            debug: Enable debug logging
        """
        self.username = username or self.DEFAULT_DEV_USER
        self.password = password or self.DEFAULT_DEV_PASSWORD
        self.token_expiry_hours = token_expiry_hours
        self.debug = debug
        self.token = None
        self.token_created_at = None
        self.is_authenticated = False
        
        if self.debug:
            logger.info(f"DevAuth initialized for user: {self.username}")
    
    def authenticate(self) -> bool:
        """
        Perform development mode authentication.
        
        In development mode, authentication is always successful
        with default or provided credentials.
        
        Returns:
            True if authentication succeeds, False otherwise
        """
        try:
            self.token = self.DEFAULT_DEV_TOKEN
            self.token_created_at = datetime.utcnow()
            self.is_authenticated = True
            
            if self.debug:
                logger.info(
                    f"Authentication successful for user: {self.username}"
                )
            
            return True
        except Exception as e:
            if self.debug:
                logger.error(f"Authentication failed: {str(e)}")
            return False
    
    def get_token(self) -> Optional[str]:
        """
        Get the current authentication token.
        
        Returns:
            The authentication token if authenticated, None otherwise
        """
        if self.is_token_valid():
            return self.token
        return None
    
    def is_token_valid(self) -> bool:
        """
        Check if the current token is valid and not expired.
        
        Returns:
            True if token is valid and not expired, False otherwise
        """
        if not self.is_authenticated or not self.token or not self.token_created_at:
            return False
        
        expiry_time = self.token_created_at + timedelta(hours=self.token_expiry_hours)
        is_valid = datetime.utcnow() < expiry_time
        
        if self.debug and not is_valid:
            logger.warning(f"Token expired at {expiry_time}")
        
        return is_valid
    
    def refresh_token(self) -> bool:
        """
        Refresh the authentication token.
        
        Returns:
            True if token is refreshed successfully, False otherwise
        """
        if not self.is_authenticated:
            if self.debug:
                logger.warning("Cannot refresh token: not authenticated")
            return False
        
        try:
            self.token_created_at = datetime.utcnow()
            
            if self.debug:
                logger.info(f"Token refreshed for user: {self.username}")
            
            return True
        except Exception as e:
            if self.debug:
                logger.error(f"Token refresh failed: {str(e)}")
            return False
    
    def logout(self) -> bool:
        """
        Logout and clear authentication data.
        
        Returns:
            True if logout is successful
        """
        try:
            self.token = None
            self.token_created_at = None
            self.is_authenticated = False
            
            if self.debug:
                logger.info(f"User {self.username} logged out")
            
            return True
        except Exception as e:
            if self.debug:
                logger.error(f"Logout failed: {str(e)}")
            return False
    
    def get_auth_headers(self) -> Optional[Dict[str, str]]:
        """
        Get HTTP headers for authenticated requests.
        
        Returns:
            Dictionary of authorization headers if authenticated, None otherwise
        """
        token = self.get_token()
        if token:
            return {
                "Authorization": f"Bearer {token}",
                "X-Dev-Auth": "true"
            }
        return None
    
    def get_credentials(self) -> Dict[str, Any]:
        """
        Get current authentication credentials and status.
        
        Returns:
            Dictionary containing credential and status information
        """
        return {
            "username": self.username,
            "is_authenticated": self.is_authenticated,
            "token_valid": self.is_token_valid(),
            "token_expiry_hours": self.token_expiry_hours,
            "created_at": self.token_created_at.isoformat() if self.token_created_at else None,
            "debug_mode": self.debug
        }
