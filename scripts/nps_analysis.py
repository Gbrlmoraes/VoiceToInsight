# Packages for using the local speech recognition model
import torch
from transformers import AutoModelForSpeechSeq2Seq, AutoProcessor, pipeline

# Packages for using the OpenAI model API
from openai import OpenAI

# Other packages
import os
import re
import warnings

# Setting parameters
warnings.filterwarnings('ignore')

# Function for starting the model
def speech_recog_model():
    device = "cuda:0" if torch.cuda.is_available() else "cpu"
    torch_dtype = torch.float16 if torch.cuda.is_available() else torch.float32

    model_id = "openai/whisper-medium"

    model = AutoModelForSpeechSeq2Seq.from_pretrained(
        model_id, torch_dtype=torch_dtype, low_cpu_mem_usage=False, use_safetensors=True
    )
    model.to(device)

    processor = AutoProcessor.from_pretrained(model_id)

    pipe = pipeline(
        "automatic-speech-recognition",
        model=model,
        tokenizer=processor.tokenizer,
        feature_extractor=processor.feature_extractor,
        max_new_tokens=128,
        chunk_length_s=30,
        batch_size=16,
        return_timestamps=True,
        torch_dtype=torch_dtype,
        device=device
    )

    return pipe

# Function to make a speech recognition prediction and save into a file
def speech_recog_pred(audio_file_location, complete_text_output_folder, timestamp_text_output_folder, model, language = "portuguese"):
    """
    Arguments:
        The mode saves the text in two formats
        complete_text_folder -> This is the full text without separation.
        timestamp_text_folder -> This is the same text but segmented with timestamps.
    """
    # Making the prediction
    prediction = model(audio_file_location, generate_kwargs={"language": language})

    # Saving in two files
    file_name = re.search("\d{7}", audio_file_location).group()
    with open(os.path.join(complete_text_output_folder, f"text_{file_name}.txt"), 'w', encoding = 'utf8') as f:
        f.write(prediction['text'])

    # Creating a file with the text segmented by timestamps
    with open(os.path.join(timestamp_text_output_folder, f"timestamp_{file_name}.txt"), 'w', encoding = 'utf8') as f:

        timestamp_text = ''
        for timestamp in prediction['chunks']:
            timestamp_text += f'{timestamp}\n'

        f.write(timestamp_text)

# Function to read the text and request a predict from OpenAI API
def extract_nps(text_file_location, json_output_folder, openai_client):
    with open(text_file_location) as f:
        texto = f.read()

    prompt = f"""
        Você receberá um texto capturado de uma ligação sobre uma pesquisa de NPS dos produtos da empresa TOTVS. Sua tarefa é analisar esse texto e produzir um JSON conforme as seguintes regras:

        1. Capture o nome da empresa para a qual o atendente da TOTVS ligou para fazer a pesquisa.
        2. Indique se foi possível realizar o atendimento com "Sim" ou "Não".
        3. Caso o atendimento tenha sido realizado, identifique e informe as notas de NPS atribuídas pelo cliente para cada categoria mencionada.
        5. Você deve capturar as notas das seguintes categorias de NPS (nps_atendimento, nps_suporte_tecnico, nps_comercial_financeiro, nps_recomendacao, nps_satisfacao, nps_custo, nps_unidade, nps_rh, nps_outros).
        6. No caso de não haverem notas para essas categorias, coloque uma string vazia.]
        7. No caso de haver mais de uma nota que se encaixe na categoria, faça uma média.
        8. O JSON deve ser montado em português.
        
        Segue o texto que deve ser analisado: {texto}
    """ 
    
    response = openai_client.completions.create(
        model = "gpt-3.5-turbo-instruct",
        prompt = prompt,
        temperature = 0,
        max_tokens = 500,
        top_p = 1,
        frequency_penalty = 0,
        presence_penalty = 0
    )

    json_result = response.choices[0].text.strip()

    file_name = re.search("\d{7}", text_file_location).group()
    with open(os.path.join(json_output_folder, f"nps_{file_name}.json"), 'w', encoding = 'utf8') as json_file:
        json_file.write(json_result)

# Function to create the folders necessary for the script to work
def check_and_create_dirs(base_dir):

    dirs = ['complete_texts', 'json_results', 'timestamp_texts']
    
    for dir_name in dirs:

        dir_path = os.path.join(base_dir, 'data', dir_name)
        
        # Check if the folder exists, otherwise create it
        if not os.path.exists(dir_path):
            
            os.makedirs(dir_path)