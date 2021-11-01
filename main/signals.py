from django.db.models.signals import post_save, pre_save, post_delete
from django.contrib.auth.models import User
from .models import CustomUser, UserProfile


# create profile
def create_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(
            user = instance,
        ).save()

    print("User profile created.")


''' user updated
def update_profile(sender, instance, **kwargs):

    badges = Badge.objects.filter(required_points__lte = instance.ratings_count)
    user_badges = AchievementBadge.objects.filter(user = instance)

    for badge in badges:
        if badge not in user_badges:
            AchievementBadge.objects.create(
                    user = instance,
                    badge = badge
                ).save()

    # only applicable if the user has lost points.
    user_badges.filter(badge__required_points__gt = instance.ratings_count).delete()

    print('User profile updated.')
'''

def registerSignals():
    post_save.connect(create_profile, sender = CustomUser)
#post_save.connect(update_profile, sender = UserProfile)
