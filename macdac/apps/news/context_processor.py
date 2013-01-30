from datetime import date



def update_context(request):
    "Steve Jobs died on the 5th of October."

    jobs_dob = date(2011, 10, 5)

    is_today = all(getattr(date.today(), x) == getattr(jobs_dob, x) \
                   for x in ("month", "day"))
    
    return {
        'jobs_dob': is_today,
    }
