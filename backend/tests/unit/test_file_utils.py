"""
Unit tests for file utilities.
"""

import pytest
import json
import os
from pathlib import Path

from app.utils.file_utils import FileUtils
from app.utils.exceptions import FileProcessingError


class TestFileUtils:
    """Tests for FileUtils class."""
    
    @pytest.mark.asyncio
    async def test_load_json(self, temp_test_dir):
        """Test loading JSON file."""
        # Create a test JSON file
        test_data = {"test": "data"}
        test_file = temp_test_dir / "test.json"
        with open(test_file, "w") as f:
            json.dump(test_data, f)
        
        # Test loading the file
        result = await FileUtils.load_json(test_file)
        assert result == test_data
    
    @pytest.mark.asyncio
    async def test_load_json_nonexistent_file(self):
        """Test loading nonexistent JSON file."""
        with pytest.raises(FileProcessingError):
            await FileUtils.load_json(Path("nonexistent.json"))
    
    @pytest.mark.asyncio
    async def test_load_json_invalid_json(self, temp_test_dir):
        """Test loading invalid JSON file."""
        # Create an invalid JSON file
        test_file = temp_test_dir / "invalid.json"
        with open(test_file, "w") as f:
            f.write("not valid json")
        
        with pytest.raises(FileProcessingError):
            await FileUtils.load_json(test_file)
    
    @pytest.mark.asyncio
    async def test_save_json(self, temp_test_dir):
        """Test saving JSON file."""
        # Test data to save
        test_data = {"test": "data"}
        test_file = temp_test_dir / "save_test.json"
        
        # Save the data
        await FileUtils.save_json(test_data, test_file)
        
        # Verify the file exists and contains the correct data
        assert test_file.exists()
        with open(test_file, "r") as f:
            saved_data = json.load(f)
        assert saved_data == test_data
    
    @pytest.mark.asyncio
    async def test_save_json_create_directory(self, temp_test_dir):
        """Test saving JSON file with directory creation."""
        # Test data to save in a nested directory
        test_data = {"test": "data"}
        nested_dir = temp_test_dir / "nested" / "dir"
        test_file = nested_dir / "save_test.json"
        
        # Save the data (should create directories)
        await FileUtils.save_json(test_data, test_file)
        
        # Verify the file exists and contains the correct data
        assert test_file.exists()
        with open(test_file, "r") as f:
            saved_data = json.load(f)
        assert saved_data == test_data
    
    @pytest.mark.asyncio
    async def test_save_json_permission_error(self, temp_test_dir, monkeypatch):
        """Test saving JSON file with permission error."""
        # Mock os.makedirs to raise PermissionError
        def mock_makedirs(*args, **kwargs):
            raise PermissionError("Permission denied")
        
        monkeypatch.setattr(os, "makedirs", mock_makedirs)
        
        # Test data to save
        test_data = {"test": "data"}
        test_file = temp_test_dir / "permission_error.json"
        
        with pytest.raises(FileProcessingError):
            await FileUtils.save_json(test_data, test_file)
    
    def test_is_valid_json_file(self):
        """Test checking if a file is a valid JSON file."""
        assert FileUtils.is_valid_json_file("test.json") is True
        assert FileUtils.is_valid_json_file("test.JSON") is True
        assert FileUtils.is_valid_json_file("test.txt") is False
        assert FileUtils.is_valid_json_file("test") is False
    
    @pytest.mark.asyncio
    async def test_read_file(self, temp_test_dir):
        """Test reading a file."""
        # Create a test file
        test_content = "test content"
        test_file = temp_test_dir / "test.txt"
        with open(test_file, "w") as f:
            f.write(test_content)
        
        # Test reading the file
        result = await FileUtils.read_file(test_file)
        assert result == test_content
    
    @pytest.mark.asyncio
    async def test_read_file_nonexistent(self):
        """Test reading a nonexistent file."""
        with pytest.raises(FileProcessingError):
            await FileUtils.read_file(Path("nonexistent.txt"))
    
    @pytest.mark.asyncio
    async def test_write_file(self, temp_test_dir):
        """Test writing a file."""
        # Test content to write
        test_content = "test content"
        test_file = temp_test_dir / "write_test.txt"
        
        # Write the content
        await FileUtils.write_file(test_content, test_file)
        
        # Verify the file exists and contains the correct content
        assert test_file.exists()
        with open(test_file, "r") as f:
            saved_content = f.read()
        assert saved_content == test_content
    
    @pytest.mark.asyncio
    async def test_write_file_create_directory(self, temp_test_dir):
        """Test writing a file with directory creation."""
        # Test content to write in a nested directory
        test_content = "test content"
        nested_dir = temp_test_dir / "nested" / "dir"
        test_file = nested_dir / "write_test.txt"
        
        # Write the content (should create directories)
        await FileUtils.write_file(test_content, test_file)
        
        # Verify the file exists and contains the correct content
        assert test_file.exists()
        with open(test_file, "r") as f:
            saved_content = f.read()
        assert saved_content == test_content 