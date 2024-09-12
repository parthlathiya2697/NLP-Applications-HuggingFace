import torch
from transformers import T5Tokenizer, T5ForConditionalGeneration

class Translator:
    '''
    Supported Models
        - t5-small
    '''
    __checkpoint: str = None
    __model: T5ForConditionalGeneration = None
    __tokenizer: T5Tokenizer = None
    supported_languages = {'english': 'en', 'french':'fr', 'romanian': 'ro', 'german': 'de'}
    __prefix = "translate English to {}: "
    __device: str = 'cpu'
    __tokenizer_params = {'padding': 'longest', 'truncation': True, 'return_tensors': 'pt'}
    example =   '''
                Good morning. Have a nice day.
                '''

    def __init__(self, checkpoint: str= 't5-small', language_to: str= 'English'):
        self.__checkpoint = checkpoint
        self.__device = "cuda" if torch.cuda.is_available() else "cpu"
        
        # Add language in prefix
        language_to = language_to.lower()
        if language_to in self.supported_languages:
            self.__prefix = self.__prefix.format(language_to)
        else:
            raise ValueError(f'Language not supported. Available languages: {self.supported_languages.keys()}')
        self.__build_model()

    def __call__(self, input_str):
        batch_tokens = self.__tokenizer( f'{self.__prefix}{input_str}', **self.__tokenizer_params ).to(self.__device)
        output = self.__model.generate(**batch_tokens)
        output = self.__tokenizer.batch_decode(output, skip_special_tokens=True)
        return output[0]

    def __build_model(self):
        self.__create_tokenizer( self.__checkpoint )
        self.__create_model( self.__checkpoint )

    def __create_tokenizer(self, checkpoint):
        self.__tokenizer = T5Tokenizer.from_pretrained( checkpoint )

    def __create_model(self, checkpoint):
        self.__model = T5ForConditionalGeneration.from_pretrained( checkpoint ).to(self.__device)


if __name__ == "__main__":

    try:
        translator = Translator(language_to= 'German')
        output = translator(translator.example)
        print(output)
    except ValueError as err:
        print(f'Please enter a supported Language and try again.')
    
