SELECT
  Country_Code,
  Year,
  Financing_type,
  Million_euro AS `Total Spending`,
  Million_purchasing_power_standards__PPS_ AS `Total Spending (PPS)`,
  Euro_per_inhabitant AS `Spending per inhabitant`,
  Purchasing_power_standard__PPS__per_inhabitant AS `Spending per inhabitant (PPS)`,
  Percentage_of_gross_domestic_product__GDP_ AS `Percentage of GDP`
FROM eurostat.healthcare_expenditure