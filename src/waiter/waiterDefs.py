import datetime
class WaiterSecDefs:
    def __init__(self,data,web_hunter, regular):
        self.is_regular = regular
        self.topic_list = data
        self.web_hunter = web_hunter
        """ [{"id":0,"topic_name": "piores",
                  "topic_companies":[
                      {"name":"pior do mundo","reclamacao":21231}
                      ]},{"id":1,"topic_name": "melhores",
                  "topic_companies":[
                      {"name":"empresa catinga elf","reclamacao":12312}
                      ]}]"""



    def setTopicList(self,topic_list):
        self.topic_list = topic_list


    def collectInput(self):
        return input("Digite a sua escolha: ")

    def listTopic(self,topic_id):
        print("Tópicos \n", str(topic_id-1))
        topic = self.topic_list[topic_id-1]
        print("id: "+ str(topic["id"]) + " - " + topic["topic_name"])    
        for company in topic["topic_companies"]:
            print(company["name"])
            self.web_hunter.printTopicInfo(company["id"],company["link"])



    def sayHello(self):
        hour = datetime.datetime.now().hour
        msg = "Bom dia!" if 5<=hour<12 else "Boa tarde!" if hour<18 else "Boa noite!"
        print(msg)
    
    def littleAlert(self):
        print("\nPara continuar, digite o número correspondente a opção oferecida. Em caso de erros o programa será encerrado; Solicite manutenção.\n")
    
    #oferece mensagem de acordo com o is regular
    def OfferMessage(self):
        #se next_is_even = True, a func define como False
        self.DefineEvenOrOdd()
        self.littleAlert()

        #first interaction
        if self.is_regular:
            print("1 )-> Ver tópicos \n2 )-> Ver tópicos e Listar empresas \n0 )-> Sair\n")
        else:
            print("Digite o número referente ao tópico ou 0 para sair.")  

        try:
            user_choice = int(self.collectInput())

        except:
            self.endService()
        if user_choice -1 > len(self.topic_list) and not self.is_regular:
            self.endService()
            #20 por regra do comercio
        if user_choice <= 0 or user_choice > len(self.topic_list):
            self.endService()

        return user_choice
        
    def serviceByDemand(self,number):
        print("numero e " + str(number))
        print("Tópiaaacos \n")
        #inicia true
        if self.is_regular:
           # topic_list = WebHunter.getTopicList()
            for topic in self.topic_list: 
                #+1 por causa de ser local o db
                print(str(topic["id"]) + ")-> " + topic["topic_name"])
                if number == 2:
                    for topic_item in topic["topic_companies"]:
                        print(topic_item["name"])

                print("----"*23)
                        
            #entra true sai false
            user_choice = self.OfferMessage()#is regular vira False aqui pois ja nao é mais regular
            return user_choice
           # WebHunter.getTopic(user_choice)#printa topico x e empresas
            #nesse ponto is even = false

            #se 0 finaliza se numero busca no db

    def DefineEvenOrOdd(self):
        if self.is_regular:
            self.is_regular = False
        else:
            self.is_regular = True

    
    def endService(self):
        print("A aplicação será encerrada.")
        exit()

