import flet as ft
import pymysql
from pymysql import Error
import hashlib
import time

db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': '',
    'database': 'new_easypay_db',
    'port': 3307
}

def main(page: ft.Page):
    page.title = "Easy Pay"
    page.bgcolor = "white"
    page.window.width = 360
    page.window.height = 740
    page.window.resizable = False
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.vertical_alignment = ft.MainAxisAlignment.CENTER

    background = ft.Container(
        content=ft.Image(
            src="assets/hand-drawn-bussines-pattern-doodle-business-seamless-pattern-doodle-business-background_698782-3476.jpg",
            fit=ft.ImageFit.COVER,
            width=360,
            height=740,
            opacity=0.2,
        ),
        alignment=ft.alignment.center,
        expand=True
    )

    def save_to_database(user_data):
        conn = None
        cursor = None
        try:
            conn = pymysql.connect(**db_config)
            print("Connection successful")
            cursor = conn.cursor()
            hashed_password = hash_password(user_data['password'])
            query = """
            INSERT INTO users (phone, password, first_name, middle_name, last_name, sex)
            VALUES (%s, %s, %s, %s, %s, %s)
            """
            values = (
                user_data['phone'],
                hashed_password,
                user_data['first_name'],
                user_data['middle_name'],
                user_data['last_name'],
                user_data['sex']
            )
            print(f"Executing query with values: {values}")
            cursor.execute(query, values)
            conn.commit()
            print("Data saved successfully")
            return True
        except Error as e:
            print(f"Database Error: {e}")
            return False
        except Exception as e:
            print(f"Unexpected error: {e}")
            return False
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

    def hash_password(password):
        return hashlib.sha256(password.encode()).hexdigest()

    def validate_login(e):
        if not login_password.value:
            warning_error("Password is required!")
            return

        loading = ft.Container(
            content=ft.Column([
                ft.ProgressRing(width=40, height=40, stroke_width=3, color=ft.colors.GREEN),
                ft.Text("Logging in...", size=12, color="black", weight="bold")
            ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=10),
            padding=20,
            width=230,
            margin=ft.margin.only(top=250, left=55, bottom=330),
            bgcolor=ft.colors.WHITE,
            border_radius=15,
            shadow=ft.BoxShadow(
                spread_radius=1,
                blur_radius=15,
                color=ft.colors.BLACK12,
            ),
            alignment=ft.alignment.center,
        )

        page.overlay.append(loading)
        page.update()

        try:
            conn = pymysql.connect(**db_config)
            cursor = conn.cursor(pymysql.cursors.DictCursor)
            hashed_password = hash_password(login_password.value)

            cursor.execute("""
                SELECT id, first_name, balance, phone
                FROM users
                WHERE password = %s
            """, (hashed_password,))
            user = cursor.fetchone()

            if user:
                time.sleep(1.5)
                page.overlay.clear()
                page.update()

                user_data = {
                    'first_name': user['first_name'],
                    'balance': float(user['balance']) if user['balance'] is not None else 0.00
                }
                page.client_storage.set("user_data", user_data)
                page.client_storage.set("user_phone", user['phone'])

                success_popup = ft.Container(
                    content=ft.Row([
                        ft.Icon(ft.icons.CHECK_CIRCLE, color="white", size=20),
                        ft.Text("Successfully logged in!", color="white", size=11, weight="bold")
                    ], alignment=ft.MainAxisAlignment.CENTER, spacing=10),
                    bgcolor=ft.colors.GREEN_400,
                    padding=15,
                    width=250,
                    border_radius=15,
                    margin=ft.margin.only(top=15, left=55)
                )

                page.overlay.append(success_popup)
                page.update()

                time.sleep(1.5)
                page.overlay.clear()
                page.update()
                show_dashboard(user_data)
            else:
                page.overlay.clear()
                page.update()
                warning_error("Incorrect password!")

        except Error as e:
            print(f"Database error: {e}")
            page.overlay.clear()
            page.update()
            warning_error("Login failed!")
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()


    def warning_error(message):
        error_popup = ft.Container(
            content=ft.Row(
                [
                    ft.Icon(ft.icons.ERROR_OUTLINE, color="white", size=20),
                    ft.Text(message, color="white", size=12, weight="bold")
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                spacing=10
            ),
            bgcolor=ft.colors.RED_400,
            padding=15,
            width=200,
            border_radius=15,
            margin=ft.margin.only(top=15,left=70),
            offset=ft.transform.Offset(0, 0),
            animate_offset=ft.animation.Animation(200, ft.AnimationCurve.EASE)
        )
        def shake():
            positions = [0.0, -20.0, 20.0, -10.0, 10.0, -5.0, 5.0, 0.0]
            duration = 50

            page.overlay.append(error_popup)
            page.update()

            for i, pos in enumerate(positions):
                page.after((i + 1) * duration, lambda p=pos: setattr(error_popup, 'offset', ft.transform.Offset(p, 0)))

            page.after(2000, lambda: page.overlay.remove(error_popup))
            page.update()

        shake()

        def success_message(message):
            success_popup = ft.Container(
                content=ft.Row(
                    [
                        ft.Icon(ft.icons.CHECK_CIRCLE, color="white", size=20),
                        ft.Text(message, color="white", size=11, weight="bold")
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                    spacing=10
                ),
                bgcolor=ft.colors.GREEN_400,
                padding=15,
                width=250,
                border_radius=15,
                margin=ft.margin.only(top=15, left=55),
                offset=ft.transform.Offset(0, 0),
                animate_offset=ft.animation.Animation(200, ft.AnimationCurve.EASE)
            )

            async def animate():
                import asyncio
                positions = [0.0, -20.0, 20.0, -10.0, 10.0, -5.0, 5.0, 0.0]
                duration = 0.05

                page.overlay.append(success_popup)
                page.update()

                for pos in positions:
                    success_popup.offset = ft.transform.Offset(pos, 0)
                    page.update()
                    await asyncio.sleep(duration)

                await asyncio.sleep(2)
                page.overlay.remove(success_popup)
                page.update()

            page.add_future(animate())

    def validate_phone(e):
        text = ''.join(filter(str.isdigit, e.control.value if e.control.value else ""))
        text = text[:11]
        e.control.value = text
        if len(text) != 11:
            e.control.error_text = "Phone number must be 11 digits"
        else:
            e.control.error_text = None
        page.update()

    image = ft.Image(
        src="assets/7990317.jpg",
        width=250,
        height=250,
        fit=ft.ImageFit.CONTAIN
    )

    image2 = ft.Image(
        src="assets/freepik__upload__13248.jpeg",
        width=250,
        height=250,
        fit=ft.ImageFit.CONTAIN
    )

    image3 = ft.Image(
        src="assets/4707071.jpg",
        width=250,
        height=250,
        fit=ft.ImageFit.CONTAIN
    )

    fname = ft.TextField(
        label="First Name",
        color="black",
        width=280,
        label_style=ft.TextStyle(size=12,color="black"),
        border_color="black",
        border_radius=15
    )

    middlename = ft.TextField(
        label="Middle Name",
        color="black",
        hint_text="(Optional)",
        width=280,
        label_style=ft.TextStyle(size=12,color="black"),
        border_color="black",
        border_radius=15
    )

    lname = ft.TextField(
        label="Last Name",
        color="black",
        width=280,
        label_style=ft.TextStyle(size=12,color="black"),
        border_color="black",
        border_radius=15
    )

    sex = ft.DropdownM2(
        label="Sex",
        label_style=ft.TextStyle(size=12,color="black"),
        border_color="black",
        border_radius=15,
        width=280,
        bgcolor="white",
        color="black",
        options=[
            ft.dropdownm2.Option("Male"),
            ft.dropdownm2.Option("Female"),
            ft.dropdownm2.Option("Prefer not to say")
        ]
    )

    phone = ft.TextField(
        label="Phone Number",
        color="black",
        width=280,
        label_style=ft.TextStyle(size=12),
        border_color="black",
        border_radius=15,
        hint_text="Enter 11 digits",
        keyboard_type=ft.KeyboardType.NUMBER,
        on_change=validate_phone
    )

    login_password = ft.TextField(
        label="Password",
        password=True,
        can_reveal_password=True,
        color="black",
        width=280,
        label_style=ft.TextStyle(size=12),
        border_color="black",
        border_radius=15
    )

    register_password = ft.TextField(
        label="Password",
        password=True,
        can_reveal_password=True,
        color="black",
        width=280,
        label_style=ft.TextStyle(size=12),
        border_color="black",
        border_radius=15
    )

    def back_to_landing(e):
        page.clean()
        show_landing_page()

    def show_landing_page():
        page.overlay.clear()
        page.clean()
        page.add(
            ft.Stack([
                background,
                ft.Container(
                    content=ft.Column(
                        [
                            ft.Row(
                                [
                                    ft.Icon(ft.icons.ACCOUNT_BALANCE_WALLET_ROUNDED,size=42,color="black"),
                                    ft.Text("Easy Pay",size=42,weight=ft.FontWeight.BOLD,color="black"),
                                ],
                                alignment=ft.MainAxisAlignment.CENTER,
                                spacing=10
                            ),
                            image,
                            ft.Divider(height=70, color="transparent", thickness=1),
                            ft.ElevatedButton(
                                "Create an account",
                                bgcolor=ft.colors.GREEN_400,
                                color="black",
                                width=270,
                                height=40,
                                on_click=create_account
                            ),
                            ft.ElevatedButton(
                                "login",
                                bgcolor=ft.colors.GREY_400,
                                color="black",
                                width=270,
                                height=40,
                                on_click=show_login
                            )
                        ],
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                        spacing=20,
                        alignment=ft.MainAxisAlignment.CENTER
                    ),
                    expand=True,
                    margin=ft.margin.only(top=100)
                )
            ])
        )

    def create_account(e):
        page.overlay.clear()
        page.clean()
        page.add(
            ft.Stack([
                background,
                ft.Container(
                    content=ft.Column(
                        [
                            ft.Divider(height=50, color="transparent", thickness=1),
                            ft.Text("Create", color="black", size=40, weight="bold"),
                            ft.Text("account", color="green", size=35, weight="bold"),
                            ft.Divider(height=80, color="transparent", thickness=1),
                        ],
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                        spacing=1
                    )
                ),
                ft.Container(
                    content=ft.Column(
                        [
                            ft.Column(
                                [
                                    ft.Divider(height=15, color="grey", thickness=1),
                                    fname,
                                    middlename,
                                    lname,
                                    sex,
                                    ft.Divider(height=15, color="grey", thickness=1),
                                ],
                                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                                spacing=18
                            ),
                            ft.Column(
                                [
                                    ft.Divider(height=30, color="transparent", thickness=1),
                                    ft.ElevatedButton("Continue",bgcolor=ft.colors.GREEN_400,width=280,height=40,color="black",on_click=validate
                                    ),
                                ],
                                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                            )
                        ],
                        spacing=10
                    ),
                    expand=True,
                    margin=ft.margin.only(top=200)
                ),
                ft.Container(
                    content=ft.IconButton(
                        icon=ft.icons.ARROW_BACK,
                        icon_size=30,
                        tooltip="Go back",
                        on_click=back_to_landing
                    ),
                    margin=ft.margin.only(left=10, top=10),
                    alignment=ft.alignment.top_left,
                )
            ])
        )

    def show_login(e):
        page.overlay.clear()
        page.clean()
        page.add(
            ft.Stack([
                background,
                ft.Container(
                    content=ft.Column(
                        [
                            ft.Divider(height=10, color="transparent", thickness=1),
                            ft.Text("Login", color="black", size=40, weight="bold"),
                            ft.Text("to your account", color="green", size=35, weight="bold"),
                            image2,
                            login_password,
                            ft.TextButton(
                                "Don't Have Account?",
                                on_click=create_account,
                                style=ft.ButtonStyle(
                                    color=ft.colors.BLACK,
                                    padding=0,
                                )
                            ),
                            ft.Divider(height=20, color="transparent", thickness=1),
                            ft.ElevatedButton("login",bgcolor=ft.colors.GREEN_400,color="black",width=270,height=40,on_click=validate_login
                            )
                        ],
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                        spacing=18,
                        alignment=ft.MainAxisAlignment.CENTER
                    ),
                    expand=True,
                    margin=ft.margin.only(top=10)
                ),
                ft.Container(
                    content=ft.IconButton(
                        icon=ft.icons.ARROW_BACK,
                        icon_size=30,
                        tooltip="Go back",
                        on_click=back_to_landing
                    ),
                    margin=ft.margin.only(left=10, top=10),
                    alignment=ft.alignment.top_left,
                )
            ])
        )

    def validate(e):
        error = False
        if not fname.value:
            fname.error_text = "First name is required!"
            error = True
        if not lname.value:
            lname.error_text = "Last name is required!"
            error = True
        if not sex.value:
            sex.error_text = "Sex is required!"
            error = True

        if error:
            page.update()
            return

        page.session_data = {
            'first_name': fname.value,
            'middle_name': middlename.value,
            'last_name': lname.value,
            'sex': sex.value
        }

        show_login_details()
        page.update()

    def validate_details(e):
        if not phone.value or len(phone.value) != 11:
            warning_error("Phone Number is required!")
            return

        if not register_password.value:
            warning_error("Password is required!")
            return

        loading = ft.Container(
            content=ft.Column([
                ft.ProgressRing(width=40, height=40, stroke_width=3, color=ft.colors.GREEN),
                ft.Text("Creating account...", size=12, color="black", weight="bold")
            ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=10),
            padding=20,
            width=230,
            margin=ft.margin.only(top=250, left=55, bottom=330),
            bgcolor=ft.colors.WHITE,
            border_radius=15,
            shadow=ft.BoxShadow(
                spread_radius=1,
                blur_radius=15,
                color=ft.colors.BLACK12,
            ),
            alignment=ft.alignment.center,
        )

        page.overlay.append(loading)
        page.update()

        user_data = {
            'phone': phone.value,
            'password': register_password.value,
            'first_name': page.session_data['first_name'],
            'middle_name': page.session_data['middle_name'],
            'last_name': page.session_data['last_name'],
            'sex': page.session_data['sex']
        }

        if save_to_database(user_data):
            import time
            time.sleep(1.5)
            page.overlay.clear()
            page.update()

            success_popup = ft.Container(
                content=ft.Row(
                    [
                        ft.Icon(ft.icons.CHECK_CIRCLE, color="white", size=20),
                        ft.Text("Account created successfully!", color="white", size=11, weight="bold")
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                    spacing=10
                ),
                bgcolor=ft.colors.GREEN_400,
                padding=15,
                width=250,
                border_radius=15,
                margin=ft.margin.only(top=15, left=55)
            )

            page.overlay.append(success_popup)
            page.update()

            time.sleep(1.5)
            page.overlay.clear()
            page.update()
            show_login(None)
        else:
            page.overlay.clear()
            page.update()
            warning_error("Failed to create account!")

    def show_login_details():
        page.overlay.clear()
        page.clean()
        page.add(
            ft.Stack([
                background,
                ft.Container(
                    content=ft.Column(
                        [
                            ft.Column(
                                [
                                    ft.Divider(height=30, color="transparent", thickness=1),
                                    ft.Text("Set your", color="black", size=40, weight="bold"),
                                    ft.Text("Login details", color="green", size=30, weight="bold"),
                                ],
                                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                                spacing=1
                            ),
                            ft.Column(
                                [
                                    image3,
                                    phone,
                                    register_password,
                                    ft.Divider(height=20, color="transparent", thickness=1),
                                    ft.ElevatedButton(
                                        "Submit",
                                        bgcolor=ft.colors.GREEN_400,
                                        color="black",
                                        width=270,
                                        height=40,
                                        on_click=validate_details
                                    )
                                ],
                                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                                spacing=8
                            )
                        ],
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                        spacing=10,
                        alignment=ft.MainAxisAlignment.CENTER
                    ),
                    expand=True,
                    margin=ft.margin.only(top=20)
                ),
                ft.Container(
                    content=ft.IconButton(
                        icon=ft.icons.ARROW_BACK,
                        icon_size=30,
                        tooltip="Go back",
                        on_click=create_account
                    ),
                    margin=ft.margin.only(left=10, top=10),
                    alignment=ft.alignment.top_left,
                )
            ])
        )

    def show_dashboard(user_data):
        page.overlay.clear()
        page.clean()
        header = ft.Container(
            content=ft.Column([
                ft.Row([
                    ft.Icon(ft.icons.ACCOUNT_CIRCLE, size=40, color="black"),
                    ft.Column([
                        ft.Text(f"Welcome, {user_data['first_name']}!",
                                size=24, weight="bold", color="black"),
                        ft.Text("Your Digital Wallet", size=16, color="black")
                    ])
                ], alignment=ft.MainAxisAlignment.CENTER),
                ft.Container(
                    content=ft.Column([
                        ft.Text("Available Balance", size=14, color="black"),
                        ft.Text(
                            f"₱ {user_data['balance']:,.2f}",
                            size=32,
                            weight="bold",
                            color="black"
                        )
                    ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                    bgcolor=ft.colors.GREEN_50,
                    padding=20,
                    border_radius=15,
                    width=320
                )
            ], spacing=20, horizontal_alignment=ft.CrossAxisAlignment.CENTER),
            padding=20
        )

        actions = ft.Container(
            content=ft.Row(
                scroll=ft.ScrollMode.AUTO,
                controls=[
                    ft.Container(
                        content=ft.Column([
                            ft.Icon(ft.icons.SEND_ROUNDED, size=30, color=ft.colors.BLACK),
                            ft.Text("Send Money", size=12, color="black")
                        ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                        padding=15,
                        border_radius=10,
                        bgcolor=ft.colors.WHITE,
                        border=ft.border.all(1, ft.colors.BLACK12),
                        on_click=lambda e: handle_send_money(e),
                        ink=True,
                    ),
                    ft.Container(
                        content=ft.Column([
                            ft.Icon(ft.icons.ADD_CARD, size=30, color=ft.colors.BLACK),
                            ft.Text("Add Money", size=12, color="black")
                        ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                        padding=15,
                        border_radius=10,
                        bgcolor=ft.colors.WHITE,
                        border=ft.border.all(1, ft.colors.BLACK12),
                        on_click=lambda e: handle_add_money(e),
                        ink=True,
                    ),
                    ft.Container(
                        content=ft.Column([
                            ft.Icon(ft.icons.SHOPPING_CART, size=30, color=ft.colors.BLACK),
                            ft.Text("Buy Load", size=12, color="black")
                        ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                        padding=15,
                        border_radius=10,
                        bgcolor=ft.colors.WHITE,
                        border=ft.border.all(1, ft.colors.BLACK12),
                        on_click=lambda e: handle_buy_load(e),
                        ink=True,
                    ),
                    ft.Container(
                        content=ft.Column([
                            ft.Icon(ft.icons.SUBSCRIPTIONS, size=30, color=ft.colors.BLACK),
                            ft.Text("Subscriptions", size=12, color="black")
                        ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                        padding=15,
                        border_radius=10,
                        bgcolor=ft.colors.WHITE,
                        border=ft.border.all(1, ft.colors.BLACK12),
                        on_click=lambda e: handle_subscriptions(e),
                        ink=True,
                    )
                ],
                spacing=15,
                alignment=ft.MainAxisAlignment.CENTER,
            ),
            padding=ft.padding.only(left=20, right=20, top=20, bottom=20),
            width=360
        )

        transactions_data = get_transactions(page.client_storage.get("user_phone"))[:4]
        transaction_tiles = []

        if not transactions_data:
            transactions_container = ft.Container(
                content=ft.Column([
                    ft.Row([
                        ft.Text("Recent Transactions", size=16, weight="bold", color="black"),
                    ], alignment=ft.MainAxisAlignment.CENTER),
                    ft.Container(
                        content=ft.Column([
                            ft.Image(
                                src="assets/no_trans.jpg",
                                width=90,
                                height=90,
                                fit=ft.ImageFit.CONTAIN,
                            ),
                            ft.Text(
                                "No transactions yet",
                                size=14,
                                color="black54",
                                text_align=ft.TextAlign.CENTER
                            ),
                            ft.Text(
                                "Your transactions will appear here",
                                size=12,
                                color="black38",
                                text_align=ft.TextAlign.CENTER
                            )
                        ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=10),
                        bgcolor=ft.colors.WHITE,
                        border_radius=10,
                        border=ft.border.all(1, ft.colors.BLACK12),
                        padding=20,
                        width=320,
                        alignment=ft.alignment.center
                    )
                ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=10),
                padding=20,
                alignment=ft.alignment.center,
            )
        else:
            for tx in transactions_data:
                icon = ft.icons.SHOPPING_BAG if tx['transaction_type'] == 'Buy Load' else \
                    ft.icons.ATTACH_MONEY if 'Received' in tx['transaction_type'] else \
                        ft.icons.ACCOUNT_BALANCE_WALLET

                color = ft.colors.RED if tx['amount'] < 0 else ft.colors.GREEN

                transaction_tiles.append(
                    ft.ListTile(
                        leading=ft.Icon(icon, color=color),
                        title=ft.Text(tx['transaction_type'], color="black"),
                        subtitle=ft.Text(tx['date'].strftime("%Y-%m-%d %H:%M")),
                        trailing=ft.Text(f"₱ {abs(tx['amount']):,.2f}", color=color)
                    )
                )

            transactions_container = ft.Container(
                content=ft.Column([
                    ft.Row([
                        ft.Text("Recent Transactions", size=16, weight="bold", color="black"),
                    ], alignment=ft.MainAxisAlignment.CENTER),
                    ft.Container(
                        content=ft.Column([
                            ft.ListView(
                                controls=transaction_tiles,
                                spacing=10,
                                height=200,
                                padding=10
                            )
                        ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                        bgcolor=ft.colors.WHITE,
                        border_radius=10,
                        border=ft.border.all(1, ft.colors.BLACK12),
                        padding=10,
                        width=320,
                        alignment=ft.alignment.center
                    )
                ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=10),
                padding=20,
                alignment=ft.alignment.center,
            )

        bottom_nav = ft.Container(
            content=ft.Row(
                [
                    ft.IconButton(
                        ft.icons.HOME,
                        selected=True,
                        icon_color=ft.colors.GREEN,
                        tooltip="Home",
                        on_click=lambda e: show_dashboard(user_data)
                    ),
                    ft.IconButton(
                        ft.icons.HISTORY,
                        tooltip="Transaction History",
                        on_click=lambda e: all_transactions(e)
                    ),
                    ft.IconButton(
                        ft.icons.ACCOUNT_CIRCLE,
                        tooltip="Profile",
                        on_click=lambda e: show_profile(e)
                    ),
                    ft.IconButton(
                        ft.icons.LOGOUT,
                        tooltip="Log-out",
                        on_click=lambda e: show_logout_confirmation(e)
                    ),
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                spacing=40
            ),
            padding=10,
            bgcolor=ft.colors.WHITE,
            border=ft.border.only(top=ft.BorderSide(1, ft.colors.BLACK12))
        )

        page.add(
            ft.Column([
                ft.Stack([
                    ft.Container(
                        content=ft.Image(
                            src="assets/hand-drawn-bussines-pattern-doodle-business-seamless-pattern-doodle-business-background_698782-3476.jpg",
                            fit=ft.ImageFit.COVER,
                            width=360,
                            height=740,
                            opacity=0.2,
                        ),
                        alignment=ft.alignment.center,
                        expand=True
                    ),
                    ft.Container(
                        content=ft.Column([
                            header,
                            actions,
                            transactions_container
                        ], scroll=ft.ScrollMode.AUTO),
                        expand=True,
                        alignment=ft.alignment.center,
                    ),
                ], expand=True),
                bottom_nav
            ], spacing=0, expand=True, alignment=ft.MainAxisAlignment.CENTER)
        )
        page.update()

    def handle_subscriptions(e):
        page.clean()
        page.overlay.clear()

        user_data = page.client_storage.get("user_data")
        if not user_data:
            user_data = {'first_name': '', 'balance': 0.00}

        subscriptions = {
            "Streaming": [
                {"name": "Netflix", "plans": ["Basic", "Standard", "Premium"], "prices": [199, 399, 549]},
                {"name": "Disney+", "plans": ["Mobile", "Premium"], "prices": [159, 369]},
                {"name": "Spotify", "plans": ["Individual", "Duo", "Family"], "prices": [149, 199, 239]},
                {"name": "YouTube Premium", "plans": ["Individual", "Family"], "prices": [159, 239]}
            ],
            "Gaming": [
                {"name": "Mobile Legends", "plans": ["Weekly Diamond", "Monthly Diamond"], "prices": [99, 299]},
                {"name": "PUBG Mobile", "plans": ["Weekly UC", "Monthly UC"], "prices": [99, 299]},
                {"name": "Valorant", "plans": ["Basic Points", "Premium Points"], "prices": [149, 499]}
            ]
        }

        selected_category = ft.Tabs(
            selected_index=0,
            on_change=lambda e: update_subscriptions(e.control.selected_index),
            tabs=[
                ft.Tab(text="STREAMING", icon=ft.icons.STREAM),
                ft.Tab(text="GAMING", icon=ft.icons.GAMES)
            ],
            tab_alignment= ft.TabAlignment.CENTER,
        )

        subscription_list = ft.ListView(
            expand=True,
            spacing=10,
            padding=10,
            height=500
        )

        def handle_subscription_payment(service, plan, price):
            page.clean()
            page.overlay.clear()

            # Check if it's a gaming service
            is_gaming = service in ["Mobile Legends", "PUBG Mobile", "Valorant"]

            # Create fields based on subscription type
            primary_field = ft.TextField(
                label="In-Game Name (IGN)" if is_gaming else "Gmail Account",
                color="black",
                width=280,
                label_style=ft.TextStyle(size=12, color="black"),
                border_color="black",
                border_radius=15,
                hint_text="Enter your IGN" if is_gaming else "example@gmail.com"
            )

            secondary_field = ft.TextField(
                label="Game ID" if is_gaming else "Password",
                password=not is_gaming,  # Only make it password field for non-gaming
                can_reveal_password=not is_gaming,
                color="black",
                width=280,
                label_style=ft.TextStyle(size=12, color="black"),
                border_color="black",
                border_radius=15,
                hint_text="Enter your Game ID" if is_gaming else None
            )

            def validate_subscription():
                if not primary_field.value:
                    warning_error(f"Please enter {'IGN' if is_gaming else 'Gmail account'}!")
                    return False
                if not secondary_field.value:
                    warning_error(f"Please enter {'Game ID' if is_gaming else 'password'}!")
                    return False
                if price > user_data['balance']:
                    warning_error("Insufficient balance!")
                    return False
                return True

            def process_subscription(e):
                if not validate_subscription():
                    return

                try:
                    conn = pymysql.connect(**db_config)
                    cursor = conn.cursor()

                    cursor.execute("""
                        UPDATE users
                        SET balance = balance - %s
                        WHERE phone = %s
                    """, (price, page.client_storage.get("user_phone")))

                    # Format details based on subscription type
                    details = (
                        f"{service} {plan} Plan - {primary_field.value} ({secondary_field.value})"
                        if is_gaming else
                        f"{service} {plan} Plan - {primary_field.value}"
                    )

                    save_transaction(
                        transaction_type=f"{service} Subscription",
                        amount=-price,
                        sender_phone=page.client_storage.get("user_phone"),
                        details=details
                    )

                    conn.commit()
                    user_data['balance'] -= price
                    page.client_storage.set("user_data", user_data)

                    show_success_message()

                except Error as e:
                    print(f"Database error: {e}")
                    warning_error("Subscription failed!")
                finally:
                    if cursor:
                        cursor.close()
                    if conn:
                        conn.close()

            def show_success_message():
                loading = ft.Container(
                    content=ft.Column([
                        ft.ProgressRing(width=40, height=40, stroke_width=3, color=ft.colors.GREEN),
                        ft.Text("Processing subscription...", size=12, color="black", weight="bold")
                    ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=10),
                    padding=20,
                    width=230,
                    margin=ft.margin.only(top=250, left=55, bottom=330),
                    bgcolor=ft.colors.WHITE,
                    border_radius=15,
                    shadow=ft.BoxShadow(
                        spread_radius=1,
                        blur_radius=15,
                        color=ft.colors.BLACK12,
                    ),
                    alignment=ft.alignment.center,
                )

                page.overlay.append(loading)
                page.update()
                time.sleep(1.5)
                page.overlay.clear()

                success_popup = ft.Container(
                    content=ft.Row([
                        ft.Icon(ft.icons.CHECK_CIRCLE, color="white", size=20),
                        ft.Text("Successfully subscribed!", color="white", size=11, weight="bold")
                    ], alignment=ft.MainAxisAlignment.CENTER, spacing=10),
                    bgcolor=ft.colors.GREEN_400,
                    padding=15,
                    width=250,
                    border_radius=15,
                    margin=ft.margin.only(top=15, left=55)
                )

                page.overlay.append(success_popup)
                page.update()
                time.sleep(1.5)
                show_dashboard(user_data)

            page.add(
                ft.Stack([
                    background,
                    ft.Container(
                        content=ft.Column([
                            ft.Row([
                                ft.IconButton(
                                    icon=ft.icons.ARROW_BACK,
                                    icon_size=30,
                                    tooltip="Go back",
                                    on_click=lambda e: handle_subscriptions(e)
                                ),
                                ft.Text("Enter Account Details",
                                        size=24,
                                        weight="bold",
                                        color="black",
                                        text_align=ft.TextAlign.CENTER,
                                        expand=True)
                            ]),
                            ft.Divider(height=20, color="transparent"),
                            ft.Text(
                                f"{service} - {plan} Plan",
                                size=16,
                                color="black",
                                text_align=ft.TextAlign.CENTER
                            ),
                            ft.Text(
                                f"Price: ₱{price}",
                                size=16,
                                color="black",
                                text_align=ft.TextAlign.CENTER
                            ),
                            ft.Divider(height=20, color="transparent"),
                            primary_field,
                            ft.Divider(height=10, color="transparent"),
                            secondary_field,
                            ft.Divider(height=20, color="transparent"),
                            ft.ElevatedButton(
                                "Subscribe",
                                bgcolor=ft.colors.GREEN_400,
                                color="black",
                                width=280,
                                height=40,
                                on_click=process_subscription
                            )
                        ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                        padding=20,
                        alignment=ft.alignment.center,
                        expand=True
                    )
                ])
            )
            page.update()

        def update_subscriptions(index):
            subscription_list.controls.clear()
            category = "Streaming" if index == 0 else "Gaming"

            for sub in subscriptions[category]:
                for plan, price in zip(sub['plans'], sub['prices']):
                    def create_handler(service=sub['name'], plan=plan, price=price):
                        return lambda e: handle_subscription_payment(service, plan, price)

                    subscription_list.controls.append(
                        ft.Container(
                            content=ft.Column([
                                ft.Text(sub['name'], size=16, weight="bold", color="black"),
                                ft.Divider(height=10, color="transparent"),
                                ft.Container(
                                    content=ft.Column([
                                        ft.Text(f"{plan} Plan",
                                                size=14,
                                                color="black",
                                                text_align=ft.TextAlign.CENTER),
                                        ft.Text(f"₱{price}",
                                                size=16,
                                                weight="bold",
                                                color="black",
                                                text_align=ft.TextAlign.CENTER),
                                        ft.ElevatedButton(
                                            "Subscribe",
                                            bgcolor=ft.colors.GREEN_400,
                                            color="black",
                                            width=140,
                                            height=40,
                                            on_click=create_handler()
                                        )
                                    ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                                    padding=10,
                                    border=ft.border.all(1, ft.colors.BLACK12),
                                    border_radius=10,
                                    margin=10
                                )
                            ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                            bgcolor=ft.colors.WHITE,
                            border_radius=10,
                            padding=15,
                            border=ft.border.all(1, ft.colors.BLACK12),
                            width=320
                        )
                    )
            page.update()

        update_subscriptions(0)

        page.add(
            ft.Stack([
                background,
                ft.Container(
                    content=ft.Column([
                        ft.Row([
                            ft.IconButton(
                                icon=ft.icons.ARROW_BACK,
                                icon_size=30,
                                tooltip="Go back",
                                on_click=lambda e: show_dashboard(user_data)
                            ),
                            ft.Text("Subscriptions", size=24, weight="bold", color="black"),
                        ], alignment=ft.MainAxisAlignment.CENTER),
                        selected_category,
                        subscription_list,
                    ], spacing=20),
                    padding=20,
                    expand=True
                )
            ])
        )
        page.update()

    def handle_send_money(e):
        global recipient, amount
        page.overlay.clear()
        page.clean()

        user_data = page.client_storage.get("user_data")
        if not user_data:
            user_data = {'first_name': '', 'balance': 0.00}

        def validate_send_money(e):
            if not recipient.value:
                warning_error("Please select a recipient!")
                return
            if not amount.value:
                warning_error("Please enter an amount!")
                return
            try:
                amount_value = float(amount.value)
                if amount_value <= 0:
                    warning_error("Amount must be greater than 0!")
                    return
                if amount_value > user_data['balance']:
                    warning_error("Insufficient balance!")
                    return

                recipient_phone = recipient.value.split('(')[-1].strip(')')
                recipient_name = recipient.value.split('(')[0].strip()

                show_transfer_summary(amount_value, recipient_name, recipient_phone)

            except ValueError:
                warning_error("Please enter a valid amount!")

        def show_transfer_summary(amount_value, recipient_name, recipient_phone):
            page.clean()
            page.add(
                ft.Stack([
                    background,
                    ft.Container(
                        content=ft.Column([
                            ft.Row([
                                ft.IconButton(
                                    icon=ft.icons.ARROW_BACK,
                                    icon_size=30,
                                    tooltip="Go back",
                                    on_click=lambda e: handle_send_money(e)
                                ),
                                ft.Text("Transfer Summary", size=24, weight="bold", color="black"),
                            ], alignment=ft.MainAxisAlignment.START),
                            ft.Divider(height=30, color="transparent"),
                            ft.Container(
                                content=ft.Column([
                                    ft.Text("Transfer Details", size=20, weight="bold", color="black",
                                            text_align=ft.TextAlign.CENTER),
                                    ft.Divider(height=20, color="transparent"),
                                    ft.Container(
                                        content=ft.Column([
                                            ft.Row([
                                                ft.Text("Recipient Name:", size=14, color="black"),
                                                ft.Text(recipient_name, size=14, weight="bold", color="black")
                                            ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                                            ft.Divider(height=10, color="transparent"),
                                            ft.Row([
                                                ft.Text("Phone Number:", size=14, color="black"),
                                                ft.Text(recipient_phone, size=14, weight="bold", color="black")
                                            ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                                            ft.Divider(height=10, color="transparent"),
                                            ft.Row([
                                                ft.Text("Amount:", size=14, color="black"),
                                                ft.Text(f"₱{amount_value:,.2f}", size=14, weight="bold", color="black")
                                            ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                                            ft.Divider(height=10, color="transparent"),
                                        ]),
                                        bgcolor=ft.colors.WHITE,
                                        padding=20,
                                        border_radius=15,
                                        border=ft.border.all(1, ft.colors.BLACK12),
                                    ),
                                    ft.Divider(height=30, color="transparent"),
                                    ft.Row([
                                        ft.ElevatedButton(
                                            "Cancel",
                                            bgcolor=ft.colors.RED_400,
                                            color="white",
                                            width=120,
                                            height=50,
                                            on_click=lambda e: handle_send_money(e)
                                        ),
                                        ft.ElevatedButton(
                                            "Confirm",
                                            bgcolor=ft.colors.GREEN,
                                            color="white",
                                            width=120,
                                            height=50,
                                            on_click=lambda e: process_transfer(amount_value, recipient_phone,
                                                                                recipient_name)
                                        ),
                                    ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                                ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                                padding=20,
                                bgcolor=ft.colors.WHITE,
                                border_radius=15,
                                width=320,
                            ),
                        ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                        padding=20,
                        expand=True,
                        alignment=ft.alignment.center
                    )
                ])
            )
            page.update()

        def get_registered_users():
            try:
                conn = pymysql.connect(**db_config)
                cursor = conn.cursor(pymysql.cursors.DictCursor)
                cursor.execute("SELECT first_name, last_name, phone FROM users WHERE phone != %s",
                               (page.client_storage.get("user_phone"),))
                users = cursor.fetchall()
                return [f"{user['first_name']} {user['last_name']} ({user['phone']})" for user in users]
            except Error as e:
                print(f"Database error: {e}")
                return []
            finally:
                if cursor:
                    cursor.close()
                if conn:
                    conn.close()

        recipient = ft.Dropdown(
            label="Select Recipient",
            width=280,
            color="black",
            label_style=ft.TextStyle(size=12, color="black"),
            border_color="black",
            border_radius=15,
            options=[ft.dropdown.Option(user) for user in get_registered_users()]
        )

        amount = ft.TextField(
            label="Amount",
            width=280,
            color="black",
            label_style=ft.TextStyle(size=12, color="black"),
            border_color="black",
            border_radius=15,
            prefix_text="₱",
            prefix_style=ft.TextStyle(size=12, color="black"),
            keyboard_type=ft.KeyboardType.NUMBER
        )

        def process_transfer(amount_value, recipient_phone, recipient_name):
            loading = ft.Container(
                content=ft.Column([
                    ft.ProgressRing(width=40, height=40, stroke_width=3, color=ft.colors.GREEN),
                    ft.Text("Processing transfer...", size=12, color="black", weight="bold")
                ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=10),
                padding=20,
                width=230,
                margin=ft.margin.only(top=250, left=55, bottom=330),
                bgcolor=ft.colors.WHITE,
                border_radius=15,
                shadow=ft.BoxShadow(
                    spread_radius=1,
                    blur_radius=15,
                    color=ft.colors.BLACK12,
                ),
                alignment=ft.alignment.center,
            )

            page.overlay.append(loading)
            page.update()

            try:
                conn = pymysql.connect(**db_config)
                cursor = conn.cursor()

                # Update sender's balance
                cursor.execute("""
                    UPDATE users
                    SET balance = balance - %s
                    WHERE phone = %s
                """, (amount_value, page.client_storage.get("user_phone")))

                # Update recipient's balance
                cursor.execute("""
                    UPDATE users
                    SET balance = balance + %s
                    WHERE phone = %s
                """, (amount_value, recipient_phone))

                # Get sender's name
                cursor.execute("""
                    SELECT first_name, last_name
                    FROM users
                    WHERE phone = %s
                """, (page.client_storage.get("user_phone"),))
                sender = cursor.fetchone()
                sender_name = f"{sender[0]} {sender[1]}"

                # Save single transaction record with correct type for each user
                if page.client_storage.get("user_phone") == recipient_phone:
                    # For recipient
                    save_transaction(
                        transaction_type="Receive Money",
                        amount=amount_value,
                        sender_phone=recipient_phone,
                        recipient=f"{sender_name} ({page.client_storage.get('user_phone')})",
                        details=f"Transfer from {sender_name}"
                    )
                else:
                    # For sender
                    save_transaction(
                        transaction_type="Send Money",
                        amount=-amount_value,
                        sender_phone=page.client_storage.get("user_phone"),
                        recipient=f"{recipient_name} ({recipient_phone})",
                        details=f"Transfer to {recipient_name}"
                    )

                conn.commit()
                user_data['balance'] -= amount_value
                page.client_storage.set("user_data", user_data)

                time.sleep(1.5)
                page.overlay.clear()
                page.update()

                success_popup = ft.Container(
                    content=ft.Row([
                        ft.Icon(ft.icons.CHECK_CIRCLE, color="white", size=20),
                        ft.Text("Transfer successful!", color="white", size=11, weight="bold")
                    ], alignment=ft.MainAxisAlignment.CENTER, spacing=10),
                    bgcolor=ft.colors.GREEN_400,
                    padding=15,
                    width=250,
                    border_radius=15,
                    margin=ft.margin.only(top=15, left=55)
                )

                page.overlay.append(success_popup)
                page.update()

                time.sleep(1.5)
                page.overlay.clear()
                page.update()
                show_dashboard(user_data)

            except Error as e:
                print(f"Database error: {e}")
                page.overlay.clear()
                page.update()
                warning_error("Transfer failed!")
            finally:
                if cursor:
                    cursor.close()
                if conn:
                    conn.close()

        page.add(
            ft.Stack([
                background,
                ft.Container(
                    content=ft.Column([
                        ft.Row([
                            ft.IconButton(
                                icon=ft.icons.ARROW_BACK,
                                icon_size=30,
                                tooltip="Go back",
                                on_click=lambda e: show_dashboard(user_data)
                            ),
                            ft.Text("Send Money", size=24, weight="bold", color="black"),
                        ], alignment=ft.MainAxisAlignment.START),
                        ft.Divider(height=20, color="transparent"),
                        ft.Container(
                            content=ft.Column([
                                ft.Text("Available Balance", size=14, color="black"),
                                ft.Text(
                                    f"₱ {user_data['balance']:,.2f}",
                                    size=32,
                                    weight="bold",
                                    color="black"
                                )
                            ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                            bgcolor=ft.colors.GREEN_50,
                            padding=20,
                            border_radius=15,
                            width=320
                        ),
                        ft.Divider(height=20, color="transparent"),
                        recipient,
                        ft.Divider(height=10, color="transparent"),
                        amount,
                        ft.Divider(height=20, color="transparent"),
                        ft.ElevatedButton(
                            "Send Money",
                            width=280,
                            height=40,
                            bgcolor=ft.colors.GREEN,
                            color="white",
                            on_click=validate_send_money
                        )
                    ], scroll=ft.ScrollMode.AUTO,
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                    padding=20,
                    expand=True
                )
            ])
        )
        page.update()

    def handle_add_money(e):
        page.clean()
        page.overlay.clear()

        user_data = page.client_storage.get("user_data")
        if not user_data:
            user_data = {'first_name': '', 'balance': 0.00}

        amount = ft.TextField(
            label="Enter Amount",
            width=280,
            color="black",
            label_style=ft.TextStyle(size=12, color="black"),
            border_color="black",
            border_radius=15,
            prefix_text="₱",
            prefix_style=ft.TextStyle(color="black", size=12),
            keyboard_type=ft.KeyboardType.NUMBER
        )

        def validate_add_money(e):
            if not amount.value:
                warning_error("Please enter an amount!")
                return
            try:
                amount_value = float(amount.value)
                if amount_value <= 0:
                    warning_error("Amount must be greater than 0!")
                    return

                loading = ft.Container(
                    content=ft.Column([
                        ft.ProgressRing(width=40, height=40, stroke_width=3, color=ft.colors.GREEN),
                        ft.Text("Processing transaction...", size=12, color="black", weight="bold")
                    ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=10),
                    padding=20,
                    width=230,
                    margin=ft.margin.only(top=250, left=55, bottom=330),
                    bgcolor=ft.colors.WHITE,
                    border_radius=15,
                    shadow=ft.BoxShadow(
                        spread_radius=1,
                        blur_radius=15,
                        color=ft.colors.BLACK12,
                    ),
                    alignment=ft.alignment.center,
                )

                page.overlay.append(loading)
                page.update()

                try:
                    conn = pymysql.connect(**db_config)
                    cursor = conn.cursor()

                    cursor.execute("""
                        UPDATE users
                        SET balance = balance + %s
                        WHERE phone = %s
                    """, (amount_value, page.client_storage.get("user_phone")))

                    save_transaction(
                        transaction_type="Add Money",
                        amount=amount_value,
                        sender_phone=page.client_storage.get("user_phone"),
                        details="Cash In"
                    )

                    conn.commit()
                    user_data['balance'] += amount_value
                    page.client_storage.set("user_data", user_data)

                    time.sleep(1.5)
                    page.overlay.clear()
                    page.update()

                    success_popup = ft.Container(
                        content=ft.Row(
                            [
                                ft.Icon(ft.icons.CHECK_CIRCLE, color="white", size=20),
                                ft.Text("Money added successfully!", color="white", size=11, weight="bold")
                            ],
                            alignment=ft.MainAxisAlignment.CENTER,
                            spacing=10
                        ),
                        bgcolor=ft.colors.GREEN_400,
                        padding=15,
                        width=250,
                        border_radius=15,
                        margin=ft.margin.only(top=15, left=55)
                    )

                    page.overlay.append(success_popup)
                    page.update()

                    time.sleep(1.5)
                    page.overlay.clear()
                    page.update()
                    show_dashboard(user_data)

                except Error as e:
                    print(f"Database error: {e}")
                    warning_error("Transaction failed!")
                finally:
                    if cursor:
                        cursor.close()
                    if conn:
                        conn.close()

            except ValueError:
                warning_error("Please enter a valid amount!")

        page.add(
            ft.Stack([
                ft.Container(
                    content=ft.Image(
                        src="assets/hand-drawn-bussines-pattern-doodle-business-seamless-pattern-doodle-business-background_698782-3476.jpg",
                        fit=ft.ImageFit.COVER,
                        width=360,
                        height=740,
                        opacity=0.2,
                    ),
                    alignment=ft.alignment.center,
                    expand=True
                ),
                ft.Column([
                    ft.Container(
                        content=ft.IconButton(
                            icon=ft.icons.ARROW_BACK,
                            icon_size=30,
                            tooltip="Go back",
                            on_click=lambda e: show_dashboard(user_data)
                        ),
                        margin=ft.margin.only(left=10, top=10),
                        alignment=ft.alignment.top_left,
                    ),
                    ft.Container(
                        content=ft.Column([
                            ft.Text("Add Money",
                                    size=24,
                                    weight="bold",
                                    color="black",
                                    text_align=ft.TextAlign.CENTER),
                            ft.Divider(height=20, color="transparent"),
                            ft.Container(
                                content=ft.Column([
                                    ft.Text("Current Balance", size=14, color="black"),
                                    ft.Text(
                                        f"₱ {user_data['balance']:,.2f}",
                                        size=32,
                                        weight="bold",
                                        color="black"
                                    )
                                ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                                bgcolor=ft.colors.GREEN_50,
                                padding=20,
                                border_radius=15,
                                width=320
                            ),
                            ft.Divider(height=30, color="transparent"),
                            amount,
                            ft.Divider(height=20, color="transparent"),
                            ft.ElevatedButton(
                                "Add Money",
                                bgcolor=ft.colors.GREEN_400,
                                color="black",
                                width=280,
                                height=40,
                                on_click=validate_add_money
                            )
                        ],
                            horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                        padding=20,
                        expand=True
                    )
                ])
            ])
        )
        page.update()

    def handle_buy_load(e):
        page.clean()
        page.overlay.clear()

        user_data = page.client_storage.get("user_data")
        if not user_data:
            user_data = {'first_name': '', 'balance': 0.00}

        def select_provider(provider):
            page.client_storage.set("selected_provider", provider)
            show_load_promos(provider)

        page.add(
            ft.Stack([
                background,
                ft.Container(
                    content=ft.Column([
                        ft.Row([
                            ft.IconButton(
                                icon=ft.icons.ARROW_BACK,
                                icon_size=30,
                                tooltip="Go back",
                                on_click=lambda e: show_dashboard(user_data)
                            ),
                            ft.Text("     Buy Load", size=24, weight="bold", color="black"),
                        ], alignment=ft.MainAxisAlignment.START, spacing=10),

                        ft.Divider(height=20, color="transparent"),
                        ft.Container(
                            content=ft.Column([
                                ft.Text("Balance", size=14, color="black"),
                                ft.Text(
                                    f"₱ {user_data['balance']:,.2f}",
                                    size=32,
                                    weight="bold",
                                    color="black"
                                )
                            ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                            bgcolor=ft.colors.GREEN_50,
                            padding=20,
                            border_radius=15,
                            width=320
                        ),
                        ft.Divider(height=30, color="transparent"),
                        ft.Text("Select Network Provider", size=16, weight="bold", color="black"),
                        ft.Container(
                            content=ft.Column([
                                ft.Container(
                                    content=ft.Column([
                                        ft.Image(
                                            src="assets/globe.png",
                                            width=80,
                                            height=80,
                                            fit=ft.ImageFit.CONTAIN
                                        ),
                                    ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                                    on_click=lambda e: select_provider("Globe"),
                                    bgcolor=ft.colors.TRANSPARENT,
                                    padding=15,
                                    border_radius=10,
                                    ink=True,
                                    width=280,
                                    # border=ft.border.all(1, ft.colors.BLACK12)
                                ),
                                ft.Container(
                                    content=ft.Column([
                                        ft.Image(
                                            src="assets/smart.png",
                                            width=80,
                                            height=80,
                                            fit=ft.ImageFit.CONTAIN
                                        ),
                                    ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                                    on_click=lambda e: select_provider("Smart"),
                                    bgcolor=ft.colors.TRANSPARENT,
                                    padding=15,
                                    border_radius=10,
                                    ink=True,
                                    width=280,
                                    # border=ft.border.all(1, ft.colors.BLACK12)
                                ),
                                ft.Container(
                                    content=ft.Column([
                                        ft.Image(
                                            src="assets/tnt.jpg",
                                            width=50,
                                            height=50,
                                            fit=ft.ImageFit.CONTAIN
                                        ),
                                    ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                                    on_click=lambda e: select_provider("tnt"),
                                    bgcolor=ft.colors.TRANSPARENT,
                                    padding=15,
                                    border_radius=10,
                                    ink=True,
                                    width=280,
                                    # border=ft.border.all(1, ft.colors.BLACK12)
                                ),
                                ft.Container(
                                    content=ft.Column([
                                        ft.Image(
                                            src="assets/dito.jpg",
                                            width=80,
                                            height=80,
                                            fit=ft.ImageFit.CONTAIN
                                        ),
                                    ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                                    on_click=lambda e: select_provider("DITO"),
                                    bgcolor=ft.colors.TRANSPARENT,
                                    padding=15,
                                    border_radius=10,
                                    ink=True,
                                    width=280,
                                    # border=ft.border.all(1, ft.colors.BLACK12)
                                ),
                                ft.Container(
                                    content=ft.Column([
                                        ft.Image(
                                            src="assets/gomo.png",
                                            width=50,
                                            height=50,
                                            fit=ft.ImageFit.CONTAIN
                                        ),
                                    ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                                    on_click=lambda e: select_provider("GOMO"),
                                    bgcolor=ft.colors.TRANSPARENT,
                                    padding=15,
                                    border_radius=10,
                                    ink=True,
                                    width=280,
                                    border=ft.border.all(1, ft.colors.TRANSPARENT)

                                )
                            ], scroll=ft.ScrollMode.AUTO, spacing=10,
                                horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                            padding=20,
                            height=400
                        )
                    ], spacing=5, horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                    padding=20,
                    expand=True
                )
            ])
        )
        page.update()

    def show_load_promos(provider):
        page.clean()
        page.overlay.clear()

        user_data = page.client_storage.get("user_data")
        if not user_data:
            user_data = {'first_name': '', 'balance': 0.00}

        phone_number = ft.TextField(
            label="Enter Phone Number",
            color="black",
            width=280,
            label_style=ft.TextStyle(size=12, color="black"),
            border_color="black",
            border_radius=15,
            hint_text="Enter 11 digits",
            keyboard_type=ft.KeyboardType.NUMBER,
            prefix_text="+63 ",
            prefix_style=ft.TextStyle(color="black", size=12),
            on_change=validate_phone
        )

        promos = {
            "Globe": [
                {"name": "GOSURF50", "desc": "5GB Data + Unli All-Net Texts, 3 Days", "price": 50},
                {"name": "GO50", "desc": "Unli All-Net Texts + 300 Minutes Calls, 3 Days", "price": 50},
                {"name": "GO100", "desc": "8GB Data + Unli All-Net Texts, 7 Days", "price": 100},
                {"name": "GO150", "desc": "15GB Data + Unli All-Net Texts, 10 Days", "price": 150},
                {"name": "GO200", "desc": "20GB Data + Unli All-Net Texts, 15 Days", "price": 200}
            ],
            "Smart": [
                {"name": "GIGA50", "desc": "5GB Data + Unli TikTok, 3 Days", "price": 50},
                {"name": "GIGA99", "desc": "8GB Data + Unli Social Media, 7 Days", "price": 99},
                {"name": "GIGA149", "desc": "12GB Data + Unli Social Media, 7 Days", "price": 149},
                {"name": "GIGA199", "desc": "15GB Data + Unli Social Media, 15 Days", "price": 199},
                {"name": "GIGA299", "desc": "24GB Data + Unli Social Media, 30 Days", "price": 299}
            ],
            "tnt": [
                {"name": "MAGIC DATA50", "desc": "3GB Data + Unli Facebook, 3 Days", "price": 50},
                {"name": "UNLI90", "desc": "5GB Data + Unli Social Media, 7 Days", "price": 90},
                {"name": "SURF SAYA140", "desc": "8GB Data + Unli Social Media, 7 Days", "price": 140},
                {"name": "GIGA199", "desc": "15GB Data + Unli Social Media, 15 Days", "price": 199},
                {"name": "GIGA299", "desc": "24GB Data + Unli Social Media, 30 Days", "price": 299}
            ],
            "DITO": [
                {"name": "DATA49", "desc": "5GB Data + Unli Calls & Texts, 3 Days", "price": 49},
                {"name": "DATA99", "desc": "10GB Data + Unli Calls & Texts, 7 Days", "price": 99},
                {"name": "DATA199", "desc": "25GB Data + Unli Calls & Texts, 15 Days", "price": 199},
                {"name": "DATA299", "desc": "35GB Data + Unli Calls & Texts, 30 Days", "price": 299},
                {"name": "DATA499", "desc": "50GB Data + Unli Calls & Texts, 30 Days", "price": 499}
            ],
            "GOMO": [
                {"name": "GO50", "desc": "8GB No Expiry Data", "price": 50},
                {"name": "GO100", "desc": "15GB No Expiry Data", "price": 100},
                {"name": "GO150", "desc": "25GB No Expiry Data", "price": 150},
                {"name": "GO299", "desc": "45GB No Expiry Data", "price": 299},
                {"name": "GO499", "desc": "75GB No Expiry Data", "price": 499}
            ]
        }

        selected_promo = ft.RadioGroup(
            content=ft.Column(
                [
                    ft.Radio(
                        value=str(i),
                        label_style=ft.TextStyle(size=12, color="black"),
                        label=f"{promo['name']} - ₱{promo['price']}\n{promo['desc']}",
                    ) for i, promo in enumerate(promos[provider])
                ],
                spacing=35,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                alignment=ft.MainAxisAlignment.CENTER,
            )
        )

        def handle_buy_promo(e):
            if not phone_number.value:
                warning_error("Please enter phone number!")
                return

            if len(phone_number.value) != 11:
                warning_error("Phone number must be 11 digits!")
                return

            if not selected_promo.value:
                warning_error("Please select a promo!")
                return

            selected_index = int(selected_promo.value)
            promo = promos[provider][selected_index]

            if promo['price'] > user_data['balance']:
                warning_error("Insufficient balance!")
                return

            loading = ft.Container(
                content=ft.Column([
                    ft.ProgressRing(width=40, height=40, stroke_width=3, color=ft.colors.GREEN),
                    ft.Text("Processing transaction...", size=12, color="black", weight="bold")
                ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=10),
                padding=20,
                width=230,
                margin=ft.margin.only(top=250, left=55, bottom=330),
                bgcolor=ft.colors.WHITE,
                border_radius=15,
                shadow=ft.BoxShadow(
                    spread_radius=1,
                    blur_radius=15,
                    color=ft.colors.BLACK12,
                ),
                alignment=ft.alignment.center,
            )

            page.overlay.append(loading)
            page.update()

            try:
                conn = pymysql.connect(**db_config)
                cursor = conn.cursor()

                cursor.execute("""
                    UPDATE users
                    SET balance = balance - %s
                    WHERE phone = %s
                """, (promo['price'], page.client_storage.get("user_phone")))

                save_transaction(
                    transaction_type="Buy Load",
                    amount=-promo['price'],
                    sender_phone=page.client_storage.get("user_phone"),
                    details=f"{provider} - {promo['name']}"
                )

                conn.commit()
                user_data['balance'] -= promo['price']
                page.client_storage.set("user_data", user_data)

                time.sleep(1.5)
                page.overlay.clear()
                page.update()

                receipt = ft.Container(
                    content=ft.Column([
                        ft.Icon(ft.icons.CHECK_CIRCLE, color=ft.colors.GREEN, size=50),
                        ft.Text("Purchase Successful!", size=20, weight="bold", color="black"),
                        ft.Divider(height=20),
                        ft.Text("RECEIPT", size=16, weight="bold", color="black"),
                        ft.Text(f"Provider: {provider}", size=14, color="black"),
                        ft.Text(f"Promo: {promo['name']}", size=14, color="black"),
                        ft.Text(f"Amount: ₱{promo['price']}", size=14, color="black"),
                        ft.Text(f"Description: {promo['desc']}", size=14, color="black"),
                        ft.Text(f"Date: {time.strftime('%Y-%m-%d %H:%M:%S')}", size=14, color="black"),
                        ft.Divider(height=20),
                        ft.ElevatedButton(
                            "Back to Dashboard",
                            on_click=lambda _: show_dashboard(user_data)
                        )
                    ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=10),
                    padding=20,
                    bgcolor=ft.colors.WHITE,
                    border_radius=15,
                    border=ft.border.all(1, ft.colors.BLACK12),
                    width=300
                )

                page.clean()
                page.add(
                    ft.Container(
                        content=receipt,
                        alignment=ft.alignment.center,
                        expand=True
                    )
                )
                page.update()

            except Error as e:
                print(f"Database error: {e}")
                warning_error("Transaction failed!")
            finally:
                if cursor:
                    cursor.close()
                if conn:
                    conn.close()

        page.add(
            ft.Stack([
                ft.Container(
                    content=ft.Image(
                        src="assets/hand-drawn-bussines-pattern-doodle-business-seamless-pattern-doodle-business-background_698782-3476.jpg",
                        fit=ft.ImageFit.COVER,
                        width=360,
                        height=740,
                        opacity=0.2,
                    ),
                    alignment=ft.alignment.center,
                    expand=True
                ),
            ft.Column([
                ft.Container(
                    content=ft.Column([
                        ft.Row([
                            ft.IconButton(
                                icon=ft.icons.ARROW_BACK,
                                icon_size=30,
                                tooltip="Go back",
                                on_click=handle_buy_load
                            ),
                            ft.Text(f"{provider} Load Promos", size=24, weight="bold", color="black"),
                        ], spacing=10
                        , alignment=ft.MainAxisAlignment.CENTER),

                        ft.Divider(height=20, color="transparent"),
                        phone_number,
                        ft.Divider(height=20, color="transparent"),
                        ft.Container(
                            content=selected_promo,
                            bgcolor=ft.colors.WHITE,
                            border_radius=15,
                            border=ft.border.all(1, ft.colors.BLACK12),
                            padding=20
                        ),
                        ft.Divider(height=20, color="transparent"),
                        ft.ElevatedButton(
                            "Buy Load",
                            bgcolor=ft.colors.GREEN_400,
                            color="black",
                            width=280,
                            height=40,
                            on_click=handle_buy_promo
                        )
                    ],
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    scroll=ft.ScrollMode.AUTO),
                    padding=20,
                    expand=True
                )
            ])
            ])
        )
        page.update()


    def get_transactions(user_phone=None):
        try:
            conn = pymysql.connect(**db_config)
            cursor = conn.cursor(pymysql.cursors.DictCursor)

            if user_phone:
                query = """
                SELECT * FROM transactions 
                WHERE sender_phone = %s OR recipient_phone = %s 
                ORDER BY date DESC
                """
                cursor.execute(query, (user_phone, user_phone))
            else:
                cursor.execute("SELECT * FROM transactions ORDER BY date DESC")

            return cursor.fetchall()
        except Error as e:
            print(f"Database error: {e}")
            return []
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

    def save_transaction(transaction_type, amount, sender_phone=None, recipient=None, details=None):
        try:
            conn = pymysql.connect(**db_config)
            cursor = conn.cursor()

            query = """
            INSERT INTO transactions (transaction_type, amount, sender_phone, recipient_phone, details, date)
            VALUES (%s, %s, %s, %s, %s, NOW())
            """
            recipient_phone = recipient.split('(')[-1].strip(')') if recipient else None
            cursor.execute(query, (transaction_type, amount, sender_phone, recipient_phone, details))
            conn.commit()

        except Error as e:
            print(f"Database error: {e}")
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

    def all_transactions(e):
        page.clean()
        page.overlay.clear()

        user_data = page.client_storage.get("user_data")
        if not user_data:
            user_data = {'first_name': '', 'balance': 0.00}

        transactions_data = get_transactions(page.client_storage.get("user_phone"))

        if not transactions_data:
            transactions_container = ft.Container(
                content=ft.Column([
                    ft.Text("Transaction History", size=24, weight="bold", color="black"),
                    ft.Divider(height=20, color="transparent"),
                    ft.Container(
                        content=ft.Column([
                            ft.Image(
                                src="assets/no_trans.jpg",
                                width=150,
                                height=150,
                                fit=ft.ImageFit.CONTAIN,
                            ),
                            ft.Text(
                                "No transaction history",
                                size=16,
                                color="black54",
                                weight="bold",
                                text_align=ft.TextAlign.CENTER
                            ),
                            ft.Text(
                                "Your transactions will appear here",
                                size=14,
                                color="black38",
                                text_align=ft.TextAlign.CENTER
                            )
                        ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=10),
                        bgcolor=ft.colors.WHITE,
                        border_radius=15,
                        border=ft.border.all(1, ft.colors.BLACK12),
                        padding=30,
                        width=320,
                        alignment=ft.alignment.center
                    )
                ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=10),
                padding=20,
                expand=True,
                alignment=ft.alignment.center,
            )
        else:
            transaction_tiles = []
            for tx in transactions_data:
                icon = ft.icons.SHOPPING_BAG if tx['transaction_type'] == 'Buy Load' else \
                    ft.icons.ATTACH_MONEY if 'Received' in tx['transaction_type'] else \
                        ft.icons.ACCOUNT_BALANCE_WALLET

                color = ft.colors.RED if tx['amount'] < 0 else ft.colors.GREEN

                transaction_tiles.append(
                    ft.ListTile(
                        leading=ft.Icon(icon, color=color),
                        title=ft.Text(tx['transaction_type'], color="black"),
                        subtitle=ft.Text(tx['date'].strftime("%Y-%m-%d %H:%M")),
                        trailing=ft.Text(f"₱ {abs(tx['amount']):,.2f}", color=color)
                    )
                )

            transactions_container = ft.Container(
                content=ft.Column([
                    ft.Text("Transaction History", size=24, weight="bold", color="black"),
                    ft.Divider(height=20, color="transparent"),
                    ft.Container(
                        content=ft.Column([
                            ft.ListView(
                                controls=transaction_tiles,
                                spacing=10,
                                padding=10,
                                expand=True
                            )
                        ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                        bgcolor=ft.colors.WHITE,
                        border_radius=15,
                        border=ft.border.all(1, ft.colors.BLACK12),
                        padding=10,
                        width=320,
                        expand=True
                    )
                ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, scroll=ft.ScrollMode.AUTO),
                padding=20,
                expand=True
            )

        bottom_nav = ft.Container(
            content=ft.Row(
                [
                    ft.IconButton(
                        ft.icons.HOME,
                        tooltip="Home",
                        on_click=lambda e: show_dashboard(user_data)
                    ),
                    ft.IconButton(
                        ft.icons.HISTORY,
                        selected=True,
                        icon_color=ft.colors.GREEN,
                        tooltip="Transaction History",
                        on_click=lambda e: all_transactions(e)
                    ),
                    ft.IconButton(
                        ft.icons.ACCOUNT_CIRCLE,
                        tooltip="Profile",
                        on_click=lambda e: show_profile(e)
                    ),
                    ft.IconButton(
                        ft.icons.LOGOUT,
                        tooltip="Log-out",
                        on_click=lambda e: show_logout_confirmation(e)
                    ),
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                spacing=40
            ),
            padding=10,
            bgcolor=ft.colors.WHITE,
            border=ft.border.only(top=ft.BorderSide(1, ft.colors.BLACK12))
        )

        page.add(
            ft.Column([
                ft.Stack([
                    background,
                    transactions_container
                ], expand=True),
                bottom_nav
            ], spacing=0, expand=True)
        )
        page.update()


    def show_profile(e):
        page.clean()
        page.overlay.clear()

        user_data = page.client_storage.get("user_data")
        if not user_data:
            user_data = {'first_name': '', 'balance': 0.00}

        try:
            conn = pymysql.connect(**db_config)
            cursor = conn.cursor(pymysql.cursors.DictCursor)
            cursor.execute("""
                SELECT first_name, middle_name, last_name, phone, sex
                FROM users 
                WHERE phone = %s
            """, (page.client_storage.get("user_phone"),))
            user_info = cursor.fetchone()
        except Error as e:
            print(f"Database error: {e}")
            user_info = None
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

        def handle_edit(e):
            edit_fname = ft.TextField(
                label="First Name",
                value=user_info['first_name'],
                width=280,
                color="black",
                label_style=ft.TextStyle(size=12, color="black"),
                border_color="black",
                border_radius=15
            )

            edit_mname = ft.TextField(
                label="Middle Name",
                value=user_info['middle_name'] or "",
                width=280,
                color="black",
                label_style=ft.TextStyle(size=12, color="black"),
                border_color="black",
                border_radius=15
            )

            edit_lname = ft.TextField(
                label="Last Name",
                value=user_info['last_name'],
                width=280,
                color="black",
                label_style=ft.TextStyle(size=12, color="black"),
                border_color="black",
                border_radius=15
            )

            edit_sex = ft.DropdownM2(
                label="Sex",
                width=280,
                value=user_info['sex'],
                label_style=ft.TextStyle(size=12, color="black"),
                border_color="black",
                border_radius=15,
                bgcolor="white",
                color="black",
                options=[
                    ft.dropdownm2.Option("Male"),
                    ft.dropdownm2.Option("Female"),
                    ft.dropdownm2.Option("Prefer not to say")
                ]
            )

            def save_changes(e):
                try:
                    conn = pymysql.connect(**db_config)
                    cursor = conn.cursor()
                    cursor.execute("""
                        UPDATE users 
                        SET first_name = %s, middle_name = %s, last_name = %s, sex = %s
                        WHERE phone = %s
                    """, (
                        edit_fname.value,
                        edit_mname.value,
                        edit_lname.value,
                        edit_sex.value,
                        user_info['phone']
                    ))
                    conn.commit()

                    user_data['first_name'] = edit_fname.value
                    page.client_storage.set("user_data", user_data)

                    success_popup = ft.Container(
                        content=ft.Row([
                            ft.Icon(ft.icons.CHECK_CIRCLE, color="white", size=20),
                            ft.Text("Profile updated successfully!", color="white", size=11, weight="bold")
                        ], alignment=ft.MainAxisAlignment.CENTER, spacing=10),
                        bgcolor=ft.colors.GREEN_400,
                        padding=15,
                        width=250,
                        border_radius=15,
                        margin=ft.margin.only(top=15, left=55)
                    )

                    page.overlay.append(success_popup)
                    page.update()

                    time.sleep(1.5)
                    page.overlay.clear()
                    show_profile(None)

                except Error as e:
                    print(f"Database error: {e}")
                    warning_error("Failed to update profile!")
                finally:
                    if cursor:
                        cursor.close()
                    if conn:
                        conn.close()

            page.clean()
            page.add(
                ft.Stack([
                    ft.Container(
                        content=ft.Image(
                            src="assets/hand-drawn-bussines-pattern-doodle-business-seamless-pattern-doodle-business-background_698782-3476.jpg",
                            fit=ft.ImageFit.COVER,
                            width=360,
                            height=740,
                            opacity=0.2,
                        ),
                        alignment=ft.alignment.center,
                        expand=True
                    ),
                    ft.Column([
                        ft.Container(
                            content=ft.IconButton(
                                icon=ft.icons.ARROW_BACK,
                                icon_size=30,
                                tooltip="Go back",
                                on_click=lambda e: show_profile(e)
                            ),
                            margin=ft.margin.only(left=10, top=10),
                            alignment=ft.alignment.top_left,
                        ),
                        ft.Container(
                            content=ft.Column([
                                ft.Text("Edit Profile",
                                        size=24,
                                        weight="bold",
                                        color="black",
                                        text_align=ft.TextAlign.CENTER),
                                ft.Divider(height=30, color="transparent"),
                                edit_fname,
                                ft.Divider(height=10, color="transparent"),
                                edit_mname,
                                ft.Divider(height=10, color="transparent"),
                                edit_lname,
                                ft.Divider(height=10, color="transparent"),
                                edit_sex,
                                ft.Divider(height=20, color="transparent"),
                                ft.ElevatedButton(
                                    "Save Changes",
                                    bgcolor=ft.colors.GREEN_400,
                                    color="black",
                                    width=280,
                                    height=40,
                                    on_click=save_changes
                                )
                            ],
                                horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                            padding=20,
                            expand=True
                        )
                    ])
                ])
            )
            page.update()

        bottom_nav = ft.Container(
            content=ft.Row(
                [
                    ft.IconButton(
                        ft.icons.HOME,
                        tooltip="Home",
                        on_click=lambda e: show_dashboard(user_data)
                    ),
                    ft.IconButton(
                        ft.icons.HISTORY,
                        tooltip="Transaction History",
                        on_click=lambda e: all_transactions(e)
                    ),
                    ft.IconButton(
                        ft.icons.ACCOUNT_CIRCLE,
                        selected=True,
                        icon_color=ft.colors.GREEN,
                        tooltip="Profile",
                        on_click=lambda e: show_profile(e)
                    ),
                    ft.IconButton(
                        ft.icons.LOGOUT,
                        tooltip="log-out",
                        on_click=lambda e: show_logout_confirmation(e)
                    ),
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                spacing=40
            ),
            padding=10,
            bgcolor=ft.colors.WHITE,
            border=ft.border.only(top=ft.BorderSide(1, ft.colors.BLACK12))
        )

        page.add(
            ft.Column([
                ft.Stack([
                    ft.Container(
                        content=ft.Image(
                            src="assets/hand-drawn-bussines-pattern-doodle-business-seamless-pattern-doodle-business-background_698782-3476.jpg",
                            fit=ft.ImageFit.COVER,
                            width=360,
                            height=740,
                            opacity=0.2,
                        ),
                        alignment=ft.alignment.center,
                        expand=True
                    ),
                    ft.Container(
                        content=ft.Column([
                            ft.Container(
                                content=ft.Column([
                                    ft.Row([
                                        ft.Text("Profile", size=24, weight="bold", color="black"),
                                    ], alignment=ft.MainAxisAlignment.CENTER, spacing=10),
                                    ft.Divider(height=20, color="transparent"),
                                    ft.Container(
                                        content=ft.Column([
                                            ft.Icon(ft.icons.ACCOUNT_CIRCLE, size=80, color="black"),
                                            ft.Text(
                                                f"{user_info['first_name']} {user_info['middle_name'] or ''} {user_info['last_name']}",
                                                size=24,
                                                weight="bold",
                                                color="black"
                                            ),
                                            ft.Text(
                                                f"+63 {user_info['phone']}",
                                                size=16,
                                                color="black"
                                            ),
                                            ft.Text(
                                                user_info['sex'],
                                                size=16,
                                                color="black"
                                            ),
                                        ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=10),
                                        bgcolor=ft.colors.WHITE,
                                        padding=30,
                                        border_radius=15,
                                        width=320,
                                        border=ft.border.all(1, ft.colors.BLACK12)
                                    ),
                                    ft.Divider(height=20, color="transparent"),
                                    ft.ElevatedButton(
                                        "Edit Profile",
                                        bgcolor=ft.colors.GREEN_400,
                                        color="black",
                                        width=280,
                                        height=40,
                                        on_click=handle_edit
                                    )
                                ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                                padding=20,
                                expand=True
                            )
                        ], scroll=ft.ScrollMode.AUTO),
                        expand=True
                    ),
                ], expand=True),
                bottom_nav
            ], spacing=0, expand=True)
        )
        page.update()

    def show_logout_confirmation(e):
        page.clean()
        page.overlay.clear()

        user_data = page.client_storage.get("user_data")
        if not user_data:
            user_data = {'first_name': '', 'balance': 0.00}

        password = ft.TextField(
            label="Enter Password to Confirm",
            password=True,
            can_reveal_password=True,
            color="black",
            width=280,
            label_style=ft.TextStyle(size=12, color="black"),
            border_color="black",
            border_radius=15
        )

        def handle_logout(e):
            if not password.value:
                warning_error("Please enter your password!")
                return

            try:
                conn = pymysql.connect(**db_config)
                cursor = conn.cursor(pymysql.cursors.DictCursor)
                hashed_password = hash_password(password.value)

                cursor.execute("""
                    SELECT id FROM users
                    WHERE phone = %s AND password = %s
                """, (page.client_storage.get("user_phone"), hashed_password))

                user = cursor.fetchone()

                if user:
                    loading = ft.Container(
                        content=ft.Column([
                            ft.ProgressRing(width=40, height=40, stroke_width=3, color=ft.colors.GREEN),
                            ft.Text("Logging out...", size=12, color="black", weight="bold")
                        ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=10),
                        padding=20,
                        width=230,
                        margin=ft.margin.only(top=250, left=55, bottom=330),
                        bgcolor=ft.colors.WHITE,
                        border_radius=15,
                        shadow=ft.BoxShadow(
                            spread_radius=1,
                            blur_radius=15,
                            color=ft.colors.BLACK12,
                        ),
                        alignment=ft.alignment.center,
                    )

                    page.overlay.append(loading)
                    page.update()

                    time.sleep(1.5)
                    page.client_storage.clear()
                    page.overlay.clear()

                    success_popup = ft.Container(
                        content=ft.Row([
                            ft.Icon(ft.icons.CHECK_CIRCLE, color="white", size=20),
                            ft.Text("Successfully logged out!", color="white", size=11, weight="bold")
                        ], alignment=ft.MainAxisAlignment.CENTER, spacing=10),
                        bgcolor=ft.colors.GREEN_400,
                        padding=15,
                        width=250,
                        border_radius=15,
                        margin=ft.margin.only(top=15, left=55)
                    )

                    page.overlay.append(success_popup)
                    page.update()

                    time.sleep(1.5)
                    show_landing_page()
                else:
                    warning_error("Incorrect password!")

            except Error as e:
                print(f"Database error: {e}")
                warning_error("Logout failed!")
            finally:
                if cursor:
                    cursor.close()
                if conn:
                    conn.close()

        bottom_nav = ft.Container(
            content=ft.Row(
                [
                    ft.IconButton(
                        ft.icons.HOME,
                        tooltip="Home",
                        on_click=lambda e: show_dashboard(user_data)
                    ),
                    ft.IconButton(
                        ft.icons.HISTORY,
                        tooltip="Transaction History",
                        on_click=lambda e: all_transactions(e)
                    ),
                    ft.IconButton(
                        ft.icons.ACCOUNT_CIRCLE,
                        tooltip="Profile",
                        on_click=lambda e: show_profile(e)
                    ),
                    ft.IconButton(
                        ft.icons.LOGOUT,
                        selected=True,
                        icon_color=ft.colors.GREEN,
                        tooltip="Log-out",
                        on_click=lambda e: show_logout_confirmation(e)
                    ),
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                spacing=40
            ),
            padding=10,
            bgcolor=ft.colors.WHITE,
            border=ft.border.only(top=ft.BorderSide(1, ft.colors.BLACK12))
        )

        page.add(
            ft.Column([
                ft.Stack([
                    background,
                    ft.Container(
                        content=ft.Column([
                            ft.Text("Confirm Logout",
                                    size=24,
                                    weight="bold",
                                    color="black",
                                    text_align=ft.TextAlign.CENTER),
                            ft.Divider(height=20, color="transparent"),
                            ft.Image(
                                src="assets/logout.jpg",
                                width=200,
                                height=200,
                                fit=ft.ImageFit.CONTAIN,
                            ),
                            ft.Divider(height=20, color="transparent"),
                            ft.Text(
                                "Please enter your password to confirm logout",
                                size=14,
                                color="black",
                                text_align=ft.TextAlign.CENTER
                            ),
                            ft.Divider(height=20, color="transparent"),
                            password,
                            ft.Divider(height=20, color="transparent"),
                            ft.ElevatedButton(
                                "Logout",
                                bgcolor=ft.colors.RED_400,
                                color="white",
                                width=280,
                                height=40,
                                on_click=handle_logout
                            ) 
                        ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                        padding=20,
                        expand=True
                    )
                ], expand=True),
                bottom_nav
            ], spacing=0, expand=True)
        )
        page.update()

    show_landing_page()
ft.app(main)