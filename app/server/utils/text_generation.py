import torch
from transformers import GPT2Tokenizer, GPT2LMHeadModel


class TextGenerator:
    '''
    Supported Models
        - distilgpt2
    '''
    __checkpoint: str = None
    __model: GPT2LMHeadModel = None
    __tokenizer: GPT2Tokenizer = None
    __device: str = 'cpu'
    __tokenizer_params = {'return_tensors': 'pt'}
    example =   '''
                Hello, my dog is cute
                '''

    def __init__(self, checkpoint: str= 'distilgpt2'):
        self.__checkpoint = checkpoint
        self.__device = "cuda" if torch.cuda.is_available() else "cpu"
        self.__build_model()

    def __call__(self, input_str):
        batch_tokens = self.__tokenizer( input_str, **self.__tokenizer_params ).to(self.__device)
        output = self.__model.generate(batch_tokens.input_ids, labels= batch_tokens["input_ids"])
        output = self.__tokenizer.decode(output[0], skip_special_tokens=True)
        # output = self.__tokenizer.batch_decode(output, skip_special_tokens=True)
        return output

    def __build_model(self):
        self.__create_tokenizer( self.__checkpoint )
        self.__create_model( self.__checkpoint )

    def __create_tokenizer(self, checkpoint):
        self.__tokenizer = GPT2Tokenizer.from_pretrained( checkpoint )

    def __create_model(self, checkpoint):
        self.__model = GPT2LMHeadModel.from_pretrained( checkpoint ).to(self.__device)


if __name__ == "__main__":
    text_geneartor = TextGenerator()
    output = text_geneartor(text_geneartor.example)
    print(output)

