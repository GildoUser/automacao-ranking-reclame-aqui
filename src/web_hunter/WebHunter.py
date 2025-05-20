from selenium import webdriver
from selenium.webdriver.common.by import By
from src.app.model import CompanyModel, CompanyInfoModel, TopicModel


class WebHunter:
    def __init__(self,db, file_exist):
        self.db = db
        self.file_exist = file_exist
        self.topic_list = []


    def verifyFile(self):
        if self.file_exist:
            print("entrou corretamente")
            self.setRankingFromDB()
        else:
            self.setRankingFromWeb()
        return self.topic_list
    
    def printTopicInfo(self,company_id,company_link):

        query_co_info = CompanyInfoModel.query.filter_by(id= company_id).first()

        company_info = query_co_info.to_dict()
        if company_info["reclamacao"] == None:
            c_info = self.getCompanyInfo(company_link,company_id)
            company_info["reclamacao"] = c_info["reclamacao"][0]
            query_co_info.reclamacao = c_info["reclamacao"][0]
            self.saveState()
        print(str(company_info["reclamacao"]) + " reclamações recebidas")
        
    def getCompanyInfo(self,link,id):
        print(link)
        self.driver = webdriver.Chrome()
        self.driver.get(link)
        rec = self.driver.find_element(By.XPATH, '//*[@id="newPerformanceCard"]/div[2]/div[1]/span/strong').text
        reclamacao = rec.split(" ")[:1]
        obj = {"reclamacao": reclamacao}
        self.driver.close()
        return obj

    def listStrToInt(self,string_list = ""):
        strfy_lista = string_list[1:len(string_list)-1].split(",")
        new_list = []
        [new_list.append(int(number)) for number in strfy_lista]
        return new_list

    def setRankingFromDB(self):
        
        topic_list = [topic.to_dict() for topic in TopicModel.query.all()]
        for item in topic_list:
            id_companies = self.listStrToInt(item["topic_companies"])
            new_array = []
            for company_id in id_companies:
                new_com = CompanyModel.query.filter_by(id = company_id).first()
                company_obj = new_com.to_dict()
                new_array.append(company_obj)
            item["topic_companies"] = new_array
        
        self.topic_list = topic_list


    def setRankingFromWeb(self):
        self.driver = webdriver.Chrome()
        self.driver.get("https://www.reclameaqui.com.br/ranking/")
        
        ranking_list = self.driver.find_elements(By.CLASS_NAME,"box-gray")

        for topic in ranking_list:
            count =1
            topic_list = topic.find_element(By.TAG_NAME,"ol").find_elements(By.TAG_NAME,"li")
            topic_companies_link = []
            company_list = []
            topic_companies = "["
            for company in topic_list:
                company_info = company.find_element(By.CSS_SELECTOR,"[ng-switch]").find_element(By.TAG_NAME,"a")
                name = company_info.get_attribute("title").strip()
                link = company_info.get_attribute("href")
                topic_companies_link.append(link)
                var_company = CompanyModel.query.filter_by(link = link).first()
                if not var_company:
                    var_company = CompanyModel(name = name, link = link)
                    self.db.session.add(var_company)
                    self.db.session.add(CompanyInfoModel())
                    self.saveState()
                new_company = var_company.to_dict()
                company_list.append(new_company)
                topic_companies += str(new_company["id"])
                if count < len(topic_list):
                    topic_companies = topic_companies + ","
                    count += 1
            topic_companies += "]"
            topic_name = topic.find_element(By.TAG_NAME,"h2").text
            my_topic = TopicModel(topic_name = topic_name, topic_companies = topic_companies)
            self.db.session.add(my_topic)
            self.saveState()
            self.topic_list.append({"id":my_topic.to_dict()["id"],"topic_name":topic_name, "topic_companies":company_list})
        self.driver.close()
    
    def saveState(self):
        self.db.session.commit()
        self.db.session.flush()