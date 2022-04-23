import multiprocessing
import run 
from os import listdir

def readin_data(file):
    route = run.run(file)
    route.get_initial_data()
    route.create_new_file()

def main():

    pool = multiprocessing.Pool(4)
    runs = pool.map(readin_data, listdir('RawData/'))

if __name__=="__main__":
    main()