# coding=utf-8

""" Fusion Tables Client.

Issue requests to Fusion Tables.
"""

__author__ = 'kbrisbin@google.com (Kathryn Brisbin)'
__maintainer__ = "javier@georemindme.com (Javier Cordero)"

import libs.httplib2 as httplib2
import urllib


class FTAPIError(Exception):
    def __init__(self, type, message=''):
        Exception.__init__(self, message)
        self.type = type

        
class FTClient():
    def _get(self, query): pass
    def _post(self, query): pass
    
    def query(self, query, request_type=None):
        """ Issue a query to the Fusion Tables API and return the result. """
        #encode to UTF-8
        try: query = query.encode("utf-8")
        except: query = query.decode('raw_unicode_escape').encode("utf-8")
        
        lowercase_query = query.lower()
        if lowercase_query.startswith("select") or \
          lowercase_query.startswith("describe") or \
          lowercase_query.startswith("show") or \
          request_type=="GET":
            return self._get(urllib.urlencode({'sql': query}))
        else:
            return self._post(urllib.urlencode({'sql': query}))
  
#    def uploadCSV(self, table_id, filename, bulk=True):
#        """Upload a CSV to an existing table."""
#        
#        fin = gfile.FastGFile(os.path.join(FLAGS.input_dir, filename))
#        csv_reader = csv.reader(fin)
#        header_parts = csv_reader.next()
#        col_keys = ','.join(["'%s'" % s for s in header_parts])
#        start_time = time.time()
#    
#        if bulk:
#            # Upload multiple rows at once
#            max_per_batch = 500
#            num_in_batch = max_per_batch
#            while num_in_batch == max_per_batch:
#                num_in_batch = 0
#                queries = []
#                for line_parts in csv_reader:
#                    line_parts = [s.replace("'", "''") for s in line_parts]
#                    fixed_line = ','.join(["'%s'" % s for s in line_parts])
#                    query = 'INSERT INTO %s (%s) VALUES (%s)' % (
#                        table_id, col_keys, fixed_line)
#                    queries.append(query)
#                    num_in_batch += 1
#                    if num_in_batch == max_per_batch:
#                        break
#        
#                try:
#                    full_query = ';'.join(queries)
#                    self.runPostQuery(full_query)
#                except urllib2.HTTPError:
#                    # Had an error with all the INSERTS; do them one at a time
#                    print 'Exception hit, subdividing:'
#                    for query in queries:
#                        try:
#                            self.runPostQuery(query)
#                        except urllib2.HTTPError, e2:
#                            print 'Error at query %s:' % query
#                            print e2
#          
#                    print 'Appended %d rows' % num_in_batch
#      
#        else:
#            # Upload one line at a time
#            for line_parts in csv_reader:
#                line_parts = [s.strip("'") for s in line_parts]
#                fixed_line = ','.join(["'%s'" % s for s in line_parts])
#                query = 'INSERT INTO %s (%s) VALUES (%s)' % (
#                    table_id, col_keys, fixed_line)
#                self.runPostQuery(query)
#        end_time = time.time()
#        print 'Time for upload to %s: %f  (bulk: %s)' % (
#            table_id, end_time - start_time, str(bulk))


class ClientLoginFTClient(FTClient):
    def __init__(self):
        from django.conf import settings
        self.auth_token = ClientLogin().authorize(settings.FUSIONTABLES['FT_USERNAME'],
                                                   settings.FUSIONTABLES['FT_PASSWORD'])
        self.request_url = "https://www.google.com/fusiontables/api/query"
        from google.appengine.api.memcache import Client
        mem = Client()
        self.request = httplib2.Http(cache=mem)

    def _get(self, query):
        headers = {
          'Authorization': 'GoogleLogin auth=' + self.auth_token,
        }
        response, content = self.request.request('%s?%s' % (self.request_url, query),
                                                method='GET',
                                                headers=headers
                                                )
        if response['status'] != 200:
            raise FTAPIError(response['status'], 'ERROR IN REQUEST')
        return content

    def _post(self, query):
        headers = {
            'Authorization': 'GoogleLogin auth=' + self.auth_token,
            'Content-Type': 'application/x-www-form-urlencoded',
        }
        response, content = self.request.request(self.request_url, method='POST',
                                                 body=query, headers=headers
                                                 )
        if response['status'] != 200:
            raise FTAPIError(response['status'])
        return content
    
import urllib2

class ClientLogin():
  def authorize(self, username, password):
    auth_uri = 'https://www.google.com/accounts/ClientLogin'
    authreq_data = urllib.urlencode({
        'Email': username,
        'Passwd': password,
        'service': 'fusiontables',
        'accountType': 'HOSTED_OR_GOOGLE'})
    auth_req = urllib2.Request(auth_uri, data=authreq_data)
    auth_resp = urllib2.urlopen(auth_req)
    auth_resp_body = auth_resp.read()

    auth_resp_dict = dict(
        x.split('=') for x in auth_resp_body.split('\n') if x)
    return auth_resp_dict['Auth']
