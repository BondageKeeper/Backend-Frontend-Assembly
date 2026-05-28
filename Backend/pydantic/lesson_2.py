#Field is used for checking VALUES(for example we need to check length or price must be more than zero - we use Field in that case)
#we give REQUIREMENTS for checking
from pydantic import BaseModel , Field
class ProductScheme(BaseModel):
    title: str = Field(min_length=2,max_length=50)
    price: float = Field(gt=0,description='price of the good') #gt - greater than ....
    rating: int = Field(default=5,ge=1,le=5) #ge - greater or equal , le - less or equal(rating must be from 1 to 5 logically)
raw_json = {'title':'sa','price':'55.5','rating':'1'}
upload = ProductScheme(**raw_json)
print(upload) #if requirements are not accomplished it gives a mistake - Perfect!
#EmailStr - this method allows us to check emails without REGEX or other time-consuming things
from pydantic import EmailStr
class AuthSchema(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8)
try:
    check = AuthSchema(email='PavelDurov@gmail.com',password='123123123123')
except Exception as e:
    print('ERROR!!')
#But what if we don't have enough included restrictions in so-called 'Field' class / For example we have to check some bad
#words or that data registration is not in the future somehow - in that case we write our own functions for checking
from pydantic import field_validator
class RegisterUserSchema(BaseModel):
    username: str
    age: int
    @field_validator("username") #we create custom validator for field "USERNAME"
    @classmethod #validators must always be like methods of class
    def check_username_spaces(cls,value:str):
        '''Here we check if there are any spaces in text'''
        if " " in value or len(value) < 3:
            raise ValueError("Nickname shouldn't have any spaces")
        return value #Otherwise we MUST return our value back
    @field_validator("age")
    @classmethod
    def check_realistic_age(cls,value:int):
        if value > 120:
            raise ValueError("You are too old for our service unfortunately")
        return value
#decorator @field_validator("age") simply tells us "when you check all json data I will check Field age due to function check_reali..
try:
    raw_json = {'username':'sa',"age":"100"}
    check2 = RegisterUserSchema(**raw_json)
    print(check2)
except Exception as error:
    print('Something is really off')
#TASK_2:
class CreatePostSchema(BaseModel):
    author_email: EmailStr
    title: str = Field(min_length=5,max_length=100)
    likes_count: int = Field(ge=0)
    @field_validator("title")
    @classmethod
    def prohibit_spam(cls,value:str):
        '''Here we check some words that can somehow resemble spam'''
        import re
        if re.search(r'\w*?(raffle|lottery)\w*?',value):
            raise ValueError("Damn it!")
        return value
try:
    raw_user = {'author_email':'bob123@email.com','title':'4554raffle54544','likes_count':'228'}
    check3 = CreatePostSchema(**raw_user)
    print(check3)
except:
    print('Something is really off!!!')

#Okay now we are definitely able to get data but how are we going to put pydantic-objects into AI?
#in that case we should convert our AI objects into simple dict or JSON(JSON or dict are needed for AI acceptance)
#for that we use methods called #model_dump() or #model_dump_json()
class User(BaseModel):
    name: str
    age: int
user_obj = User(name='Ivan',age=17)
user_dict = user_obj.model_dump() #here we convert our pydantic into simple python-dict
print('********************************')
print(f'{user_dict} - looks like a dict')
print(type(user_dict))
user_json = user_obj.model_dump_json() #here we convert our pydantic into simple json-string format
print(user_json)
#sometimes for validation we need to check multiple field just imagine that there are two fields like password and
#confirm_password and they DEPEND on each other - in that case we use @model_validator with parameter 'after'
#parameter 'after' will make a check after all types of fields appear , an example of such dependencies:
from pydantic import model_validator
class CourierDeliverySchema(BaseModel):
    city: str
    delivery_method: str
    @model_validator(mode='after')
    def check_delivery_location(self):
        #self already contains all checked fields of model
        import re
        if self.delivery_method == 'deliverer' and re.findall('village|countryside|hamlet',self.city):
            #raise ValueError('In such locations delivery is unavailable!') #it will give a mistake as predicted
            print('Error!')
        return self
just_order = {"city":"St.Paul village","delivery_method":"deliverer"}
check3 = CourierDeliverySchema(**just_order)
#print('*'*10)
print(check3)

