import subprocess
import os
import glob

from utils.print_options import *
from utils.common import getcwd

# For each credential found in /aws_credentials, import using "aws configure import" command
# Print out number of profiles successfully imported

def import_aws_profiles():

    AWS_CREDENTIALS_PATH = os.path.abspath(getcwd()) + "/data/aws_credentials"
    AWS_CREDENTIALS_CSV = glob.glob(AWS_CREDENTIALS_PATH + "/*.csv")
    
    successful_imports = 0
    unsuccessful_imports = 0

    if not os.path.exists(AWS_CREDENTIALS_PATH) or len(AWS_CREDENTIALS_CSV) == 0:
        print_warning("\nThere are no aws credentials to import!")
        return

    for credential in range(len(AWS_CREDENTIALS_CSV)):
        try:
            successful_imports += 1
            subprocess.Popen(
                [
                    "aws", 
                    "configure", 
                    "import", 
                    "--csv", 
                    "file://%s" % AWS_CREDENTIALS_CSV[credential]
                ], 
                cwd=AWS_CREDENTIALS_PATH, 
                stdout=subprocess.DEVNULL, 
                stderr=subprocess.DEVNULL
            ).wait()
            
        except Exception as e:
            print(e)
            unsuccessful_imports += 1
            print(
                "Error! Only %d out of %d profiles were imported." % (successful_imports-unsuccessful_imports, len(AWS_CREDENTIALS_CSV))
            )

    if unsuccessful_imports == 0:
        print("Successfully imported all %d profile(s)" % (credential+1))