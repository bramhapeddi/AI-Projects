"""
Database tests for acme-banking-qa backend services
"""

import pytest
import psycopg2
from typing import Dict, Any
import json

@pytest.mark.integration
class TestDatabaseOperations:
    """Test database operations and data integrity"""
    
    def test_database_connection_pool(self, db_connection):
        """Test database connection pool functionality"""
        # Test multiple connections
        connections = []
        try:
            for i in range(5):
                conn = psycopg2.connect(db_connection.dsn)
                connections.append(conn)
                cursor = conn.cursor()
                cursor.execute("SELECT %s", (i,))
                result = cursor.fetchone()
                assert result[0] == i
                cursor.close()
        finally:
            for conn in connections:
                conn.close()
    
    def test_database_transactions(self, db_connection):
        """Test database transaction handling"""
        cursor = db_connection.cursor()
        
        try:
            # Start transaction
            cursor.execute("BEGIN")
            
            # Insert test data
            cursor.execute("""
                CREATE TEMP TABLE test_transactions (
                    id SERIAL PRIMARY KEY,
                    name VARCHAR(100),
                    value INTEGER
                )
            """)
            
            cursor.execute("""
                INSERT INTO test_transactions (name, value) 
                VALUES (%s, %s)
            """, ("test_item", 42))
            
            # Verify data was inserted
            cursor.execute("SELECT COUNT(*) FROM test_transactions")
            count = cursor.fetchone()[0]
            assert count == 1
            
            # Rollback transaction
            cursor.execute("ROLLBACK")
            
            # Verify data was rolled back
            cursor.execute("SELECT COUNT(*) FROM test_transactions")
            count = cursor.fetchone()[0]
            assert count == 0
            
        finally:
            cursor.close()
    
    def test_database_constraints(self, db_connection):
        """Test database constraint enforcement"""
        cursor = db_connection.cursor()
        
        try:
            # Create test table with constraints
            cursor.execute("""
                CREATE TEMP TABLE test_constraints (
                    id SERIAL PRIMARY KEY,
                    email VARCHAR(255) UNIQUE NOT NULL,
                    age INTEGER CHECK (age >= 0 AND age <= 150)
                )
            """)
            
            # Test unique constraint
            cursor.execute("""
                INSERT INTO test_constraints (email, age) 
                VALUES (%s, %s)
            """, ("test@example.com", 25))
            
            # Try to insert duplicate email
            with pytest.raises(psycopg2.IntegrityError):
                cursor.execute("""
                    INSERT INTO test_constraints (email, age) 
                    VALUES (%s, %s)
                """, ("test@example.com", 30))
            
            # Test check constraint
            with pytest.raises(psycopg2.IntegrityError):
                cursor.execute("""
                    INSERT INTO test_constraints (email, age) 
                    VALUES (%s, %s)
                """, ("another@example.com", -5))
            
            with pytest.raises(psycopg2.IntegrityError):
                cursor.execute("""
                    INSERT INTO test_constraints (email, age) 
                    VALUES (%s, %s)
                """, ("another@example.com", 200))
            
        finally:
            cursor.close()
    
    def test_database_performance(self, db_connection):
        """Test database query performance"""
        cursor = db_connection.cursor()
        
        try:
            # Create test data
            cursor.execute("""
                CREATE TEMP TABLE test_performance (
                    id SERIAL PRIMARY KEY,
                    name VARCHAR(100),
                    category VARCHAR(50),
                    value DECIMAL(10,2),
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            # Insert test data
            for i in range(1000):
                cursor.execute("""
                    INSERT INTO test_performance (name, category, value) 
                    VALUES (%s, %s, %s)
                """, (f"item_{i}", f"cat_{i % 10}", i * 1.5))
            
            # Test query performance with index
            cursor.execute("""
                CREATE INDEX idx_test_performance_category 
                ON test_performance(category)
            """)
            
            # Measure query time
            import time
            start_time = time.time()
            
            cursor.execute("""
                SELECT category, COUNT(*), AVG(value) 
                FROM test_performance 
                WHERE category = %s 
                GROUP BY category
            """, ("cat_5",))
            
            result = cursor.fetchone()
            query_time = time.time() - start_time
            
            # Query should complete in reasonable time
            assert query_time < 1.0, f"Query took {query_time:.2f}s, expected < 1.0s"
            assert result is not None
            assert result[0] == "cat_5"
            assert result[1] == 100  # 1000 items / 10 categories
            
        finally:
            cursor.close()

@pytest.mark.slow
class TestDatabaseLoad:
    """Test database under load conditions"""
    
    def test_concurrent_connections(self, db_connection):
        """Test multiple concurrent database connections"""
        import threading
        import queue
        
        results = queue.Queue()
        
        def worker(worker_id):
            try:
                conn = psycopg2.connect(db_connection.dsn)
                cursor = conn.cursor()
                cursor.execute("SELECT %s", (worker_id,))
                result = cursor.fetchone()
                results.put((worker_id, result[0]))
                cursor.close()
                conn.close()
            except Exception as e:
                results.put((worker_id, f"ERROR: {e}"))
        
        # Start multiple worker threads
        threads = []
        for i in range(10):
            thread = threading.Thread(target=worker, args=(i,))
            threads.append(thread)
            thread.start()
        
        # Wait for all threads to complete
        for thread in threads:
            thread.join()
        
        # Verify all workers completed successfully
        successful_results = []
        while not results.empty():
            worker_id, result = results.get()
            if isinstance(result, str) and result.startswith("ERROR"):
                pytest.fail(f"Worker {worker_id} failed: {result}")
            successful_results.append((worker_id, result))
        
        assert len(successful_results) == 10
        for worker_id, result in successful_results:
            assert result == worker_id