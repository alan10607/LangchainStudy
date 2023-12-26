
from langchain.llms import OpenAI
from langchain.utilities import SQLDatabase
from langchain_experimental.sql import SQLDatabaseChain
import setApiKey

db = SQLDatabase.from_uri("mysql+pymysql://root:root@127.0.0.1:3307/ag")
llm = OpenAI(temperature=0)

db_chain = SQLDatabaseChain(llm=llm, database=db, verbose=True)
db_chain.run("How many articles are there?")