from StringIO import StringIO
import sys
import os
import fnmatch

namespaceInput = raw_input("Podaj namespace:\n")

if (os.path.isdir(namespaceInput)):
    if (os.path.exists(namespaceInput)):
        print("Namespace: {0}".format(namespaceInput))
    else:
        sys.exit("Podano bledny namespace")
else:
    sys.exit("Podano bledny namespace.")


retentionInput = raw_input("Podaj czas retencji:\n")
retentionSplited = retentionInput.split(':', 1)

try:
    val = int(retentionSplited[0])
except ValueError:
    print("Podana wartosc nie jest liczba")

if (retentionSplited[1] == "h" or retentionSplited[1] == "H"):
    retentionForm = 3600
elif (retentionSplited[1] == "d" or retentionSplited[1] == "D"):
    retentionForm = 86400
elif (retentionSplited[1] == "m" or retentionSplited[1] == "M"):
    retentionForm = 2592000
elif (retentionSplited[1] == "y" or retentionSplited[1] == "Y"):
    retentionForm = 31556926
else:
    print("Nieprawidlowy format czasu retencji. (Example 1:d)\n")
print(retentionForm)

print("Czy podane wartosci sa prawidlowe?\n Namespace:{0}\n Czas retencji:{1} {2}".format(namespaceInput, retentionSplited[0], retentionSplited[1]))

acceptedValue = raw_input("Kontynuowac?T/N")

if (acceptedValue == "n" or acceptedValue == "N"):
    sys.exit("Zakonczono na zyczenie uzytkownika.")
elif (acceptedValue == "t" or acceptedValue == "T"):
    print("Przystepuje do ustawiania czasu retencji.")
else:
    sys.exit()
added = 0
notAdded = 0

matches = []
for root, dirnames, filenames in os.walk(namespaceInput):
    for filename in fnmatch.filter(filenames, 'creation.txt'):
        fileCreationJoin = os.path.join(root, filename)
        
        matches.append(fileCreationJoin)
        
        creationFile = open(fileCreationJoin, 'r')
        creationTime = creationFile.readline()
        
        retentionFileJoin = os.path.join(root, "retention.txt")
        if not(os.path.exists(retentionFileJoin)):
            retentionFile = open(retentionFileJoin, 'w+')
                            
            retentionTime = int(creationTime) + int(int(retentionSplited[0]) * int(retentionForm))
            retentionFile.write(str(retentionTime))
        
            print("Ustawiono retencje {0} w pliku {1}".format(retentionTime, retentionFileJoin))        
            retentionFile.close()
            creationFile.close()
            added = added + 1
        else:
            
            retentionFile = open(retentionFileJoin, 'r')
        
            checkRetention = retentionFile.readline()
            checkRetention = str(checkRetention).rstrip("\n")
            if (checkRetention == "0" or checkRetention == '0' or checkRetention == 0):
                retentionFile.close()
                retentionFile = open(retentionFileJoin, 'w+')
            
                retentionTime = int(creationTime) + int(int(retentionSplited[0]) * int(retentionForm))
                retentionFile.write(str(retentionTime))
        
                print("Ustawiono retencje {0} w pliku {1}".format(retentionTime, retentionFileJoin))        
                retentionFile.close()
                creationFile.close()
                added = added + 1
            
            else:  
                print("Retencja na pliku {0} zalozona.".format(retentionFileJoin))        
                retentionFile.close()
                creationFile.close()
                notAdded = notAdded + 1
        
print("Retencje zalozono na {0} plikach. Na {1} plikach retencja byla zalozona.".format(str(added), str(notAdded)))