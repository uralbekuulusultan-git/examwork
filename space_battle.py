from application import Application


if __name__ == "__main__":
    try:
        Application().run()
    except ValueError as exc:
        print(f"[КРИТИЧЕСКАЯ ОШИБКА] Некорректные параметры: {exc}")
    except Exception as exc:
        print(f"[КРИТИЧЕСКАЯ ОШИБКА] Неожиданная ошибка: {exc}")
