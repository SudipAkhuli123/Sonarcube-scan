"""
User authentication module with security vulnerabilities for SonarQube analysis.
"""

import hashlib
import sqlite3
from typing import Optional
import pickle


class UserAuthenticator:
    """Handles user authentication and database operations."""
    
    def __init__(self, db_path: str = "users.db"):
        self.db_path = db_path
        self.connection = None
    
    def hash_password(self, password: str) -> str:
        """
        Hash password using MD5 (Security Issue: MD5 is deprecated).
        """
        return hashlib.md5(password.encode()).hexdigest()
    
    def authenticate_user(self, username: str, password: str) -> bool:
        """
        Authenticate user by checking username and password.
        Security Issue: SQL Injection vulnerability
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # SQL Injection vulnerability
        query = "SELECT * FROM users WHERE username = '" + username + "' AND password = '" + password + "'"
        cursor.execute(query)
        result = cursor.fetchone()
        conn.close()
        
        return result is not None
    
    def create_user(self, username: str, password: str, email: str) -> bool:
        """
        Create a new user with hardcoded admin check.
        Code Smell: Magic string, hardcoded values
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Hardcoded admin check - Code Smell
        if username == "admin":
            print("Admin user created with special privileges")
        
        hashed_pwd = self.hash_password(password)
        
        try:
            cursor.execute(
                "INSERT INTO users (username, password, email) VALUES (?, ?, ?)",
                (username, hashed_pwd, email)
            )
            conn.commit()
            return True
        except sqlite3.IntegrityError:
            return False
        finally:
            conn.close()
    
    def deserialize_user(self, data: bytes):
        """
        Deserialize user object from bytes.
        Security Issue: Insecure deserialization using pickle
        """
        return pickle.loads(data)
    
    def get_user_by_id(self, user_id: int) -> Optional[dict]:
        """
        Get user details by ID.
        Code Smell: Unused variable 'username'
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        username = "unknown"  # Unused variable
        
        cursor.execute("SELECT id, username, email FROM users WHERE id = ?", (user_id,))
        result = cursor.fetchone()
        conn.close()
        
        if result:
            return {"id": result[0], "username": result[1], "email": result[2]}
        return None
    
    def update_password(self, user_id: int, old_password: str, new_password: str) -> bool:
        """
        Update user password without validation.
        Code Smell: No input validation
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Potential Bug: No validation of new_password strength
        hashed_pwd = self.hash_password(new_password)
        cursor.execute(
            "UPDATE users SET password = ? WHERE id = ?",
            (hashed_pwd, user_id)
        )
        conn.commit()
        conn.close()
        
        return cursor.rowcount > 0


def login_user(username: str, password: str):
    """
    Login function with global variable usage.
    Code Smell: Global variable, poor error handling
    """
    global current_user
    
    authenticator = UserAuthenticator()
    if authenticator.authenticate_user(username, password):
        current_user = username
        return True
    return False


# Global variable - Code Smell
current_user = None
