import os
import json

cfgpath = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'config.json')

def get_gs_path():
    try:
        with open(cfgpath, 'r') as cfg:
            config = json.load(cfg)

            return config['gs_path']
    except:
        return None

def set_gs_path(gs_path):
    with open(cfgpath, 'w') as cfg:
        json.dump({'gs_path': gs_path}, cfg)

def doShrink(gs_path, file_input, file_output, quality):
    import subprocess

    # result = subprocess.Popen(
    #     '"{}" -sDEVICE=pdfwrite -dCompatibilityLevel=1.4 -dPDFSETTINGS=/{} -dNOPAUSE -dBATCH -dQUIET -sOutputFile="{}" "{}"'\
    #     .format(gs_path, quality, file_output, file_input)
    # )

    result = subprocess.run([
        gs_path,
        '-sDEVICE=pdfwrite',
        '-dCompatibilityLevel=1.4',
        '-dPDFSETTINGS=/{}'.format(quality),
        '-dNOPAUSE',
        '-dBATCH',
        '-dQUIET',
        '-sOutputFile="{}"'.format(file_output),
        '"{}"'.format(file_input)
    ])

if __name__ == '__main__':
    print("")
    print("##################")
    print("#  PDF SHRINKER  #")
    print("##################")
    print("")

    gs_path = get_gs_path()
    if gs_path is None:
        gs_path = input('Ghostscript path is not set, please insert: ').strip('"')
        set_gs_path(r'{}'.format(gs_path))
    
    quality = input('Quality (screen/ebook/printer): ')
    file_input = input("Insert input file: ")
    file_output = input("Insert output file: ")

    doShrink(gs_path, file_input.strip('"'), file_output.strip('"'), quality)

    print("")
    print("Finished!")