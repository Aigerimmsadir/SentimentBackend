from rest_framework.views import APIView
from main.serializers import CommentSerializer
from rest_framework.response import Response
from .models import Comment
from .emoji_sentiment import emoji_sentiment
from .get_polarity_subjectivity import DiplomaSentimentAnalyzer
from .fuzzy_calculation_sentiment import FuzzySentiment


class CommentList(APIView):
    http_method_names = ['post']

    def post(self, request):
        serializer = CommentSerializer(data=request.data,
                                       context={'request': request}, many=True)
        if serializer.is_valid():
            dsa = DiplomaSentimentAnalyzer()
            result_sent = []
            fs=FuzzySentiment()
            for comment in serializer.data:
                comment_info = dict(comment)
                emoji_score = emoji_sentiment([comment_info['message']])
                emoji_score = 50 if emoji_score is None else emoji_score[3]*100
                text_score = dsa.get_sentiment_values(comment_info['message'])
                final_sentiment = fs.get_sentiment(text_score['subjectivity'], text_score['polarity'], emoji_score)
                comment_info['sentiment_res'] = final_sentiment
                result_sent.append(comment_info)
            return Response(result_sent)
        return Response(serializer.errors)
