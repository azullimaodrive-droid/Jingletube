"""
HuggingFace OAuth Authentication Module

This module provides OAuth authentication functionality for integrating
with HuggingFace services using the OAuth2 protocol.
"""

import os
import json
import hashlib
import secrets
from typing import Optional, Dict, Any
from urllib.parse import urlencode, parse_qs, urlparse
import requests


class HFOAuth:
    """
    HuggingFace OAuth2 authentication handler.
    
    This class manages the OAuth2 authentication flow for HuggingFace,
    including authorization request generation, token exchange, and
    user information retrieval.
    """
    
    # HuggingFace OAuth endpoints
    HF_AUTHORIZE_URL = "https://huggingface.co/oauth/authorize"
    HF_TOKEN_URL = "https://huggingface.co/oauth/token"
    HF_USER_INFO_URL = "https://huggingface.co/api/user"
    
    def __init__(
        self,
        client_id: str,
        client_secret: str,
        redirect_uri: str,
        scope: Optional[str] = None
    ):
        """
        Initialize HuggingFace OAuth handler.
        
        Args:
            client_id: HuggingFace OAuth application client ID
            client_secret: HuggingFace OAuth application client secret
            redirect_uri: Redirect URI registered with HuggingFace
            scope: OAuth scopes to request (space-separated)
        """
        self.client_id = client_id
        self.client_secret = client_secret
        self.redirect_uri = redirect_uri
        self.scope = scope or "openid profile email"
        self.state = None
        self.code_verifier = None
        
    def _generate_state(self) -> str:
        """
        Generate a secure random state parameter for CSRF protection.
        
        Returns:
            Random state string
        """
        self.state = secrets.token_urlsafe(32)
        return self.state
    
    def _generate_pkce_verifier(self) -> str:
        """
        Generate a PKCE code verifier for enhanced security.
        
        Returns:
            Base64-encoded code verifier
        """
        self.code_verifier = secrets.token_urlsafe(32)
        return self.code_verifier
    
    def _generate_pkce_challenge(self, verifier: str) -> str:
        """
        Generate a PKCE code challenge from a verifier.
        
        Args:
            verifier: PKCE code verifier
            
        Returns:
            Base64-encoded code challenge
        """
        challenge = hashlib.sha256(verifier.encode()).digest()
        return hashlib.sha256(challenge).hexdigest()
    
    def get_authorization_url(self, use_pkce: bool = True) -> str:
        """
        Generate the authorization URL for initiating OAuth flow.
        
        Args:
            use_pkce: Whether to use PKCE flow for enhanced security
            
        Returns:
            Authorization URL to redirect user to
        """
        self._generate_state()
        
        params = {
            "client_id": self.client_id,
            "redirect_uri": self.redirect_uri,
            "response_type": "code",
            "scope": self.scope,
            "state": self.state,
        }
        
        if use_pkce:
            verifier = self._generate_pkce_verifier()
            params["code_challenge"] = self._generate_pkce_challenge(verifier)
            params["code_challenge_method"] = "S256"
        
        return f"{self.HF_AUTHORIZE_URL}?{urlencode(params)}"
    
    def validate_state(self, state: str) -> bool:
        """
        Validate the state parameter from OAuth callback.
        
        Args:
            state: State parameter from callback
            
        Returns:
            True if state is valid, False otherwise
        """
        return state == self.state
    
    def exchange_code_for_token(
        self,
        code: str,
        state: Optional[str] = None
    ) -> Optional[Dict[str, Any]]:
        """
        Exchange authorization code for access token.
        
        Args:
            code: Authorization code from callback
            state: State parameter from callback (optional for validation)
            
        Returns:
            Token response dictionary or None if exchange fails
        """
        if state and not self.validate_state(state):
            raise ValueError("Invalid state parameter")
        
        payload = {
            "client_id": self.client_id,
            "client_secret": self.client_secret,
            "code": code,
            "grant_type": "authorization_code",
            "redirect_uri": self.redirect_uri,
        }
        
        if self.code_verifier:
            payload["code_verifier"] = self.code_verifier
        
        try:
            response = requests.post(
                self.HF_TOKEN_URL,
                data=payload,
                timeout=10
            )
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            print(f"Error exchanging code for token: {e}")
            return None
    
    def get_user_info(self, access_token: str) -> Optional[Dict[str, Any]]:
        """
        Retrieve authenticated user information.
        
        Args:
            access_token: OAuth access token
            
        Returns:
            User information dictionary or None if request fails
        """
        headers = {
            "Authorization": f"Bearer {access_token}",
            "Accept": "application/json"
        }
        
        try:
            response = requests.get(
                self.HF_USER_INFO_URL,
                headers=headers,
                timeout=10
            )
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            print(f"Error retrieving user info: {e}")
            return None
    
    def refresh_token(self, refresh_token: str) -> Optional[Dict[str, Any]]:
        """
        Refresh an access token using a refresh token.
        
        Args:
            refresh_token: OAuth refresh token
            
        Returns:
            New token response dictionary or None if refresh fails
        """
        payload = {
            "client_id": self.client_id,
            "client_secret": self.client_secret,
            "grant_type": "refresh_token",
            "refresh_token": refresh_token,
        }
        
        try:
            response = requests.post(
                self.HF_TOKEN_URL,
                data=payload,
                timeout=10
            )
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            print(f"Error refreshing token: {e}")
            return None
    
    def revoke_token(self, token: str) -> bool:
        """
        Revoke an access or refresh token.
        
        Args:
            token: Token to revoke
            
        Returns:
            True if revocation was successful, False otherwise
        """
        payload = {
            "client_id": self.client_id,
            "client_secret": self.client_secret,
            "token": token,
        }
        
        try:
            response = requests.post(
                f"{self.HF_TOKEN_URL}/revoke",
                data=payload,
                timeout=10
            )
            response.raise_for_status()
            return True
        except requests.RequestException as e:
            print(f"Error revoking token: {e}")
            return False
    
    @staticmethod
    def create_from_env() -> "HFOAuth":
        """
        Create HFOAuth instance from environment variables.
        
        Expected environment variables:
            - HF_CLIENT_ID: HuggingFace OAuth client ID
            - HF_CLIENT_SECRET: HuggingFace OAuth client secret
            - HF_REDIRECT_URI: OAuth redirect URI
            - HF_SCOPE: OAuth scopes (optional)
            
        Returns:
            Configured HFOAuth instance
            
        Raises:
            ValueError: If required environment variables are missing
        """
        client_id = os.getenv("HF_CLIENT_ID")
        client_secret = os.getenv("HF_CLIENT_SECRET")
        redirect_uri = os.getenv("HF_REDIRECT_URI")
        
        if not all([client_id, client_secret, redirect_uri]):
            raise ValueError(
                "Missing required HuggingFace OAuth environment variables: "
                "HF_CLIENT_ID, HF_CLIENT_SECRET, HF_REDIRECT_URI"
            )
        
        scope = os.getenv("HF_SCOPE")
        return HFOAuth(client_id, client_secret, redirect_uri, scope)
