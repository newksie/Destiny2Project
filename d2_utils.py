import json
import os
import time
from urllib.parse import urljoin
import pandas as pd
import requests

def get_activity_period(activity):
    return activity["period"]


def get_activity_reference_id(activity):
    return activity["activityDetails"]["referenceId"]


def get_activity_instance_id(activity):
    # Used for looking up post-game carnage reports (PGCRs)
    return activity["activityDetails"]["instanceId"]


def get_activity_values(activity):
    return activity["values"]


def get_value_kills(values):
    if "kills" in values:
        return values["kills"]["basic"]["value"]
    else:
        return None


def get_value_deaths(values):
    if "deaths" in values:
        return values["deaths"]["basic"]["value"]
    else:
        return None


def get_value_assists(values):
    if "assists" in values:
        return values["assists"]["basic"]["value"]
    else:
        return None


def get_value_score(values):
    if "score" in values:
        return values["score"]["basic"]["value"]
    else:
        return None


def get_value_completed(values):
    # 1 if completed
    if "completed" in values:
        return values["completed"]["basic"]["value"]
    else:
        return None


def get_value_opponents_defeated(values):
    if "opponentsDefeated" in values:
        return values["opponentsDefeated"]["basic"]["value"]
    else:
        return None


def get_value_combat_efficiency(values):
    if "efficiency" in values:
        return values["efficiency"]["basic"]["value"]
    else:
        return None


def get_value_kdr(values):
    if "killsDeathsRatio" in values:
        return values["killsDeathsRatio"]["basic"]["value"]
    else:
        return None


def get_value_kda(values):
    if "killsDeathsAssists" in values:
        return values["killsDeathsAssists"]["basic"]["value"]
    else:
        return None


def get_value_activity_duration(values, in_units_of="seconds"):
    if "activityDurationSeconds" in values:
        return values["activityDurationSeconds"]["basic"]["value"]
    else:
        return None


def get_value_team(values):
    if "team" in values:
        return values["team"]["basic"]["value"]
    else:
        return None


def get_value_standing(values):
    # The API marks 1 as defeat, 0 as victory, so 1-***
    if "standing" in values:
        return 1 - values["standing"]["basic"]["value"]
    else: 
        return None


def get_value_team_score(values):
    if "teamScore" in values:
        return values["teamScore"]["basic"]["value"]
    else:
        return None


def get_activity_history(character_data, params=None):
    path = urljoin(API_URL, GET_ACTIVITY_HISTORY.format(**character_data))
    r = requests.get(path, headers=HEADERS, params=params)

    activities = r.json()["Response"]["activities"]
    print(f"{len(activities)} activities found")

    history = []

    for activity in activities:
        period = get_activity_period(activity)
        details = activity["activityDetails"]
        activity_name = get_director_activity_name(activity)
        values = get_activity_values(activity)
        id = get_activity_instance_id(activity)
        print(f"{period}, {activity_name}, {id}")
        history.append(
            {
                "period": period,
                "activity_name": activity_name,
                "details": details,
                "values": values,
            }
        )

    return history