import requests
import subprocess
import os

def last_version(repo):
    response = requests.get('https://api.github.com/repos/binance/desktop/releases/latest')
    version = response.json()['tag_name'].split("v")[1]
    return version

def open_template():
    main_path = os.path.dirname(__file__)
    file_path = os.path.join(main_path, 'template_dpkg')
    file = open(file_path, mode='r')
    read_file = file.read()
    file.close()
    return read_file

def replace_template(original_text, list_replace):
    replace = original_text
    for key, value in dict_replace.items():
        replace = replace.replace(key, value)
    return replace

def write_dpkg(content):
    main_path = os.path.dirname(__file__)
    file_path = os.path.join(main_path, 'PKGBUILD')
    with open(file_path, 'w') as f:
        f.write(content)

def install():
    proc = subprocess.Popen(['makepkg', "-si"], shell = True, stdin = subprocess.PIPE, stdout = subprocess.PIPE, text = True)
    while True:
      line = proc.stdout.readline()
      if not line:
        break
      print(line.rstrip())


sha256sums = requests.get('https://ftp.binance.com/electron-desktop/linux/production/binance-amd64-linux-deb-sha256.txt').text
last_version = last_version('https://github.com/binance/desktop')
print("check last version: {}".format(last_version))

print("prepare dpkg file...")
dict_replace = {'{VERSION}': last_version, '{SHA256SUMS}': sha256sums}
dpkg_content = replace_template(open_template(), dict_replace)

print("create dpkg")
write_dpkg(dpkg_content)

print("install dpkg binance...")
install()
print("finish to install binance {}".format(last_version))
