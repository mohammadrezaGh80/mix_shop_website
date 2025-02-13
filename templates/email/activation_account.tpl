{% extends "mail_templated/base.tpl" %}

{% block subject %}
Activation account for MixShop
{% endblock %}

{% block html %}
    <h2>Hello {{ email_name }}</h2>
    <p>Click the link to activate your account.
        <a href="{{ protocol }}://{{ domain }}{% url 'accounts:activation_account' uid=uid token=token %}">Link</a>
    </p>
    <p>
       If you didn't make this request, you can simply ignore this email.
    </p>

    <h4>Your email is: {{ email }}</h4>

    <p>Thank you for choosing us</p>
    <p>The MixShop Team</p>
{% endblock %}
