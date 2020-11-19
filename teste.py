with open("ManageDB.py", "r") as f:
    lines = f.readlines()

linesToWrite = []
for line in lines:
    if line[:6] == "appURL":
        line = 'appURL = "certo"'
        linesToWrite.append(line)
    else:
        linesToWrite.append(line)

with open("ManageDB.py", "w") as f:
    f.writelines(linesToWrite)