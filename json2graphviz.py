from argparse import ArgumentParser
import json
import sys
import html

def json2graphviz(jsonobj):
    '''
    jsonobj is a json object, i.e. a mapping from strings to values, where
    a value is: a string, a number, an array of values, a boolean, null,
    or a nested json object

    output: a graphviz dot string
    '''

    ret = ['digraph { graph[rankdir=LR, nodesep=0.1, ranksep=0.3];',
        'node[shape=plaintext, height=0.1];']

    # id counter; represents a unique node
    uid = 0

    # we must take consideration to handle booleans (which have to be printed
    # lowercase), nulls (which are transformed to None), and nested objects
    # specially

    # doesn't accept dicts or lists; html escapes strings
    def plainvalue2str(v):
        if isinstance(v, bool):
            return 'true' if v else 'false'
        elif v is None:
            return 'null'
        elif isinstance(v, str):
            return html.escape(v)
        else:
            return str(v)

    def isplainvalue(v):
        if isinstance(v, dict) or isinstance(v, list):
            return false
        else:
            return true

    def declaration(k, v):
        uid += 1
        if isplainvalue(v):
            v = plainvalue2str(v)
            return f'''{uid}[label=<
            <TABLE BORDER="0" CELLBORDER="1" CELLSPACING="0">
            <TR><TD PORT="f0">{k}</TD><TD PORT="f2">{v}</TD></TR>
            </TABLE>>];'''
        else:
            # v is a dict or list (object or array in json-land)

    def partialgraph(obj):
        for k, v in obj.items():
            ret.append(None)

    ret.append('}')

    return '\n'.join(ret)

def jsonfile2graphviz(filename):
    if filename == '-':
        return json2graphviz(json.load(sys.stdin))
    else:
        with open(filename, 'r') as f:
            return json2graphviz(json.load(f))

def main():
    parser = ArgumentParser(description='Convert JSON to Graphviz Dot notation')
    parser.add_argument('file', nargs='+', help='file to read; - for stdin')
    args = parser.parse_args()

    for f in args.file:
        print(jsonfile2graphviz(f))

if __name__ == '__main__':
    main()
