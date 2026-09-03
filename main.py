import os
import time
import urllib.parse
import flet as ft
from gtts import gTTS

def main(page: ft.Page):
    # Page settings - Dark Theme
    page.title = "UMG App"
    page.bgcolor = "black"
    page.theme_mode = ft.ThemeMode.DARK
    page.vertical_alignment = ft.MainAxisAlignment.START
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.padding = 15

    # ----------------- 1. Repeater View -----------------
    t1_status = ft.Text(value="", weight=ft.FontWeight.BOLD, color="white")
    
    input_char = ft.TextField(
        label="Enter Character, Emoji or Kannada Text",
        border_color="blue",
        color="white"
    )
    
    input_count = ft.TextField(
        label="Enter Count (e.g., 500)",
        keyboard_type=ft.KeyboardType.NUMBER,
        border_color="blue",
        color="white"
    )

    output_field = ft.TextField(
        label="Generated Output (Select or click Copy)",
        multiline=True,
        read_only=False,
        expand=True,
        border_color="green",
        color="white",
        min_lines=8,
        max_lines=12
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
            if count > 5000:
                t1_status.value = "ದಯವಿಟ್ಟು ಕೌಂಟ್ ಅನ್ನು 5000 ರ ಒಳಗೆ ಇರಿಸಿ!"
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
            try:
                page.set_clipboard(output_field.value)
                t1_status.value = "✅ Text ಯಶಸ್ವಿಯಾಗಿ Copy ಆಗಿದೆ!"
                t1_status.color = "green"
            except Exception:
                t1_status.value = "✅ Text ಸಿದ್ಧವಿದೆ. Box ಮೇಲೆ Long Press ಮಾಡಿ Copy ಮಾಡಬಹುದು."
                t1_status.color = "yellow"
            page.update()
        else:
            t1_status.value = "ಕಾಪಿ ಮಾಡಲು ಟೆಕ್ಸ್ಟ್ ಇಲ್ಲ!"
            t1_status.color = "red"
            page.update()

    repeater_content = ft.Column([
        ft.Divider(height=10, color="transparent"),
        input_char,
        input_count,
        ft.ElevatedButton(
            "⚡ Generate Text", 
            on_click=generate_repeated_text, 
            bgcolor="green", 
            color="white",
            width=400
        ),
        output_field,
        ft.ElevatedButton(
            "📋 Copy Text to Clipboard", 
            on_click=copy_text, 
            bgcolor="blue", 
            color="white",
            width=400
        ),
        t1_status
    ], expand=True, scroll=ft.ScrollMode.AUTO)

    # ----------------- 2. TTS Voice View -----------------
    tts_input = ft.TextField(
        label="Enter Text for Kannada Voice Generation",
        multiline=True,
        border_color="orange",
        color="white",
        min_lines=5,
        max_lines=8
    )
    t2_status = ft.Text(value="", weight=ft.FontWeight.BOLD, color="white")
    
    current_audio_file = {"path": "", "name": ""}

    def generate_voice(e):
        text = tts_input.value.strip() if tts_input.value else ""
        if not text:
            t2_status.value = "ದಯವಿಟ್ಟು ಟೆಕ್ಸ್ಟ್ ನಮೂದಿಸಿ!"
            t2_status.color = "red"
            page.update()
            return
        
        try:
            t2_status.value = "ವಾಯ್ಸ್ ಫೈಲ್ ಸಿದ್ಧವಾಗುತ್ತಿದೆ..."
            t2_status.color = "blue"
            page.update()

            filename = f"UMG_Voice_{int(time.time())}.mp3"
            save_path = os.path.join(os.getcwd(), filename)

            tts = gTTS(text=text, lang='kn', slow=False)
            tts.save(save_path)

            current_audio_file["path"] = save_path
            current_audio_file["name"] = filename

            t2_status.value = "✅ ವಾಯ್ಸ್ ಯಶಸ್ವಿಯಾಗಿ ಸಿದ್ಧವಾಗಿದೆ!"
            t2_status.color = "green"
            page.update()
        except Exception as ex:
            t2_status.value = "❌ ವಾಯ್ಸ್ ಸೃಷ್ಟಿ ವಿಫಲವಾಗಿದೆ (ಇಂಟರ್ನೆಟ್ ಪರಿಶೀಲಿಸಿ)."
            t2_status.color = "red"
            page.update()

    def play_preview(e):
        if not current_audio_file["path"] or not os.path.exists(current_audio_file["path"]):
            t2_status.value = "ಮೊದಲು ವಾಯ್ಸ್ ಜನರೇಟ್ ಮಾಡಿ!"
            t2_status.color = "orange"
            page.update()
            return

        try:
            file_url = "file://" + urllib.parse.quote(current_audio_file["path"])
            page.launch_url(file_url)
            t2_status.value = "🔊 ಆಡಿಯೋ ಪ್ಲೇ ಆಗುತ್ತಿದೆ..."
            t2_status.color = "cyan"
            page.update()
        except Exception:
            t2_status.value = "ಪ್ಲೇ ಮಾಡಲು ಸಾಧ್ಯವಾಗಲಿಲ್ಲ. ಡೌನ್‌ಲೋಡ್ ಮಾಡಿ ಆಲಿಸಿ."
            t2_status.color = "yellow"
            page.update()

    def download_voice(e):
        if not current_audio_file["path"] or not os.path.exists(current_audio_file["path"]):
            t2_status.value = "ಮೊದಲು ವಾಯ್ಸ್ ಜನರೇಟ್ ಮಾಡಿ!"
            t2_status.color = "orange"
            page.update()
            return

        try:
            # Android Storage Download Path
            download_folder = "/sdcard/Download/UMG_Voice"
            if not os.path.exists(download_folder):
                os.makedirs(download_folder, exist_ok=True)

            dest_path = os.path.join(download_folder, current_audio_file["name"])
            
            # Copy generated file to Download directory
            with open(current_audio_file["path"], "rb") as src, open(dest_path, "wb") as dst:
                dst.write(src.read())

            t2_status.value = f"📁 ಫೋನ್‌ನಲ್ಲಿ ಸೇವ್ ಆಗಿದೆ: Download/UMG_Voice/{current_audio_file['name']}"
            t2_status.color = "green"
            page.update()
        except Exception as ex:
            # Fallback if custom folder fails
            try:
                alt_dest = os.path.join("/sdcard/Download", current_audio_file["name"])
                with open(current_audio_file["path"], "rb") as src, open(alt_dest, "wb") as dst:
                    dst.write(src.read())
                t2_status.value = f"📁 ಫೋನ್ ಡೌನ್‌ಲೋಡ್ಸ್‌ನಲ್ಲಿ ಸೇವ್ ಆಗಿದೆ: {current_audio_file['name']}"
                t2_status.color = "green"
                page.update()
            except Exception:
                t2_status.value = "ಸೇವ್ ಮಾಡಲು ಪರ್ಮಿಷನ್ ಕೊಡಿ ಅಥವಾ ಫೈಲ್ ಮ್ಯಾನೇಜರ್ ಪರಿಶೀಲಿಸಿ."
                t2_status.color = "red"
                page.update()

    tts_content = ft.Column([
        ft.Divider(height=10, color="transparent"),
        tts_input,
        ft.ElevatedButton(
            "🎙️ 1. Generate Voice", 
            on_click=generate_voice, 
            bgcolor="orange", 
            color="white",
            width=400
        ),
        ft.Row([
            ft.ElevatedButton(
                "🔊 Preview", 
                on_click=play_preview, 
                bgcolor="blue", 
                color="white",
                expand=True
            ),
            ft.ElevatedButton(
                "⬇️ Download File", 
                on_click=download_voice, 
                bgcolor="green", 
                color="white",
                expand=True
            ),
        ], spacing=10),
        t2_status
    ], expand=True, scroll=ft.ScrollMode.AUTO)

    # ----------------- Navigation Setup -----------------
    body_container = ft.Container(content=repeater_content, expand=True, padding=5)

    btn_tab1 = ft.ElevatedButton("1. Text Repeater", bgcolor="blue", color="white")
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

    nav_row = ft.Row([btn_tab1, btn_tab2], alignment=ft.MainAxisAlignment.CENTER, spacing=15)

    title_text = ft.Text("UMG Multi-Tool App", size=22, weight=ft.FontWeight.BOLD, color="blue")

    page.add(
        ft.Row([title_text], alignment=ft.MainAxisAlignment.CENTER),
        nav_row,
        body_container
    )

ft.app(target=main)
