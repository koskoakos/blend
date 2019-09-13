### Blender keyconfig debloater.

A script to remove identical entries from a keyconfig file.
Requires:
- python3 interpreter 
- your keyconfig file. Usually you can find it at
```%appdata%\Blender Foundation\Blender\2.80\scripts\presets\keyconfig\<your_config_name.py>``` on Windows 
or ```$HOME/.config/blender/2.80/scripts/presets/keyconfig\<your_config_name.py>``` on a reasonable OS

Run
```
python dedupe.py <path_to_keyconfig.py> -o <new_keyconfig_name.py>
```
This will produce a new file, which you then place back to the keyconfig directory.
Don't forget to back up, even better on a regular basis. 
