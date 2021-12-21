from api import PetFriends
from settings import *
import os

pf = PetFriends()


def test_get_api_key_for_valid_user(email=valid_email, password=valid_password):
    """ Проверяем что запрос api ключа возвращает статус 200 и в тезультате содержится слово key"""

    # Отправляем запрос и сохраняем полученный ответ с кодом статуса в status, а текст ответа в result
    status, result = pf.get_api_key(email, password)

    # Сверяем полученные данные с нашими ожиданиями
    assert status == 200
    assert 'key' in result


def test_get_all_pets_with_valid_key(filter=''):
    """ Проверяем что запрос всех питомцев возвращает не пустой список.
    Для этого сначала получаем api ключ и сохраняем в переменную auth_key. Далее используя этого ключ
    запрашиваем список всех питомцев и проверяем что список не пустой.
    Доступное значение параметра filter - 'my_pets' либо '' """

    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.get_list_of_pets(auth_key, filter)

    assert status == 200
    assert len(result['pets']) > 0


def test_add_new_pet_with_valid_data(name='Порри', animal_type='Гаттер',
                                     age='1', pet_photo='images/Cats.jpg'):
    """Проверяем что можно добавить питомца с корректными данными"""

    # Получаем полный путь изображения питомца и сохраняем в переменную pet_photo
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    # Запрашиваем ключ api и сохраняем в переменую auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    # Добавляем питомца
    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)

    # Сверяем полученный ответ с ожидаемым результатом
    assert status == 200
    assert result['name'] == name


def test_successful_delete_self_pet():
    """Проверяем возможность удаления питомца"""

    # Получаем ключ auth_key и запрашиваем список своих питомцев
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Проверяем - если список своих питомцев пустой, то добавляем нового и опять запрашиваем список своих питомцев
    if len(my_pets['pets']) == 0:
        pf.add_new_pet(auth_key, "Суперкот", "кот", "3", "images/Cats.jpg")
        _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Берём id первого питомца из списка и отправляем запрос на удаление
    pet_id = my_pets['pets'][0]['id']
    status, _ = pf.delete_pet(auth_key, pet_id)

    # Ещё раз запрашиваем список своих питомцев
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Проверяем что статус ответа равен 200 и в списке питомцев нет id удалённого питомца
    assert status == 200
    assert pet_id not in my_pets.values()


def test_successful_update_self_pet_info(name='Расти', animal_type='Собакен', age=17):
    """Проверяем возможность обновления информации о питомце"""

    # Получаем ключ auth_key и список своих питомцев
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Если список не пустой, то пробуем обновить его имя, тип и возраст
    if len(my_pets['pets']) > 0:
        status, result = pf.update_pet_info(auth_key, my_pets['pets'][3]['id'], name, animal_type, age)

        # Проверяем что статус ответа = 200 и имя питомца соответствует заданному
        assert status == 200
        assert result['name'] == name
    else:
        # если спиок питомцев пустой, то выкидываем исключение с текстом об отсутствии своих питомцев
        raise Exception("Sorry, there is no my pets")

def test_add_new_pet_without_photo(name='Матроскин', animal_type='Котэ', age='5'):
    # Проверяем возможность добавления питомца без фотографии

    # Получаем ключ auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    # Добавляем питомца
    status, result = pf.add_new_pet_without_photo(auth_key, name, animal_type, age)

    assert status == 200
    assert result['name'] == name


def test_add_new_pet_with_incorrect_data(name='Горец', animal_type='Бессмертный',
                                     age='стопицот', pet_photo='images/turtle.jpg'):
    """Проверяем что можно добавить питомца с некорректными данными возраста (тип строка)"""

    # Получаем полный путь изображения питомца и сохраняем в переменную pet_photo
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    # Запрашиваем ключ api и сохраняем в переменую auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    # Добавляем питомца
    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)

    # Сверяем полученный ответ с ожидаемым результатом
    assert status == 200
    assert result['age'] == age


def test_get_all_pets_with_incorrect_key(filter=''):
    """ Проверяем что запрос всех питомцев с использованием неверного api ключа не возвращает статус 200.
        Для этого сначала получаем api ключ и сохраняем в переменную auth_key.
        Далее изменяем переменную auth_key и выполняем запрос"""

    # Запрашиваем ключ api и сохраняем в переменную auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    # Делаем api ключ неверным
    auth_key['key'] = auth_key['key'] + "123"

    status, result = pf.get_list_of_pets(auth_key, filter)
    assert status != 200


def test_get_api_key_for_incorrect_email(email=valid_email, password=valid_password):
    """Проверяем что запрос api ключа с неверным email не возвращает статус 200"""

    # Меняем email на несуществующий.
    status, result = pf.get_api_key(email + "123", password)
    assert status != 200


def test_get_api_key_for_incorrect_password(email=valid_email, password=valid_password):
    """Проверяем что запрос api ключа с неверным password не возвращает статус 200"""

    # Меняем password на неверный
    status, result = pf.get_api_key(email, password + "123")
    assert status != 200


def test_get_api_key_for_invalid_email(email=null_email, password=null_password):
    """Проверяем что запрос api ключа с пустыми полями email и password не возвращает статус 200"""

    # Отправляем запрос и сохраняем полученный ответ с кодом статуса в status
    status, result = pf.get_api_key(email, password)

    assert status != 200


def test_successful_updating_pet_info_incorrect_key(name='Басти', animal_type='Котяра', age=3):
    """ Проверяем возможность обновления информации о питомце с использованием
    неверного api ключа"""

    # Получаем ключ auth_key и запрашиваем список своих питомцев
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Делаем api ключ неверным
    auth_key['key'] = auth_key['key'] + "123"

    # Отправляем запрос на изменение данных первого питомца
    status, result = pf.update_pet_info(auth_key, my_pets['pets'][0]['id'], name, animal_type, age)

    # Проверяем, что в ответе не возращается статус 200
    assert status != 200


def test_successful_updating_info_nonexistent_pet(name='Тестис', animal_type='Собака', age=13):
    """ Проверяем возможность обновления информации о несуществующем питомце"""

    # Получаем ключ auth_key и запрашиваем список своих питомцев
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Отправляем запрос на изменение данных несуществущего питомца
    status, result = pf.update_pet_info(auth_key, my_pets['pets'][0]['id'] + "123", name, animal_type, age)

    # Проверяем, что в ответе не возращается статус 200
    assert status != 200


def test_successful_delete_pet_incorrect_key():
    # Проверяем невозможность удаления питомца с использованием неверного api ключа

    # Получаем ключ auth_key и запрашиваем список своих питомцев
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Делаем api ключ неверным
    auth_key['key'] = auth_key['key'] + "123"

    # Берём id питомца из списка и отправляем запрос на удаление
    pet_id = my_pets['pets'][0]['id']
    status, _ = pf.delete_pet(auth_key, pet_id)

    # Проверяем, что в ответе не возращается статус 200
    assert status != 200


def test_add_new_pet_without_data_only_with_photo(name='', animal_type='', age='', pet_photo='images/dog_smile.jpg'):
    # Проверяем возможность добавления питомца без данных, только с фотографией

    # Получаем полный путь изображения питомца и сохраняем в переменную pet_photo
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    # Получаем ключ auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    # Добавляем питомца
    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)

    # Проверяем что в ответе возвращается статус 200
    assert status == 200
    assert result['pet_photo']