# coding = utf-8

import logging
logger = logging.getLogger(__name__)

from django.conf import settings
from django.db import models, connection
from django.db.models.sql import InsertQuery


def DEBUG(msg):
    if settings.DEBUG:
        logger.debug(msg)
        

class BatchInsertQuery( InsertQuery ):
    ####################################################################
    # http://stackoverflow.com/questions/2655670/how-do-i-perform-a-batch-insert-in-django/3459915
    ####################################################################
    def as_sql(self):
        """
        Constructs a SQL statement for inserting all of the model instances
        into the database.

        Differences from base class method:        

        - The VALUES clause is constructed differently to account for the
        grouping of the values (actually, placeholders) into
        parenthetically-enclosed groups. I.e., VALUES (a,b,c),(d,e,f)
        """
        qn = self.connection.ops.quote_name
        opts = self.model._meta
        result = ['INSERT INTO %s' % qn(opts.db_table)]
        result.append('(%s)' % ', '.join([qn(c) for c in self.columns]))
        result.append( 'VALUES %s' % ', '.join( '(%s)' % ', '.join( 
            values_group ) for values_group in self.values ) ) # This line is different
        params = self.params
        if self.return_id and self.connection.features.can_return_id_from_insert:
            col = "%s.%s" % (qn(opts.db_table), qn(opts.pk.column))
            r_fmt, r_params = self.connection.ops.return_insert_id()
            result.append(r_fmt % col)
            params = params + r_params
        return ' '.join(result), params
    
    def insert_values( self, insert_values ):
        """
        Adds the insert values to the instance. Can be called multiple times
        for multiple instances of the same model class.

        Differences from base class method:

        -Clears self.columns so that self.columns won't be duplicated for each
        set of inserted_values.        
        -appends the insert_values to self.values instead of extends so that
        the values (actually the placeholders) remain grouped separately for
        the VALUES clause of the SQL statement. I.e., VALUES (a,b,c),(d,e,f)
        -Removes inapplicable code
        """
        self.columns = [] # This line is new

        placeholders, values = [], []
        for field, val in insert_values:
            placeholders.append('%s')

            self.columns.append(field.column)
            values.append(val)

        self.params += tuple(values)
        self.values.append( placeholders ) # This line is different