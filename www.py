def unicode_list(string):
    # create an empty list to store the Unicode values
    result = []
    # loop through each character in the string
    for char in string:
        # get the Unicode value of the character using ord() function
        value = ord(char)
        # append the value to the result list
        result.append(hex(value))
    # return the result list
    return result


word = input()
hexList = unicode_list(word)
out = ""
for i in hexList:
    i = i[2:6]
    out += "\\u"
    out += i
print(out)
