import torch
from transformers import DistilBertTokenizer, DistilBertForSequenceClassification

class SentimentClassifier:
    '''
    Supported Models
        - distilbert-base-uncased-finetuned-sst-2-english
    '''
    __checkpoint: str = None
    __model: DistilBertForSequenceClassification = None
    __tokenizer: DistilBertTokenizer = None
    __device: str = 'cpu'
    __tokenizer_params = {'padding': 'longest', 'truncation': True, 'return_tensors': 'pt'}
    example =   '''
                I am happy.
                '''

    def __init__(self, checkpoint: str= 'distilbert-base-uncased-finetuned-sst-2-english'):
        self.__checkpoint = checkpoint
        self.__device = "cuda" if torch.cuda.is_available() else "cpu"
        self.__build_model()

    def __call__(self, input_str):
        batch_tokens = self.__tokenizer( input_str, **self.__tokenizer_params ).to(self.__device)
        logits = self.__model(**batch_tokens).logits
        output = logits.argmax().item()
        output = self.__model.config.id2label[output]
        return output

    def __build_model(self):
        self.__create_tokenizer( self.__checkpoint )
        self.__create_model( self.__checkpoint )

    def __create_tokenizer(self, checkpoint):
        self.__tokenizer = DistilBertTokenizer.from_pretrained( checkpoint )

    def __create_model(self, checkpoint):
        self.__model = DistilBertForSequenceClassification.from_pretrained( checkpoint ).to(self.__device)


if __name__ == "__main__":
    classifier = SentimentClassifier()
    output = classifier(classifier.example)
    print(output)

