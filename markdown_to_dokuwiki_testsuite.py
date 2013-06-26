import unittest
import markdown_to_dokuwiki
import os
import filecmp
import shutil

class ConversionsTest(unittest.TestCase):
    """Teststuite for the conversion.
       Uses external files containing the expected input and output
    """
    def __init__( self ):
        unittest.TestCase.__init__( self )

    def runTest( self ):
        input_file_name = "markdown_to_dokuwiki_test_input.md"
        expected_file_name = "markdown_to_dokuwiki_test_expected.txt"
        temp_file_name = "markdown_to_dokuwiki_test_output.txt"

        # TODO Convert the following os.system() to a direct call of
        #      markdown_to_dokuwiki.convert_file()
        python_cmd = os.getenv( "CCDC_BUILD_PYTHON", "python" )
        command_line = python_cmd + " markdown_to_dokuwiki.py " + input_file_name + " > " + temp_file_name
        os.system( command_line )
        
        if filecmp.cmp( temp_file_name, expected_file_name ) != 1:
            # TODO Fix use of PC-specific comparison program FC
            os.system( "FC " + expected_file_name + " " + temp_file_name )
            # uncomment the next line to update the expected output
            # it will fail on the first run as the output is updated, then succeed on
            # the second run
            # shutil.copyfile( temp_file_name, expected_file_name )

            #os.unlink( temp_file_name )
            self.fail( "ConversionsTest output differs, uncomment code to update expected text" )
            
        os.unlink( temp_file_name )

class ConvertHandleTestSuite( unittest.TestSuite ):
    """A TestSuite object containing the testsuite for the whole script
    """

    def __init__( self ):
        unittest.TestSuite.__init__( self )
        self.addTest( ConversionsTest() )

if __name__ == '__main__':
    tests = ConvertHandleTestSuite()
    runner = unittest.TextTestRunner()
    runner.run( tests )
