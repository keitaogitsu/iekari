from iekari.models import ScoreLog, Profile, RentRoom
import pandas as pd
import numpy as np

def _make_profile():
    profiles = pd.DataFrame.from_records(list(Profile.objects.values() ))
    profiles.set_index('id')
    return profiles

def _make_table():
    idx_profile = Profile.objects.values_list('id', flat=True)
    col_rentroom = RentRoom.objects.values_list('id', flat=True)
    cf = pd.DataFrame(index=idx_profile, columns=col_rentroom).fillna(0)
    
    for log in ScoreLog.objects.iterator():
        cf.at[log.profile_id, log.rent_room_id] = log.score
    return cf

def get_cross_table():
    profile = _make_profile()
    cf = _make_table()

    joined = profile.set_index('id').join(cf)
    # return joined, cf
    return joined