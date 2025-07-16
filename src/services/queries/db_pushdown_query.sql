select 
    Country_Code,
    Financing_type as Type, 
    Year,
    round(sum(Million_euro),0) as Spending,
    round(sum(Euro_per_inhabitant),0) as Spending_per_inhabitant
from workspace.eurostat.healthcare_expenditure
--where Year = 2023
group by all
having Spending is not null