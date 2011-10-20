<h1>VavagClient</h1>
Python client for the URL shortener Vavag.com

Licensed under GNU AFFERO GPL v. 3

This version only supports JSON response.

www.georemindme.com

<h1>Howto:</h1>

Create account and get api key: http://vavag.com/new_account

client = VavagRequest(login, api_key)

client.set_pack('url') # to create a pack with one url
client.set_pack(['url1', 'url2',...]) # for a pack of urls

client.get_pack(hash) # get info about packs

client.get_info('url') # get info about a url

