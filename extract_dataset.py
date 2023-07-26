import zipfile
import argparse
import os

def main():
    parser = argparse.ArgumentParser(
                prog='extract_dataset.py',
                description='Automatically extracts the contents of the HLE Dataset.',
                epilog='If you have any questions or problems, create an issue at https://github.com/Henningson/HLEDataset')

    parser.add_argument('--dataset_path', '-d', help="The path of the dataset folder", default="dataset/")
    args = parser.parse_args()

    keys = ["CF", "CM", "DD", "FH", "LS", "MK", "MS", "RH", "SS", "TM"]
    
    for key in keys:
        zip_path = os.path.join(args.dataset_path, key, "{0}.zip".format(key))
        target_dir = os.path.join(args.dataset_path, key)
        
        with zipfile.ZipFile(zip_path,"r") as zip_ref:
             print("Extracting {0} to {1}".format(key, target_dir))
             zip_ref.extractall(target_dir)



if __name__ == "__main__":
    main()