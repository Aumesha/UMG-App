import os
import time
import flet as ft
from gtts import gTTS

def main(page: ft.Page):
    page.title = "UMG App"
    page.vertical_alignment = ft.MainAxisAlignment.START
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.bgcolor = "white"

    # ----------------- 1. Repeater View -----------------
    t1_status = ft.Text(value="", weight=ft.FontWeight.BOLD)
    
    output_field = ft.TextField(
        label="Generated Output (Kannada & Emoji Supported)",
        multiline=True,
        read_only=True,
        expand=True,
        border_color="blue"
    )

    input_char = ft.TextField(
        label="Enter Character, Emoji or Kannada Text",
        multiline=False,
        border_color="blue"
    )
    
    input_count = ft.TextField(
        label="Enter Count (e.g., 500)",
        keyboard_type=ft.KeyboardType.NUMBER,
        border_color="blue"
    )

    def generate_repeated_text(e):
        char = input_char.value
        count_str = input_count.value
        if not char or not count_str:
            t1_status.value = "ದಯವಿಟ್ಟು ಎಲ್ಲಾ ಬಾಕ್ಸ್‌ಗಳನ್ನು ಭರ್ತಿ ಮಾಡಿ!"
            t1_status.color = "red"
            page.update()
            return
        try:
            count = int(count_str)
            if count > 2000:
                t1_status.value = "ದಯವಿಟ್ಟು ಕೌಂಟ್ ಅನ್ನು 2000 ರ ಒಳಗೆ ಇರಿಸಿ!"
                t1_status.color = "orange"
                page.update()
                return
            
            result = "\n".join([char] * count)
            output_field.value = result
            t1_status.value = "ಯಶಸ್ವಿಯಾಗಿ ಜನರೇಟ್ ಆಗಿದೆ!"
            t1_status.color = "green"
            page.update()
        except Exception:
            t1_status.value = "ತಪ್ಪಾದ ಸಂಖ್ಯೆ (Invalid Number)!"
            t1_status.color = "red"
            page.update()

    def copy_text(e):
        if output_field.value:
            page.set_clipboard(output_field.value)
            t1_status.value = "ಕ್ಲಿಪ್‌ಬೋರ್ಡ್‌ಗೆ ಕಾಪಿ ಆಗಿದೆ!"
            t1_status.color = "blue"
            page.update()
        else:
            t1_status.value = "ಕಾಪಿ ಮಾಡಲು ಏನೂ ಇಲ್ಲ!"
            t1_status.color = "red"
            page.update()

    repeater_content = ft.Column([
        ft.Divider(height=5),
        input_char,
        input_count,
        ft.ElevatedButton(
            "Generate", 
            on_click=generate_repeated_text, 
            bgcolor="green", 
            color="white",
            width=400
        ),
        output_field,
        ft.ElevatedButton(
            "Copy Text", 
            on_click=copy_text, 
            bgcolor="blue", 
            color="white",
            width=400
        ),
        t1_status
    ], expand=True, scroll=ft.ScrollMode.AUTO)

    # ----------------- 2. TTS Voice View -----------------
    tts_input = ft.TextField(
        label="Enter Unlimited Text for Kannada Voice",
        multiline=True,
        expand=True,
        border_color="orange"
    )
    t2_status = ft.Text(value="", weight=ft.FontWeight.BOLD)

    def generate_and_save_voice(text):
        try:
            t2_status.value = "ವಾಯ್ಸ್ ಫೈಲ್ ಸಿದ್ಧವಾಗುತ್ತಿದೆ..."
            t2_status.color = "blue"
            page.update()

            filename = f"umg_voice_{int(time.time())}.mp3"
            
            # Application folder path
            save_path = os.path.join(os.getcwd(), filename)

            tts = gTTS(text=text, lang='kn', slow=False)
            tts.save(save_path)

            t2_status.value = f"ವಾಯ್ಸ್ ಸಿದ್ಧವಾಗಿದೆ! ಸೇವ್ ಆದ ಹೆಸರು: {filename}"
            t2_status.color = "green"
            page.update()
        except Exception as ex:
            t2_status.value = f"ವಾಯ್ಸ್ ಸೃಷ್ಟಿ ವಿಫಲವಾಗಿದೆ: {str(ex)}"
            t2_status.color = "red"
            page.update()

    def start_voice_generation(e):
        text = tts_input.value.strip()
        if not text:
            t2_status.value = "ದಯವಿಟ್ಟು ಟೆಕ್ಸ್ಟ್ ನಮೂದಿಸಿ!"
            t2_status.color = "red"
            page.update()
            return
        generate_and_save_voice(text)

    tts_content = ft.Column([
        ft.Divider(height=5),
        tts_input,
        ft.ElevatedButton(
            "🎙️ Generate Kannada Voice MP3", 
            on_click=start_voice_generation, 
            bgcolor="orange", 
            color="white",
            width=400
        ),
        t2_status
    ], expand=True)

    # ----------------- Navigation Setup -----------------
    body_container = ft.Container(content=repeater_content, expand=True, padding=10)

    btn_tab1 = ft.ElevatedButton("1. Repeater", bgcolor="blue", color="white")
    btn_tab2 = ft.ElevatedButton("2. TTS Voice", bgcolor="grey", color="white")

    def switch_to_repeater(e):
        body_container.content = repeater_content
        btn_tab1.bgcolor = "blue"
        btn_tab2.bgcolor = "grey"
        page.update()

    def switch_to_tts(e):
        body_container.content = tts_content
        btn_tab1.bgcolor = "grey"
        btn_tab2.bgcolor = "blue"
        page.update()

    btn_tab1.on_click = switch_to_repeater
    btn_tab2.on_click = switch_to_tts

    nav_row = ft.Row([btn_tab1, btn_tab2], alignment=ft.MainAxisAlignment.CENTER, spacing=20)

    page.add(
        ft.Row(
            [ft.Text("Welcome to my UMG App", size=24, weight=ft.FontWeight.BOLD, color="blue")],
            alignment=ft.MainAxisAlignment.CENTER
        ),
        nav_row,
        body_container
    )

ft.app(target=main)
