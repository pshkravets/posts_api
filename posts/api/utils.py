import pandas

from ninja.security import APIKeyQuery

from users.models import MyUser
from posts.settings import client
from api.models import CommentStatistic


class ApiKey(APIKeyQuery):
    param_name = "jwt_token"

    def authenticate(self, request, key):
        try:
            return MyUser.objects.get(jwt_token=key)
        except MyUser.DoesNotExist:
            pass


def text_valid(text: str):
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", f"content": f'''You must check the given text for the presence of obscene language,
         insults, etc., and if it contains obscene language, return only True; otherwise, return False. 
         Here is the text: "{text}"'''}]
    )
    return response.choices[0].message.content


def comments_statistic_counting(date_from, date_to):
    date_range = pandas.date_range(start=date_from, end=date_to).tolist()
    dict_count = {}
    total_comments = CommentStatistic.objects.filter(created_at__range=[date_from, date_to])
    dict_count['total'] = {
        'total blocked': len(total_comments.filter(blocked=True)),
        'total avaliable': len(total_comments.filter(blocked=False))

    }
    for day in date_range:
        comments = CommentStatistic.objects.filter(created_at=day.date())
        dict_count[str(day.date())] = {
            'blocked': len(comments.filter(blocked=True)),
            'avaliable': len(comments.filter(blocked=False))
        }
    return dict_count


def create_auto_comment(post):
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", f"content": f'''You must crate comment for this post: {post}'''}]
    )
    return response.choices[0].message.content
