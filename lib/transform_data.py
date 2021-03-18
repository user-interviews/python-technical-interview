# Installation instructions:
# pip install psycopg2

import psycopg2

def get_tag_usage():
  dbConn = psycopg2.connect(
    host='localhost',
    port='5432',
    dbname='user-interviews-rails-server-dev',
    user='',
    password=''
  )
  dbCursor = dbConn.cursor()
  dbCursor.execute('SELECT * FROM public.queued_possible_project_participants')
  rows = dbCursor.fetchall()
  tag_count = {}
  for row1 in rows:
    if row1[5] == None:
      continue
    if row1[6] == None:
      continue
    for tag_id in row1[5]:
      if tag_id in tag_count:
        continue
      tag_count[tag_id] = 0
      for row2 in rows:
        if row2[5] == None:
          continue
        if tag_id in row2[5]:
          tag_count[tag_id] = tag_count[tag_id] + 1
  strings = []
  for tag_id in tag_count:
    strings.append(f'({tag_id}, {tag_count[tag_id]})')
  string = ', '.join(strings)
  dbCursor.execute(f'INSERT INTO public.targeting_tag_counts (targeting_tag_id, count) VALUES {string};')
  dbConn.commit()
  dbCursor.close()
  dbConn.close()
  return tag_count
