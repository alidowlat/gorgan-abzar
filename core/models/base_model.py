from django.db import models


# STATUS_CHOICES = [
#     ('pending', 'در انتظار تایید'),
#     ('approved', 'تایید شده'),
#     ('rejected', 'رد شده'),
# ]
#
#
# class BaseReview(models.Model):
#     user = models.ForeignKey('accounts.User', null=True, blank=True, on_delete=models.CASCADE, verbose_name='کاربر')
#     parent = models.ForeignKey('self', null=True, blank=True, related_name='replies', on_delete=models.CASCADE, verbose_name='پاسخ')
#     title = models.CharField(max_length=75, verbose_name='عنوان', )
#     text = models.TextField(max_length=450, verbose_name='متن')
#     created_at = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ثبت')
#     status = models.CharField(max_length=8, choices=STATUS_CHOICES, default='pending', blank=True, verbose_name='وضعیت')
#
#     RECOMMENDATION_CHOICES = [
#         ('good', 'میکنم'),
#         ('bad', 'نمیکنم'),
#     ]
#     recommendation = models.CharField(max_length=7, null=True, blank=True, choices=RECOMMENDATION_CHOICES,
#                                       verbose_name='پیشنهاد کاربر')
#
#     class Meta:
#         abstract = True
#         ordering = ['-create_date']
#
#     def __str__(self):
#         return f"{self.user} - {self.text[:20]}"
#
#
# class BaseReviewReaction(models.Model):
#     user = models.ForeignKey('accounts.User', on_delete=models.CASCADE, verbose_name='کاربر')
#     reaction = models.CharField(max_length=7, choices=[('like', 'پسندیدم'), ('dislike', 'نپسندیدم')], verbose_name='ری اکشن')
#     created_at = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ثبت')
#
#     class Meta:
#         abstract = True


class AbstractFavorite(models.Model):
    user = models.ForeignKey('accounts.User', on_delete=models.CASCADE, verbose_name='کاربر')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True


class AbstractVisit(models.Model):
    ip = models.CharField(max_length=64)
    user = models.ForeignKey('accounts.User', null=True, blank=True, on_delete=models.CASCADE)
    user_agent = models.TextField(null=True, blank=True)
    referer = models.URLField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True
        verbose_name = "Visit"
        verbose_name_plural = "Visits"
