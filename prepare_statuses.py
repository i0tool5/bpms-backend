# Creates default statuses
# It should be done in different way
# (As described https://docs.djangoproject.com/en/3.2/howto/initial-data/)

def prepare():
    from projects.models import Status
    default_statuses = ['Квалификация', 'Отправлено КП',
            'Выслан договор', 'Договор подписан',
            'Выставлен счёт', 'Аванс получен',
            'Исполнение',
    ]

    ns = [Status(name=status) for status in default_statuses]
    Status.objects.bulk_create(ns)

