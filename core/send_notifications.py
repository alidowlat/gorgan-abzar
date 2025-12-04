# def notify_user(user, title, message, type_key, link=None):
#     notif_type, _ = NotificationType.objects.get_or_create(key=type_key, title=title)
#     Notification.objects.create(
#         user=user,
#         title=title,
#         message=message,
#         link=link,
#         notif_type=notif_type
#     )