# TelegramBotsCallbackData

[EN]This library was created to facilitate working with callback data from inline buttons in Telegram.

[RU]Эта библиотека была создана для облегчения работы с callback data у inline кнопок в Телеграмме.

# How its work? / Как это работает?

```python
from TelegramBotsCallbackData import CallbackData

callback_data = CallbackData()

# Create Callback Data
...
button = InlineKeyboardButton(
  text="Text",
  callback_data=callback_data.new({
    # Any object that can be pickled
  }))
...

# Restore Callback Data
...
data = callback_data.restore(CallbackQuery.data)
...
```
