require('dotenv').config(); //instatiate environment variables

CONFIG = {} //Make this global to use all over the application

CONFIG.app = process.env.APP || 'development';
CONFIG.port = process.env.PORT || '8000';

CONFIG.db_dialect = process.env.DB_DIALECT || 'mongo';
CONFIG.db_host = process.env.DB_HOST || 'localhost';
CONFIG.db_ip = process.env.DB_IP || 'hi@12.345.678.910'
CONFIG.db_port = process.env.DB_PORT || '27017';
CONFIG.db_name = process.env.DB_NAME || 'name';
CONFIG.db_user = process.env.DB_USER || 'root';
CONFIG.db_password = process.env.DB_PASSWORD || 'db-password';
CONFIG.mongo_uri = process.env.MONGO_URI || 'mongodb://localhost:27017/musiq';


// Oauth2
CONFIG.google_oauth_client_id = process.env.GOOGLE_OAUTH_CLIENT_ID;
CONFIG.google_oauth_client_secret = process.env.GOOGLE_OAUTH_CLIENT_SECRET;