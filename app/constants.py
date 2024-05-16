from app.core.config import settings

GOOGLE_SPRDSHEET_URL_TEMPLATE = 'https://docs.google.com/spreadsheets/d/'


class FieldExamples:
    COMMENT = 'Котухам на еду'
    DESCRIPTION_1 = 'Требуются средства на закупку сухого кошачьего корма'
    DESCRIPTION_2 = ('Требуются средства на закупку сухого кошачьего корма, '
                     'а также консерв и полуфабрикатов')
    FULL_AMOUNT_1 = 10_000
    FULL_AMOUNT_2 = 15_000
    FULL_AMOUNT_3 = 7_500
    ID_1 = 1
    ID_2 = 2
    NAME_1 = 'Накормим кошек!'
    NAME_2 = 'Накормим кошек вместе!'


class Messages:
    NAME_ALR_EXIST = 'Проект с таким именем уже существует!'
    PASSWORD_CONTAINS_EMAIL = 'Пароль не должен содержать в себе адрес почты'
    PASSWORD_TO_SHORT = ('Пароль должен состоять минимум '
                         f'из {settings.password_length} символов')
    PROJECT_ALR_CLOSED = 'Закрытый проект нельзя редактировать!'
    PROJECT_ALR_INVESTED = ('В проект были внесены средства, '
                            'не подлежит удалению!')
    PROJECT_NOT_FOUND = 'Благотворительный проект не найден!'
    USER_CREATED = 'Пользователь {} зарегистрирован.'
    WRONG_FULL_AMOUNT = ('Нелья установить значение full_amount '
                         'меньше уже вложенной суммы.')
