{% extends "mail_templated/base.tpl" %}

{% block subject %}
Password Reset Request for MixShop
{% endblock %}

{% block html %}
    <h2>Hello {{ email_name }}</h2>

    <p>
        We received a request to reset the password for your account for this email address. Click the link below to set a new password.
        <a href="{{ protocol }}://{{ domain }}{% url 'accounts:password_reset_confirm' uid=uid token=token %}">Link</a>
    </p>
    <p>
       If you didn't make this request, you can simply ignore this email.
    </p>

    <h4>Your email is: {{ email }}</h4>

    <p>Thank you for choosing us</p>
    <p>The MixShop Team</p>

{% endblock %}
