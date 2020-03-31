
import requests
import json

class Darkvpn :
  def login( self, username, password ) :
    ''' Login to the darkVPN system'''
    url  = 'https://billing.darkvpn.io/api/check-access/by-login-pass?_key=SazfD3kzSq2EvHIocTm1&login=%s&pass=%s' % ( username, password )
    resp = requests.get( url )
    xj   = resp.content
    xok  = json.loads( xj )
    if xok[ 'ok' ] :
      return xok['login']
    return False
    
  def countries( self ) :
    ''' Fetch available countries from darkvpn'''
    url = 'https://api.darkvpn.io/servers/list'
    resp = requests.get( url )
    return json.loads( resp.content )
  def servers( self, country ) :
    ''' Fetch available servers for specific country'''
    url = 'https://api.darkvpn.io/servers/random/?country=%s' % country
    resp = requests.get( url )
    return json.loads( resp.content )
