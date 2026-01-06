from validator.secretspresent_validator import SecretValidator


# def main():
#     sentence = input("Enter a prompt: ")

#     validator = SecretValidator()
#     result = validator.has_secret(sentence)

#     print("Secret detected:", result)


# if __name__ == "__main__":
#     main()

if __name__=="__main__":
    text=input("Enter text:")
    validator=SecretValidator()
    print(validator.validate(text))
