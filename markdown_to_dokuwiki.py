# -*- coding: latin-1 -*-

import sys
import os
import json

__doc__ = """This script will read a text file in Markdown format,
and convert it to DokuWiki format.

The basic approach is to run pandoc to convert the markdown to JSON,
and then to parse the JSON output, and convert it to dokuwiki, which
is written to standard output

Requirements:
 - pandoc is in the user's PATH
"""

# TODOs
# underlined, fixed-width
# Code quotes

list_depth = 0
list_depth_increment = 2

def process_list( list_marker, value ):
    global list_depth
    list_depth += list_depth_increment
    result = ""
    for item in value:
        result += '\n' + list_depth * unicode( ' ' ) + list_marker + process_container( item )
    list_depth -= list_depth_increment
    if list_depth == 0:
        result += '\n'
    return result

def process_container( container ):
    if isinstance( container, dict ):
        assert( len(container) == 1 )
        key = container.keys()[ 0 ]
        value = container.values()[ 0 ]
        if key == 'Para':
            return process_container( value ) + '\n\n'
        if key == 'Str':
            return value
        elif key == 'Header':
            level = value[0]
            marker = ( 7 - level ) * unicode( '=' )
            return marker + unicode(' ') + process_container( value[1] ) + unicode(' ') + marker + unicode('\n\n')
        elif key == 'Strong':
            return unicode('**') + process_container( value ) + unicode('**')
        elif key == 'Emph':
            return unicode('//') + process_container( value ) + unicode('//')
        elif key == 'Code':
            return unicode("''") + value[1] + unicode("''")
        elif key == 'Image':
            return unicode("{{:") + value[1][0] + unicode("}}")
        elif key == "Link":
            url = value[1][0]
            return unicode('[[') + url + unicode('|') + process_container( value[0] ) + unicode(']]')
        elif key == "BulletList":
            return process_list( unicode( '* ' ), value)
        elif key == "OrderedList":
            return process_list( unicode( '- ' ), value[1])
        elif key == "Plain":
            return process_container( value )
        elif key == "BlockQuote":
            # There is no representation of blockquotes in DokuWiki - we'll just
            # have to spit out the unmodified text
            return '\n' + process_container( value ) + '\n'
        elif key == "CodeBlock":
            return '<code>\n' + value[1] + '\n</code>'

        #elif key == 'Code':
        #    return unicode("''") + process_container( value ) + unicode("''")
        else:
            return unicode("unknown map key: ") + key + unicode( " value: " ) + str( value )

    if isinstance( container, list ):
        result = unicode("")
        for value in container:
            result += process_container( value )
        return result

    if isinstance( container, unicode ):
        if container == unicode( "Space" ):
            return unicode( " " )
        elif container == unicode( "HorizontalRule" ):
            return unicode( "----\n\n" )

    return unicode("unknown") + str( container )

def process_pandoc_jason( data ):
    assert( len(data) == 2 )
    result = unicode('')
    for values in data[1]:
        result += process_container( values )
    print result

def convert_file( filename ):
    # Use pandoc to parse the input file, and write it out as json
    tempfile = "temp_script_output.json"
    command = "pandoc --to=json \"%s\" --output=%s" % ( filename, tempfile )
    #print command
    os.system( command )
    
    input_file = open(tempfile, 'r' )
    input_text = input_file.readline()
    input_file.close()

    ## Parse the data
    data = json.loads( input_text )
    process_pandoc_jason( data )

def main( files ):
    for filename in files:
        convert_file( filename )

if __name__ == "__main__":
    files = sys.argv[1:]
    
    if len( files ) == 0:
        sys.stderr.write( "Supply one or more filenames to convert on the command line\n" )
        return_code = 1
    else:
        main( files )
        return_code = 0
        
    sys.exit( return_code )
