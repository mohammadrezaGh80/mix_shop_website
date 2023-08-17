{% extends "mail_templated/base.tpl" %}

{% block subject %}
Activation account for MixShop
{% endblock %}

{% block html %}
    <h2>Hello {{ email_name }}</h2>
    <p>Click the link to activate your account.
        <a href="{{ protocol }}://{{ domain }}{% url 'accounts:activation_account' uid=uid token=token %}">Link</a>
    </p>
{% endblock %}
