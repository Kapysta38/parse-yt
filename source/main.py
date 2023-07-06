from client import Client


def get_urls(filename='urls.txt'):
    try:
        with open(filename, 'r') as file:
            return list(filter(lambda x: x, file.read().split('\n')))
    except FileNotFoundError:
        print('Проверьте наличие файла "urls.txt" рядом с программой!')
    return False


def main():
    print('Начало работы скрипта')

    urls = get_urls()
    if not urls:
        return

    client = Client()
    result = client.parse(urls)

    result.to_excel('result.xlsx', index=False)

    print('Скрипт успешно завершил работу, результат в файле result.xlsx')


if __name__ == '__main__':
    main()
    input('\n\nДля выхода из программы введите любую клавишу:')
