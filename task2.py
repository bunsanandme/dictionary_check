from nltk import edit_distance

changed_content = []  # Здесь будем хранить весь текст
changed_sentence = []  # Промежуточный контейнер для отдельных предложений
dictionary = []  # Распаковываем словарь из файла и добавляем в список
with open("dict.txt") as file:
    dictionary = file.read().split("\n")


def change_word(word):
    """
    Основная функция замены слов.
    Слово проверяется по списку, и заменяется словом с меньшей разницей в ошибке
    """
    error = len(word)
    error_index = 0
    for i in dictionary:
        if edit_distance(i, word) < error:
            error = edit_distance(i, word)
            error_index = dictionary.index(i)
    if word == word.capitalize():
        word = dictionary[error_index].capitalize()
    else:
        word = dictionary[error_index]
    return word


with open("txt.txt") as file:
    # Открываем файл, форматируем файл
    # Проходимся по словам, собираем их снова в предложение и добавляем в контейнер всего текста
    content = file.read().replace("\n", "").split('.')
    content = [sentence.strip() for sentence in content]
    for sentence in content:
        for word in sentence.split(" "):
            changed_sentence.append(change_word(word))
        changed_content.append(" ".join(changed_sentence))
        changed_sentence = []

# Записываем в файл, разделяем предложения по 5 в одной строке
with open("result2.txt", "w") as file:
    for i in changed_content:
        print(i, file=file, end="."),
        if changed_content.index(i) % 5 == 4:
            file.write("\n\n")
