from django.db import models

class Database(models.Model):
  def __str__(self):
    return self.user + '_' + str(self.id)

  # The owner of the database
  user = models.TextField()
  
  # When the database was created
  created_on = models.DateTimeField('date created')

  # When the database was last modified
  last_modified = models.DateTimeField('last modified')
  
  # Stored as an array of column names
  columns = models.TextField()

  # Stored as an array of objects with members for each column
  rows = models.TextField()
