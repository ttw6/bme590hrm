import os.path
from heartdata import HeartData


def main():
    # Set up path and file names
    path = 'test_data/'
    filename = 'test_data1.csv'             # think of how to automate
    file = os.path.join(path, filename)
    HeartData(file)


if __name__ == "__main__":
    main()