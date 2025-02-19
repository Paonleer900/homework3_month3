from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
import buttons
from aiogram.dispatcher.filters.state import State, StatesGroup


class FSM_store(StatesGroup):
    name_product = State()
    size_product = State()
    price_product = State()
    id_product = State()
    photo_product = State()
    submit = State()


async def fsm_start(message: types.Message):
    await FSM_store.name_product.set()
    await message.answer(text='Введите название товара: ',
                         reply_markup=buttons.cancel)


async def load_name_product(message: types.Message, state: FSMContext):
    async with state.proxy() as data_store:
        data_store['name_product'] = message.text

    await FSM_store.next()
    await message.answer(text='Укажите размер товара: ')


async def load_size_product(message: types.Message, state: FSMContext):
    async with state.proxy() as data_store:
        data_store['size_product'] = message.text

    await FSM_store.next()
    await message.answer(text='Укажите цену товара: ')


async def load_price_product(message: types.Message, state: FSMContext):
    async with state.proxy() as data_store:
        data_store['price_product'] = message.text

    await FSM_store.next()
    await message.answer(text='Укажите артикул товара: ')


async def load_id_product(message: types.Message, state: FSMContext):
    async with state.proxy() as data_store:
        data_store['id_product'] = message.text

    await FSM_store.next()
    await message.answer(text='Отправьте фотографию товара:')


async def load_photo(message: types.Message, state: FSMContext):
    async with state.proxy() as data_store:
        data_store['photo'] = message.photo[-1].file_id

    await message.answer_photo(photo=data_store['photo'],
                               caption=f"Название товара - {data_store['name_product']}\n"
                                       f"Размер - {data_store['size_product']}\n"
                                       f"Цена - {data_store['price_product']}\n"
                                       f"Артикул - {data_store['id_product']}",
                               reply_markup=buttons.submit_buttons)
    await FSM_store.next()


async def submit(message: types.Message, state: FSMContext):
    if message.text == "Да":
        kb = types.ReplyKeyboardRemove()
        await message.answer(text='Ваши данные сохранены!', reply_markup=kb)
        await state.finish()
    else:
        await message.answer(text='Отменено!')
        await state.finish()


async def cancel_fsm(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is not None:
        await state.finish()
        await message.answer(text='Отменено!')


def store_fsm(dp: Dispatcher):
    dp.register_message_handler(cancel_fsm, Text(equals='Отмена',
                                                 ignore_case=True),
                                state="*")

    dp.register_message_handler(fsm_start, commands=['product'])
    dp.register_message_handler(load_name_product, state=FSM_store.name_product)
    dp.register_message_handler(load_size_product, state=FSM_store.size_product)
    dp.register_message_handler(load_price_product, state=FSM_store.price_product)
    dp.register_message_handler(load_id_product, state=FSM_store.id_product)
    dp.register_message_handler(load_photo, state=FSM_store.photo_product, content_types=['photo'])
    dp.register_message_handler(submit, state=FSM_store.submit)
