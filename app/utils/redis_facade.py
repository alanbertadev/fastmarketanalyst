import redis as redis_XYZ
import base64 as base64_XYZ

class RedisFacade:
    
    def __init__(self):
        self.pool = redis_XYZ.ConnectionPool(host='localhost', port=6379, db=0)
        self.db = redis_XYZ.Redis(connection_pool=self.pool)
        
    def set(self, key, str_data):
        self.db.set(key, str_data)
        
    def setex(self, key, str_data, time):
        self.db.setex(key, str_data, time)
        
    def get(self, key):
        return self.db.get(key)
                
    def delete(self, key):
        self.db.delete(key)
    
    def exists(self, key):
        return self.db.exists(key)
        
    def setBase64(self, key, str_data):
        self.db.set(key, base64_XYZ.b64encode(str_data))
            
    def getBase64(self, key):
        return base64_XYZ.b64decode(self.db.get(key))
        
