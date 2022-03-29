import multiprocessing
from multiprocessing import Queue, Process
from nltk import edit_distance

changed_content = []  # Здесь будем хранить весь текст
changed_sentence = []  # Промежуточный контейнер для отдельных предложений
dictionary = []  # Распаковываем словарь из файла и добавляем в список
with open("dict.txt") as file:
    dictionary = file.read().split("\n")

n = 5


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


def change_sentence(q, sentence):
    '''
    Функция для изменения целого предложения
    В конце добавляется в очередь измененное предложение
    '''
    changed_sentence = []
    for word in sentence.split(" "):
        changed_sentence.append(change_word(word))
    q.put(changed_sentence)


if __name__ == "__main__":
    q = Queue() # Создаем очередь и список процессов
    processes = []
    with open("txt.txt") as file:
        # Открываем файл, форматируем файл
        # Создаем список всех предложений
        content = file.read().replace("\n", "").split('.')
        content = [sentence.strip() for sentence in content]
        changed_content = []
    for j in range(20): # Запускаем цикл по всему тексту двумя циклами, разделяя на n
        for i in range(n):
            # Создаем процесс, добавляем список и запускаем процесс
            process = Process(target=change_sentence, args=(q, content.pop()))
            processes.append(process)
            process.start()
        for i in range(n):
            # Добавляем из очереди предложения
            changed_content.append(" ".join(q.get(True)))
        for i in range(n):
            # Завершаем процессы
            processes[i].join()

    # Также, как и в прошлых заданиях записываем в файл
    with open("result3.txt", "w") as file:
        for i in changed_content[::-1]:
            print(i, file=file, end="."),
            if changed_content.index(i) % 5 == 4:
                file.write("\n\n")
