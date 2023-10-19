from abc import ABCMeta, abstractmethod


class CommissionModel(object, metaclass=ABCMeta):
    """ABC for commission models

    Commission models are responsible for accepting order/transaction pairs and
    calculating how much commission should be charged to an algorithm's account
    on each transaction.
    """

    @abstractmethod
    def calculate(self, ) -> float:
        """
        Returns
        -------
        amount_charged: float
            The additional commission, in yuans, that we should attribute to this order.
        """
        raise NotImplementedError(f"{self.__name__}.calculate")