job_function = [
    {
        'name':"stores_fabric_issue",
        'src':'scd_plan',
        'gap':1,
        'planned':'plan_details.plan_dates.scd',
        'compeleted':'job_completed_date.stores_fabric_issue'
},
    {
        'name': "cutting_lay",
        'src': 'scd_plan',
        'gap': 0,
        'planned': 'plan_details.plan_dates.scd',
        'compeleted': 'job_completed_date.cutting_lay'
    },
    {
        'name': "cutbank_packageready",
        'src': 'production_plan',
        'gap': 1,
        'planned': 'plan_details.plan_dates.ssd',
        'compeleted': 'job_completed_date.cutbank_packageready'
    },
    {
        'name': "sewing_sewing",
        'src': 'production_plan',
        'gap': 0,
        'planned': 'plan_details.plan_dates.ssd',
        'compeleted': 'job_completed_date.sewing_sewing'
    },
{
        'name': "sewing_iron",
        'src': 'production_plan',
        'gap': 0,
        'planned': 'plan_details.plan_dates.sed',
        'compeleted': 'job_completed_date.sewing_iron'
    }
]