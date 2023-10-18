from policyengine_us.model_api import *


class medicaid_income(Variable):
    value_type = float
    entity = TaxUnit
    label = "Medicaid/CHIP/ACA-related MAGI"
    unit = USD
    documentation = "Medicaid/CHIP/ACA-related modified AGI for this tax unit."
    definition_period = YEAR
    reference = (
        "https://www.law.cornell.edu/uscode/text/42/1396a#e_14_G",  # Medicaid law pointing to IRC
        "https://www.law.cornell.edu/uscode/text/26/36B#d_2",  # IRC defining income
    )

    def formula(tax_unit, period, parameters):
        agi = tax_unit("adjusted_gross_income", period)
        agi_additions = parameters(period).gov.hhs.medicaid.income.modification
        return max_(0, agi + add(tax_unit, period, agi_additions))
