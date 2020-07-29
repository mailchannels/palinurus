def camelCase(inputStr, delimiterChar='-'):
    # remove all spaces
    inputStr = "".join(inputStr.split())
    # remove all delimiter headind and trailing spaces
    inputStr = inputStr.strip(delimiterChar)
    
    result = "".join([ x.upper() if i>0 and inputStr[i-1] == delimiterChar else x for i,x in enumerate(inputStr) if x is not delimiterChar ])
    return result

