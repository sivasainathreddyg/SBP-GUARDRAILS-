from validator.Bias_validator import BiasValidator

if __name__ == "__main__":
    text = input("Enter text: ")

    validator = BiasValidator()
    result = validator.validate(text)

    print(result)
