from aiogram.fsm.state import StatesGroup, State


class SubscriberState(StatesGroup):
    """
    States for managing the subscription process.

    This class defines states representing different steps in the subscription process.
    Each state corresponds to collecting specific information from the user,
    such as their email or password.
    """
    email = State()
    password = State()
