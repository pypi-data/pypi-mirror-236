import sys

for line in sys.path:
     print(line)
#Third Party Imports
from src.taxes.brackets import FederalIncomeTaxBrackets
from src.taxes.brackets import GeorgiaStateIncomeTaxBrackets
from src.taxes.brackets import SocialSecurityIncomeTaxBrackets
from src.taxes.brackets import MedicareIncomeTaxBrackets
from src.taxes.Logger import logger

# Load in tax brackets for your year and filing-status.
federal_taxes = FederalIncomeTaxBrackets.married_filing_jointly_2022_tax
georgia_taxes = GeorgiaStateIncomeTaxBrackets.married_filing_jointly_2022_tax
social_security_taxes = SocialSecurityIncomeTaxBrackets.social_security_employee_2022_tax
medicare_taxes = MedicareIncomeTaxBrackets.medicare_employee_2022_tax

# Compute the taxes.
agi = 100000
# long_term_capital_gains = 20000
federal_tax = federal_taxes.calculate_taxes(agi)
state_tax = georgia_taxes.calculate_taxes(agi)
social_security_tax = social_security_taxes.calculate_taxes(agi)
medicare_tax = medicare_taxes.calculate_taxes(agi)

# Show the result.
logger.info(f'adjusted gross income: ${agi:,.0f}')
logger.info(f'federal tax: ${federal_tax:,.0f}')
logger.info(f'state tax: ${state_tax:,.0f}')
logger.info(f'social security tax: ${social_security_tax:,.0f}')
logger.info(f'medicare tax: ${medicare_tax:,.0f}')
