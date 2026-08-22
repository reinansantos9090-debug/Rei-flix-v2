import flet as ft
from views.home_view import HomeView
from views.detail_view import DetailView
from views.player_view import PlayerView

def main(page: ft.Page):
    page.title = "Rei-Flix Pro"
    page.theme_mode = ft.ThemeMode.DARK
    page.window_width = 400
    page.window_height = 750
    page.window_resizable = True
    page.padding = 0

    def route_change(route):
        page.views.clear()
        
        if page.route == "/":
            page.views.append(
                ft.View(
                    "/",
                    [HomeView.build(page, on_select_anime=lambda anime: navigate_to_detail(anime))]
                )
            )
        elif page.route == "/detail":
            # Aqui receberemos os dados do anime selecionado
            pass
        elif page.route == "/player":
            pass
            
        page.update()

    def navigate_to_detail(anime_data):
        # Transição limpa para a tela de detalhes
        page.views.append(
            ft.View(
                "/detail",
                [DetailView.build(page, anime_data, on_back=lambda: page.views.pop() or page.update())]
            )
        )
        page.update()

    page.on_route_change = route_change
    page.go("/")

ft.app(target=main)

