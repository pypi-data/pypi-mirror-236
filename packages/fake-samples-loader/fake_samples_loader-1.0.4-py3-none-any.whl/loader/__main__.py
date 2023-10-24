import sys
from loader import load


def main():
    arg1 = sys.argv[1]
    arg2 = int(sys.argv[2])
    arg3 = sys.argv[3]
    arg4 = 29
    
    return load(arg1, arg2, arg3, arg4)


if __name__ == "__main__":
    main()