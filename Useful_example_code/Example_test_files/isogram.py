#string1 = 'cliff'

def is_Isogram(string1):
    string1.lower()
    string1.strip()
    string1.replace(" ", "")
    string1.replace("-", "")

    string2 = set(string1)
    if string1.isalpha() == False:
        raise ValueError(" String cannot contain numbers")

    if len(string2) != len(string1):
        return(False)
    else:
        return(True)
