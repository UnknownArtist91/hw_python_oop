class InfoMessage:
    """Информационное сообщение о тренировке."""
    def __init__(self,
                 training_type: str,
                 duration: float,
                 distance: float,
                 speed: float,
                 calories: float
                 ) -> None:
        self.training_type = training_type
        self.duration = duration
        self.distance = distance
        self.speed = speed
        self.calories = calories

    def get_message(self) -> str:
        return(f'Тип тренировки: {self.training_type}; '
               f'Длительность: {self.duration:.3f} ч.; '
               f'Дистанция: {self.distance:.3f} км; '
               f'Ср. скорость: {self.speed:.3f} км/ч; '
               f'Потрачено ккал: {self.calories:.3f}.')


class Training:
    """Базовый класс тренировки."""
    LEN_STEP = 0.65
    M_IN_KM = 1000
    M_IN_HOUR = 60

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 ) -> None:
        self.action = action
        self.duration = duration
        self.weight = weight

    def get_distance(self) -> float:
        """Получить результат в км."""
        return self.action * self.LEN_STEP / self.M_IN_KM

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость ."""
        return self.get_distance() / self.duration

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        raise NotImplementedError('Определите калории.')

    def show_training_info(self) -> InfoMessage:
        """Возврат сообщения о выполненной тренировке."""
        return InfoMessage(self.__class__.__name__,
                           self.duration,
                           self.get_distance(),
                           self.get_mean_speed(),
                           self.get_spent_calories()
                           )


class Running(Training):
    """Тренировка: бег."""
    CEFF_CALORIE_RUN_1 = 18
    CEFF_CALORIE_RUN_2 = 20

    def get_spent_calories(self) -> float:
        """Расчет потраченных калорий при беге."""
        return ((self.CEFF_CALORIE_RUN_1
                * self.get_mean_speed() - self.CEFF_CALORIE_RUN_2)
                * self.weight / self.M_IN_KM
                * (self.duration * self.M_IN_HOUR))


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""
    CEFF_CALORIE_WALK_1 = 0.035
    CEFF_CALORIE_WALK_2 = 0.029

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 height: float) -> None:
        super().__init__(action, duration, weight)
        self.height = height

    def get_spent_calories(self) -> float:
        """Расчет  калорий при ходьбе."""
        mean_speed: float = self.get_mean_speed()
        return ((self.CEFF_CALORIE_WALK_1
                * self.weight
                + (mean_speed**2 // self.height)
                * self.CEFF_CALORIE_WALK_2
                * self.weight)
                * self.M_IN_HOUR * self.duration)


class Swimming(Training):
    """Тренировка: плавание."""
    LEN_STEP: float = 1.38

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 length_pool: float,
                 count_pool: float) -> None:
        super().__init__(action, duration, weight)
        self.length_pool = length_pool
        self.count_pool = count_pool

    def get_mean_speed(self) -> float:
        """Средний расчет скорости при плавании"""
        return (self.length_pool * self.count_pool
                / self.M_IN_KM / self.duration)

    def get_spent_calories(self) -> float:
        """Расчет  калорий при плавании."""
        COEFF_CALORIE_SWIM_1: float = 1.1
        COEFF_CALORIE_SWIM_2: float = 2
        spent_calories_swim: float = ((self.get_mean_speed()
                                      + COEFF_CALORIE_SWIM_1)
                                      * COEFF_CALORIE_SWIM_2 * self.weight)
        return spent_calories_swim


def read_package(workout_type: str, data: list) -> Training:
    """Данные с датчиков."""
    meaning: dict[str , type[Training]] = {'SWM': Swimming,
                                           'RUN': Running,
                                           'WLK': SportsWalking}
    if workout_type not in meaning:
        raise ValueError(f'Не известный {workout_type},'
                         f'  тип тренеровки!')
    return meaning[workout_type](*data)


def main(training: Training) -> None:
    """Главная функция."""
    info = training.show_training_info()
    info_result = InfoMessage.get_message(info)
    print(info_result)


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]
    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)
