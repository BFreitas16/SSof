import sys
from Util import write_list_to_file
from ProgramParser import ProgramParser


def main():
    program = sys.argv[1]
    pattern = sys.argv[2]

    parser = ProgramParser(program, pattern)
    parser.build_graph()
    vulnerability_list = parser.evaluate_flows()
    
    write_list_to_file(program, vulnerability_list)


if __name__ == '__main__':
    main()
