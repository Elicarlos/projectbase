from datetime import date


def can_create_user(organization):
    if not organization.plan:
        return False

    return organization.user_set.count() < organization.plan.user_limit


def can_create_project(organization):
    if not organization:
        return False
    return organization.project_set.count() < organization.plan.project_limit


def is_trial_expired(org):
    if org.is_trial and org.trial_ends_at:
        return date.today() > org.trial_ends_at
    return False
