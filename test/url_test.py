from validator.HasValidURL_validator import URLValidator

if __name__=="__main__":
    text=input("Enter URL or sentenece:")
    
    validator=URLValidator()
    result=validator.validate(text)
    print(result)