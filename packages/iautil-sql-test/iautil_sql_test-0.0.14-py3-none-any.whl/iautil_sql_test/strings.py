""" test strings """

from pathlib import Path

QUERY_STRING:str = "SELECT * FROM table\n"
QUERY_PATH:Path  = Path("etc/query.sql")

with open(QUERY_PATH, mode='r', encoding='utf-8') as file:
    contents:str = file.read()
assert contents == QUERY_STRING
