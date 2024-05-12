import flet as ft
import requests


def show_user_details(page: ft.Page, user_id: int):
    response = requests.get(f"https://dummyjson.com/users/{user_id}")
    user_data = response.json()

    # Components for displaying user details
    user_image = ft.Image(src=user_data["image"], width=150, height=150)
    user_name = ft.TextField(
        value=f"{user_data['firstName']} {user_data['lastName']}",
        read_only=True,
        label="Full Name",
    )
    user_email = ft.TextField(value=user_data["email"], read_only=True, label="Email")
    user_phone = ft.TextField(value=user_data["phone"], read_only=True, label="Phone")

    # Create an AlertDialog to display user details
    details_alert = ft.AlertDialog(
        title=ft.Text("User Details"),
        content=ft.Column([user_image, user_name, user_email, user_phone]),
        actions=[
            ft.TextButton(
                text="CLOSE", on_click=lambda e: close_dialog(page, details_alert)
            )
        ],
    )

    # Set dialog to page and open it
    page.dialog = details_alert
    details_alert.open = True
    page.update()


def close_dialog(page: ft.Page, dialog: ft.AlertDialog):
    dialog.open = False
    page.update()


def main(page: ft.Page):
    page.title = "User List"
    page.vertical_alignment = ft.MainAxisAlignment.START
    page.horizontal_alignment = ft.MainAxisAlignment.CENTER

    # Fetch list of users
    response = requests.get("https://dummyjson.com/users")
    users = response.json()["users"]

    # Create a ListView for users
    user_list = ft.ListView(expand=True)

    for user in users:
        # Create a ListTile for each user
        tile = ft.ListTile(
            leading=ft.Icon(ft.icons.PERSON),
            title=ft.Text(f"{user['firstName']} {user['lastName']}"),
            subtitle=ft.Text(user["email"]),
            trailing=ft.IconButton(
                icon=ft.icons.INFO,
                on_click=lambda e, user_id=user["id"]: show_user_details(page, user_id),
            ),
        )
        user_list.controls.append(tile)

    page.add(user_list)


ft.app(target=main)
