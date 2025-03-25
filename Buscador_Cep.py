import tkinter as tk
import requests
import re
from PIL import Image, ImageTk

# Função para realizar a pesquisa do CEP
def pesquisar_cep(event=None):
    cep = cep_entry.get()

    # Validação do CEP (exemplo: verificar se possui 8 dígitos)
    if not re.match(r"^\d{8}$", cep):
        resultado_label.config(text="CEP inválido.")
        return
    else:
        resultado_label.config(text="")  # Limpa o texto de resultado

    url = f"https://viacep.com.br/ws/{cep}/json/"
    response = requests.get(url)
    data = response.json()

    if "erro" in data:
        resultado_label.config(text="CEP não encontrado.")
    else:
        endereco_label.config(text=f"{data['logradouro']}")
        bairro_label.config(text=f"{data['bairro']}")
        cidade_label.config(text=f"{data['localidade']}")
        estado_label.config(text=f"{data['uf']}")
        ddd_label.config(text=f"{data['ddd']}")
        cep_label.config(text=f"{data['cep']}")

# Configuração da janela principal
root = tk.Tk()
root.geometry("500x350")
root.overrideredirect(True)  # Remove a borda padrão da janela

# Definir uma cor de fundo transparente
bg_color = "#000001"
root.wm_attributes("-transparentcolor", bg_color)

# Criar um canvas para a interface arredondada
canvas = tk.Canvas(root, width=500, height=350, bg=bg_color, highlightthickness=0)
canvas.pack()

# Criar uma imagem com cantos arredondados para fundo
radius = 40
image = Image.new("RGBA", (500, 350), (0, 0, 0, 0))
mask = Image.new("L", (500, 350), 0)

for x in range(500):
    for y in range(350):
        if (
            (x < radius and y < radius and (x - radius) ** 2 + (y - radius) ** 2 > radius**2) or
            (x >= 500 - radius and y < radius and (x - (500 - radius)) ** 2 + (y - radius) ** 2 > radius**2) or
            (x < radius and y >= 350 - radius and (x - radius) ** 2 + (y - (350 - radius)) ** 2 > radius**2) or
            (x >= 500 - radius and y >= 350 - radius and (x - (500 - radius)) ** 2 + (y - (350 - radius)) ** 2 > radius**2)
        ):
            mask.putpixel((x, y), 0)
        else:
            mask.putpixel((x, y), 255)

# Carregar a imagem de fundo e aplicar a máscara arredondada
bg_image = Image.open("C:\\Users\\Dell\\Downloads\\Aulas_Python\\BuscaCEP\\BuscadorCEP.png").convert("RGBA")
bg_image = bg_image.resize((500, 350))
bg_image.putalpha(mask)

bg_photo = ImageTk.PhotoImage(bg_image)

# Exibir a imagem no canvas
canvas.create_image(0, 0, anchor="nw", image=bg_photo)

# Permitir arrastar a janela ao pressionar o botão esquerdo do mouse
def move_window(event):
    root.geometry(f"+{event.x_root}+{event.y_root}")

canvas.bind("<B1-Motion>", move_window)

# Função para fechar a janela
def fechar_ao_clicar_fora(event):
    root.destroy()  # Fecha a janela

root.bind("<FocusOut>", fechar_ao_clicar_fora)

# Caixa de texto para digitar o CEP
cep_entry = tk.Entry(root, width=19, bg="#007c8a", relief="flat", font=("Helvetica", 10))
cep_entry.place(x=280, y=78)

# Carregue a imagem do botão
button_image = tk.PhotoImage(file="C:\\Users\\Dell\\Downloads\\Aulas_Python\\BuscaCEP\\BotaoPeq.png")

# Criar botão personalizado
custom_button = tk.Button(root, image=button_image, command=pesquisar_cep, bd=0, highlightthickness=0, activebackground="#001c30")
custom_button.place(x=430, y=78)

# Rótulos de informações
resultado_label = tk.Label(root, font=("Helvetica", 11), fg="red", bg="#001c30")
resultado_label.place(x=310, y=105)

endereco_label = tk.Label(root, font=("Helvetica", 10), fg="#d7b317", bg="#001c30")
endereco_label.place(x=35, y=200)

bairro_label = tk.Label(root, font=("Helvetica", 10), fg="#d7b317", bg="#001c30")
bairro_label.place(x=350, y=200)

cidade_label = tk.Label(root, font=("Helvetica", 10), fg="#d7b317", bg="#001c30")
cidade_label.place(x=35, y=260)

estado_label = tk.Label(root, font=("Helvetica", 10), fg="#d7b317", bg="#001c30")
estado_label.place(x=250, y=260)

ddd_label = tk.Label(root, font=("Helvetica", 10), fg="#d7b317", bg="#001c30")
ddd_label.place(x=400, y=260)

cep_label = tk.Label(root, font=("Helvetica", 10), fg="#d7b317", bg="#001c30")
cep_label.place(x=35, y=320)

# Associa a tecla Enter à função pesquisar_cep
root.bind("<Return>", pesquisar_cep)

root.mainloop()
