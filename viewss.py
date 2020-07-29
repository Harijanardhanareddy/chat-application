@csrf_exempt
def init(request):
    ...
    username = body['username']
    client = StreamChat(api_key=settings.STREAM_API_KEY,
                        api_secret=settings.STREAM_API_SECRET)
    channel = client.channel('messaging', 'General')

    try:
        member = Member.objects.get(username=username)
        token = bytes(client.create_token(
            user_id=member.username)).decode('utf-8')
        return JsonResponse(status=200, data={"username": member.username, "token": token, "apiKey": settings.STREAM_API_KEY})

    except Member.DoesNotExist:
        member = Member(username=username)
        member.save()
        token = bytes(client.create_token(
            user_id=username)).decode('utf-8')
        client.update_user({"id": username, "role": "admin"})
        channel.add_members([username])

        return JsonResponse(status=200, data={"username": member.username, "token": token, "apiKey": settings.STREAM_API_KEY})