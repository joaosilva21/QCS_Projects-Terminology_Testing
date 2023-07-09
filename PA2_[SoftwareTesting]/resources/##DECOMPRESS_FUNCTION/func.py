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