import telebot
from telebot import types

bot = telebot.TeleBot('5135451773:AAFj-8ZUeEa58t-jDVEBkOoZ8-pAox1r2U8')

skolko_kup = 0
kurs_bir = 0
kurs_bank = 0
skolko_prod = 0
cena_prod_bank = 0
cena_prod_bir = 0
def isfloat(value):
    try:
        float(value)
        return True
    except ValueError:
        return False


@bot.message_handler(content_types=['text'])
def start(message):
    if message.text == '/reg':
        bot.send_message(message.from_user.id, "Сколько куплено?")
        bot.register_next_step_handler(message, get_info_skolko_kup) #следующий шаг – функция get_name
    else:
        bot.send_message(message.from_user.id, 'Напиши /reg')

def get_info_skolko_kup(message):
    global skolko_kup
    skolko_kup = message.text
    if skolko_kup.isdigit():
        skolko_kup = int(skolko_kup)
        print(skolko_kup)
        bot.send_message(message.from_user.id, 'Введите цену банка')
        bot.register_next_step_handler(message, get_info_cena_banka)
    else:
        bot.send_message(message.from_user.id, 'Введите корректно')
        bot.register_next_step_handler(message, get_info_skolko_kup)

def get_info_cena_banka(message):
    global kurs_bank
    kurs_bank = message.text
    if isfloat(kurs_bank):
        kurs_bank = float(kurs_bank)
        print(kurs_bank)
        bot.send_message(message.from_user.id, 'Введите цену биржи')
        bot.register_next_step_handler(message, get_info_cena_bir)
    else:
        bot.send_message(message.from_user.id, 'Введите корректно')
        bot.register_next_step_handler(message, get_info_cena_banka)

def get_info_cena_bir(message):
    global kurs_bir
    kurs_bir = message.text
    if isfloat(kurs_bir):
        kurs_bir = float(kurs_bir)
        print(kurs_bir)
        bot.send_message(message.from_user.id, 'Введите сколько продано')
        bot.register_next_step_handler(message, get_info_skolko_prod)
    else:
        bot.send_message(message.from_user.id, 'Введите корректно')
        bot.register_next_step_handler(message, get_info_cena_bir)

def get_info_skolko_prod(message):
    global skolko_prod
    skolko_prod = message.text
    if skolko_prod.isdigit():
        skolko_prod = int(skolko_prod)
        print(skolko_prod)
        bot.send_message(message.from_user.id, 'Введите цену продажи банка')
        bot.register_next_step_handler(message, f_cena_prod_bank)
    else:
        bot.send_message(message.from_user.id, 'Введите корректно')
        bot.register_next_step_handler(message, get_info_skolko_prod)

def f_cena_prod_bank(message):
    global cena_prod_bank
    cena_prod_bank = message.text
    if isfloat(cena_prod_bank):
        cena_prod_bank = float(cena_prod_bank)
        print('lo', cena_prod_bank)
        bot.send_message(message.from_user.id, 'Введите цену продажи биржи')
        bot.register_next_step_handler(message, f_cena_prod_bir)
    else:
        bot.send_message(message.from_user.id, 'Введите корректно')
        bot.register_next_step_handler(message, get_info_cena_bir)

def f_cena_prod_bir(message):
    global cena_prod_bir
    cena_prod_bir = message.text
    if isfloat(cena_prod_bir):
        cena_prod_bir = float(cena_prod_bir)
        print(cena_prod_bir)
        bot.send_message(message.from_user.id, 'ОК')
        itog_sum_pokup_bez_kom = skolko_kup*kurs_bank
        if skolko_kup >= 1 and skolko_kup <= 999:
            kom_bir = 1
        else:
            kom_bir = kurs_bir * skolko_kup * 0.0015 / 100
            print(kom_bir)
        kom_brok = skolko_kup * kurs_bir * 0.04 / 100
        print(kom_brok)
        kom_prod_brok = skolko_prod * cena_prod_bir * 0.04 / 100
        if skolko_prod >= 1 and skolko_prod <= 999:
            kom_prod_bir = 1
        else:
            kom_prod_bir = cena_prod_bir * skolko_prod * 0.0015 / 100
        print('fj', kom_prod_brok)

        bot.send_message(message.from_user.id, f'Сколько куплено: {skolko_kup}')
        bot.send_message(message.from_user.id, f'Итог покупки без комиссий: {round(itog_sum_pokup_bez_kom, 4)}')
        bot.send_message(message.from_user.id, f'Комиссия брокера: {round(kom_brok, 4)}')
        bot.send_message(message.from_user.id, f'Комиссия биржи: {round(kom_bir, 4)}')
        bot.send_message(message.from_user.id, f'Итоговая покупка: {round(kom_bir + kom_brok + itog_sum_pokup_bez_kom, 4)}')
        bot.send_message(message.from_user.id, '------------------------------------------------------')
        bot.send_message(message.from_user.id, f'Сколько продано: {skolko_prod}')
        bot.send_message(message.from_user.id, f'Итог покупки без комиссии: {round(cena_prod_bank * skolko_prod, 4)}')
        bot.send_message(message.from_user.id, f'Коммисия брокера при продаже: {round(kom_prod_brok, 4)}')
        bot.send_message(message.from_user.id, f'Коммисия биржи при продаже: {round(kom_prod_bir, 4)}')
        bot.send_message(message.from_user.id, f'Итоговая цена при продаже с комиссией: {round((skolko_prod*cena_prod_bank)-(kom_prod_brok + kom_prod_bir) , 4)}')
        bot.send_message(message.from_user.id, '__________________________________________')
        bot.send_message(message.from_user.id, f'Выигрышь: {round(((skolko_prod*cena_prod_bank)-(kom_prod_brok + kom_prod_bir))-(skolko_prod*kurs_bank * 0.0015 / 100 + skolko_prod*kurs_bank * 0.04 / 100 + skolko_prod*kurs_bank), 4)}')

    else:
        bot.send_message(message.from_user.id, 'Введите корректно')
        bot.register_next_step_handler(message, get_info_cena_banka)
def main():
    while True:
        try:
            bot.polling(none_stop=True)
        except Exception as e:
            print(e)

if __name__ == "__main__":
    main()

bot.polling(none_stop=True, interval=0)

