from app.dtos import CreatePaymentMethodDto, UpdatePaymentMethodDto
from app.exceptions import PaymentMethodNotFound
from app.models import PaymentMethod
from app.types import FindAllParams


class PaymentMethodService:
    @staticmethod
    def create(dto: CreatePaymentMethodDto) -> PaymentMethod:
        payment_method = PaymentMethod(**dto)
        PaymentMethod.save(payment_method)
        return payment_method

    @staticmethod
    def find_all(params: FindAllParams) -> list[PaymentMethod]:
        return PaymentMethod.find_all(params)

    @staticmethod
    def find_first(id: int) -> PaymentMethod:
        payment_method = PaymentMethod.find_first_by_id(id)

        if not payment_method:
            raise PaymentMethodNotFound()

        return payment_method

    @classmethod
    def update(cls, id: int, dto: UpdatePaymentMethodDto) -> PaymentMethod:
        payment_method = cls.find_first(id)
        payment_method.update(**dto)
        PaymentMethod.save(payment_method)
        return payment_method

    @classmethod
    def deactivate(cls, id: int) -> None:
        payment_method = cls.find_first(id)
        PaymentMethod.deactivate(payment_method)
        PaymentMethod.save(payment_method)
