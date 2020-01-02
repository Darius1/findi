import subprocess
import pickle

class Windows_IO:
    ''' 
        Handles initializing and maintaining the environment on a Windows machine so that the scan script can run successfully.

        Attributes:
            address (str): The IP address to scan
            FNULL (?): Special value that indicates that FNULL should be used
    '''

    def __init__(self, address, FNULL):
        self.address = address
        self.FNULL = FNULL
        self.win_path = ".\\openIPs"

        # Convert the passed in IP address into a directory name
        address_file = address.replace("/", "\\")
        self.address_as_dir_name = address_file.replace(":", ".")

    def prepare_env(self):
        '''
                Set up our environment that the script will run in by creating the directory that will store all of our scanned IP addresses

                The openIPs folder will be created in the location that the findi_scan script is run
        '''

        create_dir = "mkdir " + "\"" + self.win_path + "\""
        # print(create_dir)
        subprocess.call(create_dir, shell=True)
        # print(make_dir)

    def create_ip_folder(self):
        '''
                Creates the folder hierarchy the program will use

                Each open IP address will have its own folder created with the IP address as the name. If a folder with the same name exists, it will be removed

                A subdirectory called content will also be created which will hold the webpage we download called data.html
        '''

        # If the directory we want to create exists, remove it
        remove = "rmdir /s /q " + "\"" + self.win_path + "\\" + self.address_as_dir_name + "\""
        subprocess.call(remove, stdout=self.FNULL, stderr=self.FNULL, shell=True)

        # Create the directory that will store our IP address information
        add_dir = "mkdir " + "\"" + self.win_path + "\\" + self.address_as_dir_name + "\""
        subprocess.call(add_dir, stdout=self.FNULL, stderr=self.FNULL, shell=True)

        # Create the content subdirectory that will hold our webpage data.html
        subprocess.call(["mkdir", self.win_path + "\\" + self.address_as_dir_name +
                        "\\content"], stdout=self.FNULL, stderr=self.FNULL, shell=True)

    def write_results_to_file(self, results):
        '''
            Creates a text file that stores all the collected results

            Args:
                results (dict of str): Dictonary that contains results collected from the IP scan
        '''
        
        open_file_str = self.win_path + "\\" + self.address_as_dir_name + "\\info.txt"
        pageDataFile = open(open_file_str, "wb")
        pickle.dump(results, pageDataFile)
        pageDataFile.close()