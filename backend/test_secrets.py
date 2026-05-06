# test_secrets.py - ARCHIVO DE TESTING SOLO
# Estos son secretos FICTICIOS para testing con Gitleaks
# ⚠️ NO SON VÁLIDOS - SOLO PARA DETECTAR PATRONES

TEST_SECRETS = {
    # AWS Credentials
    "AWS_ACCESS_KEY": "AKIAIOSFODNN7EXAMPLE",
    "AWS_SECRET_KEY": "wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY",
    
    # GitHub & Git
    "GITHUB_TOKEN": "ghp_1234567890abcdefghijklmnopqrstuvwxyz",
    "GITHUB_OAUTH": "ghu_16c7e42f292c6912efd52a8259e4c1d3d56c4a7a",
    "GITLAB_TOKEN": "glpat-1234567890abcdefghij",
    
    # Payment & APIs
    "STRIPE_SECRET": "sk_live_51234567890abcdefghijklmnopqrstuvwxyz",
    "STRIPE_PUBLISHABLE": "pk_live_51234567890abcdefghijklmnopqrstuvwxyz",
    "PAYPAL_SIGNATURE": "AFcWxV21C7fd0v3bYYYRCpSSRl31AgpO6O0eYJ0n0tFHgxL.L8c0H0YvH5XY",
    
    # Database Connections
    "MONGODB_URI": "mongodb+srv://admin:P@ssw0rd123@cluster-fake.mongodb.net/database",
    "POSTGRES_URL": "postgresql://user:P@ssw0rd123@postgres-fake.rds.amazonaws.com:5432/dbname",
    "MYSQL_URL": "mysql://root:Mysql@P@ssw0rd123!@fake-db.example.com:3306/dbname",
    
    # JWT & Tokens
    "JWT_SECRET": "your-256-bit-secret-key-that-is-very-long-and-secure-1234567890abcdef",
    "JWT_TOKEN": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyfQ.SflKxwRJSMeKKF2QT4fwpMeJf36POk6yJV_adQssw5c",
    "API_KEY": "sk_live_fakekey123456789abcdefghijklmnopqrstuvwxyz",
    
    # Private Keys
    "RSA_PRIVATE_KEY": """-----BEGIN RSA PRIVATE KEY-----
MIIEpAIBAAKCAQEA0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ
ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ
-----END RSA PRIVATE KEY-----""",
    
    "SSH_PRIVATE_KEY": """-----BEGIN OPENSSH PRIVATE KEY-----
b3BlbnNzaC1rZXktdjEAAAAABG5vbmUtbm9uZQAAAAgbm9uZS1ub25lAAAAAA
AAAAQ123456789abcdefghijklmnopqrstuvwxyzAAAAAg
-----END OPENSSH PRIVATE KEY-----""",
    
    # Passwords in Connections
    "DB_PASSWORD": "Mysql@P@ssw0rd123!fake",
    "ADMIN_PASSWORD": "Admin#Secure$Pass@2024",
    
    # OAuth Tokens
    "OAUTH_ACCESS_TOKEN": "ya29.a0AfH6SMBx_abc123XYZ_1234567890abcdefgh",
    "OAUTH_REFRESH_TOKEN": "1//0gxyz123ABC456789XYZ0_abcd1234567890",
}