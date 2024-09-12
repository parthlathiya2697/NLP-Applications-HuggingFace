import torch
from transformers import PegasusTokenizer, PegasusForConditionalGeneration


class Summarizer:
    '''
    Supported Models
        - google/pegasus-xsum
    '''
    __checkpoint: str = None
    __model: PegasusForConditionalGeneration = None
    __tokenizer: PegasusTokenizer = None
    __device: str = 'cpu'
    __tokenizer_params = {'padding': 'longest', 'truncation': True, 'return_tensors': 'pt'}
    example =   '''
                PG&E stated it scheduled the blackouts in response to forecasts for high winds amid dry conditions. The aim is to reduce the risk of wildfires. Nearly 800 thousand customers were scheduled to be affected by the shutoffs which were expected to last through at least midday tomorrow.
                '''

    def __init__(self, checkpoint: str= 'google/pegasus-xsum'):
        self.__checkpoint = checkpoint
        self.__device = "cuda" if torch.cuda.is_available() else "cpu"
        self.__build_model()

    def __call__(self, input_str):
        batch_tokens = self.__tokenizer( input_str, **self.__tokenizer_params ).to(self.__device)
        output = self.__model.generate(**batch_tokens)
        output = self.__tokenizer.batch_decode(output, skip_special_tokens=True)
        return output[0]

    def __build_model(self):
        self.__create_tokenizer( self.__checkpoint )
        self.__create_model( self.__checkpoint )

    def __create_tokenizer(self, checkpoint):
        self.__tokenizer = PegasusTokenizer.from_pretrained( checkpoint )

    def __create_model(self, checkpoint):
        self.__model = PegasusForConditionalGeneration.from_pretrained( checkpoint ).to(self.__device)


if __name__ == "__main__":
    summarizer = Summarizer()
    output = summarizer(summarizer.example)
    print(output)

