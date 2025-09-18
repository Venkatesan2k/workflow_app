"""
Data source node handlers
"""
import json
import requests
from typing import Dict, Any
from django.db import connection
from .base import BaseNodeHandler

class DatabaseQueryHandler(BaseNodeHandler):
    """Handler for database query nodes"""
    
    def execute(self, config: Dict[str, Any], input_data: Dict[str, Any], context: Dict[str, Any]) -> Dict[str, Any]:
        query_type = config.get('query_type', 'SELECT').upper()
        table_name = config.get('table_name', '')
        conditions = config.get('conditions', '')
        fields = config.get('fields', '*')
        limit = config.get('limit', 100)
        
        if not table_name:
            raise ValueError("Table name is required")
        
        # Build query based on type
        if query_type == 'SELECT':
            query = f"SELECT {fields} FROM {table_name}"
            if conditions:
                query += f" WHERE {conditions}"
            if limit:
                query += f" LIMIT {limit}"
        elif query_type == 'INSERT':
            # For INSERT, expect data in input
            data = input_data.get('data', {})
            if not data:
                raise ValueError("No data provided for INSERT operation")
            
            columns = ', '.join(data.keys())
            placeholders = ', '.join(['%s'] * len(data))
            query = f"INSERT INTO {table_name} ({columns}) VALUES ({placeholders})"
            params = list(data.values())
        elif query_type == 'UPDATE':
            data = input_data.get('data', {})
            if not data or not conditions:
                raise ValueError("Data and conditions are required for UPDATE operation")
            
            set_clause = ', '.join([f"{k} = %s" for k in data.keys()])
            query = f"UPDATE {table_name} SET {set_clause} WHERE {conditions}"
            params = list(data.values())
        elif query_type == 'DELETE':
            if not conditions:
                raise ValueError("Conditions are required for DELETE operation")
            query = f"DELETE FROM {table_name} WHERE {conditions}"
        else:
            raise ValueError(f"Unsupported query type: {query_type}")
        
        try:
            with connection.cursor() as cursor:
                if query_type == 'SELECT':
                    cursor.execute(query)
                    columns = [col[0] for col in cursor.description]
                    results = [dict(zip(columns, row)) for row in cursor.fetchall()]
                    
                    return {
                        'data': results,
                        'count': len(results),
                        'success': True,
                        'message': f"Retrieved {len(results)} records"
                    }
                else:
                    cursor.execute(query, params if 'params' in locals() else [])
                    affected_rows = cursor.rowcount
                    
                    return {
                        'data': {'affected_rows': affected_rows},
                        'success': True,
                        'message': f"{query_type} operation affected {affected_rows} rows"
                    }
                    
        except Exception as e:
            self.log_execution(f"Database query failed: {str(e)}", 'error')
            raise ValueError(f"Database query failed: {str(e)}")

class HttpRequestHandler(BaseNodeHandler):
    """Handler for HTTP request nodes"""
    
    def execute(self, config: Dict[str, Any], input_data: Dict[str, Any], context: Dict[str, Any]) -> Dict[str, Any]:
        method = config.get('method', 'GET').upper()
        url = config.get('url', '')
        headers = config.get('headers', {})
        body = config.get('body', '')
        timeout = config.get('timeout', 30)
        
        if not url:
            raise ValueError("URL is required")
        
        # Parse headers if string
        if isinstance(headers, str):
            try:
                headers = json.loads(headers) if headers else {}
            except json.JSONDecodeError:
                headers = {}
        
        # Parse body if string
        request_body = None
        if body:
            if isinstance(body, str):
                try:
                    request_body = json.loads(body)
                except json.JSONDecodeError:
                    request_body = body
            else:
                request_body = body
        
        try:
            self.log_execution(f"Making {method} request to {url}")
            
            response = requests.request(
                method=method,
                url=url,
                headers=headers,
                json=request_body if isinstance(request_body, (dict, list)) else None,
                data=request_body if isinstance(request_body, str) else None,
                timeout=timeout
            )
            
            # Try to parse JSON response
            try:
                response_data = response.json()
            except:
                response_data = response.text
            
            result = {
                'data': response_data,
                'status_code': response.status_code,
                'headers': dict(response.headers),
                'success': response.status_code < 400,
                'message': f"HTTP {method} request completed with status {response.status_code}"
            }
            
            if not result['success']:
                self.log_execution(f"HTTP request failed with status {response.status_code}", 'warning')
            
            return result
            
        except requests.exceptions.Timeout:
            raise ValueError(f"HTTP request timed out after {timeout} seconds")
        except requests.exceptions.RequestException as e:
            raise ValueError(f"HTTP request failed: {str(e)}")
