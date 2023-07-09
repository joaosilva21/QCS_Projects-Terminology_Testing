import sys
import dahuffman
import pickle

class deflate:
    def __init__(self, window = 65535, buffer = 255, preview=1, extension="txt"):
        self.preview = preview
        self.error = 0
        self.verify_int(window, buffer)
        if self.error == 1:
            print("Program closing...\n")
            exit(1)

        self.window = int(window)
        self.buffer = int(buffer)
        self.extension = "."+extension


    def compress(self, str):
        with open(str, "rb") as file:
            text = file.read()

        text = bytearray(text)

        i = 0
        BIN = bytearray('', 'utf-8')
        
        while i < len(text):
            i_start_window = i-self.window
            if i_start_window < 0:
                i_start_window = 0
            
            window = text[i_start_window:i]
            buffer = text[i:i+self.buffer]

            binary = bytes([0]) + bytes([0]) + bytes([text[i]])
            toskip=0

            for size in reversed(range(1, len(buffer)+1)):
                posW = window.rfind(buffer[0:size])
                if posW >=0:
                    char = 0
                    pos = len(window) - posW -1

                    if i+size < len(text):
                        char = text[i+size]

                    toskip=size
                    binary = bytes([pos]) + bytes([size]) + bytes([char])

                    break
            
            i += toskip+1
            BIN += binary
 
        BIN = bytearray(BIN)

        codec = dahuffman.HuffmanCodec.from_data(BIN)
        BIN2 = codec.encode(BIN)
        
        splitted = str.split(".")
        toremove = splitted[len(splitted)-1]
        towrite = 'deflate/compressed/compressed_'+str[0:len(str)-len(toremove)-1]+".bin"
        
        with open('deflate/compressed/huffman_aux.bin', 'wb') as freq:
            pickle.dump(codec, freq)

        with open(towrite, "wb") as encodedFile:
            encodedFile.write(BIN2)


        if self.preview==1:
            print("\nPREVIEW OF COMPRESSION:")
            print( [ (BIN[i], BIN[i+1], '') if BIN[i+2]==0 else(BIN[i], BIN[i+1], chr(BIN[i+2])) for i in range(0, len(BIN), 3) ] )
            print()


    def decompress(self, name):
        with open('huffman_aux.bin', 'rb') as freq:
            codec = pickle.load(freq)

        with open(name, 'rb') as encodedFile:
            dic = encodedFile.read()
        
        text = bytearray('', 'utf-8')
        for char in codec.decode(dic):
            text += bytes([char])
            
        aux = []
        for i in range(0,len(text),3):
            if text[i+2] == 0:
                aux.append((text[i], text[i+1], ''))
            else:
                aux.append((text[i], text[i+1], chr(text[i+2])))
        
        text = aux
        
        text2=""
        for elem in text:
            start = len(text2)-(elem[0]+1)
            text2 += text2[start:start+elem[1]]+elem[2]

        splitted = name.split("_")
        toremove = splitted[0]
        towrite = 'deflate/decompressed/decompressed_'+name[len(toremove)+1:len(name)-4]+self.extension

        with open(towrite, "w") as decodedFile:
            decodedFile.write(text2)

        if self.preview==1:
            print("\nPREVIEW OF DECOMPRESSION:")
            print(text)
            print()


    def verify_int(self, window, buffer):
        ints = ['0','1','2','3','4','5','6','7','8','9']

        for i in range(len(window)):
            if window[i] not in ints:
                print("\n1st argument (aka len of window) must be an intenger")
                self.error=1
                break

        for j in range(len(buffer)):
            if buffer[j] not in ints:
                if(self.error==0):
                    print("")
                print("2nd argument (aka len of buffer) must be an intenger")
                self.error=1
                break




if __name__ == "__main__":
    if(len(sys.argv)>=6):
        if sys.argv[4]=="on":
            preview = 1
        elif sys.argv[4]=="off":
            preview = 0
        else:
            print("\n4th argument must be on or off\nProgram closing..\n")
            exit(1)

        if(sys.argv[3]=="-compress"):
            deflate(sys.argv[1], sys.argv[2], preview).compress(sys.argv[5])

        elif(sys.argv[3]=="-decompress"):
            if(len(sys.argv)==7):
                deflate(sys.argv[1], sys.argv[2], preview, sys.argv[6]).decompress(sys.argv[5])
            else:
                print("\nNumber of arguments invalid\nTo use this program write the correct parameters:\n\t <window-size> <buffer-size> <-compress/-decompress> <on/off> <name-of-file> <extension-of-file>\n")
                print("Program closing..\n")

    else:
        print("\nNumber of arguments invalid\nTo use this program write the correct parameters:\n\t <window-size> <buffer-size> <-compress/-decompress> <on/off> <name-of-file>\n")
        print("Program closing..\n")