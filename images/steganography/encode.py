#Mark Boady
#Drexel University 2021
#Steganography Example

#This program takes a jpg image and
#a text file.
#It encodes the text into the pixels
#of the image and saves the result as a lossless
#bmp image.
#We need a lossless format to ensure the message
#is not changed by any websites.

#We need a library to work with images
#This can be installed with PIP if you don't have it.
from PIL import Image
#For working with file names
import os.path
#For command line arguments
import sys

#A string is just an array of characters.
#A character is an array of bits.
#This function returns the target-th bit
#of the text.
def bitAt(target,text):
    #Determine which character the bit is part of
    position = target//8
    #If a bit outside the text is requested
    #put 0.
    if position >= len(text):
        return 0
    #Determine that bit the user wants
    #We count the highest order bit as index 0
    bit = target%8
    #Get the ASCII value of the character
    letter = ord(text[position])
    #Determine the value of the bit's location
    targetBit = int(2**(7-bit))
    #Determine if the bit is set to 1 or 0
    if (targetBit & letter) == targetBit:
        return 1
    return 0
    
#Encode a Single Bit into a color
#We want the last bit of the color
#to be the encoded bit.
#If the bit is 1 we need the color to be odd
#If the bit is 0 we need the color to be even
#Returns the new color code
def encodeBit(color,bit):
    #If the color already has the right bit
    #Nothing to do
    if color%2==bit%2:
        return color
    #The bit is wrong, we need to subtract
    #or add 1.
    #We can't subtract 1 from 0.
    #We can't add one to 255
    if color==0:
        color+=1
    else:
        color-=1
    #Return the new color we created.
    return color

#Encode a text file into an image.
#Takes an image and a text file.
#Outputs as new image with _encode added to name.
def encode(imgFile, textFile):
    print("Hiding text of {:s}".format(textFile),end="")
    print(" inside {:s}.".format(imgFile))
    #Step 1: Make Sure we can read the image
    try:
        #Load the Image
        im = Image.open(imgFile)
        #Convert the image to an array of pixels
        pix = im.load()
    except Exception as e:
        print("Image File could not be read.")
        print(e)
        return
    #Step 2: Read the text file in
    try:
        file=open(textFile,"r")
        text=file.read()
        file.close()
    except Exception as e:
        print("Text File Count not be read.")
        print(e)
        return
    #Step 3: Make sure the file has enough space
    xMax = im.size[0]
    yMax = im.size[1]
    #The total pixels is x*y
    totalPixels = xMax*yMax
    #We can fit 3 bits per pixel
    totalBits = 3*totalPixels
    #We need full 8-bit spaces
    #and 8 bits for 00000000 to end the file
    totalChars = (totalBits-(totalBits%8)-8)//8
    #Print out stats
    display1="The image can hold {:d} characters."
    print(display1.format(totalChars))
    #How many characters does the file have
    neededChars = len(text)
    display2="The text file uses {:d} characters."
    print(display2.format(neededChars))
    if neededChars > totalChars:
        print("Image is to small to hide text.")
        return
    #Step 4: Encode the text into the image
    #We start at the first bit in the file
    bitLocation=0
    #For every pixel on the y axis
    for y in range(0,yMax):
        #for every pixel on the x axis
        for x in range(0,xMax):
            #Get the current pixel's red value
            #encode the bit and move on
            r = pix[x,y][0]
            nextBit = bitAt(bitLocation,text)
            r = encodeBit(r,nextBit)
            bitLocation+=1
            #Encode another bit into green value
            g = pix[x,y][1]
            nextBit = bitAt(bitLocation,text)
            g = encodeBit(g,nextBit)
            bitLocation+=1
            #Encode a third bit into blue value
            b = pix[x,y][2]
            nextBit = bitAt(bitLocation,text)
            b = encodeBit(b,nextBit)
            bitLocation+=1
            #Change the color value in the image
            pix[x,y] = (r,g,b)
    #Step 5: Save the file
    filenameSplit = os.path.splitext(imgFile)
    newFilename = filenameSplit[0]+"_encoded.bmp"
    #Save as a BMP so none of your bits are compressed away
    im.save(newFilename)
    print("New Image Saved as {:s}".format(newFilename))

#Main function for when called from command line
#Requires name of image and text file.
def main():
    print("This program encodes text secretly into an image.")
    print("Example of Stenography in action.")
    #Not enough arguements
    if len(sys.argv)!=3:
        print("Usage: python3 encode.py [image.jpg] [text.txt]")
        sys.exit(0)
    #Parse the arguments
    imgName = sys.argv[1]
    textName = sys.argv[2]
    #Call the real function
    encode(imgName,textName)

#This is a command line program
#that takes two inputs.
if __name__=="__main__":
    main()
