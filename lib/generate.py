#!/usr/bin/env python

import os
import sys
import fileinput
from jinja2 import Environment, FileSystemLoader
from darkvpn import Darkvpn
from collections import namedtuple

dvpn   = Darkvpn()
cnames = { 'uk': 'United Kingdom',
           'us': 'United States',
           'fr': 'France',
           'ch': 'Switzerland',
           'de': 'Germany',
           'ee': 'Estonia',
           'hk': 'Hong Kong',
           'nl': 'Netherlands',
           'pl': 'Poland',
           'ro': 'Romania',
           'se': 'Sweden',
           }
cwd  = os.path.dirname( os.path.dirname( os.path.realpath( __file__ ) ) )
auth_file = "%s/conf/auth" % cwd 
config    = "%s/conf/configuration.conf" % cwd
conf_tpl  = "conf.tpl"

def main() :
  ''' The main application handler'''
  if not os.path.isfile( auth_file ) :
    username = raw_input( 'Please input your username: ' )
    password = raw_input( 'Please input your password: ' )
  else :
    lines = [line.rstrip('\n') for line in open( auth_file ) ]
    username = lines[0]
    password = lines[1]

  login = dvpn.login( username, password )
  if login :
    if not save_auth( login, password ) :
      print "Could not save authentication file!"
      sys.exit(113)

    country  = ask_country( )
    protocol = ask_protocol()
    port     = ask_port()
    ipaddr   = dvpn.servers( country )['ip_address']
    env      = Environment(loader = FileSystemLoader( "%s/conf" % cwd ) )
    template = env.get_template( conf_tpl )
    output   = template.render( ip_addr=ipaddr,port=port, protocol=protocol )
    cfile    = open( config, 'w' )
    cfile.write( output )
    cfile.close()

  else :
    print "Wrong username / password!"
    sys.exit(1)

def listCountries() :
  ''' List available countries for the darkVPN'''
  records = dvpn.countries()['records']
  unique = {}
  for x in records :
    unique[ x.get('name') ] = cnames.get( x['name'] )
  return unique

def ask_country( ) :
  ''' Ask user for the input'''
  print "Please choose Country: "
  for c in listCountries():
    print "\t%s) %s" % (c, cnames[c] )
  country = ''
  while country not in cnames :
    country = raw_input( 'Choose Country: ' )
    if country not in cnames :
      print "Wrong value, please try again..."
  return country 

def ask_protocol( ) :
  ''' Ask user for the protocol'''
  proto = False
  while not proto :
    print "Choose protocol\n0) tcp\n1) udp\n"
    tcp = raw_input( '0 / 1 ? : ' )
    if tcp == '1' :
      proto = 'udp'
    elif tcp == '0' :
      proto = 'tcp'
    else :
      print "Wrong value, please try again..."
  return proto

def ask_port( ) :
  ''' Ask for the port number'''
  while True:
    print "Choose port\n0) 1194\n1) 443\n"
    chosen = raw_input( '0 / 1 ?: ' )
    if chosen == '1' :
      return 443
    elif chosen == '0' :
      return 1194
    else :
      print "Wrong value, please try again..."

def save_auth( login, password ) :
  ''' Save authentication details to a pre-defined file'''
  try :
    text = "%s\n%s" % ( login, password )
    f = open( auth_file, 'w' )
    f.write( text )
    f.close()
    return True
  except:
    return False


if __name__ == "__main__":
    main()