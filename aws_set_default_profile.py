from common_lib.aws_credentials_file_helper import AwsCredentialsFileHelper
from common_lib.common_base import valid_mandatory_parameters,get_input_parameter_value
from common_lib.common_error import BadUserInputError
from os.path import dirname, abspath
from dotenv import load_dotenv
import sys

path = dirname(abspath(__file__)) + '/.env'
load_dotenv(path)

def start(argv):
    if (('-h' in argv) or ('-?' in argv)):
        print("""
        python3 aws_set_default_profile.py 
                        -u AWS_CONFIGURE_SSO_ACCOUNTS_PYTHON_SCRIPT_PATH 
                        -url AWS_SSO_START_URL 
                        [-h|-?]
        Program to load a csv to a mysql table
        Parameters:
            -u AWS_CONFIGURE_SSO_ACCOUNTS_PYTHON_SCRIPT_PATH --> mandatory
            -url AWS_SSO_START_URL --> mandatory 
            -h or -? help
        """)
    
    elif not valid_mandatory_parameters(argv, ['-u']):
        raise BadUserInputError(
            """Input error. To run, python3 aws_set_default_profile.py -u AWS_CONFIGURE_SSO_ACCOUNTS_PYTHON_SCRIPT_PATH 
                                                                        [-h|-?]""")

    else:
        aws_configure_sso_accounts_python_script_path:str = get_input_parameter_value(argv,'-u')
        aws_sso_start_url:str = get_input_parameter_value(argv,'-url')
        aws_credentials_file_helper = AwsCredentialsFileHelper(aws_configure_sso_accounts_python_script_path = aws_configure_sso_accounts_python_script_path,
                                                               aws_sso_start_url=aws_sso_start_url)
        aws_credentials_file_helper.set_default_profile()
    
start(sys.argv)
