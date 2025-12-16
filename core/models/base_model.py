from django.db import models


class AbstractReview(models.Model):
    user = models.ForeignKey('accounts.User', null=True, blank=True, on_delete=models.CASCADE)
    title = models.CharField(max_length=75)
    text = models.TextField(max_length=450)
    created_at = models.DateTimeField(auto_now_add=True)
    RECOMMENDATION_CHOICES = [
        ('good', 'میکنم'),
        ('bad', 'نمیکنم'),
    ]
    recommendation = models.CharField(max_length=7, null=True, blank=True, choices=RECOMMENDATION_CHOICES)

    def __str__(self):
        return f"{self.user} - {self.text[:20]}"


    class Meta:
        abstract = True
        ordering = ['-created_at']


class AbstractReviewReaction(models.Model):
    user = models.ForeignKey('accounts.User', on_delete=models.CASCADE)
    reaction = models.CharField(max_length=7, choices=[('like', 'پسندیدم'), ('dislike', 'نپسندیدم')])
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True


class AbstractFavorite(models.Model):
    user = models.ForeignKey('accounts.User', on_delete=models.CASCADE, db_index=True)
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
