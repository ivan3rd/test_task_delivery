import os

# SQLDatabase
DATABASE_URL = os.getenv('DATABASE_URL')
TEST_DATABASE_URL = DATABASE_URL+'/test_delivery?local_infile=1'

# Redis
CACHE_URL = os.getenv('CACHE_URL', '')
CACHE_DB = '0'

