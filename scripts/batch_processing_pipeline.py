# Packages
from openai import OpenAI
import os
from tqdm import tqdm
import warnings

# Functions
from nps_analysis import speech_recog_model, speech_recog_pred, extract_nps, check_and_create_dirs

# Parameters
warnings.filterwarnings('ignore')

# Function to apply the process in a entire directory
def batch_processing_pipeline(root_folder = '/home/gbrlmoraes/git_reps/VoiceToInsight'):

    print('Iniciando processo:')

    print('Criando diretórios...')
    check_and_create_dirs(base_dir = root_folder)

    # Start the local model and the OpenAI client
    client = OpenAI(api_key = os.environ['GBRL_API_KEY'])
    model = speech_recog_model()

    # Processing each file (audio file -> json result)
    for file in tqdm(os.listdir(os.path.join(root_folder, 'audio_samples'))):

        file_base_name = file.replace('.wav', '')

        # Applying the speech recognition
        speech_recog_pred(
            os.path.join(root_folder, 'audio_samples', file),
            os.path.join(root_folder, 'data', 'complete_texts'),
            os.path.join(root_folder, 'data', 'timestamp_texts'),
            model
        )

        # Sending the text to the GPT model generate the Json
        extract_nps(
            os.path.join(root_folder, 'data', 'complete_texts', f"text_{file_base_name}.txt"),
            os.path.join(root_folder, 'data', 'json_results'),
            client
        )

    print('Processamento concluído!')

batch_processing_pipeline()