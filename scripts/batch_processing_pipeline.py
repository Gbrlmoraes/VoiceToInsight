# Packages
from openai import OpenAI
import os
from tqdm import tqdm
import warnings

# Functions
from nps_analysis import speech_recog_model, speech_recog_pred, extract_nps

# Parameters
warnings.filterwarnings('ignore')

# Function to apply the process in a entire directory
def batch_processing_pipeline(root_folder = r'J:\Estudo\Projetos\VoiceToInsight'):

    print('Iniciando processo:')

    # Start the local model and the OpenAI client
    client = OpenAI(api_key = os.environ['gbrl_api_key'])
    model = speech_recog_model()

    # Processing each file (audio file -> json result)
    for file in tqdm(os.listdir(os.path.join(root_folder, 'audio_samples'))):

        file_base_name = file.replace('.wav', '')

        # Applying the speech recognition
        speech_recog_pred(
            os.path.join(root_folder, 'audio_samples', file),
            os.path.join(root_folder, r'data\complete_texts'),
            os.path.join(root_folder, r'data\timestamp_texts'),
            model
        )

        # Sending the text to the GPT model generate the Json
        extract_nps(
            os.path.join(root_folder, r'data\complete_texts', f"text_{file_base_name}.txt"),
            os.path.join(root_folder, r'data\json_results'),
            client
        )

batch_processing_pipeline()