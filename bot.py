import telebot
from telebot.types import InlineKeyboardButton,InlineKeyboardMarkup

import films

bot = telebot.TeleBot("ENTER BOT ID")
@bot.message_handler(commands=["start"])
def start(message):
    keyboard = InlineKeyboardMarkup()
    keyboard.add(InlineKeyboardButton("Help",callback_data="Help"))

    bot.send_message(message.chat.id,"Hello, I am a movie bot. How can I assist you today?",reply_markup=keyboard)
@bot.message_handler(commands=["help"])
def help(message):
    keyboard = InlineKeyboardMarkup()
    keyboard.add(InlineKeyboardButton("Films",callback_data="Films"))
    bot.send_message(message.chat.id,"Here you can access to films",reply_markup=keyboard)
@bot.message_handler(commands=["films"])
def movies(message):
    keyboard = InlineKeyboardMarkup()
    buttons = [InlineKeyboardButton(movie,callback_data=f"movie:{movie}")for movie in films.movies]
    keyboard.add(*buttons)
    bot.send_message(message.chat.id,"Choose a film",reply_markup=keyboard)


@bot.callback_query_handler(func=lambda call:True)
def click(call):
    if call.data == "Help":
           keyboard = InlineKeyboardMarkup()
           keyboard.add(InlineKeyboardButton("Films",callback_data="Films"))
           bot.answer_callback_query(call.id)
           bot.send_message(call.message.chat.id,"Here you can access to films",reply_markup=keyboard)
    if call.data == "Films":
          keyboard = InlineKeyboardMarkup()
          buttons = [InlineKeyboardButton(movie,callback_data=f"movie:{movie}")for movie in films.movies]
          keyboard.add(*buttons)
          bot.answer_callback_query(call.id)
          bot.send_message(call.message.chat.id,"Choose a film",reply_markup=keyboard)
    else:
          MovieTitle = call.data.replace("movie:","")
          if MovieTitle in films.movies:
               MovieInfo = films.movies[MovieTitle]
               Photo = MovieInfo.get("Photo","")
               Response = f"{MovieTitle} ({MovieInfo['Year']})\nDirector: {MovieInfo['Director']}\nGenre: {MovieInfo['Genre']}"
               if Photo:
                    bot.send_photo(call.message.chat.id,Photo,Response)
               else:
                    bot.send_message(call.message.chat.id,Response)
          else:
               bot.send_message(call.message.chat.id,"Film not found")

@bot.message_handler(commands=["Addfilm"])
def AddMovie(message):
     bot.reply_to(message,"Enter film name")
     bot.register_next_step_handler(message,AddDirector)
def AddDirector(message):
     UserInfo = {}
     UserInfo["Name"] = message.text
     bot.reply_to(message,"Enter film director")
     bot.register_next_step_handler(message,AddYear,UserInfo)
def AddYear(message,UserInfo):
     UserInfo["Director"] = message.text
     bot.reply_to(message,"Enter film year")
     bot.register_next_step_handler(message,AddGenre,UserInfo)
def AddGenre(message,UserInfo):
     UserInfo["Year"] = message.text
     bot.reply_to(message,"Enter film genre")
     bot.register_next_step_handler(message,AddPhoto,UserInfo)
def AddPhoto(message,UserInfo):
     UserInfo["Genre"] = message.text
     bot.reply_to(message,"Enter film photo")
     bot.register_next_step_handler(message,SaveFilm,UserInfo)
def SaveFilm(message,UserInfo):
     films.movies[UserInfo["Name"]] = {
          "Director": UserInfo["Director"],
          "Year": UserInfo["Year"],
          "Genre": UserInfo["Genre"],
          "Photo": message.text
     }
     bot.reply_to(message,"Film added successfully")
















bot.polling()
