#Mark Boady
#Drexel University 2021
#Steganography Example

#This function takes a bmp image with
#text hidden inside it.
#It extracts the text and saves it as a file.

#We need a library to work with images
#This can be installed with PIP if you don't have it.
from PIL import Image
#For working with file names
import os.path
#For command line arguments
import sys

#Convert an array of 8 bits to a character
#We read the bits as we go, so we can
#Only convert them to characters every 8 bits.
def convert(bits):
    #Place to store the number
    num=0
    #Loop over the bits
    for i in range(0,len(bits)):
        #The bit at index i
        #is the bit for 2^(7-i)
        num = num + bits[i]*(2**(7-i))
    #return the character
    return chr(num)

#When we read a bit we add it to the bit array.
#When we hit the 8th bit we make it a character.
#Otherwise, we return the null string.
#Get the bit from the color
def add(color,bits):
    #Determine the last bit of the color
    bit = color%2
    #Add to array of bits
    bits.append(bit)
    #If this is the 8th bit
    #We have a letter
    if len(bits)==8:
        #Determine the letter
        num = convert(bits)
        #Erase the bits
        bits.clear()
        #Return non-null characters
        if ord(num)!=0:
            return num
    #Return the empty string
    #Not enough bits yet
    return ""

#Decode the image and save it in [imagename].txt
def decode(imgFile):
    print("Decoding {:s}".format(imgFile))
    #Step 1: Open the file
    try:
        #Load the image file
        im = Image.open(imgFile)
        #Get the pixels as an array
        pix = im.load()
    except Exception as e:
        print("Could not open image.")
        print(e)
        return
    #Step 2: Open a file to write into
    #Create New File Name
    fileParts = os.path.splitext(imgFile)
    newFile = fileParts[0]+"_decoded.txt"
    #Open file for writing
    try:
        output=open(newFile,"w")
    except Exception as e:
        print("Cannot open file to write.")
        print(e)
        return
    #Step 3: Loop over pixels
    xMax = im.size[0]
    yMax = im.size[1]
    #Make an empty array to store bits
    bits=[]
    #Loop over image
    for y in range(0,yMax):
        for x in range(0,xMax):
            #Write the text as we read it
            r = pix[x,y][0]
            output.write(add(r,bits))
            g = pix[x,y][1]
            output.write(add(g,bits))
            b = pix[x,y][2]
            output.write(add(b,bits))
    #Step 4: Close the file
    output.close()
    print("Output Written to {:s}".format(newFile))

#Main Program for Command Line Use
def main():
    print("This program decodes secret text",end="")
    print(" hidden in an image.")
    print("Example of Stenography in action.")
    #Check for right command line arguments
    if len(sys.argv)!=2:
        print("Usage: python3 decode.py [image.bmp]")
        #Quit Program
        sys.exit(0)
    #Parse Command Line Arguments
    img = sys.argv[1]
    #Decode the image
    decode(img)
    
#Run main when called from command line
if __name__=="__main__":
    main()
