import subprocess
import sys

def install(package):
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])

required_packages = [
    "bcrypt==3.2.0",
    "fastapi",
    "httpx",
    "passlib[bcrypt]",
    "psycopg2-binary",
    "pydantic[email]",
    "pytest-asyncio",
    "pytest",
    "python-dotenv",
    "python-jose",
    "sentry-sdk[fastapi]",
    "sqlalchemy-utils",
    "sqlalchemy",
    "uvicorn"
]

# Instalar pacotes Python
for package in required_packages:
    install(package)

print("Todos os pacotes necessários foram instalados com sucesso!")