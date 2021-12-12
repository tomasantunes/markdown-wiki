# Note: If you write to the same file you have to git pull before you start writing. Conflicts have to be solved manually.
import os
import subprocess
import datetime

print("Updating repo.")

wiki_route = "/wiki"
wiki_folder = "wiki"
excluded_files = [wiki_folder + '/logs/feed.md']
link_excluded_files = ['README.md']
extensions = ('.jpg', '.jpeg', '.png', '.gif', '.webp', '.md')


status = subprocess.run(['git', 'status', '--porcelain'], stdout=subprocess.PIPE, shell=True).stdout.decode('utf-8')

files = []
for line in status.splitlines():
    f = line[3:]
    if f not in excluded_files:
        files.append(f)
    
if len(files) > 0:
    print("Updating feed.")
    entry = "The following files have been modified:<ul>"
    for f in files:
        f = f.replace("\"","")
        if f.endswith(extensions) and f not in link_excluded_files:
            entry += '<li><a href="' + wiki_route + '?fileToOpen=' + f + '">' + f + "</a></li>"
        else:
            entry += "<li>" + f + "</li>"
    entry += "</ul>"
    time = str(datetime.datetime.now().replace(microsecond=0))

    file = open(wiki_folder + "/logs/feed.md", "a")
    file.write("- " + time + " - " + entry + "\n")
    file.close()

os.system("git pull")
os.system("git add --all")
os.system("git commit . -m 'Update'")
os.system("git push")
print("Finished.")