from validator.HasValidURL_validator import URLValidator
from validator.secretspresent_validator import SecretValidator
from validator.Bias_validator import BiasValidator
from validator.cucumber_validator import CucumberValidator
from validator.profanity_validator import ProfanityValidator
from validator.pii_validator import PIIDetector
from validator.BannedWords_validator import BannedWordsValidator
from validator.competitor_validator import CompetitorValidator
from cucumber_expressions.parameter_type import ParameterType


positive_number = ParameterType("positive_number", regexp=r"\d+", type=int)
cucumber_validator = CucumberValidator(
    "I buy {positive_number} apple(s)/banana(s)/orange(s)",
    parameter_types=[positive_number]
)

VALIDATOR_REGISTRY={
    "url":URLValidator(),
    "secret":SecretValidator(),
    "bias":BiasValidator() ,
    "cucumberexp":cucumber_validator,
    "profanity":ProfanityValidator(),
    "detectpii":PIIDetector(),
    "bannedwords":BannedWordsValidator(),
    "competitor":CompetitorValidator()
}