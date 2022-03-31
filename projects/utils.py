from django.core.mail import EmailMessage


def send_email_invoice(donation, pdf):
    if donation.case is not None:
        case = donation.case.title
    else:
        case = f'{donation.category}'

    msg = EmailMessage(
        f'Invoice #00{donation.id} for {donation.amount} Donation for {case}',
        f'Hi {donation.full_name},'
        f'Thanks for donating to {case}. Your donation means a lot to us and we are very greatful for your {donation.amount} donation'
        'Kind regards,'
        'iGET'
        'igetbangalore@gmail.com',
        [donation.email],
    )
    # msg.attach(pdf)
    msg.send()
