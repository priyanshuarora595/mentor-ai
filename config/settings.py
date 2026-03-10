import os
from dotenv import load_dotenv

load_dotenv()

# The application now primarily uses database-backed configuration.
# ENCRYPTION_KEY is still required for secure API key storage.
ENCRYPTION_KEY = os.getenv("ENCRYPTION_KEY")
