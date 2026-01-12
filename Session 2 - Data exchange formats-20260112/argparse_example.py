import string
import sys
import time
import argparse

def veryImportantFunction(sleep_time):
    print("This function is very important")
    time.sleep(sleep_time)
    if __name__ == '__main__':
        print("This script is done")
    else: 
        print("This function is done")

if __name__ == '__main__':
    # Parse the arguments
    parser = argparse.ArgumentParser(description="My first script with arguments", formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument("-f", "--float", type=float, help="A usueless float",required=True)
    parser.add_argument("-S", "--string", help="A useless string",required=True, type=str)
    parser.add_argument("-s","--sleep-time",default=10,type=int ,help="Sleep duration")
    args = parser.parse_args()
    config = vars(args)
    #print(config)
    my_float=config["float"]
    my_string=config["string"]
    sleep=config["sleep_time"]

    print(f"I've parsed these arguments, Float: {my_float}, String: {my_string}, Sleep duration: {sleep}")
    veryImportantFunction(sleep)