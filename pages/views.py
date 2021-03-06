from django.shortcuts import render
from vk_auth.settings import SOCIAL_AUTH_VK_OAUTH2_KEY, SOCIAL_AUTH_VK_OAUTH2_SECRET
import vk_api
from social_django.models import UserSocialAuth


def index(request):
    try:
        profile = UserSocialAuth.objects.get(user=request.user.id)
        vk_session = vk_api.VkApi(app_id=SOCIAL_AUTH_VK_OAUTH2_KEY, token='TOKEN_1',
                                  client_secret=SOCIAL_AUTH_VK_OAUTH2_SECRET)
        vk_session.server_auth()
        vk_session.token = {'access_token': profile.extra_data['access_token'], 'expires_in': 0}
        vk = vk_session.get_api()
        friends = vk.friends.get(count=[5], fields=['nickname'])
        friends_list = []
        for friend in friends['items']:
            name = friend['first_name'] + ' ' + friend['last_name']
            friends_list.append(name)
        context = {'friends_list': friends_list}
    except:
        friends_list = ['У тебя нет друзей :(']
        context = {'friends_list': friends_list}
    return render(request, 'home.html', context=context)
