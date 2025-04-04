from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import Group
from django.core.mail import send_mail
from django.contrib.auth.tokens import default_token_generator
from django.conf import settings
from .models import CustomUser


@receiver(post_save, sender=CustomUser)
def send_activation_email(sender, instance, created, **kwargs):
    if created and not instance.is_active:
        token = default_token_generator.make_token(instance)
        activation_link = f"{settings.SITE_URL}/activate/{instance.id}/{token}/"
        subject = "Activate Your Account"
        message = f"Hi {instance.username},\n\nClick the link below to activate your account:\n\n{activation_link}\n\nThank you!"
        send_mail(subject, message, settings.EMAIL_HOST_USER, [instance.email])


@receiver(post_save, sender=CustomUser)
def assign_role(sender, instance, created, **kwargs):
    if created:
        participant_group, created = Group.objects.get_or_create(
            name='Participant')
        instance.groups.add(participant_group)
        instance.save()
