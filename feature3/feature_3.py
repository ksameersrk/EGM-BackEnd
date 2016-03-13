'''
user(phone_number(pkey),age,name,photo_url,date_creation)
group(g_id(pkey),name,date_creation, destination)
group_message(gm_id(pkey),video_url,photo_url,text)
user_is_admin_group(g_id(pkey)(fkey from group),phone_number(fkey from user))
user_is_group_member(g_id(pkey)(fkey from group),phone_number(pkey)(fkey from user))
user_send_group_message(phone_number(pkey)(fkey from user),gm_id(pkey)(fkey from group_message),g_id(fkey from group))
user_receives_group_message(phone_number(pkey)(fkey from user),gm_id(pkey)(fkey from group_message),g_id(fkey from group))
'''

import sqlite

class DBQueryObject:

	__table_list=['user', 'group', 'group_message', 'user_is_admin_group', 'user_is_group_member', 'user_send_group_message', 'user_receives_group_message']

	# this opens a connection with the database
	def __init__(self, database_name=":memory:"):
		self.con=sqlite3.connect(database_name)

	# this is called to query a particular table to return information
	def query(self, table, primary_key):
		if table not in DBQueryObject.__table_list: 
			raise Exception("Invalid table name")

		# primary_key has the format { keyName: value }

		query_string=""

		query_results=[]

		try:
			for result con.execute(query_string):
				query_results.append(result)
		except:
			raise Exception("Error during query")

	# this is called to insert many records
	def insert_many(self, table, value_list):
		if table not in DBQueryObject.__table_list: 
			raise Exception("Invalid table name")

		for entry in value_list:
			insert_entry(table, entry)

	# this is called to delete many records
	def delete_many(self, table, primary_key_list):
		if table not in DBQueryObject.__table_list: 
			raise Exception("Invalid table name")

		for primary_key in primary_key_list:
			delete_entry(table, primary_key)

	# this is called to insert a single record
	def insert_entry(self, table, entry):
		query_string="insert into %s (" %table;
		 
			for value in entry: 
				query_string+=value+", "
			query_string+=");"

		try:
			self.con.execute(query_string)
		except:
			raise Exception("Error during insertion")
		
	# this is called to delete a single record
	def delete_entry(self, table, primary_key):
		# primary_key has the format { keyName: value }
		try:
			self.con.execute("delete from %s where  %s = %s;" %(table, str(primary_key.key()), str(primary_key.value()))
		except:
			raise Exception("Error during deletion")

if __name__=="__main__":
	object=DBQueryObject()
