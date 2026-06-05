"""
Data processing module with code quality issues for SonarQube analysis.
"""

import os
import json
from typing import List, Dict, Any
import logging


class DataProcessor:
    """Process and transform data with various code issues."""
    
    def __init__(self):
        self.data = []
        self.cache = {}
        self.counter = 0
    
    def process_csv(self, file_path: str) -> List[Dict]:
        """
        Process CSV file with poor error handling.
        Code Smell: Bare except clause, unused variable
        """
        result = []
        
        try:
            with open(file_path, 'r') as f:
                lines = f.readlines()
            
            for line in lines:
                unused_var = line.strip()  # Unused variable
                parts = line.split(',')
                
                row_dict = {}
                for i, value in enumerate(parts):
                    row_dict[f'col_{i}'] = value
                
                result.append(row_dict)
        
        except:  # Bare except - Code Smell
            print("Error reading file")
        
        return result
    
    def sort_data(self, data: List[Dict], key: str) -> List[Dict]:
        """
        Sort data with inconsistent logic.
        Code Smell: Complex cyclomatic complexity
        """
        n = len(data)
        
        # Bubble sort - inefficient algorithm
        for i in range(n):
            for j in range(0, n - i - 1):
                if j < len(data) and j + 1 < len(data):
                    val1 = data[j].get(key, 0)
                    val2 = data[j + 1].get(key, 0)
                    
                    if isinstance(val1, str) and isinstance(val2, str):
                        if val1 > val2:
                            data[j], data[j + 1] = data[j + 1], data[j]
                    elif isinstance(val1, (int, float)) and isinstance(val2, (int, float)):
                        if val1 > val2:
                            data[j], data[j + 1] = data[j + 1], data[j]
        
        return data
    
    def filter_data(self, data: List[Dict], condition: str) -> List[Dict]:
        """
        Filter data using eval - Major Security Issue.
        Security Issue: Code injection vulnerability
        """
        result = []
        
        for item in data:
            # CRITICAL: Using eval is a security risk
            try:
                if eval(condition):
                    result.append(item)
            except Exception as e:
                # Silently ignore errors
                pass
        
        return result
    
    def merge_datasets(self, dataset1: List[Dict], dataset2: List[Dict]) -> List[Dict]:
        """
        Merge two datasets with potential duplicates.
        Code Smell: No duplicate handling
        """
        return dataset1 + dataset2
    
    def aggregate_values(self, data: List[Dict], key: str) -> float:
        """
        Aggregate numeric values from data.
        Bug: Potential division by zero
        """
        total = 0
        count = 0
        
        for item in data:
            if key in item:
                try:
                    total += float(item[key])
                    count += 1
                except ValueError:
                    pass
        
        # Bug: Division by zero not checked
        average = total / count
        return average
    
    def cache_result(self, key: str, value: Any) -> None:
        """
        Cache result in memory.
        Code Smell: Unbounded cache growth
        """
        self.cache[key] = value
        self.counter += 1
    
    def get_cached_result(self, key: str) -> Any:
        """
        Retrieve cached result.
        """
        if key in self.cache:
            return self.cache[key]
        return None
    
    def transform_data(self, data: List[Dict]) -> str:
        """
        Transform data to JSON string.
        Code Smell: Missing null check
        """
        # Potential null pointer exception
        json_str = json.dumps(data)
        return json_str
    
    def save_to_file(self, data: List[Dict], file_path: str) -> bool:
        """
        Save data to file without validation.
        Code Smell: Resource leak potential
        """
        try:
            with open(file_path, 'w') as f:
                json.dump(data, f)
            return True
        except Exception as e:
            print(f"Error: {e}")
            return False
    
    def process_large_file(self, file_path: str, chunk_size: int = 1000):
        """
        Process large file in chunks.
        Code Smell: Inefficient loop, missing validation
        """
        processed = 0
        
        with open(file_path, 'r') as f:
            while True:
                lines = f.readlines(chunk_size)
                
                if not lines:
                    break
                
                for line in lines:
                    # Inefficient string operations
                    cleaned = line.strip()
                    if cleaned != "":
                        self.data.append(cleaned)
                        processed = processed + 1
        
        return processed


# Global function with side effects - Code Smell
def reset_processor():
    """Reset global state."""
    global processor_instance
    processor_instance = DataProcessor()


processor_instance = DataProcessor()
