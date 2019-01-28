#! /usr/bin/python3

import time
import cgi, cgitb
cgitb.enable()

def main():
    form = cgi.FieldStorage()
    if 'sleep' in form:
        sn = form['sleep'].value
        time.sleep(int(sn))
        print ('Content-type: text/plain\n\nSlept for %s seconds' % sn)
    else:
        print ('Content-type: text/plain\n\nNo sleep parameter')

main()
