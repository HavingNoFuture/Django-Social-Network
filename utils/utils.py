from django.shortcuts import render


def simple_response(request, message: str):
    """
    Возвращает сообщение на отдельной странице с базовым оформлением
    :param request: Стандартный запрос из вьюхи
    :param message: Сообщение
    :return:
    """

    return render(request, "simple_response.html", {"message": message})
