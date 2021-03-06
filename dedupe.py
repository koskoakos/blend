import os
import sys
import pickle
import argparse
import pprint
from functools import partial
import importlib.util

hashify = partial(pickle.dumps)
dictify = partial(pickle.loads)

parser = argparse.ArgumentParser()

parser.add_argument('input', help="Path to input keymap.py")
parser.add_argument('-o', '--output', help="Output file", default='out.py')
parser.add_argument('--dry', help="Output result to stdout", 
                    default=False, action="store_true")

cmd_args = parser.parse_args()

if not os.path.exists(cmd_args.input):
    print("Could not find the specified file. Please check your input")
    sys.exit(1)

try:    
    spec = importlib.util.spec_from_file_location("keyconfig.data", cmd_args.input)
    keyconfig = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(keyconfig)
except:
    print("Failed to import provided keyconfig file.")
    raise
    sys.exit(1)

kcd = keyconfig.keyconfig_data
total_pre = 0
total_post = 0
for a, b, c in kcd:
    keys = set()
    for item in c['items']:
        command, shortcut, args = map(hashify, item)
        keys.add((command, shortcut, args))
    total_pre += len(c['items'])

    k_i = []
    for key in list(keys):
        command, shortcut, args = map(dictify, key)
        if args and 'properties' in args:
            args['properties'] = [tuple(tuple(i) if isinstance(i, list) else i for i in item)
                                  for item in args['properties']]
        k_i.append((command, shortcut, args))

    c['items'] = k_i
    total_post += len(c['items'])

if cmd_args.dry:
    pprint.pprint(kcd)
    sys.exit(0)

deduped = total_pre - total_post
if deduped == 0:
    print("No duplicate entries found.")
    sys.exit(0)
else: 
    print(f"Deduped {deduped} entries.")

with open(cmd_args.output, 'w') as f:
    f.write("keyconfig_data = \\\n")
    pprint.pprint(kcd, f)
    f.write("""
    
if __name__ == "__main__":
    import os
    from bl_keymap_utils.io import keyconfig_import_from_data
    keyconfig_import_from_data(os.path.splitext(os.path.basename(__file__))[0], keyconfig_data)
""")
