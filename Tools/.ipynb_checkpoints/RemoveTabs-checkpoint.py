def main():
    inFile = open("input.txt",'r')
    outFile = open("output.txt",'w')
    
    tab = list(' '*4)
    
    for line in inFile:
        matchFound = True if list(line[:4]) == tab else False
        if matchFound:
            outFile.write(line[4:])
        else:
            outFile.write(line)
        
    inFile.close()
    outFile.close()

if __name__ == "__main__":
    main()