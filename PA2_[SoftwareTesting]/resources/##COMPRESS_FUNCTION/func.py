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
        for i in range(0, len(BIN), 3):
            if BIN[i+2]==0:
                print((BIN[i], BIN[i+1], ''))
            else:
                print((BIN[i], BIN[i+1], chr(BIN[i+2])))
        #print( [ (BIN[i], BIN[i+1], '') if BIN[i+2]==0 else(BIN[i], BIN[i+1], chr(BIN[i+2])) for i in range(0, len(BIN), 3) ] )
    
    print()