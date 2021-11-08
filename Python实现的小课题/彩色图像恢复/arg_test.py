import sys

# 传入3个参数，具体操作根据个人情况
def main(argv):
    print(argv[1])
    if argv[1] == 'jjj':
        print("ok!")
    print(argv[2])
    print(argv[3])


if __name__ == "__main__":
    main(sys.argv)