#excellent , let's now lust imagine that user sent JSON with TOO MUCH fields for example som of them we don't need
#and there is no checking in our methods - hackers can easily send something bad(another not-checked field) and
#pydantic just skip it and eventually everything can be broken / so we can forbid other fields using pydantic
#for such case we add ConfigDict(literally) and put into it parameter extra='forbid' which basically prohibits any garbage or threat
from pydantic import ConfigDict
class StrictUserControl(BaseModel):
    #here we turn on strict model configuration control
    model_config = ConfigDict(extra='forbid')
    username: str
    email: EmailStr
try:
    bad_user = StrictUserControl(username="hacker",email='spam_test@email.com',status='admin') #note,there is no status in the model
except Exception as error:
    print('*' * 100)
    print('Some extra-dangerous data was found!')

#TASK_3:
class GenerateImageData(BaseModel):
    model_config = ConfigDict(extra='forbid')
    prompt: str = Field(min_length=10)
    aspect_ratio: str = "1:1"
    is_premium_model: bool = False
    @model_validator(mode='after')
    def check_subscript(self):
        if not self.is_premium_model and self.aspect_ratio == '16:9':
            raise ValueError("You didn't buy a subscription")
        else:
            print('changed!')
        return self
try:
    data = {"aspect_ratio":"16:9","prompt":"give me a name of music","is_premium_model":False}
    print('*' * 100)
    request = GenerateImageData(**data)
    print(request.model_dump_json())
except Exception as some_error:
    print('*' * 100)
    print(some_error)

#before that we unpack tuple using two ** , but usually we have got already ready data as python-dict
#for swift validation of ready python dicts we use NOT a validator : included class method - model_validate()
class User(BaseModel):
    name: str
    age: int
user_dict = {"name":"Ivan","age":17}
#instead of two ** we write more professionally:
user_obj = User.model_validate(user_dict) #for swift validation
print(user_obj.name)

#from AI we usually have got raw JSON string '{"prompt": "text", "tokens": 100}'
#we would need lo use method json.loads in order to convert it into python dict and than insert into pydantic
#hopefully model_validate_json() does it in one step
class AIResponse(BaseModel):
    text: str
    confidence: float
raw_json_string = '{"text": "Hello world", "confidence": 0.98}'
response = AIResponse.model_validate_json(raw_json_string) #we just instantly validate this JSON  without converting it
print(response.confidence)

#sometimes to create an entire Basemodel in order to check one variable - just inexpedient
#for so-called instant validation we use TypeAdapter
from pydantic import TypeAdapter
email_list_adapter = TypeAdapter(list[EmailStr]) #how given structure is going to look for our adapter
user_emails = ["test@mail.com","admin@site.ru","arkadi228@gmail.com"]
validated_emails = email_list_adapter.validate_python(user_emails)
print(validated_emails)

#Task_4:
class AIModelConfig(BaseModel):
    model_config = ConfigDict(extra='forbid')
    model_name: str
    temperature: float = Field(ge=0.0,le=2.0)
    stop_sequences: list[str] = list[str]
    @field_validator('model_name')
    @classmethod
    def check_model_name(cls,value: str):
        import re
        if not re.search(r'^(gpt|llama)',value):
            raise ValueError('We only have such models as gpt or llama')
        return value
try:
    raw_request = '{"model_name": "gpt-4o", "temperature": 0.7, "stop_sequences": ["stop","404"]}'
    response = AIModelConfig.model_validate_json(raw_request)
    print(response.model_name)
    print(response.temperature)
    print(response.stop_sequences)
except Exception as error:
    print(error)

#Task_5:
class AIMediaRequest(BaseModel):
    model_config = ConfigDict(extra='forbid')
    request_id: int
    user_email: EmailStr
    task_type: str = 'text_generation'
    prompt: str = Field(min_length=15,max_length=500)
    generation_count: int = Field(le=5,ge=1)
    system_tags: list[str] = list[str]
    @field_validator('task_type')
    @classmethod
    def check_type_function(cls,value:str):
        import re
        if not re.findall(r'^(text_generation|image_generation|video_generation)',value):
            raise ValueError('It is not supported by Artificial Intelligence')
        return value
    @model_validator(mode='after')
    def field_dependencies(self):
        if self.generation_count > 1:
            raise ValueError('If you want to generate more videos - buy subscription')
        return self
try:
    raw_bad_json = ('{"request_id": 999, "user_email": "student@mail.com","task_type": '
                    '"video_generation", "prompt": "Create a beautiful cinematic futuristic city loop", "generation_count": 1}')
    test_out = AIMediaRequest.model_validate_json(raw_bad_json)
    print(test_out.generation_count)
except Exception as error:
    print(error)


