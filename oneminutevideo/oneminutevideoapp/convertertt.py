import subprocess
# from pycaption import detect_format

def main():
    print("jjjjjjjjjjjjjjjjjjjjjjjjj")
    subprocess.call(['ffmpeg', '-i', "output.ass"  , "output1.vtt"])
    # ffmpeg -formats
    
main()

