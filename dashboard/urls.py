from django.urls import path

from . import views

app_name = "dashboard"
urlpatterns = [
    path("", views.home, name="home"),
    path("notes", views.notes_view, name="notes-page"),
    path("delete_note/<int:pk>", views.delete_note, name="delete-note"),
    path("detail_note/<int:pk>", views.NotesDetailView, name="notes-detail"),
    path("homework", views.homework_view, name="homework"),
    path(
        "update_homework/<int:pk>", views.update_homework_view, name="update-homework"
    ),
    path(
        "delete_homework/<int:pk>", views.delete_homework_view, name="delete-homework"
    ),
    path("youtube", views.youtube_view, name="youtube"),
    path("todo", views.todo_view, name="todo"),
    path(
        "delete_todo/<int:pk>", views.delete_todo_view, name="delete-todo"
    ),
    path(
        "update_todo/<int:pk>", views.update_todo_view, name="update-todo"
    ),
    path("books", views.book_view, name="books"),
    path("wikipedia", views.wikipedia_view, name="wikipedia"),
    path("dictionary", views.dictionary_view, name="dictionary"),
    path("conversion", views.conversion_view, name="conversion"),
    
]

