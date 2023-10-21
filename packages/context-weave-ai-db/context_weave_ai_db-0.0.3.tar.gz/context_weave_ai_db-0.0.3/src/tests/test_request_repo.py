import os
import sys
sys.path.insert(0, os.getcwd())
print(sys.path)
from context_weave_ai_db import setup, request_repo
from dotenv import load_dotenv


load_dotenv()
setup.create_db("blog_creator_db")
setup.setup_tables()

requests = request_repo.RequestRepo.get_all(status=None)
assert len(requests) > 0
