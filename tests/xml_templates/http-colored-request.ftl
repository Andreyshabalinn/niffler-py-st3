<html>
<head>
    <meta http-equiv="content-type" content="text/html; charset = UTF-8">
    <script src="https://yastatic.net/jquery/2.2.3/jquery.min.js" crossorigin="anonymous"></script>

    <link href="https://yastatic.net/bootstrap/3.3.6/css/bootstrap.min.css" rel="stylesheet" crossorigin="anonymous">
    <script src="https://yastatic.net/bootstrap/3.3.6/js/bootstrap.min.js" crossorigin="anonymous"></script>

    <link type="text/css" href="https://yandex.st/highlightjs/8.0/styles/github.min.css" rel="stylesheet"/>
    <script type="text/javascript" src="https://yandex.st/highlightjs/8.0/highlight.min.js"></script>
    <script type="text/javascript" src="https://yandex.st/highlightjs/8.0/languages/bash.min.js"></script>
    <script type="text/javascript" src="https://yandex.st/highlightjs/8.0/languages/json.min.js"></script>
    <script type="text/javascript" src="https://yandex.st/highlightjs/8.0/languages/xml.min.js"></script>
    <script type="text/javascript">hljs.initHighlightingOnLoad();</script>

    <style>
        pre {
            white-space: pre-wrap;
        }
    </style>
</head>
<body>
<div>
    <pre><code>{% if request.method %}{{request.method}}{% else %}GET{% endif %} to {% if request.url %}{{request.url}}{% else %}None{% endif %}</code></pre>
</div>

{% if request.body %}
    <h4>Body</h4>
    <div>
        <pre><code>{{request.body}}</code></pre>
    </div>
{% endif %}


{% if request.headers %}
    <h4>Headers</h4>
    <div>
    {% for key, value in request.headers.items() %}
        <div>
            <pre><code><b>{{key}}</b>: {{value}}</code></pre>
        </div>
    {% endfor %}
    </div>
{% endif %}


{% if request.cookies %}
    <h4>Cookies</h4>
    <div>
    {% for key, value in request.cookies.items() %}
        <div>
            <pre><code><b>{{key}}</b>: {{value}}</code></pre>
        </div>
    {% endfor %}
    </div>
{% endif %}

{% if curl %}
    <h4>Curl</h4>
    <div>
        <pre><code>{{curl}}</code></pre>
    </div>
{% endif %}
</body>
</html>