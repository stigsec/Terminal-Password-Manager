import os, random as r

def delete_file(f):
    fs = os.path.getsize(f)
    with open(f, 'r+b') as x:
        for _ in range(25):
            x.seek(0)
            x.write(b'\x00'*fs)
            x.seek(0)
            x.write(bytes([r.randint(0, 255) for _ in range(fs)]))
            x.seek(0)
            x.write(b'\xFF'*fs)
    os.remove(f)
    
def delete_directory(d):
    for root, dirs, files in os.walk(d, topdown=False):
        for name in files:
            delete_file(os.path.join(root, name))
        for name in dirs:
            os.rmdir(os.path.join(root, name))
    os.rmdir(d)

def main(path):
    if os.path.isfile(path):
        delete_file(path)
    elif os.path.isdir(path):
        delete_directory(path)