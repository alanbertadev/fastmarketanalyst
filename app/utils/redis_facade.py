import redis as redis_XYZ
import base64 as base64_XYZ

class RedisFacade:
	
	def __init__(self):
		self.pool = redis_XYZ.ConnectionPool(host='localhost', port=6379, db=0)
		self.db = redis_XYZ.Redis(connection_pool=self.pool)
		
	def set( self, key, str_data ):
		self.db.set( key, str_data )
		
	def get( self, key ):
		return self.db.get( key )
	
	def exists( self, key ):
		return self.db.exists(key)
		
	def setBase64( self, key, str_data ):
		self.db.set( key, base64_XYZ.b64encode( str_data ))
			
	def getBase64( self, key ):
		return base64_XYZ.b64decode(self.db.get( key ))
				
	
if __name__ == '__main__':
	
	print "Test 1 - Simple SET/GET"
	redis = RedisFacade()
	redis.set( "alan", "test" )
	assert redis.get("alan") == "test"
	print "PASS"
	
	print "Test 2 - Base64 SET/GET"
	redis = RedisFacade()
	redis.setBase64( "alan", "test" )
	assert redis.getBase64("alan") == "test"
	print "PASS"
	
	print "Test 3 - Exists"
	redis = RedisFacade()
	redis.set( "alan", "test2" )
	assert redis.exists("alan")
	print "PASS"
	