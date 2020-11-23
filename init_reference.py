from about_service.models import AboutService
from support.models import Support
from ext import db


def init_reference():
    create_about_service = AboutService(
        description='Приветствуем вас на сервисе обмена товаров Pinhome! С помощью данного сервиса вы '
                    'сможете найти применение ненужным вещам, обменяв их с другими пользователями на то, '
                    'что вам действительно нужно. Основное правило экологичного образа жизни: ненужных вещей '
                    'нет. Помимо обмена, вы можете воспользоваться услугами социальных и экологических '
                    'проектов. Они отправят ваши вещи на переработку или отдадут их тем, кто в них '
                    'действительно нуждается. Основные принципы сервиса — все сделки проводятся на бартерной '
                    'основе, без использования денег.')
    db.session.add(create_about_service)
    db.session.commit()
    create_support = Support(description='По вопросам — работы приложения, — бартера или сотрудничества пишите на '
                                         'почту pinhome_support@gmail.com.')
    db.session.add(create_support)
    db.session.commit()


if __name__ == '__main__':
    init_reference()
