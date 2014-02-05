import os
import sys
import subprocess
from cStringIO import StringIO
import pstats
import argparse

def run_command(command, stdout=subprocess.PIPE):
    p = subprocess.Popen(command, shell=True,
            stdout=stdout,
            stderr=subprocess.STDOUT)
    return p.communicate()

def get_profile_results(prof_filename):
    old_stdout = sys.stdout
    sys.stdout = profile_results = StringIO()

    pstats.Stats(prof_filename).strip_dirs(). \
        sort_stats("cumulative").print_stats()

    sys.stdout = old_stdout
    
    return profile_results.getvalue()
    
def profile(filename):
    dir = create_profile_dir(filename)
    prof_filename = os.path.join(dir, 'profile_results')
    run_command("python -m cProfile -o {0:s} {1:s}".format(
        prof_filename, filename))
    results = get_profile_results(prof_filename)
    filename_results = os.path.join(
        dir, os.path.splitext(os.path.basename(filename))[0] + '.profile.txt')
    with open(filename_results, 'w') as f:
        f.write(results)

def profile_line(filename):
    filename = os.path.abspath(filename)
    scriptdir = os.path.dirname(os.path.abspath(__file__))
    kernprof_path = os.path.join(scriptdir, 'kernprof.py')
    dir = create_profile_dir(filename)
    dir = os.path.abspath(dir)
    filename_results = os.path.join(
        dir, os.path.splitext(os.path.basename(filename))[0] + '.profile_line.txt')
    os.chdir(dir)
    results, _ = run_command("python {0:s} -l -v {1:s}".format(
        kernprof_path, filename))
    with open(filename_results, 'w') as f:
        f.write(results)
        
def create_profile_dir(filename):
    # Create .easyprofile directory.
    dir = os.path.dirname(filename)
    dir = os.path.join(dir, '.easyprofile')
    if not os.path.exists(dir):
        os.mkdir(dir)
    return dir
        
def main():
    parser = argparse.ArgumentParser(
        description="""Easy profiling. Pass the filename as argument, 
        and optionally -l if you want line-by-line profiling.""")
    parser.add_argument('filename',)
    parser.add_argument('-l',
        '--line-profiler', 
        help='use a line-by-line profiler', 
        action='store_true',)
    args = parser.parse_args()
    
    if args.line_profiler:
        profile_line(args.filename)
    else:
        profile(args.filename)
        
if __name__ == '__main__':
    main()
    
