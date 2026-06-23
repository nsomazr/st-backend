USD_TO_TZS_RATE = 2600


def usd_to_tzs(usd):
    return round(float(usd) * USD_TO_TZS_RATE)


def fmt_usd(amount, prefix=''):
    value = float(amount)
    return f'{prefix}${value:,.0f}'


def fmt_tzs(amount, prefix=''):
    value = round(float(amount))
    return f'{prefix}TZS {value:,}'


def fmt_price_from(usd):
    amount = float(usd)
    if amount <= 0:
        return ''
    return f'From {fmt_usd(amount)} · {fmt_tzs(usd_to_tzs(amount))}'


def fmt_budget_range(budget_range):
    labels = {
        'under_500': f'< {fmt_usd(500)} · < {fmt_tzs(usd_to_tzs(500))}',
        '500_1500': (
            f'{fmt_usd(500)} – {fmt_usd(1500)} · '
            f'{fmt_tzs(usd_to_tzs(500))} – {fmt_tzs(usd_to_tzs(1500))}'
        ),
        '1500_5000': (
            f'{fmt_usd(1500)} – {fmt_usd(5000)} · '
            f'{fmt_tzs(usd_to_tzs(1500))} – {fmt_tzs(usd_to_tzs(5000))}'
        ),
        'over_5000': f'Over {fmt_usd(5000)} · Over {fmt_tzs(usd_to_tzs(5000))}',
    }
    return labels.get(budget_range, budget_range)
