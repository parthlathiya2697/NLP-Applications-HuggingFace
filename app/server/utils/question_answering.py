import torch
from transformers import RobertaTokenizer, RobertaForQuestionAnswering

class QuestionAnswerer:
    '''
    Supported Models
        - deepset/roberta-base-squad2
    '''
    __checkpoint: str = None
    __model: RobertaForQuestionAnswering = None
    __tokenizer: RobertaTokenizer = None
    __device: str = 'cpu'
    __tokenizer_params = {'padding': 'longest', 'truncation': True, 'return_tensors': 'pt'}
    example =   '''
                Who was Jim Henson?
                '''
    example_context = 'Jim Henson was a nice puppet'

    def __init__(self, checkpoint: str= 'deepset/roberta-base-squad2'):
        self.__checkpoint = checkpoint
        self.__device = "cuda" if torch.cuda.is_available() else "cpu"
        self.__build_model()

    def __call__(self, input_str, context_str):
        batch_tokens = self.__tokenizer( input_str, context_str, **self.__tokenizer_params ).to(self.__device)
        outputs = self.__model(**batch_tokens)
        answer_start_index = outputs.start_logits.argmax()
        answer_end_index = outputs.end_logits.argmax()
        predict_answer_tokens = batch_tokens.input_ids[0, answer_start_index : answer_end_index + 1]
        output = self.__tokenizer.decode(predict_answer_tokens)
        return output

    def __build_model(self):
        self.__create_tokenizer( self.__checkpoint )
        self.__create_model( self.__checkpoint )

    def __create_tokenizer(self, checkpoint):
        self.__tokenizer = RobertaTokenizer.from_pretrained( checkpoint )

    def __create_model(self, checkpoint):
        self.__model = RobertaForQuestionAnswering.from_pretrained( checkpoint ).to(self.__device)


if __name__ == "__main__":
    classifier = QuestionAnswerer()
    output = classifier(classifier.example, classifier.example_context)
    print(output)

